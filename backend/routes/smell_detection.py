"""Route handlers for test smell detection."""

from flask import Blueprint, request, jsonify, send_file
import os
import tempfile
import shutil
import git
from werkzeug.utils import secure_filename
from modules.smell_detector import TestSmellAnalyzer
from services.gemini_service import generate_explanations_for_logs, generate_explanations_for_logs_from_code
from services.llm_smell_service import detect_smells_with_llm, AVAILABLE_MODELS as LLM_MODELS

smell_detect_bp = Blueprint('smell_detector', __name__)
analyzer = TestSmellAnalyzer()


@smell_detect_bp.route('/llm-models', methods=['GET'])
def get_llm_models():
    """Return available LLM models for smell detection."""
    return jsonify(LLM_MODELS)


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

    # Detection method: rule_based (default) or llm_based
    detection_method = request.args.get('detection_method', 'rule_based')
    model_type = request.args.get('model_type', 'ollama')
    model_name = request.args.get('model_name', 'llama3.2')
    
    try:
        # Read file content
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            file_content = f.read()

        # ---- LLM-based detection ----
        if detection_method == 'llm_based':
            result = detect_smells_with_llm(
                code=file_content,
                filename=filename,
                model_type=model_type,
                model_name=model_name,
            )
            if not result['success']:
                return jsonify({"error": result['error']}), 500
            return jsonify({
                "status": "success",
                "detection_method": "llm_based",
                "model_used": result['model_used'],
                "total_smells": result['total_smells'],
                "smells": result['smells'],
                "code": file_content,
                "report_available": False,
            })

        # ---- Rule-based detection (existing) ----
        all_logs, projects, ts_qtd, cont_total = analyzer.analyze_files([filepath])
        
        # Optional Gemini LLM explanations for the HTML report
        use_llm = request.args.get('use_llm', 'false').lower() in ('1', 'true', 'yes')
        explanations = None
        if use_llm:
            explanations = {}
            for idx, logs in enumerate(all_logs):
                proj_path = projects[idx]
                explanations.update(generate_explanations_for_logs(proj_path, logs))
        
        # Generate report
        analyzer.generate_report(all_logs, projects, ts_qtd, cont_total, explanations)

        # Build smells list
        smells = []
        if all_logs:
            prev = None
            for log in all_logs[0]:
                if log.lines != prev:
                    smells.append({
                        "type": log.test_smell_type,
                        "method": log.method_name,
                        "lines": log.lines
                    })
                    prev = log.lines
        
        return jsonify({
            "status": "success",
            "detection_method": "rule_based",
            "total_smells": cont_total,
            "smells": smells,
            "code": file_content,
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
    detection_method = request.json.get("detection_method") or request.args.get('detection_method', 'rule_based')
    model_type = request.json.get("model_type") or request.args.get('model_type', 'ollama')
    model_name = request.json.get("model_name") or request.args.get('model_name', 'llama3.2')
    
    if not code:
        return jsonify({"error": "No code provided"}), 400
    
    try:
        # ---- LLM-based detection ----
        if detection_method == 'llm_based':
            result = detect_smells_with_llm(
                code=code,
                filename=filename,
                model_type=model_type,
                model_name=model_name,
            )
            if not result['success']:
                return jsonify({"error": result['error']}), 500
            return jsonify({
                "status": "success",
                "detection_method": "llm_based",
                "model_used": result['model_used'],
                "total_smells": result['total_smells'],
                "smells": result['smells'],
                "report_available": False,
            })

        # ---- Rule-based detection (existing) ----
        result = analyzer.analyze_code_string(code, filename)
        
        # Generate report with this single file
        all_logs = [result['logs']]
        projects = [result['filepath']]
        ts_qtd = [result['smell_count']]
        cont_total = result['smell_count']
        
        # Optional Gemini LLM explanations for the HTML report
        use_llm = request.args.get('use_llm', 'false').lower() in ('1', 'true', 'yes')
        explanations = None
        if use_llm:
            explanations = generate_explanations_for_logs_from_code(code, filename, all_logs[0])

        analyzer.generate_report(all_logs, projects, ts_qtd, cont_total, explanations)
        
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
            "detection_method": "rule_based",
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

    detection_method = request.args.get('detection_method', 'rule_based')
    model_type = request.args.get('model_type', 'ollama')
    model_name = request.args.get('model_name', 'llama3.2')
    
    temp_dir = tempfile.mkdtemp()
    
    try:
        # Save all uploaded files
        uploaded_files = []
        file_original_names = []
        for file in files:
            if file and file.filename.endswith('.py'):
                orig_name = file.filename
                filename = secure_filename(orig_name)
                filepath = os.path.join(temp_dir, filename)
                file.save(filepath)
                uploaded_files.append(filepath)
                file_original_names.append(orig_name)
        
        if not uploaded_files:
            return jsonify({"error": "No Python files found"}), 400

        # ---- LLM-based detection ----
        if detection_method == 'llm_based':
            files_result = []
            total_smells = 0
            for fp, orig_name in zip(uploaded_files, file_original_names):
                try:
                    with open(fp, 'r', encoding='utf-8', errors='replace') as f:
                        file_code = f.read()
                except Exception:
                    file_code = ""
                llm_result = detect_smells_with_llm(
                    code=file_code,
                    filename=orig_name,
                    model_type=model_type,
                    model_name=model_name,
                )
                smells = llm_result['smells'] if llm_result['success'] else []
                total_smells += len(smells)
                files_result.append({
                    "filename": os.path.basename(fp),
                    "code": file_code,
                    "smells": smells,
                    "smell_count": len(smells),
                })
            return jsonify({
                "status": "success",
                "detection_method": "llm_based",
                "model_used": model_name,
                "files_analyzed": len(uploaded_files),
                "total_smells": total_smells,
                "files": files_result,
                "report_available": False,
            })

        # ---- Rule-based detection (existing) ----
        all_logs, projects, ts_qtd, cont_total = analyzer.analyze_files(uploaded_files)
        
        # Optional Gemini LLM explanations for the HTML report
        use_llm = request.args.get('use_llm', 'false').lower() in ('1', 'true', 'yes')
        explanations = None
        if use_llm:
            explanations = {}
            for idx, logs in enumerate(all_logs):
                proj_path = projects[idx]
                explanations.update(generate_explanations_for_logs(proj_path, logs))
        
        # Generate report
        analyzer.generate_report(all_logs, projects, ts_qtd, cont_total, explanations)

        # Build per-file results (rule-based)
        files_result = []
        for i, fp in enumerate(uploaded_files):
            fname = os.path.basename(fp)
            try:
                with open(fp, 'r', encoding='utf-8', errors='replace') as f:
                    file_code = f.read()
            except Exception:
                file_code = ""

            file_logs = all_logs[i] if i < len(all_logs) else []
            file_smells = []
            prev = None
            for log in file_logs:
                if log.lines != prev:
                    file_smells.append({
                        "type": log.test_smell_type,
                        "method": log.method_name,
                        "lines": log.lines
                    })
                    prev = log.lines

            files_result.append({
                "filename": fname,
                "code": file_code,
                "smells": file_smells,
                "smell_count": ts_qtd[i] if i < len(ts_qtd) else len(file_smells)
            })

        return jsonify({
            "status": "success",
            "detection_method": "rule_based",
            "files_analyzed": len(uploaded_files),
            "total_smells": cont_total,
            "files": files_result,
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
    detection_method = request.json.get('detection_method') or request.args.get('detection_method', 'rule_based')
    model_type = request.json.get('model_type') or request.args.get('model_type', 'ollama')
    model_name = request.json.get('model_name') or request.args.get('model_name', 'llama3.2')
    
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

        # ---- LLM-based detection ----
        if detection_method == 'llm_based':
            files_result = []
            total_smells = 0
            for fp in test_files:
                try:
                    with open(fp, 'r', encoding='utf-8', errors='replace') as f:
                        file_code = f.read()
                except Exception:
                    file_code = ""
                fname = os.path.basename(fp)
                llm_result = detect_smells_with_llm(
                    code=file_code,
                    filename=fname,
                    model_type=model_type,
                    model_name=model_name,
                )
                smells = llm_result['smells'] if llm_result['success'] else []
                total_smells += len(smells)
                files_result.append({
                    "filename": fname,
                    "code": file_code,
                    "smells": smells,
                    "smell_count": len(smells),
                })
            return jsonify({
                "status": "success",
                "detection_method": "llm_based",
                "model_used": model_name,
                "files_analyzed": len(test_files),
                "total_smells": total_smells,
                "files": files_result,
                "report_available": False,
            })

        # ---- Rule-based detection (existing) ----
        all_logs, projects, ts_qtd, cont_total = analyzer.analyze_files(test_files)
        
        # Optional Gemini LLM explanations for the HTML report
        use_llm = request.args.get('use_llm', 'false').lower() in ('1', 'true', 'yes')
        explanations = None
        if use_llm:
            explanations = {}
            for idx, logs in enumerate(all_logs):
                proj_path = projects[idx]
                explanations.update(generate_explanations_for_logs(proj_path, logs))
        
        # Generate report
        analyzer.generate_report(all_logs, projects, ts_qtd, cont_total, explanations)

        # Build per-file results (rule-based)
        files_result = []
        for i, fp in enumerate(test_files):
            fname = os.path.basename(fp)
            try:
                with open(fp, 'r', encoding='utf-8', errors='replace') as f:
                    file_code = f.read()
            except Exception:
                file_code = ""

            file_logs = all_logs[i] if i < len(all_logs) else []
            file_smells = []
            prev = None
            for log in file_logs:
                if log.lines != prev:
                    file_smells.append({
                        "type": log.test_smell_type,
                        "method": log.method_name,
                        "lines": log.lines
                    })
                    prev = log.lines

            files_result.append({
                "filename": fname,
                "code": file_code,
                "smells": file_smells,
                "smell_count": ts_qtd[i] if i < len(ts_qtd) else len(file_smells)
            })

        return jsonify({
            "status": "success",
            "detection_method": "rule_based",
            "files_analyzed": len(test_files),
            "total_smells": cont_total,
            "files": files_result,
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
