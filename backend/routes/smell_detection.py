"""Route handlers for test smell detection."""

from flask import Blueprint, request, jsonify, send_file
import os
import tempfile
import shutil
import git
from werkzeug.utils import secure_filename
from modules.smell_detector import TestSmellAnalyzer
from services.gemini_service import generate_explanations_for_logs, generate_explanations_for_logs_from_code

smell_detect_bp = Blueprint('smell_detector', __name__)
analyzer = TestSmellAnalyzer()


@smell_detect_bp.route('/analyze/file', methods=['POST'])
def analyze_uploaded_file():
    """Analyze a single uploaded test file for smells."""
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    if file.filename == '' or not file.filename.endswith('.py'):
        return jsonify({"error": "Please upload a Python (.py) file"}), 400
    
    # Save file temporarily
    temp_dir = tempfile.mkdtemp()
    filename = secure_filename(file.filename)
    filepath = os.path.join(temp_dir, filename)
    file.save(filepath)
    
    try:
        # Analyze the file
        all_logs, projects, ts_qtd, cont_total = analyzer.analyze_files([filepath])
        
        # Optional LLM explanations
        use_llm = request.args.get('use_llm', 'false').lower() in ('1', 'true', 'yes')
        explanations = None
        if use_llm:
            explanations = {}
            # Only one project/file here
            for idx, logs in enumerate(all_logs):
                proj_path = projects[idx]
                explanations.update(generate_explanations_for_logs(proj_path, logs))
        
        # Generate report
        report_path = analyzer.generate_report(all_logs, projects, ts_qtd, cont_total, explanations)
        
        return jsonify({
            "status": "success",
            "total_smells": cont_total,
            "report_available": True
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


@smell_detect_bp.route('/analyze/code', methods=['POST'])
def analyze_code_string():
    """Analyze test code from a string."""
    code = request.json.get("code")
    filename = request.json.get("filename", "test_code.py")
    
    if not code:
        return jsonify({"error": "No code provided"}), 400
    
    try:
        # Analyze the code
        result = analyzer.analyze_code_string(code, filename)
        
        # Generate report with this single file
        all_logs = [result['logs']]
        projects = [result['filepath']]
        ts_qtd = [result['smell_count']]
        cont_total = result['smell_count']
        
        # Optional LLM explanations
        use_llm = request.args.get('use_llm', 'false').lower() in ('1', 'true', 'yes')
        explanations = None
        if use_llm:
            # Use code text directly to build context with correct line numbers
            explanations = generate_explanations_for_logs_from_code(code, filename, all_logs[0])

        report_path = analyzer.generate_report(all_logs, projects, ts_qtd, cont_total, explanations)
        
        # Return detailed results
        smells = []
        prev = None
        for log in result['logs']:
            if log.lines != prev:
                smells.append({
                    "type": log.test_smell_type,
                    "method": log.method_name,
                    "lines": log.lines
                })
                prev = log.lines
        
        return jsonify({
            "status": "success",
            "total_smells": cont_total,
            "smells": smells,
            "report_available": True
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@smell_detect_bp.route('/analyze/directory', methods=['POST'])
def analyze_directory():
    """Analyze multiple uploaded test files."""
    if 'files[]' not in request.files:
        return jsonify({"error": "No files uploaded"}), 400
    
    files = request.files.getlist('files[]')
    if not files or files[0].filename == '':
        return jsonify({"error": "No files selected"}), 400
    
    temp_dir = tempfile.mkdtemp()
    
    try:
        # Save all uploaded files
        uploaded_files = []
        for file in files:
            if file and file.filename.endswith('.py'):
                filename = secure_filename(file.filename)
                filepath = os.path.join(temp_dir, filename)
                file.save(filepath)
                uploaded_files.append(filepath)
        
        if not uploaded_files:
            return jsonify({"error": "No Python files found"}), 400
        
        # Analyze all files
        all_logs, projects, ts_qtd, cont_total = analyzer.analyze_files(uploaded_files)
        
        # Optional LLM explanations
        use_llm = request.args.get('use_llm', 'false').lower() in ('1', 'true', 'yes')
        explanations = None
        if use_llm:
            explanations = {}
            for idx, logs in enumerate(all_logs):
                proj_path = projects[idx]
                explanations.update(generate_explanations_for_logs(proj_path, logs))
        
        # Generate report
        report_path = analyzer.generate_report(all_logs, projects, ts_qtd, cont_total, explanations)
        
        return jsonify({
            "status": "success",
            "files_analyzed": len(uploaded_files),
            "total_smells": cont_total,
            "report_available": True
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


@smell_detect_bp.route('/analyze/github', methods=['POST'])
def analyze_github():
    """Analyze test files from a GitHub repository."""
    git_url = request.json.get('github_url', '').strip()
    
    if not git_url or 'github.com/' not in git_url:
        return jsonify({"error": "Please enter a valid GitHub URL"}), 400
    
    project_dir = tempfile.mkdtemp()
    
    try:
        # Clone repository
        git.Repo.clone_from(git_url, project_dir)
        
        # Search for test files
        from modules.smell_detector.analyzer import search_test_files
        test_files = search_test_files(project_dir)
        
        if not test_files:
            return jsonify({"error": "No test files found in the repository"}), 404
        
        # Analyze test files
        all_logs, projects, ts_qtd, cont_total = analyzer.analyze_files(test_files)
        
        # Optional LLM explanations
        use_llm = request.args.get('use_llm', 'false').lower() in ('1', 'true', 'yes')
        explanations = None
        if use_llm:
            explanations = {}
            for idx, logs in enumerate(all_logs):
                proj_path = projects[idx]
                explanations.update(generate_explanations_for_logs(proj_path, logs))
        
        # Generate report
        report_path = analyzer.generate_report(all_logs, projects, ts_qtd, cont_total, explanations)
        
        return jsonify({
            "status": "success",
            "files_analyzed": len(test_files),
            "total_smells": cont_total,
            "report_available": True
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        shutil.rmtree(project_dir, ignore_errors=True)


@smell_detect_bp.route('/report')
def get_report():
    """Retrieve the generated HTML report."""
    report_path = os.path.abspath('./report/log.html')
    if os.path.exists(report_path):
        return send_file(report_path)
    else:
        return jsonify({"error": "No report available"}), 404


@smell_detect_bp.route('/report/download')
def download_report():
    """Download the generated HTML report as an attachment."""
    report_path = os.path.abspath('./report/log.html')
    if os.path.exists(report_path):
        return send_file(report_path, as_attachment=True, download_name='test_smells_report.html')
    else:
        return jsonify({"error": "No report available"}), 404


@smell_detect_bp.route('/report/ai')
def get_ai_report():
    """Retrieve the AI-powered generated HTML report."""
    report_path = os.path.abspath('./report/log_ai.html')
    if os.path.exists(report_path):
        return send_file(report_path)
    else:
        return jsonify({"error": "No AI report available"}), 404


@smell_detect_bp.route('/report/ai/download')
def download_ai_report():
    """Download the AI-powered report as an attachment."""
    report_path = os.path.abspath('./report/log_ai.html')
    if os.path.exists(report_path):
        return send_file(report_path, as_attachment=True, download_name='test_smells_report_ai.html')
    else:
        return jsonify({"error": "No AI report available"}), 404
