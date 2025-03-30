#!/usr/bin/env python3
import numpy as np
import json
import os
from src.chroma_manager import ChromaCodeDB
from config.settings import Settings
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main():
    # Initialize ChromaDB
    db = ChromaCodeDB()

    # Define paths to embeddings and metadata
    embeddings_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "embeddings", "embeddings.npy")
    metadata_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "embeddings", "metadata.json")

    # Load embeddings and metadata from disk
    try:
        embeddings = np.load(embeddings_path)
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
        logging.info("Embeddings and metadata loaded from disk successfully.")
        logging.info(f"Loaded {len(embeddings)} embeddings and {len(metadata['files'])} metadata entries.")
    except Exception as e:
        logging.error(f"Failed to load embeddings or metadata: {e}")
        return

    # Load embeddings and add to ChromaDB
    if db.load_from_disk():
        logging.info("Checking for existing embeddings and adding new ones.")

        #get all the ids that are in the database.
        existing_ids = db.collection.get(include=[])['ids']

        for i, embedding in enumerate(embeddings):
            if str(i) not in existing_ids:
                db.collection.add(
                    embeddings=[embedding.tolist()],
                    metadatas=[metadata['files'][i]],
                    ids=[str(i)]
                )
                # logging.info(f"Added embedding with ID: {i}")
            else:
                pass
                # logging.warning(f"Embedding with ID: {i} already exists.")

        # logging.info("Finished adding new embeddings to ChromaDB.")
    else:
        logging.error("Failed to load embeddings and metadata into ChromaDB.")
        return

    logging.info("Embeddings added to ChromaDB.");

if __name__ == "__main__":
    main()