import numpy as np
import json
import chromadb
from pathlib import Path
from typing import List, Dict, Optional
import logging
from config.settings import Settings

logger = logging.getLogger(__name__)

class ChromaCodeDB:
    def __init__(self):
        """Initialize ChromaDB connection with optimized settings"""
        self.client = chromadb.PersistentClient(
            path=str(Settings.CHROMA_DIR),
            settings=chromadb.config.Settings(allow_reset=False)
        )
        self.collection = self.client.get_or_create_collection(
            name=Settings.COLLECTION_NAME,
            metadata=Settings.INDEX_CONFIG
        )
        logger.info("ChromaDB initialized for code embeddings")

    def load_from_disk(self) -> bool:
        """
        Load embeddings and metadata from disk into ChromaDB
        Returns True if successful, False otherwise
        """
        try:
            # Load numpy embeddings
            embeddings = np.load(Settings.EMBEDDINGS_PATH)
            
            # Load metadata
            with open(Settings.METADATA_PATH) as f:
                metadata_list = json.load(f)['files']
            
            # Verify alignment
            if len(embeddings) != len(metadata_list):
                raise ValueError(
                    f"Embedding count ({len(embeddings)}) "
                    f"doesn't match metadata count ({len(metadata_list)})"
                )
            
            # Generate document contents
            documents = []
            for meta in metadata_list:
                try:
                    with open(meta['file_path'], 'r') as f:
                        documents.append(f.read())
                except Exception as e:
                    logger.warning(f"Couldn't read {meta['file_path']}: {str(e)}")
                    documents.append("")
            
            # Store in ChromaDB
            self.collection.add(
                ids=[str(i) for i in range(len(embeddings))],
                embeddings=embeddings.tolist(),
                metadatas=metadata_list,
                documents=documents
            )
            
            logger.info(f"Loaded {len(embeddings)} code embeddings")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load embeddings: {str(e)}", exc_info=True)
            return False

    def search(self, query_embedding: List[float], top_k: int = 5) -> List[Dict]:
        """
        Search for similar code snippets
        Args:
            query_embedding: 768-dimensional embedding vector
            top_k: Number of results to return
        Returns:
            List of dictionaries with results
        """
        try:
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k,
                include=["metadatas", "distances", "documents"]
            )
            
            return [{
                'file_path': meta['file_path'],
                'similarity': 1 - distance,
                'language': meta.get('language', 'unknown'),
                'repo': meta.get('repo_name', 'unknown'),
                'code': doc[:1000]  # Return first 1000 chars of code
            } for meta, distance, doc in zip(
                results['metadatas'][0],
                results['distances'][0],
                results['documents'][0]
            )]
            
        except Exception as e:
            logger.error(f"Search failed: {str(e)}")
            return []

    def get_stats(self) -> Dict:
        """Get collection statistics"""
        return {
            'total_embeddings': self.collection.count(),
            'index_status': self.collection.get_index_status(),
            'config': Settings.INDEX_CONFIG
        }