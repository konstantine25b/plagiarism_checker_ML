# plagiarism_checker/main.py
import os
import sys
from fastapi import FastAPI, HTTPException, Form
from fastapi.responses import HTMLResponse, JSONResponse
import logging
import openai  # Import openai here
import json
import csv
from typing import Optional

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from plagiarism_checker.src.plagiarism_checker_functions import PlagiarismChecker
from plagiarism_checker.config.settings import Settings
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()
plagiarism_checker = PlagiarismChecker()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

CHECK_RESULTS = []
CHECK_RESULTS_CSV_FILENAME = "plagiarism_check_results.csv"

def pretty_json(data):
    return json.dumps(data, indent=4)

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <html>
        <head>
            <title>Plagiarism Checker</title>
        </head>
        <body>
            <h1>Enter Code to Check for Plagiarism</h1>
            <form method="post" action="/check_plagiarism_full/">
                <label for="code">Code to Check:</label><br>
                <textarea id="code" name="code" rows="10" cols="80"></textarea><br>
                <input type="hidden" name="check_type" value="Full System">
                <input type="submit" value="Check Plagiarism (Full System)">
            </form>
            <hr>
            <h2>Check Plagiarism (RAG Only)</h2>
            <form method="post" action="/check_plagiarism_rag_only/">
                <label for="code_rag">Code to Check:</label><br>
                <textarea id="code_rag" name="code" rows="10" cols="80"></textarea><br>
                <label for="threshold_rag">Similarity Threshold (0.0 - 1.0):</label>
                <input type="number" id="threshold_rag" name="threshold" min="0.0" max="1.0" step="0.01" value="0.8"><br>
                <input type="hidden" name="check_type" value="RAG Only">
                <input type="submit" value="Check Plagiarism (RAG Only)">
            </form>
            <hr>
            <h2>Check Plagiarism (LLM Only)</h2>
            <form method="post" action="/check_plagiarism_llm_only/">
                <label for="code_llm">Code to Check:</label><br>
                <textarea id="code_llm" name="code" rows="10" cols="80"></textarea><br>
                <input type="hidden" name="check_type" value="LLM Only">
                <input type="submit" value="Check Plagiarism (LLM Only)">
            </form>
            <hr>
            <form method="post" action="/save_check_results/">
                <input type="submit" value="Save Plagiarism Check Results to CSV">
            </form>
        </body>
    </html>
    """

@app.post("/check_plagiarism_rag_only/")
async def check_plagiarism_rag_only(code: str = Form(...), threshold: float = Form(0.8), check_type: str = Form("RAG Only")):
    logging.info(f"Received request for RAG-only plagiarism check with code: {code[:50]}...")
    try:
        embedding = plagiarism_checker.embedder.embed([code])[0].tolist()
        results = plagiarism_checker.db.search(embedding, top_k=5)
        logging.info(f"RAG-only raw search results: {results}")
        max_similarity = 0.0
        similar_codes = []
        if results:
            for result in results:
                similarity = result.get('similarity', 0.0)
                code_snippet = result.get('code', '')
                file_path = result.get('file_path', '')
                if code_snippet:
                    similar_codes.append({"file_path": file_path, "code": code_snippet, "similarity": similarity})
                    max_similarity = max(max_similarity, similarity)

        plagiarism_result = "Not plagiarized (RAG)"
        if max_similarity > threshold:
            plagiarism_result = f"Plagiarized (Similarity: {max_similarity:.2f})"

        CHECK_RESULTS.append({
            "check_type": check_type,
            "input_code": code,
            "result": plagiarism_result,
            "similarity": max_similarity,
            "references": None
        })

        logging.info(f"RAG-only check result: {plagiarism_result}")
        return JSONResponse(content={"input_code": code, "similar_code": similar_codes, "result": plagiarism_result})
    except Exception as e:
        logging.error(f"Error during RAG-only plagiarism check: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")

@app.post("/check_plagiarism_llm_only/")
async def check_plagiarism_llm_only(code: str = Form(...), check_type: str = Form("LLM Only")):
    logging.info(f"Received request for LLM-only plagiarism check with code: {code[:50]}...")
    try:
        prompt = f"""Is the following code snippet likely plagiarized? Answer 'yes' or 'no'.\n```\n{code}\n```\nPlagiarism Verdict: """
        logging.info(f"LLM-only prompt: {prompt}")
        response = openai.Completion.create(
            model="gpt-3.5-turbo-instruct",  # Or your preferred model
            prompt=prompt,
            max_tokens=10,
            n=1,
            stop=None,
            temperature=0.2,
        )
        llm_response = response.choices[0].text.strip().lower()
        result = "Plagiarized (LLM)" if "yes" in llm_response else "Not plagiarized (LLM)"
        logging.info(f"LLM-only raw response: {response}")
        logging.info(f"LLM-only check result: {result}")
        CHECK_RESULTS.append({
            "check_type": check_type,
            "input_code": code,
            "result": result,
            "similarity": None,
            "references": None
        })
        return JSONResponse(content={"input_code": code, "result": result})
    except Exception as e:
        logging.error(f"Error during LLM-only plagiarism check: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")

@app.post("/check_plagiarism_full/")
async def check_plagiarism_full(code: str = Form(...), check_type: str = Form("Full System")):
    logging.info(f"Received request for full system plagiarism check with code: {code[:50]}...")
    try:
        embedding = plagiarism_checker.embedder.embed([code])[0].tolist()
        results = plagiarism_checker.db.search(embedding, top_k=5)
        logging.info(f"Full system raw search results: {results}")

        similar_codes_for_llm = []
        if results:
            for result in results:
                code_snippet = result.get('code', '')
                file_path = result.get('file_path', '')
                if code_snippet:
                    similar_codes_for_llm.append({"file_path": file_path, "code": code_snippet})

        context = "\n\n".join([f"Reference File: {match['file_path']}\n```\n{match['code']}\n```" for match in similar_codes_for_llm])
        prompt = f"""You are a code plagiarism detection expert. Analyze the following user-provided code snippet and determine if it is plagiarized based on the context of similar code files.\n\nUser Code:\n```\n{code}\n```\n\nSimilar Code Files (Context):\n{context}\n\nRespond with only two words: "yes" if the user code is plagiarized, or "no" if it is not. If you determine the code is plagiarized, also indicate the file paths of the reference code files from the context that support your conclusion.\n\nPlagiarism Verdict (yes/no) and References (if yes): """
        logging.info(f"Full system LLM prompt: {prompt}")
        response = openai.Completion.create(
            model="gpt-3.5-turbo-instruct",  # Or your preferred model
            prompt=prompt,
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.2,  # Lower temperature for more deterministic output
        )
        llm_response = response.choices[0].text.strip().lower()
        logging.info(f"Full system LLM raw response: {response}")

        plagiarism_result = "Not plagiarized"
        references = []
        if "yes" in llm_response:
            for match in similar_codes_for_llm:
                if f"reference file: {match['file_path']}" in llm_response:
                    references.append(match['file_path'])

            if references:
                plagiarism_result = f"Plagiarized (References: {', '.join(references)})"
            else:
                plagiarism_result = "Plagiarized"

        CHECK_RESULTS.append({
            "check_type": check_type,
            "input_code": code,
            "result": plagiarism_result,
            "similarity": None,
            "references": ", ".join(references)
        })

        logging.info(f"Full system check result: {plagiarism_result}")
        return JSONResponse(content={"input_code": code, "context": context, "result": plagiarism_result, "references": references})
    except Exception as e:
        logging.error(f"Error during full system plagiarism check: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")

@app.post("/save_check_results/")
async def save_check_results():
    try:
        if not CHECK_RESULTS:
            return {"message": "No plagiarism check results to save."}

        with open(CHECK_RESULTS_CSV_FILENAME, mode='w', newline='') as csvfile:
            fieldnames = CHECK_RESULTS[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for row in CHECK_RESULTS:
                writer.writerow(row)

        return {"message": f"Plagiarism check results saved to {CHECK_RESULTS_CSV_FILENAME}"}
    except Exception as e:
        logging.error(f"Error saving plagiarism check results to CSV: {e}")
        raise HTTPException(status_code=500, detail="Error saving plagiarism check results.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)