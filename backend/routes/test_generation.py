"""Route handlers for test generation."""

from flask import Blueprint, request, jsonify, Response
import uuid
import queue
import threading
import json
import os
import tempfile
import shutil
from pathlib import Path
from werkzeug.utils import secure_filename
from modules.test_generator import PynguinGenerator, AITestGenerator

test_gen_bp = Blueprint('test_generator', __name__)

# Task storage for streaming
tasks = {}

# Allowed file extensions
ALLOWED_EXTENSIONS = {'.py'}

def allowed_file(filename):
    """Check if file has allowed extension."""
    return Path(filename).suffix in ALLOWED_EXTENSIONS


@test_gen_bp.route('/generate-tests/pynguin', methods=['POST'])
def generate_pynguin_tests():
    """Generate tests using Pynguin with streaming logs."""
    code = request.json.get("code")
    algorithm = request.json.get("algorithm", "DYNAMOSA")  # Default to DYNAMOSA
    if not code:
        return jsonify({"error": "No code provided"}), 400

    task_id = str(uuid.uuid4())
    tasks[task_id] = {"queue": queue.Queue(), "done": False}

    def _run_task(tid, src_code, algo):
        q = tasks[tid]["queue"]
        generator = PynguinGenerator()
        
        try:
            generator.generate_tests_async(src_code, q, algorithm=algo)
        except Exception as e:
            q.put({"type": "error", "message": str(e)})
        finally:
            tasks[tid]["done"] = True

    thread = threading.Thread(target=_run_task, args=(task_id, code, algorithm), daemon=True)
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
    """Generate tests using AI (GPT-OSS or Llama 3.2).
    
    Supports both standalone code and project-aware generation.
    If project_id is provided, will analyze imports and include dependency context.
    """
    code = request.json.get("code")
    model = request.json.get("model", "gpt-oss")  # Default to gpt-oss
    project_id = request.json.get("project_id")  # Optional: for project-aware generation
    
    if not code:
        return jsonify({"error": "No code provided"}), 400
    
    # Get project path if project_id is provided
    project_path = None
    if project_id and project_id in tasks and tasks[project_id].get("type") == "project":
        project_info = tasks[project_id]
        base_path = project_info["path"]
        package_name = project_info.get("package_name")
        
        # Set project path to package directory if exists
        if package_name:
            project_path = os.path.join(base_path, package_name)
        else:
            project_path = base_path
        
    try:
        generator = AITestGenerator(model_name=model)
        result = generator.generate_tests(code, project_path=project_path)
        
        if result.error:
            return jsonify({"error": result.error}), 500
            
        return jsonify({
            "test_code": result.test_code,
            "method": result.method,
            "model_used": model
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@test_gen_bp.route('/upload-file', methods=['POST'])
def upload_file():
    """Upload a single Python file and return its content."""
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    if not allowed_file(file.filename):
        return jsonify({"error": "Only .py files are allowed"}), 400
    
    try:
        # Read file content with proper encoding handling
        try:
            content = file.read().decode('utf-8')
        except UnicodeDecodeError:
            # Try with latin-1 as fallback (handles all byte values)
            file.seek(0)
            content = file.read().decode('latin-1')
        
        filename = secure_filename(file.filename)
        
        return jsonify({
            "filename": filename,
            "content": content,
            "size": len(content)
        })
    except Exception as e:
        return jsonify({"error": f"Error reading file: {str(e)}"}), 500


@test_gen_bp.route('/upload-project', methods=['POST'])
def upload_project():
    """Upload project folder and list Python files."""
    if 'files' not in request.files:
        return jsonify({"error": "No files provided"}), 400
    
    files = request.files.getlist('files')
    if not files:
        return jsonify({"error": "No files selected"}), 400
    
    try:
        # Create temporary directory to store project
        temp_dir = tempfile.mkdtemp(prefix="pytestgenie_project_")
        project_id = os.path.basename(temp_dir)
        
        python_files = []
        package_name = None
        
        for file in files:
            if file.filename and allowed_file(file.filename):
                # Get relative path from the file
                filepath = file.filename
                
                # Normalize path separators (handle both / and \)
                filepath = filepath.replace('\\', '/')
                
                # Get package name from first path component
                path_parts = filepath.split('/')
                if len(path_parts) > 1 and package_name is None:
                    package_name = path_parts[0]
                
                # Ensure safe filename - keep folder structure
                safe_path = os.path.join(temp_dir, filepath)
                
                # Create directories if needed
                safe_dir = os.path.dirname(safe_path)
                if safe_dir:
                    os.makedirs(safe_dir, exist_ok=True)
                
                # Save file with proper encoding handling
                try:
                    # Read content from uploaded file
                    content_bytes = file.read()
                    # Try to decode and re-encode as UTF-8
                    try:
                        content_str = content_bytes.decode('utf-8')
                    except UnicodeDecodeError:
                        # Fallback: decode as latin-1 (handles all byte values)
                        content_str = content_bytes.decode('latin-1')
                    
                    # Write as UTF-8
                    with open(safe_path, 'w', encoding='utf-8') as f:
                        f.write(content_str)
                except Exception as save_err:
                    print(f"Error saving file {filepath}: {save_err}")
                    continue
                
                # Add to list of Python files (with relative path from package root)
                python_files.append({
                    "path": filepath,
                    "name": os.path.basename(filepath),
                    "size": os.path.getsize(safe_path)
                })
        
        # Create __init__.py in package folder if it doesn't exist (for relative imports)
        if package_name:
            package_dir = os.path.join(temp_dir, package_name)
            init_file = os.path.join(package_dir, '__init__.py')
            if not os.path.exists(init_file):
                with open(init_file, 'w', encoding='utf-8') as f:
                    f.write('# Auto-generated package file\n')
                print(f"Created __init__.py in {package_name}")
        
        # Store project info in tasks dict for later retrieval
        tasks[project_id] = {
            "type": "project",
            "path": temp_dir,
            "package_name": package_name,
            "files": python_files
        }
        
        return jsonify({
            "project_id": project_id,
            "files": python_files,
            "total_files": len(python_files),
            "package_name": package_name
        })
    
    except Exception as e:
        return jsonify({"error": f"Error uploading project: {str(e)}"}), 500


@test_gen_bp.route('/generate-tests/project', methods=['POST'])
def generate_project_tests():
    """Generate tests for a specific module in uploaded project using Pynguin."""
    data = request.json
    project_id = data.get("project_id")
    module_name = data.get("module_name")  # e.g., "calculator" or "MyPackage/calculator"
    algorithm = data.get("algorithm", "DYNAMOSA")
    
    if not project_id or not module_name:
        return jsonify({"error": "project_id and module_name are required"}), 400
    
    if project_id not in tasks or tasks[project_id].get("type") != "project":
        return jsonify({"error": "Invalid project_id"}), 400
    
    project_info = tasks[project_id]
    project_path = project_info["path"]
    package_name = project_info.get("package_name")
    
    # Build proper module path for Pynguin
    # e.g., "MyPackage/calculator.py" -> "MyPackage.calculator"
    module_path = module_name.replace('\\', '/').replace('.py', '')
    
    # If module is inside package, use dot notation
    if '/' in module_path:
        pynguin_module = module_path.replace('/', '.')
    else:
        # If package exists, prepend it
        if package_name:
            pynguin_module = f"{package_name}.{module_path}"
        else:
            pynguin_module = module_path
    
    # Create a new task for streaming
    task_id = str(uuid.uuid4())
    tasks[task_id] = {"queue": queue.Queue(), "done": False}
    
    def _run_project_task(tid, proj_path, mod_name, algo):
        q = tasks[tid]["queue"]
        generator = PynguinGenerator()
        
        try:
            generator.generate_tests_for_project(proj_path, mod_name, q, algorithm=algo)
        except Exception as e:
            q.put({"type": "error", "message": str(e)})
        finally:
            tasks[tid]["done"] = True
    
    thread = threading.Thread(
        target=_run_project_task,
        args=(task_id, project_path, pynguin_module, algorithm),
        daemon=True
    )
    thread.start()
    
    return jsonify({"task_id": task_id})


@test_gen_bp.route('/project/<project_id>/file/<path:filepath>', methods=['GET'])
def get_project_file(project_id, filepath):
    """Get content of a specific file from uploaded project."""
    if project_id not in tasks or tasks[project_id].get("type") != "project":
        return jsonify({"error": "Invalid project_id"}), 400
    
    project_path = tasks[project_id]["path"]
    file_path = os.path.join(project_path, filepath)
    
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        return jsonify({"error": "File not found"}), 404
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return jsonify({
            "filepath": filepath,
            "content": content,
            "size": len(content)
        })
    except Exception as e:
        return jsonify({"error": f"Error reading file: {str(e)}"}), 500
