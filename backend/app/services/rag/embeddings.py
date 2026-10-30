"""
KhetGPT Vector Embeddings & ChromaDB Storage
Uses BAAI/bge-small-en-v1.5 (384 dimensions) for dense representation
and manages persistent ChromaDB collections.
"""

import os
import logging
from typing import List, Dict, Any, Optional
import chromadb

logger = logging.getLogger("khetgpt.rag.embeddings")

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "data"))
CHROMA_PERSIST_DIR = os.path.join(DATA_DIR, "chroma_db")
COLLECTION_NAME = "khetgpt_knowledge_base"

class VectorStore:
    _instance: Optional["VectorStore"] = None

    def __init__(self, persist_dir: str = CHROMA_PERSIST_DIR):
        os.makedirs(persist_dir, exist_ok=True)
        self.persist_dir = persist_dir
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.collection = self.client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"description": "KhetGPT Multilingual Agricultural Knowledge Base"}
        )
        logger.info(f"Initialized ChromaDB at {persist_dir}, collection: {COLLECTION_NAME} (Count: {self.collection.count()})")
        self._fast_model = None
        self._model = None

    @classmethod
    def get_instance(cls) -> "VectorStore":
        if cls._instance is None:
            cls._instance = VectorStore()
        return cls._instance

    @property
    def fast_model(self):
        if self._fast_model is None:
            try:
                from fastembed import TextEmbedding
                self._fast_model = TextEmbedding(model_name="BAAI/bge-small-en-v1.5", threads=1)
                logger.info("FastEmbed ONNX model BAAI/bge-small-en-v1.5 initialized (threads=1).")
            except Exception as e:
                logger.warning(f"FastEmbed unavailable ({e}), using SentenceTransformer fallback.")
        return self._fast_model

    @property
    def model(self):
        if self._model is None:
            logger.info("Loading embedding model BAAI/bge-small-en-v1.5 fallback...")
            from sentence_transformers import SentenceTransformer
            self._model = SentenceTransformer("BAAI/bge-small-en-v1.5")
            logger.info("Embedding fallback model loaded.")
        return self._model

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        if not texts:
            return []
        clamped_texts = [t[:500] for t in texts]
        try:
            if self.fast_model is not None:
                return [emb.tolist() for emb in self.fast_model.embed(clamped_texts, batch_size=8)]
        except Exception as e:
            logger.warning(f"FastEmbed inference error: {e}, resetting ONNX session.")
            import gc
            self._fast_model = None
            gc.collect()
            try:
                from fastembed import TextEmbedding
                self._fast_model = TextEmbedding(model_name="BAAI/bge-small-en-v1.5", threads=1)
                return [emb.tolist() for emb in self._fast_model.embed(clamped_texts, batch_size=4)]
            except Exception as e2:
                logger.warning(f"Reset failed: {e2}, using SentenceTransformer fallback.")
        embeddings = self.model.encode(clamped_texts, normalize_embeddings=True, show_progress_bar=False)
        return embeddings.tolist()

    def add_chunks(self, chunks: List[Dict[str, Any]], batch_size: int = 64):
        """
        Adds pre-chunked documents into ChromaDB.
        Each chunk item: {"id": str, "text": str, "metadata": dict}
        """
        if not chunks:
            return

        total = len(chunks)
        for i in range(0, total, batch_size):
            batch = chunks[i:i + batch_size]
            ids = [c["id"] for c in batch]
            texts = [c["text"] for c in batch]
            metadatas = [c["metadata"] for c in batch]
            embeddings = self.embed_texts(texts)

            self.collection.upsert(
                ids=ids,
                embeddings=embeddings,
                documents=texts,
                metadatas=metadatas
            )
        logger.info(f"Successfully upserted {total} chunks into {COLLECTION_NAME}.")

    def search(
        self,
        query: str,
        top_k: int = 5,
        where_filter: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Performs dense semantic vector search for a query string.
        """
        if not query or not query.strip():
            return []

        query_embedding = self.embed_texts([query])[0]
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=where_filter,
            include=["documents", "metadatas", "distances"]
        )

        matched_chunks = []
        if results and "documents" in results and results["documents"]:
            docs = results["documents"][0]
            metas = results["metadatas"][0] if "metadatas" in results else [{}] * len(docs)
            dists = results["distances"][0] if "distances" in results else [0.0] * len(docs)

            for doc, meta, dist in zip(docs, metas, dists):
                # Cosine distance: similarity = 1 - (dist / 2) or 1 - dist
                sim_score = max(0.0, 1.0 - (dist if dist <= 1.0 else dist / 2.0))
                matched_chunks.append({
                    "text": doc,
                    "metadata": meta,
                    "distance": float(dist),
                    "similarity": float(round(sim_score, 4))
                })

        return matched_chunks

    def count(self) -> int:
        return self.collection.count()

    def get_indexed_stats(self) -> Dict[str, Any]:
        count = self.collection.count()
        # Query distinct filenames
        try:
            records = self.collection.get(include=["metadatas"])
            metas = records["metadatas"] if records else []
            files = set(m.get("filename") for m in metas if m and "filename" in m)
            categories = set(m.get("category") for m in metas if m and "category" in m)
            return {
                "total_chunks": count,
                "total_documents": len(files),
                "documents": sorted(list(files)),
                "categories": sorted(list(categories))
            }
        except Exception as e:
            return {
                "total_chunks": count,
                "total_documents": 0,
                "error": str(e)
            }

