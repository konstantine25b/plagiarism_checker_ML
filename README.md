# Code Plagiarism Checker System

## Project Description

This project is a demo system for detecting code plagiarism. The objective is to build a system that can find similar code snippets from existing code repositories based on a user-provided code snippet and determine whether the presented code is plagiarized. This system utilizes a combination of Retrieval-Augmented Generation (RAG) principles and Large Language Models (LLMs) to achieve this.

## Main Stages of the Project

### Fetching Code Repositories

This stage involves gathering a collection of code repositories that will serve as the knowledge base for plagiarism detection. For this demo, we are using a predefined list of GitHub repository URLs. These repositories are cloned to the local environment using `git clone`.


### Code Indexing

In this stage, the system searches for code files (e.g., `.py` files) within the downloaded repositories. For each code file, a vector representation (embedding) is calculated using a suitable embedding model. These embeddings capture the semantic content of the code. The generated embeddings are then stored in a vector database (ChromaDB in this case) for efficient similarity searching.

### Building the Plagiarism Checking System (RAG Principle)

This system provides an API (built using FastAPI) that accepts code content as a string from the user. When a code snippet is submitted:

1.  The system generates an embedding for the provided code.
2.  It searches the vector database for similar code files based on the embedding.
3.  The original user code and the retrieved similar code snippets (as context) are sent to an LLM (via the OpenAI API).
4.  The LLM, guided by prompt engineering, determines if the user's code is plagiarized and responds with either "Yes" or "No", potentially referencing the similar code files found.

The system offers three ways to check for plagiarism through the API:

* **RAG Only:** Determines plagiarism based on a similarity threshold from the vector database search.
* **LLM Only:** Directly queries the LLM with the user's code snippet to assess for plagiarism.
* **Full System:** Combines vector search and LLM with context to provide a plagiarism verdict with potential references.

### System Evaluation

A small dataset of plagiarized and non-plagiarized code snippets can be created to evaluate the performance of the following approaches:

1.  **Only RAG:** Using a similarity threshold to detect plagiarism.
2.  **Only LLM:** Directly asking the LLM about plagiarism.
3.  **Your Complete System:** The full RAG-based system with LLM.

The results of this evaluation (input code, expected outcome, actual outcome, similarity scores/references) are saved in a CSV file (`evaluation_results.csv`).

## Important Notes (This is a Demo System)

* This project demonstrates the concept of plagiarism checking and is not a fully optimized system.
* Indexing a large number of GitHub repositories requires significant resources and time. For simplicity, we are using a few repositories with smaller code files.
* In an ideal scenario, plagiarism checking would occur between repositories. However, for simplicity, the comparison is limited to individual code files.

## Requirements

* **Indexing Script (`github_extractor/main.py`, `code_embedder/main.py`, `vector_db/main.py`):** Downloads repositories and indexes code files into the vector database.
* **Plagiarism Checking API (`plagiarism_checker/main.py`):** Built using FastAPI, accepts code content, and returns a plagiarism verdict.
* **Evaluation Script (part of `plagiarism_checker/main.py`):** Included within the FastAPI application to evaluate the system.

## Installation

1.  **Prerequisites:**
    * Python 3.11+
    * pip (Python package installer)
    * Git (recommended)

2.  **Clone the Repository:**
    ```bash
    git clone https://github.com/konstantine25b/plagiarism_checker_ML
    cd plagiarism_checker_ML
    ```

3.  **Create a Virtual Environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On macOS/Linux
    # venv\Scripts\activate  # On Windows
    ```

4.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    # If no requirements.txt, install manually:
    # pip install fastapi uvicorn python-dotenv openai chromadb sentence-transformers nltk scikit-learn
    ```

5.  **Set up .env:**
    * Create a `.env` file in the root directory by
    ```bash
     cp .env.example .env
    ```
    * Add your OpenAI API or any other LLM key:
        ```
        OPENAI_API_KEY=<your_openai_api_key>
        ```

## Running the Plagiarism Checker

You can run the plagiarism checker using the combined script or by running the API directly.

**Using the Combined Script (`main.py` in the root directory)**

1.  Ensure your virtual environment is activated.
2.  Navigate to the root directory of the project.
3.  Run:
    ```bash
    python3 main.py
    ```
    This will execute the GitHub extractor, code embedder, vector database setup, and finally start the FastAPI application. The API will be accessible at `http://0.0.0.0:8000`. Press `CTRL+C` to stop.


## Component Explanation

1.  **`github_extractor/main.py`:**
    * **Installation:** No specific installation needed beyond the project dependencies.
    * **Running:** Executed by `python3 github_extractor/main.py`.
    * **Functionality:** Clones the predefined list of GitHub repositories to the `data/repositories` directory.

2.  **`code_embedder/main.py`:**
    * **Installation:** Requires the project dependencies, including `sentence-transformers`.
    * **Running:** Executed by `python3 code_embedder/main.py`.
    * **Functionality:** Reads code files from the cloned repositories, generates embeddings for them using a pre-trained model, and saves the embeddings and metadata to `data/embeddings/embeddings.npy` and `data/embeddings/metadata.json`.

3.  **`vector_db/main.py`:**
    * **Installation:** Requires the project dependencies, including `chromadb`.
    * **Running:** Executed by `python3 vector_db/main.py`.
    * **Functionality:** Loads the embeddings and metadata generated by `code_embedder/main.py` and creates or updates a ChromaDB vector database in the `data` directory.

4.  **`plagiarism_checker/main.py`:**
    * **Installation:** Requires the project dependencies, including `fastapi`, `uvicorn`, and `openai`.
    * **Running:** Executed by `python3 plagiarism_checker/main.py` (from the `plagiarism_checker` directory).
    * **Functionality:** Starts the FastAPI web application. It provides endpoints to:
        * Display a web interface for plagiarism checking.
        * Check plagiarism using RAG only (based on similarity).
        * Check plagiarism using LLM only (direct query to OpenAI).
        * Check plagiarism using the full system (RAG + LLM with context).
        * Save the results of plagiarism checks to `plagiarism_check_results.csv`.
        * (If evaluation features are added) Evaluate the different plagiarism checking approaches and save results to `evaluation_results.csv`.

5.  **`main.py` (in the root directory):**
    * **Installation:** No specific installation needed.
    * **Running:** Executed by `python3 main.py` (from the root directory).
    * **Functionality:** A convenience script to run all the main components sequentially: GitHub repository cloning, code embedding, vector database creation, and starting the plagiarism checker API.

## CSV Output Explanation

The plagiarism checker can save results to CSV files in the same directory where the FastAPI application (`plagiarism_checker/main.py`) is run.

1.  **`plagiarism_check_results.csv`:** This file stores the results of each plagiarism check you perform through the web interface when you click the "Save Plagiarism Check Results to CSV" button. It includes the following columns:
    * `check_type`: The type of plagiarism check performed ("Full System", "RAG Only", "LLM Only").
    * `input_code`: The code snippet you submitted for checking.
    * `result`: The plagiarism detection result (e.g., "Plagiarized (Similarity: ...)").
    * `similarity`: The similarity score (only for RAG Only checks).
    * `references`: The file paths of the reference code files identified by the full system.

2.  **`evaluation_results.csv` (if evaluation features are added):** This file stores the results of the system evaluation. It includes columns such as:
    * `input_code`: The code snippet used for evaluation.
    * `expected_plagiarism`: The expected plagiarism status (yes/no).
    * `actual_result`: The plagiarism result from the system.
    * `similarity`: The similarity score (for RAG).
    * `references`: The references identified by the full system.
    * `expected_references`: The expected reference file paths (for the full system).
    * `evaluation_status`: Whether the system's result matched the expected outcome.



### Project full description:

Final Project: Code Plagiarism Checker System
Objective: In this project, you will create a demo system for detecting code plagiarism. Your task is to build a system that can find similar code snippets from existing code repositories based on the code snippet provided by the user and determine whether the presented code is plagiarized.

Main Stages of the Project:

Fetching Code Repositories:
You need to gather a list of code repositories. For this, you can use the GitHub API or simply specify the links to the repositories in a configuration file.
The repositories you fetch should be cloned to your local environment using git clone.
Our recommendation is to choose 2-3 simple repositories for the system as we are building a simple system.

Code Indexing:
From the downloaded repositories, you should search for code files (for example, .py, .java, .c, etc.).
For each code file, you need to calculate a vector representation (embedding). For this, you should select an appropriate embedding model from the Hugging Face library. Ideally, find a model that works well for representing the semantic content of code.
The generated embeddings should be stored in a vector database. You can use libraries such as Faiss, ChromaDB, Pinecone, or another option you prefer.

Building the Plagiarism Checking System (RAG Principle):
You need to create an API (for example, using FastAPI) that will receive the content of a code file uploaded by the user (not the file itself, but its content as a string).
When the user submits a code snippet, your system must first search for similar code files in the vector database. For this, you will use the embedding of the provided code snippet and the vector database search function.
Next, you should connect to the LLMs (Large Language Models) through your preferred API. You should send the entire aggregated prompt to the LLM, including the code snippet provided by the user and the similar code files returned from the vector database (as context).
Importantly: The LLM should return only two words: "Yes" (if the code is plagiarized) or "No" (if the code is not plagiarized). To achieve this, you must use prompt engineering techniques. Also, ask the LLM to refer to the code files returned from the vector database as references (if plagiarism is confirmed).

System Evaluation:
You need to create a small dataset containing both plagiarized and non-plagiarized cases. You can create this manually or with the help of AI.
Using the created dataset, you should compare the results of the following three approaches:

Only RAG: Use your built RAG system and some threshold value for similarity to determine if the code is plagiarized.
Only LLM: Directly query the LLM with the user's code snippet and ask it to assess whether it's plagiarized.
Your Complete System: Use the fully functional system that combines vector search and LLM with reference-based answers.
The evaluation results should be saved in a CSV file.
Important Notes (This is a Demo System):

Note that this project primarily demonstrates the concept of plagiarism checking and not an ideal, fully-optimized system.
Indexing a large number of GitHub repositories requires significant computational resources (calculating embeddings) and time. There are also technical difficulties related to processing large code files. You may need to devise tricks to handle comparing large code files. For simplicity, select a few repositories with smaller code files.
Also, bear in mind that in an ideal case, plagiarism checking should be done between repositories rather than individual code files. However, for the simplicity of the project, we will limit the comparison to code files (as text files).
Requirements:

Indexing Script: You must write a separate Python script that will download the repositories and index the code files into the vector database. This script should be containerized using Docker.
Embedding Server: The embedding model should be hosted as a separate service. This service should also be containerized using Docker.
Plagiarism Checking API: The API responsible for checking plagiarism should be built using FastAPI. This API will accept an HTTP POST request with the content of the code file (as a string). The API should return a boolean variable indicating whether the code is plagiarized. This API should also be containerized using Docker.
Evaluation Script: You should write a script that runs the evaluation process and compares the results of the three approaches. This script should also be containerized.
Project Presentation:
After completing the project, you will individually present your work. We will not accept projects in ZIP file format. You should upload your project code to GitHub in your personal repository. The repository should be public (not public during the development process to avoid plagiarism ;) Your own code will be tested for plagiarism on each other). When presenting, you must provide the link to your repository. Your repository should contain a well-described README.md file in English, detailing the project structure, instructions for running it, and other important information. During the presentation, you will demonstrate your system, explain how you set it up, the technologies you used, the challenges you faced, and how you solved them. You should also show your code and answer any questions we have.

Deadlines and Support:
You will have 3 weeks to complete this project. During this time, you can reach out with any questions that will help you successfully complete the project.

Evaluation:
Please note that partial completion of the project will also be evaluated. So, don’t be discouraged by the complexity of the project, and try to do your best, even if you cannot complete every part of the task.

Additional Recommendations:

Start the project early to ensure you have enough time to complete all the stages.
Break the project into smaller, manageable sub-tasks.
Use Git from the beginning; don’t upload everything in one commit at the end.
Document your code and the project architecture.
Don’t hesitate to ask questions if something is unclear.
