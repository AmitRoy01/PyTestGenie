"""Route handlers for test generation."""

from flask import Blueprint, request, jsonify, Response
import uuid
import queue
import threading
import json
from modules.test_generator import PynguinGenerator, AITestGenerator

test_gen_bp = Blueprint('test_generator', __name__)

# Task storage for streaming
tasks = {}


@test_gen_bp.route('/generate-tests/pynguin', methods=['POST'])
def generate_pynguin_tests():
    """Generate tests using Pynguin with streaming logs."""
    code = request.json.get("code")
    if not code:
        return jsonify({"error": "No code provided"}), 400

    task_id = str(uuid.uuid4())
    tasks[task_id] = {"queue": queue.Queue(), "done": False}

    def _run_task(tid, src_code):
        q = tasks[tid]["queue"]
        generator = PynguinGenerator()
        
        try:
            generator.generate_tests_async(src_code, q)
        except Exception as e:
            q.put({"type": "error", "message": str(e)})
        finally:
            tasks[tid]["done"] = True

    thread = threading.Thread(target=_run_task, args=(task_id, code), daemon=True)
    thread.start()
    
    return jsonify({"task_id": task_id})


@test_gen_bp.route('/generate-tests/stream/<task_id>')
def stream_task(task_id):
    """SSE stream for a running Pynguin generation task."""
    if task_id not in tasks:
        return jsonify({"error": "Unknown task id"}), 404

    q = tasks[task_id]["queue"]

    def event_stream():
        while True:
            try:
                item = q.get(timeout=0.5)
            except queue.Empty:
                if tasks[task_id]["done"]:
                    break
                yield ': keep-alive\n\n'
                continue

            try:
                payload = json.dumps(item, ensure_ascii=False)
            except Exception:
                payload = json.dumps({"type": "log", "line": str(item)})

            yield f"data: {payload}\n\n"

        yield 'data: {"type": "done"}\n\n'

    return Response(event_stream(), mimetype='text/event-stream')


@test_gen_bp.route('/generate-tests/ai', methods=['POST'])
def generate_ai_tests():
    """Generate tests using AI (OpenAI via HuggingFace)."""
    code = request.json.get("code")
    if not code:
        return jsonify({"error": "No code provided"}), 400
        
    try:
        generator = AITestGenerator()
        result = generator.generate_tests(code)
        
        if result.error:
            return jsonify({"error": result.error}), 500
            
        return jsonify({
            "test_code": result.test_code,
            "method": result.method
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
