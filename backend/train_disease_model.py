"""
Train and Evaluate Plant Disease Classifier
Uses PyTorch with Transfer Learning (EfficientNet-B0) on real plant disease dataset.
Evaluates on an independent test set and exports real metrics and confusion matrix.
"""

import os
import sys
import json
import time
import random
import numpy as np
import pandas as pd
from PIL import Image

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
import torchvision.transforms as transforms
import torchvision.models as models
from sklearn.metrics import (
    accuracy_score,
    precision_recall_fscore_support,
    confusion_matrix,
    classification_report
)

# Set seeds for reproducibility
SEED = 42
random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)

DATASET_ROOT = r"C:\COLLEGE\Projects\cv_NEW_project\PlantDoc Classification dataset"
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "app", "services", "cv", "artifacts")
os.makedirs(OUTPUT_DIR, exist_ok=True)

class PlantDataset(Dataset):
    def __init__(self, samples, transform=None):
        self.samples = samples  # List of (filepath, class_idx)
        self.transform = transform

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        path, label = self.samples[idx]
        try:
            image = Image.open(path).convert("RGB")
        except Exception as e:
            # Fallback to black image if corrupt
            image = Image.new("RGB", (224, 224), (0, 0, 0))
        if self.transform:
            image = self.transform(image)
        return image, label

def parse_class_name(folder_name):
    """
    Parses folder name like 'Tomato___Early_blight' into (crop, disease)
    """
    if "___" in folder_name:
        parts = folder_name.split("___")
        crop = parts[0].replace("_", " ").strip()
        disease = parts[1].replace("_", " ").strip()
    elif "_" in folder_name:
        parts = folder_name.split("_", 1)
        crop = parts[0].strip()
        disease = parts[1].replace("_", " ").strip()
    else:
        crop = folder_name
        disease = "healthy" if "healthy" in folder_name.lower() else "unspecified"
    
    is_healthy = "healthy" in disease.lower() or disease.lower() == "healthy"
    return crop, disease, is_healthy

def build_data_splits(dataset_root, train_per_class=100, val_per_class=25, test_per_class=25):
    train_dir = os.path.join(dataset_root, "train")
    val_dir = os.path.join(dataset_root, "val")
    
    classes = sorted([d for d in os.listdir(train_dir) if os.path.isdir(os.path.join(train_dir, d))])
    class_to_idx = {c: i for i, c in enumerate(classes)}
    
    class_info = []
    for c, idx in class_to_idx.items():
        crop, disease, is_healthy = parse_class_name(c)
        class_info.append({
            "class_id": idx,
            "raw_name": c,
            "crop": crop,
            "disease": disease,
            "is_healthy": is_healthy
        })
    
    train_samples = []
    val_samples = []
    test_samples = []
    
    print(f"Loading and validating dataset across {len(classes)} classes...")
    total_found = 0
    corrupt_count = 0
    
    for c in classes:
        idx = class_to_idx[c]
        c_train_dir = os.path.join(train_dir, c)
        c_val_dir = os.path.join(val_dir, c) if os.path.exists(val_dir) else None
        
        all_imgs = []
        for p in [c_train_dir, c_val_dir]:
            if p and os.path.exists(p):
                for f in os.listdir(p):
                    if f.lower().endswith(('.jpg', '.jpeg', '.png')):
                        full_p = os.path.join(p, f)
                        all_imgs.append(full_p)
        
        # Shuffle deterministically
        random.shuffle(all_imgs)
        
        # Verify samples
        valid_imgs = []
        for img_p in all_imgs:
            try:
                # Fast header verification
                with Image.open(img_p) as img:
                    img.verify()
                valid_imgs.append(img_p)
            except Exception:
                corrupt_count += 1
            if len(valid_imgs) >= (train_per_class + val_per_class + test_per_class):
                break
        
        total_found += len(valid_imgs)
        
        # Split into train, val, independent test
        n_train = min(train_per_class, int(len(valid_imgs) * 0.7))
        n_val = min(val_per_class, int(len(valid_imgs) * 0.15))
        
        c_train = valid_imgs[:n_train]
        c_val = valid_imgs[n_train:n_train + n_val]
        c_test = valid_imgs[n_train + n_val:]
        
        train_samples.extend([(p, idx) for p in c_train])
        val_samples.extend([(p, idx) for p in c_val])
        test_samples.extend([(p, idx) for p in c_test])
        
    print(f"Dataset preparation complete:")
    print(f"  Valid images: {total_found}, Corrupt images rejected: {corrupt_count}")
    print(f"  Train split: {len(train_samples)} samples")
    print(f"  Validation split: {len(val_samples)} samples")
    print(f"  Independent Test split: {len(test_samples)} samples")
    
    return class_info, class_to_idx, train_samples, val_samples, test_samples

def train_and_evaluate():
    print("=" * 60)
    print("KHETGPT - CROP DISEASE SCAN MODEL TRAINING & EVALUATION")
    print("=" * 60)
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using compute device: {device}")
    
    # 1. Build splits
    class_info, class_to_idx, train_samples, val_samples, test_samples = build_data_splits(
        DATASET_ROOT, train_per_class=100, val_per_class=25, test_per_class=25
    )
    
    # Save class mapping
    class_mapping_path = os.path.join(OUTPUT_DIR, "class_mapping.json")
    with open(class_mapping_path, "w", encoding="utf-8") as f:
        json.dump(class_info, f, indent=2)
    print(f"Saved class mapping to: {class_mapping_path}")
    
    # 2. Transforms & DataLoaders
    train_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.RandomRotation(degrees=15),
        transforms.ColorJitter(brightness=0.1, contrast=0.1),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    eval_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    train_loader = DataLoader(PlantDataset(train_samples, train_transform), batch_size=32, shuffle=True, num_workers=0)
    val_loader = DataLoader(PlantDataset(val_samples, eval_transform), batch_size=32, shuffle=False, num_workers=0)
    test_loader = DataLoader(PlantDataset(test_samples, eval_transform), batch_size=32, shuffle=False, num_workers=0)
    
    # 3. Model Architecture
    num_classes = len(class_info)
    print(f"Initializing EfficientNet-B0 with {num_classes} output classes...")
    model = models.efficientnet_b0(weights=models.EfficientNet_B0_Weights.DEFAULT)
    
    # Freeze initial feature extraction layers for fast, stable transfer learning
    for param in model.features[:5].parameters():
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
    model = model.to(device)
    
    criterion = nn.CrossEntropyLoss(label_smoothing=0.05)
    optimizer = torch.optim.AdamW(filter(lambda p: p.requires_grad, model.parameters()), lr=1e-3, weight_decay=1e-4)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=4)
    
    # 4. Training Loop
    epochs = 4
    best_val_acc = 0.0
    best_weights_path = os.path.join(OUTPUT_DIR, "plant_disease_model.pth")
    
    print("\nStarting model training...")
    t_start = time.time()
    
    for epoch in range(1, epochs + 1):
        model.train()
        running_loss = 0.0
        correct = 0
        total = 0
        
        for images, labels in train_loader:
            images = images.to(device)
            labels = labels.to(device)
            
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            
            running_loss += loss.item() * images.size(0)
            _, preds = torch.max(outputs, 1)
            correct += torch.sum(preds == labels).item()
            total += labels.size(0)
            
        train_loss = running_loss / total
        train_acc = correct / total
        scheduler.step()
        
        # Validation
        model.eval()
        val_loss = 0.0
        val_correct = 0
        val_total = 0
        with torch.no_grad():
            for images, labels in val_loader:
                images = images.to(device)
                labels = labels.to(device)
                outputs = model(images)
                loss = criterion(outputs, labels)
                val_loss += loss.item() * images.size(0)
                _, preds = torch.max(outputs, 1)
                val_correct += torch.sum(preds == labels).item()
                val_total += labels.size(0)
                
        val_loss = val_loss / val_total
        val_acc = val_correct / val_total
        
        print(f"Epoch {epoch}/{epochs} | Train Loss: {train_loss:.4f} Acc: {train_acc*100:.2f}% | Val Loss: {val_loss:.4f} Acc: {val_acc*100:.2f}%")
        
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            torch.save(model.state_dict(), best_weights_path)
            print(f"  --> Saved new best checkpoint (Val Acc: {val_acc*100:.2f}%)")
            
    train_time = time.time() - t_start
    print(f"\nTraining completed in {train_time:.1f} seconds. Best Val Acc: {best_val_acc*100:.2f}%")
    
    # 5. Independent Test Evaluation
    print("\nRunning comprehensive evaluation on Independent Test Set...")
    model.load_state_dict(torch.load(best_weights_path, map_location=device))
    model.eval()
    
    all_preds = []
    all_targets = []
    latencies = []
    
    with torch.no_grad():
        for images, labels in test_loader:
            images = images.to(device)
            
            t0 = time.time()
            outputs = model(images)
            t1 = time.time()
            latencies.append((t1 - t0) / images.size(0))
            
            _, preds = torch.max(outputs, 1)
            all_preds.extend(preds.cpu().numpy())
            all_targets.extend(labels.numpy())
            
    all_preds = np.array(all_preds)
    all_targets = np.array(all_targets)
    
    # Compute Metrics
    test_acc = accuracy_score(all_targets, all_preds)
    p_macro, r_macro, f1_macro, _ = precision_recall_fscore_support(all_targets, all_preds, average="macro", zero_division=0)
    p_weight, r_weight, f1_weight, _ = precision_recall_fscore_support(all_targets, all_preds, average="weighted", zero_division=0)
    
    avg_latency_ms = float(np.mean(latencies) * 1000)
    model_size_mb = float(os.path.getsize(best_weights_path) / (1024 * 1024))
    
    print("=" * 60)
    print("FINAL TEST METRICS ON INDEPENDENT SAMPLES:")
    print(f"  Test Accuracy:     {test_acc*100:.2f}%")
    print(f"  Macro Precision:   {p_macro*100:.2f}%")
    print(f"  Macro Recall:      {r_macro*100:.2f}%")
    print(f"  Macro F1-Score:    {f1_macro*100:.2f}%")
    print(f"  Weighted F1-Score: {f1_weight*100:.2f}%")
    print(f"  Inference Latency: {avg_latency_ms:.2f} ms/image (CPU)")
    print(f"  Model Size:        {model_size_mb:.2f} MB")
    print("=" * 60)
    
    # Per-class metrics
    class_names = [info["raw_name"] for info in class_info]
    p_cls, r_cls, f1_cls, sup_cls = precision_recall_fscore_support(all_targets, all_preds, average=None, zero_division=0)
    
    per_class_results = []
    for i, c_name in enumerate(class_names):
        per_class_results.append({
            "class_id": i,
            "raw_name": c_name,
            "crop": class_info[i]["crop"],
            "disease": class_info[i]["disease"],
            "precision": float(round(p_cls[i], 4)),
            "recall": float(round(r_cls[i], 4)),
            "f1_score": float(round(f1_cls[i], 4)),
            "test_samples": int(sup_cls[i])
        })
        
    # Confusion Matrix
    cm = confusion_matrix(all_targets, all_preds)
    cm_df = pd.DataFrame(cm, index=class_names, columns=class_names)
    cm_csv_path = os.path.join(OUTPUT_DIR, "confusion_matrix.csv")
    cm_df.to_csv(cm_csv_path)
    
    # Summary CSV
    test_summary_df = pd.DataFrame([{
        "Architecture": "EfficientNet-B0 (Transfer Learning)",
        "Num_Classes": num_classes,
        "Total_Test_Samples": len(all_targets),
        "Accuracy": float(round(test_acc, 4)),
        "Macro_Precision": float(round(p_macro, 4)),
        "Macro_Recall": float(round(r_macro, 4)),
        "Macro_F1": float(round(f1_macro, 4)),
        "Weighted_F1": float(round(f1_weight, 4)),
        "Inference_Latency_ms": float(round(avg_latency_ms, 2)),
        "Model_Size_MB": float(round(model_size_mb, 2))
    }])
    test_summary_csv = os.path.join(OUTPUT_DIR, "test_metrics.csv")
    test_summary_df.to_csv(test_summary_csv, index=False)
    
    # Full JSON evaluation report
    report = {
        "model_architecture": "EfficientNet-B0",
        "dataset_source": "PlantVillage / PlantDoc Indian Crop Benchmark",
        "training_samples": len(train_samples),
        "validation_samples": len(val_samples),
        "test_samples": len(test_samples),
        "total_classes": num_classes,
        "metrics": {
            "accuracy": float(round(test_acc, 4)),
            "macro_precision": float(round(p_macro, 4)),
            "macro_recall": float(round(r_macro, 4)),
            "macro_f1": float(round(f1_macro, 4)),
            "weighted_f1": float(round(f1_weight, 4)),
            "inference_time_ms": float(round(avg_latency_ms, 2)),
            "model_size_mb": float(round(model_size_mb, 2))
        },
        "per_class": per_class_results,
        "training_time_seconds": float(round(train_time, 2)),
        "status": "COMPLETED_AND_VERIFIED"
    }
    
    report_path = os.path.join(OUTPUT_DIR, "evaluation_report.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
        
    print(f"Saved evaluation report to: {report_path}")
    print(f"Saved test summary to: {test_summary_csv}")
    print(f"Saved confusion matrix to: {cm_csv_path}")

if __name__ == "__main__":
    train_and_evaluate()

