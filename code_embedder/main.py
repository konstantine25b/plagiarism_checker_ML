#!/usr/bin/env python3
import logging
import os
import sys
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional

# Configure logging FIRST to avoid undefined logger errors
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

# Fix HuggingFace tokenizer warning
os.environ["TOKENIZERS_PARALLELISM"] = "false"

def main() -> Optional[Dict[str, np.ndarray]]:
    """Run the complete embedding pipeline"""
    try:
        # Add the project root to Python path
        project_root = Path(__file__).parent.parent
        sys.path.insert(0, str(project_root))

        # Import modules using absolute paths
        from code_embedder.src.code_finder import CodeFinder
        from code_embedder.src.embedder import CodeBertEmbedder
        from code_embedder.config.settings import settings

        logger.info("=== Starting Code Embedding Service ===")
        
        # Initialize components - using code_dir instead of repos_root
        finder = CodeFinder(
            base_dir=settings.code_dir,  # Changed to use code_dir property
            extensions=settings.CODE_EXTENSIONS,
            ignore_dirs=settings.IGNORE_DIRS,
            max_size=settings.MAX_FILE_SIZE
        )
        
        embedder = CodeBertEmbedder(model_name=settings.EMBEDDING_MODEL)
        
        # Get files with metadata
        code_files = finder.find_all_code_files()
        if not code_files:
            logger.error("No code files found in %s", settings.code_dir)
            return None

        # Process in batches
        all_embeddings = []
        batch = []
        processed_files = 0
        
        for file in code_files:
            if content := finder.read_file(file['path']):
                batch.append(content)
                
                if len(batch) >= settings.EMBEDDING_BATCH_SIZE:
                    embeddings = embedder.embed(batch)
                    all_embeddings.append(embeddings)
                    processed_files += len(batch)
                    batch = []
                    logger.info("Processed %d/%d files", processed_files, len(code_files))

        # Process final batch
        if batch:
            embeddings = embedder.embed(batch)
            all_embeddings.append(embeddings)
            processed_files += len(batch)

        # Save results using output_dir property
        output_path = Path(settings.output_dir) / "embeddings.npy"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        final_embeddings = np.vstack(all_embeddings)
        np.save(output_path, final_embeddings)
        
        logger.info("Successfully saved %d embeddings to %s", len(code_files), output_path)
        
        return {
            "embeddings": final_embeddings,
            "metadata": code_files,
            "output_path": str(output_path)
        }
        
    except Exception as e:
        logger.error("Pipeline failed: %s", str(e), exc_info=True)
        return None

if __name__ == "__main__":
    main()