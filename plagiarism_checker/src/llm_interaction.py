# plagiarism_checker/src/llm_interaction.py
import os
from dotenv import load_dotenv
import openai

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class LLMInteractor:
    def check_plagiarism_with_llm(self, user_code: str, similar_codes: list[dict]) -> str:
        """
        Interacts with the LLM to check for plagiarism.
        """
        context = "\n\n".join([f"Reference File: {match['file_path']}\n```\n{match['code']}\n```" for match in similar_codes])
        prompt = f"""You are a code plagiarism detection expert. Analyze the following user-provided code snippet and determine if it is plagiarized based on the context of similar code files.\n\nUser Code:\n```\n{user_code}\n```\n\nSimilar Code Files (Context):\n{context}\n\nRespond with only two words: "yes" if the user code is plagiarized, or "no" if it is not. If you determine the code is plagiarized, also indicate the file paths of the reference code files from the context that support your conclusion.\n\nPlagiarism Verdict (yes/no) and References (if yes): """

        try:
            response = openai.Completion.create(
                model="gpt-3.5-turbo-instruct",  # Or your preferred model
                prompt=prompt,
                max_tokens=50,
                n=1,
                stop=None,
                temperature=0.2,  # Lower temperature for more deterministic output
            )
            return response.choices[0].text.strip()
        except Exception as e:
            return f"Error during LLM interaction: {e}"