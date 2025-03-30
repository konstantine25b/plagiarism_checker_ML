# plagiarism_checker/src/plagiarism_checker_functions.py
import os
import sys
from typing import List, Dict

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), '..')))

from vector_db.src.chroma_manager import ChromaCodeDB
from plagiarism_checker.config.settings import Settings
from code_embedder.src.embedder import CodeBertEmbedder
from plagiarism_checker.src.llm_interaction import LLMInteractor
import openai
from dotenv import load_dotenv
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class PlagiarismChecker:
    def __init__(self):
        self.db = ChromaCodeDB()
        db_loaded = self.db.load_from_disk()
        if db_loaded:
            logging.info("Existing vector database loaded successfully.")
        else:
            logging.warning("No existing vector database found, or load failed.")

        self.embedder = CodeBertEmbedder()
        self.llm_interactor = LLMInteractor()

    def rag_only_check(self, code: str, similarity_threshold: float = 0.8) -> str:
        print(f"Debugging RAG Results: {self.db.search(self.embedder.embed([code])[0].tolist(), top_k=5)}")
        embedding = self.embedder.embed([code])[0].tolist()
        results = self.db.search(embedding, top_k=5)
        print(f"RAG Results: {results}") # Keep this for now too
        max_similarity = 0.0
        if results:
            for result in results:
                similarity = result.get('similarity', 0.0)
                max_similarity = max(max_similarity, similarity)

        if max_similarity > similarity_threshold:
            return f"Plagiarized (Similarity: {max_similarity:.2f})"
        return "Not plagiarized (RAG)"

    def llm_only_check(self, code: str) -> str:
        """
        Checks for plagiarism by directly asking the LLM.
        """
        prompt = f"""Is the following code snippet likely plagiarized? Answer 'yes' or 'no'.\n```\n{code}\n```\nPlagiarism Verdict: """
        try:
            response = openai.Completion.create(
                model="gpt-3.5-turbo-instruct",  # Or your preferred model
                prompt=prompt,
                max_tokens=10,
                n=1,
                stop=None,
                temperature=0.2,
            )
            llm_response = response.choices[0].text.strip().lower()
            return "Plagiarized (LLM)" if "yes" in llm_response else "Not plagiarized (LLM)"
        except Exception as e:
            return f"Error during LLM interaction: {e}"

    def full_system_check(self, code: str) -> str:
        """
        Checks for plagiarism using vector search and then LLM verification.
        """
        embedding = self.embedder.embed([code])[0].tolist()
        results = self.db.search(embedding, top_k=5)
        print(f"Full System Results: {results}") # Print results for debugging

        similar_codes_for_llm = []
        if results and results[0] and 'ids' in results[0]:
            for i in range(len(results[0]['ids'])):
                metadata = self.db.get(ids=[results[0]['ids'][i]], include=['metadatas'])['metadatas'][0]
                code_snippet = metadata.get('code', '')
                if code_snippet:
                    similar_codes_for_llm.append({"file_path": metadata['filepath'], "code": code_snippet})

        plagiarism_result = self.llm_interactor.check_plagiarism_with_llm(code, similar_codes_for_llm)
        return f"Plagiarism Check Result (Full System): {plagiarism_result}"

if __name__ == "__main__":
    checker = PlagiarismChecker()
    test_code = "def example_function():\n    print('This is a test.')\n"
    print(checker.rag_only_check(test_code))
    print(checker.llm_only_check(test_code))
    print(checker.full_system_check(test_code))