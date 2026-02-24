"""
Pipeline Report Archive Routes
Save / list / view / delete HTML pipeline reports.
"""
from flask import Blueprint, request, jsonify, Response
from models.pipeline_report import PipelineReportModel
from middleware.auth import token_required

pipeline_report_bp = Blueprint('pipeline_reports', __name__)
_model = PipelineReportModel()


@pipeline_report_bp.route('/', methods=['POST'])
@token_required
def save_report():
    """Save a generated HTML report to the archive."""
    data = request.get_json() or {}
    title = data.get('title', '').strip() or 'Pipeline Report'
    html  = data.get('html', '').strip()
    meta  = data.get('meta', {})

    if not html:
        return jsonify({'error': 'html is required'}), 400

    user_id   = request.current_user['_id']
    report_id = _model.save_report(user_id, title, html, meta)
    return jsonify({'id': report_id, 'title': title, 'saved': True}), 201


@pipeline_report_bp.route('/', methods=['GET'])
@token_required
def list_reports():
    """List all saved reports for the current user (no HTML body)."""
    user_id = request.current_user['_id']
    reports = _model.list_reports(user_id)
    return jsonify({'reports': reports})


@pipeline_report_bp.route('/<report_id>', methods=['GET'])
@token_required
def get_report(report_id):
    """Return full report including HTML."""
    user_id = request.current_user['_id']
    report  = _model.get_report(report_id, user_id)
    if not report:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(report)


@pipeline_report_bp.route('/<report_id>/html', methods=['GET'])
@token_required
def view_report_html(report_id):
    """Return the raw HTML for rendering in an iframe / new tab."""
    user_id = request.current_user['_id']
    report  = _model.get_report(report_id, user_id)
    if not report:
        return jsonify({'error': 'Not found'}), 404
    return Response(report['html'], mimetype='text/html')


@pipeline_report_bp.route('/<report_id>', methods=['DELETE'])
@token_required
def delete_report(report_id):
    """Delete a saved report."""
    user_id = request.current_user['_id']
    if _model.delete_report(report_id, user_id):
        return jsonify({'message': 'Deleted'})
    return jsonify({'error': 'Not found'}), 404
