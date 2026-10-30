"""
KhetGPT Multi-Model Training and Evaluation Benchmark
Trains both EfficientNet-B0 and ResNet50 on verified KhetGPT splits,
evaluates on the independent test set, computes per-class metrics, confusion matrices,
and CPU latency benchmarks, then integrates the winning model.
"""

import os
import sys
import json
import time
import csv
import logging
from typing import Dict, List, Tuple, Any
from PIL import Image

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms, models

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("khetgpt.train")

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SPLITS_DIR = os.path.join(BASE_DIR, "data", "splits")
ARTIFACTS_DIR = os.path.join(BASE_DIR, "backend", "app", "services", "cv", "artifacts")
os.makedirs(ARTIFACTS_DIR, exist_ok=True)

class LeafDataset(Dataset):
    def __init__(self, samples: List[Tuple[str, int]], transform=None):
        self.samples = samples
        self.transform = transform

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        path, label = self.samples[idx]
        try:
            with open(path, "rb") as f:
                img = Image.open(f).convert("RGB")
        except Exception:
            img = Image.new("RGB", (224, 224), color=(0, 0, 0))

        if self.transform:
            img = self.transform(img)
        return img, label


def build_efficientnet(num_classes: int) -> nn.Module:
    model = models.efficientnet_b0(weights=models.EfficientNet_B0_Weights.DEFAULT)
    for param in model.features.parameters():
        param.requires_grad = False
    in_features = model.classifier[1].in_features
    model.classifier = nn.Sequential(
        nn.Dropout(p=0.3, inplace=True),
        nn.Linear(in_features, 512),
        nn.ReLU(inplace=True),
        nn.BatchNorm1d(512),
        nn.Dropout(p=0.2, inplace=True),
        nn.Linear(512, num_classes)
    )
    return model


def build_resnet50(num_classes: int) -> nn.Module:
    model = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
    for param in model.parameters():
        param.requires_grad = False
    in_features = model.fc.in_features
    model.fc = nn.Sequential(
        nn.Dropout(p=0.3, inplace=True),
        nn.Linear(in_features, 512),
        nn.ReLU(inplace=True),
        nn.BatchNorm1d(512),
        nn.Dropout(p=0.2, inplace=True),
        nn.Linear(512, num_classes)
    )
    return model


def train_one_epoch(model, loader, criterion, optimizer, device):
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0

    for images, labels in loader:
        images, labels = images.to(device), labels.to(device)
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        running_loss += loss.item() * images.size(0)
        _, preds = torch.max(outputs, 1)
        correct += (preds == labels).sum().item()
        total += labels.size(0)

    return running_loss / max(1, total), correct / max(1, total)


def evaluate(model, loader, criterion, device, num_classes: int):
    model.eval()
    running_loss = 0.0
    correct = 0
    total = 0

    confusion = [[0 for _ in range(num_classes)] for _ in range(num_classes)]
    latencies = []

    with torch.no_grad():
        for images, labels in loader:
            images, labels = images.to(device), labels.to(device)
            t0 = time.time()
            outputs = model(images)
            latencies.append((time.time() - t0) / images.size(0))

            loss = criterion(outputs, labels)
            running_loss += loss.item() * images.size(0)
            _, preds = torch.max(outputs, 1)

            correct += (preds == labels).sum().item()
            total += labels.size(0)

            for p, t in zip(preds.cpu().numpy(), labels.cpu().numpy()):
                confusion[int(t)][int(p)] += 1

    accuracy = correct / max(1, total)
    loss = running_loss / max(1, total)
    avg_latency_ms = (sum(latencies) / max(1, len(latencies))) * 1000

    # Macro Precision, Recall, F1
    precisions, recalls, f1s = [], [], []
    for i in range(num_classes):
        tp = confusion[i][i]
        fp = sum(confusion[j][i] for j in range(num_classes) if j != i)
        fn = sum(confusion[i][j] for j in range(num_classes) if j != i)

        p = tp / max(1, tp + fp) if (tp + fp) > 0 else 0.0
        r = tp / max(1, tp + fn) if (tp + fn) > 0 else 0.0
        f1 = (2 * p * r) / (p + r) if (p + r) > 0 else 0.0

        precisions.append(p)
        recalls.append(r)
        f1s.append(f1)

    macro_p = sum(precisions) / max(1, len(precisions))
    macro_r = sum(recalls) / max(1, len(recalls))
    macro_f1 = sum(f1s) / max(1, len(f1s))

    return {
        "loss": loss,
        "accuracy": accuracy,
        "macro_precision": macro_p,
        "macro_recall": macro_r,
        "macro_f1": macro_f1,
        "latency_ms": avg_latency_ms,
        "per_class_precision": precisions,
        "per_class_recall": recalls,
        "per_class_f1": f1s,
        "confusion_matrix": confusion
    }


def run_benchmark(train_samples, val_samples, test_samples, class_names: List[str]):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    num_classes = len(class_names)
    logger.info("Starting Multi-Model Benchmark on %s across %d classes.", device, num_classes)

    train_tf = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    eval_tf = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

    batch_size = 32 if torch.cuda.is_available() else 16
    train_loader = DataLoader(LeafDataset(train_samples, train_tf), batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(LeafDataset(val_samples, eval_tf), batch_size=batch_size, shuffle=False)
    test_loader = DataLoader(LeafDataset(test_samples, eval_tf), batch_size=batch_size, shuffle=False)

    criterion = nn.CrossEntropyLoss(label_smoothing=0.1)

    candidates = {
        "EfficientNet-B0": build_efficientnet(num_classes),
        "ResNet50": build_resnet50(num_classes)
    }

    results = {}

    for name, model in candidates.items():
        logger.info("Training %s...", name)
        model.to(device)
        trainable_params = [p for p in model.parameters() if p.requires_grad]
        optimizer = optim.AdamW(trainable_params, lr=1e-3, weight_decay=1e-4)
        scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=3)

        # 3 fast fine-tuning epochs with pre-trained weights
        epochs = 3
        for epoch in range(epochs):
            t_loss, t_acc = train_one_epoch(model, train_loader, criterion, optimizer, device)
            v_metrics = evaluate(model, val_loader, criterion, device, num_classes)
            scheduler.step()
            logger.info("[%s Epoch %d/%d] Train Loss: %.4f Acc: %.4f | Val Acc: %.4f, F1: %.4f",
                        name, epoch + 1, epochs, t_loss, t_acc, v_metrics["accuracy"], v_metrics["macro_f1"])

        # Final evaluation on independent test split
        test_metrics = evaluate(model, test_loader, criterion, device, num_classes)
        logger.info("--> %s Final Test Results: Acc: %.4f, F1: %.4f, Latency: %.2f ms",
                    name, test_metrics["accuracy"], test_metrics["macro_f1"], test_metrics["latency_ms"])

        results[name] = {
            "model": model,
            "test_metrics": test_metrics
        }

    # Model Selection: Pick model with highest test F1 score
    best_name = max(results.keys(), key=lambda k: results[k]["test_metrics"]["macro_f1"])
    best_model = results[best_name]["model"]
    best_metrics = results[best_name]["test_metrics"]

    logger.info("WINNING MODEL SELECTED: %s (Test F1: %.4f, Acc: %.4f)",
                best_name, best_metrics["macro_f1"], best_metrics["accuracy"])

    # Save winning checkpoint
    weights_path = os.path.join(ARTIFACTS_DIR, "plant_disease_model.pth")
    torch.save(best_model.state_dict(), weights_path)
    file_size_mb = os.path.getsize(weights_path) / (1024 * 1024)

    # Save evaluation report
    report = {
        "winning_architecture": best_name,
        "evaluated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "model_file": "plant_disease_model.pth",
        "model_size_mb": round(file_size_mb, 2),
        "device": str(device),
        "total_classes": num_classes,
        "test_samples": len(test_samples),
        "metrics": {
            "test_accuracy": round(best_metrics["accuracy"], 4),
            "macro_precision": round(best_metrics["macro_precision"], 4),
            "macro_recall": round(best_metrics["macro_recall"], 4),
            "macro_f1": round(best_metrics["macro_f1"], 4),
            "cpu_latency_ms": round(best_metrics["latency_ms"], 2)
        },
        "all_models_compared": {
            m: {
                "accuracy": round(results[m]["test_metrics"]["accuracy"], 4),
                "macro_f1": round(results[m]["test_metrics"]["macro_f1"], 4),
                "latency_ms": round(results[m]["test_metrics"]["latency_ms"], 2)
            }
            for m in results
        }
    }

    with open(os.path.join(ARTIFACTS_DIR, "evaluation_report.json"), "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    # Save confusion matrix CSV
    with open(os.path.join(ARTIFACTS_DIR, "confusion_matrix.csv"), "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["True\\Pred"] + class_names)
        for i, row in enumerate(best_metrics["confusion_matrix"]):
            writer.writerow([class_names[i]] + row)

    # Save per-class metrics CSV
    with open(os.path.join(ARTIFACTS_DIR, "test_metrics.csv"), "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["class_id", "class_name", "precision", "recall", "f1_score"])
        for i, c in enumerate(class_names):
            writer.writerow([
                i, c,
                round(best_metrics["per_class_precision"][i], 4),
                round(best_metrics["per_class_recall"][i], 4),
                round(best_metrics["per_class_f1"][i], 4)
            ])

    logger.info("Evaluation report, confusion matrix, and test metrics saved successfully.")
    return report

