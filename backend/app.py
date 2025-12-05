from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import os
import tempfile
import subprocess
import threading
import queue
import uuid
import json
import time
from dotenv import load_dotenv
from ai_test_generator import create_generator, TestGenerationResult

# Load environment variables from .env file
load_dotenv()

os.environ["PYNGUIN_DANGER_AWARE"] = "1"


app = Flask(__name__)
CORS(app)

@app.route("/generate-tests", methods=["POST"])
def generate_tests():
    # Start a background pynguin generation task and return a task id.
    code = request.json.get("code")
    if not code:
        return jsonify({"error": "No code provided"}), 400

    task_id = str(uuid.uuid4())
    tasks[task_id] = {"queue": queue.Queue(), "done": False}

    def _run_task(tid, src_code):
        q = tasks[tid]["queue"]
        tmp_dir = tempfile.mkdtemp()
        code_file = os.path.join(tmp_dir, "user_code.py")
        output_dir = os.path.join(tmp_dir, "tests")
        os.makedirs(output_dir, exist_ok=True)

        with open(code_file, "w", encoding="utf-8") as f:
            f.write(src_code)

        # Ensure subprocess uses UTF-8 for IO to avoid encoding issues
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"

        cmd = [
            "pynguin",
            "--project-path", tmp_dir,
            "--output-path", output_dir,
            "--module-name", "user_code",
            "-v"
        ]

        try:
            # Start process and stream stdout/stderr
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env, text=True, bufsize=1)
            for line in p.stdout:
                # Send each line to queue
                q.put({"type": "log", "line": line.rstrip("\n")})

            p.wait()

            # After process ends, attempt to read generated test
            test_file_path = os.path.join(output_dir, "test_user_code.py")
            if os.path.exists(test_file_path):
                with open(test_file_path, "r", encoding="utf-8") as f:
                    test_code = f.read()
                q.put({"type": "result", "test_code": test_code})
            else:
                q.put({"type": "error", "message": "Test file not generated"})

        except Exception as e:
            q.put({"type": "error", "message": str(e)})
        finally:
            tasks[tid]["done"] = True

    thread = threading.Thread(target=_run_task, args=(task_id, code), daemon=True)
    thread.start()
    return jsonify({"task_id": task_id})


# Note: symbol extraction endpoint removed per user request.


# Simple in-memory task store for streaming logs
tasks = {}


@app.route("/generate-ai-tests", methods=["POST"])
def generate_ai_tests():
    """Generate tests using OpenAI via HuggingFace."""
    code = request.json.get("code")
    if not code:
        return jsonify({"error": "No code provided"}), 400
        
    try:
        generator = create_generator()  # Will use HF_TOKEN from env
        result = generator.generate_tests(code)
        
        if result.error:
            return jsonify({"error": result.error}), 500
            
        return jsonify({"test_code": result.test_code})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/generate-tests/stream/<task_id>')
def stream_task(task_id):
    """SSE stream for a running generation task."""
    if task_id not in tasks:
        return jsonify({"error": "Unknown task id"}), 404

    q = tasks[task_id]["queue"]

    def event_stream():
        # Stream until task is done and queue is exhausted
        while True:
            try:
                item = q.get(timeout=0.5)
            except queue.Empty:
                if tasks[task_id]["done"]:
                    break
                # send a keep-alive comment to avoid proxies closing connection
                yield ': keep-alive\n\n'
                continue

            # Send structured JSON per event
            try:
                payload = json.dumps(item, ensure_ascii=False)
            except Exception:
                payload = json.dumps({"type": "log", "line": str(item)})

            yield f"data: {payload}\n\n"

        # Final done event
        yield 'data: {"type": "done"}\n\n'

    return Response(event_stream(), mimetype='text/event-stream')

if __name__ == "__main__":
    app.run(debug=True)
