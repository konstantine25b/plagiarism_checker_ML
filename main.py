# main.py (in the root directory of your plagiarism_checker_ML project)
import subprocess
import os
import sys

def run_script(script_path, description):
    """Runs a Python script using subprocess and prints output."""
    print(f"\n--- Starting {description} ---")
    try:
        process = subprocess.Popen([sys.executable, script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        while True:
            output = process.stdout.readline()
            if output == b'' and process.poll() is not None:
                break
            if output:
                print(output.strip().decode())
        stderr = process.stderr.read().decode()
        if stderr:
            print(f"Error in {description}:\n{stderr}")
        return process.returncode == 0
    except FileNotFoundError:
        print(f"Error: Script not found at {script_path}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred while running {description}: {e}")
        return False

if __name__ == "__main__":
    project_root = os.path.dirname(os.path.abspath(__file__))

    github_extractor_path = os.path.join(project_root, "github_extractor", "main.py")
    code_embedder_path = os.path.join(project_root, "code_embedder", "main.py")
    vector_db_path = os.path.join(project_root, "vector_db", "main.py")
    plagiarism_checker_path = os.path.join(project_root, "plagiarism_checker", "main.py")

    # Activate virtual environment (optional - assumes it's already active)
    print("--- Ensuring Virtual Environment is Active ---")
    if 'venv' in sys.prefix:
        print("Virtual environment is active.")
    else:
        print("Warning: Virtual environment might not be active. Consider activating it before running this script.")

    # Run the scripts sequentially
    github_success = run_script(github_extractor_path, "GitHub Repository Cloning")
    if github_success:
        embedder_success = run_script(code_embedder_path, "Code Embedding")
        if embedder_success:
            vector_db_success = run_script(vector_db_path, "Vector Database Creation/Update")
            if vector_db_success:
                print("\n--- Starting Plagiarism Checker FastAPI Application ---")
                try:
                    # Run the plagiarism checker in a new process so this script doesn't block
                    subprocess.Popen([sys.executable, plagiarism_checker_path])
                    print("Plagiarism checker application is starting. You can access it at http://0.0.0.0:8000")
                    print("This script will continue to run in the background. Press CTRL+C to stop the FastAPI application.")
                    # Keep the main script alive to allow the FastAPI app to run
                    while True:
                        import time
                        time.sleep(1)
                except FileNotFoundError:
                    print(f"Error: Script not found at {plagiarism_checker_path}")
                except Exception as e:
                    print(f"An unexpected error occurred while starting the plagiarism checker: {e}")
            else:
                print("Vector database step failed. Stopping.")
        else:
            print("Code embedding step failed. Stopping.")
    else:
        print("GitHub repository cloning failed. Stopping.")