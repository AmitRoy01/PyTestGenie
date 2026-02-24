"""
Project History Routes
CRUD for projects and their versions
"""
from flask import Blueprint, request, jsonify
from models.project import ProjectModel
from middleware.auth import token_required

projects_bp = Blueprint('projects', __name__)
_model = ProjectModel()


# ── Projects ──────────────────────────────────────────────────────────────────

@projects_bp.route('/', methods=['GET'])
@token_required
def get_projects():
    user_id = request.current_user['_id']
    return jsonify({'projects': _model.get_projects(user_id)})


@projects_bp.route('/', methods=['POST'])
@token_required
def create_project():
    data = request.get_json() or {}
    name = data.get('name', '').strip()
    if not name:
        return jsonify({'error': 'Project name is required'}), 400
    user_id = request.current_user['_id']
    project_id = _model.create_project(user_id, name, data.get('description', ''))
    return jsonify({'id': project_id, 'name': name}), 201


@projects_bp.route('/<project_id>', methods=['GET'])
@token_required
def get_project(project_id):
    user_id = request.current_user['_id']
    project = _model.get_project(project_id, user_id)
    if not project:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(project)


@projects_bp.route('/<project_id>', methods=['DELETE'])
@token_required
def delete_project(project_id):
    user_id = request.current_user['_id']
    if _model.delete_project(project_id, user_id):
        return jsonify({'message': 'Project deleted'})
    return jsonify({'error': 'Not found'}), 404


# ── Versions...

@projects_bp.route('/<project_id>/versions', methods=['GET'])
@token_required
def get_versions(project_id):
    user_id = request.current_user['_id']
    versions = _model.get_versions(project_id, user_id)
    if versions is None:
        return jsonify({'error': 'Project not found'}), 404
    return jsonify({'versions': versions})


@projects_bp.route('/<project_id>/versions', methods=['POST'])
@token_required
def create_version(project_id):
    user_id = request.current_user['_id']
    if not _model.get_project(project_id, user_id):
        return jsonify({'error': 'Project not found'}), 404

    data = request.get_json() or {}
    label = data.get('label', 'Version').strip() or 'Version'
    step  = data.get('step', 'source')

    version_id = _model.create_version(project_id, user_id, label, step, data)
    return jsonify({'id': version_id, 'label': label, 'version_saved': True}), 201


@projects_bp.route('/versions/<version_id>', methods=['GET'])
@token_required
def get_version(version_id):
    user_id = request.current_user['_id']
    version = _model.get_version(version_id, user_id)
    if not version:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(version)


@projects_bp.route('/versions/<version_id>', methods=['DELETE'])
@token_required
def delete_version(version_id):
    user_id = request.current_user['_id']
    success, message = _model.delete_version(version_id, user_id)
    if success:
        return jsonify({'message': message})
    return jsonify({'error': message}), 400
