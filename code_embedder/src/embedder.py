import torch
from transformers import AutoTokenizer, AutoModel
import numpy as np
from typing import List  # Add this import

class CodeBertEmbedder:
    def __init__(self, model_name: str = "microsoft/codebert-base"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name).to(self.device)
        
    def embed(self, texts: List[str]) -> np.ndarray:
        """Convert code texts to embeddings"""
        inputs = self.tokenizer(
            texts,
            padding=True,
            truncation=True,
            max_length=512,
            return_tensors="pt"
        ).to(self.device)
        
        with torch.no_grad():
            outputs = self.model(**inputs)
        
        # Mean pooling for sentence embeddings
        mask = inputs['attention_mask'].unsqueeze(-1)
        embeddings = (outputs.last_hidden_state * mask).sum(1) / mask.sum(1)
        return embeddings.cpu().numpy()
    
    