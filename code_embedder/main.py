#!/usr/bin/env python3
import json
import logging
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional
import sys
from datetime import datetime

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

def save_embeddings(embeddings: np.ndarray, 
                   metadata: List[Dict], 
                   output_dir: Path) -> Dict:
    """Save embeddings and metadata with validation"""
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save embeddings
    embeddings_path = output_dir / "embeddings.npy"
    np.save(embeddings_path, embeddings)
    
    # Save enriched metadata
    full_metadata = {
        "generated_at": datetime.now().isoformat(),
        "embedding_version": "1.0",
        "total_files": len(embeddings),
        "files": metadata
    }
    
    metadata_path = output_dir / "metadata.json"
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(full_metadata, f, indent=2, ensure_ascii=False)
    
    return {
        "embeddings_path": str(embeddings_path.absolute()),
        "metadata_path": str(metadata_path.absolute()),
        "count": len(embeddings)
    }

def main() -> Optional[Dict]:
    """Run the embedding pipeline with proper metadata handling"""
    try:
        # Add project root to Python path
        project_root = Path(__file__).parent.parent
        sys.path.insert(0, str(project_root))

        # Import modules
        from code_embedder.src.code_finder import CodeFinder
        from code_embedder.src.embedder import CodeBertEmbedder
        from code_embedder.src.metadata_generator import MetadataGenerator
        from code_embedder.config.settings import settings

        logger.info("=== Starting Embedding Pipeline ===")
        
        # Initialize components
        finder = CodeFinder(
            base_dir=settings.code_dir,
            extensions=settings.CODE_EXTENSIONS,
            ignore_dirs=settings.IGNORE_DIRS,
            max_size=settings.MAX_FILE_SIZE
        )
        embedder = CodeBertEmbedder(model_name=settings.EMBEDDING_MODEL)
        
        # Process files
        code_files = finder.find_all_code_files()
        if not code_files:
            logger.error("No code files found in %s", settings.code_dir)
            return None

        all_embeddings = []
        all_metadata = []
        batch = []
        
        for file_info in code_files:
            file_path = file_info['path']
            try:
                if content := finder.read_file(file_path):
                    # Generate enriched metadata
                    metadata = MetadataGenerator.generate(file_path)
                    if not metadata:
                        continue
                    
                    batch.append(content)
                    all_metadata.append(metadata)
                    
                    # Process batch when full
                    if len(batch) >= settings.EMBEDDING_BATCH_SIZE:
                        embeddings = embedder.embed(batch)
                        all_embeddings.append(embeddings)
                        batch = []
                        logger.info("Processed %d files", len(all_metadata))
            except Exception as e:
                logger.error("Failed to process %s: %s", file_path, str(e))
                continue

        # Process final batch
        if batch:
            embeddings = embedder.embed(batch)
            all_embeddings.append(embeddings)

        # Combine and save results
        if not all_embeddings:
            logger.error("No valid embeddings generated")
            return None
            
        final_embeddings = np.vstack(all_embeddings)
        return save_embeddings(
            embeddings=final_embeddings,
            metadata=all_metadata,
            output_dir=Path(settings.output_dir)
        )
        
    except Exception as e:
        logger.error("Pipeline failed: %s", str(e), exc_info=True)
        return None

if __name__ == "__main__":
    result = main()
    if result:
        print("\n=== Embedding Generation Successful ===")
        print(f"Embeddings: {result['embeddings_path']}")
        print(f"Metadata: {result['metadata_path']}")
        print(f"Files Processed: {result['count']}")
        sys.exit(0)
    else:
        print("\n!!! Embedding Generation Failed !!!")
        sys.exit(1)