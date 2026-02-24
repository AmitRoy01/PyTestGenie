"""
Dashboard Routes
User stats summary + profile/password management.
"""
from flask import Blueprint, request, jsonify
from middleware.auth import token_required
from models.project import ProjectModel
from models.pipeline_report import PipelineReportModel
from models.user import UserModel
from services.auth_service import AuthService
from pymongo import MongoClient
from bson import ObjectId
import os

dashboard_bp = Blueprint('dashboard', __name__)

_project_model = ProjectModel()
_report_model  = PipelineReportModel()
_user_model    = UserModel()
_auth_service  = AuthService()


# ── helpers ───────────────────────────────────────────────────────────────────

def _versions_col():
    """Return the project_versions collection directly for aggregation."""
    client = MongoClient(os.getenv('MONGODB_URL', 'mongodb://localhost:27017'))
    return client[os.getenv('DATABASE_NAME', 'pyTestGenie')]['project_versions']


def _reports_col():
    client = MongoClient(os.getenv('MONGODB_URL', 'mongodb://localhost:27017'))
    return client[os.getenv('DATABASE_NAME', 'pyTestGenie')]['pipeline_reports']


# ── GET /api/dashboard/stats ──────────────────────────────────────────────────

@dashboard_bp.route('/stats', methods=['GET'])
@token_required
def get_stats():
    """Return 4 quick-stat counts for the current user."""
    user_id = request.current_user['_id']
    versions = _versions_col()
    reports  = _reports_col()

    # 1. Saved project versions
    saved_projects = versions.count_documents({'user_id': user_id})

    # 2. Saved pipeline reports
    saved_reports = reports.count_documents({'user_id': user_id})

    # 3. Total smells across all saved versions
    pipeline = [
        {'$match': {'user_id': user_id}},
        {'$group': {
            '_id': None,
            'total': {'$sum': {'$ifNull': ['$data.smell_results.total_smells', 0]}}
        }}
    ]
    agg = list(versions.aggregate(pipeline))
    total_smells = agg[0]['total'] if agg else 0

    # 4. Refactoring count (versions where step == 'refactored')
    total_refactorings = versions.count_documents({
        'user_id': user_id,
        'step': 'refactored',
    })

    # Recent activity: last 5 saves (versions) + last 5 reports, merged & sorted
    recent_versions = list(
        versions.find({'user_id': user_id}, {'data': 0})
                .sort('created_at', -1).limit(5)
    )
    recent_reports = list(
        reports.find({'user_id': user_id}, {'html': 0})
               .sort('created_at', -1).limit(5)
    )

    def fmt_version(v):
        return {
            'id':    str(v['_id']),
            'kind':  'project',
            'title': v.get('label') or v.get('name') or 'Project Save',
            'step':  v.get('step', ''),
            'date':  v['created_at'].isoformat() if v.get('created_at') else '',
        }

    def fmt_report(r):
        return {
            'id':    str(r['_id']),
            'kind':  'report',
            'title': r.get('title', 'Pipeline Report'),
            'step':  '',
            'date':  r['created_at'].isoformat() if r.get('created_at') else '',
        }

    activity = [fmt_version(v) for v in recent_versions] + \
               [fmt_report(r) for r in recent_reports]
    activity.sort(key=lambda x: x['date'], reverse=True)
    activity = activity[:8]

    return jsonify({
        'saved_projects':    saved_projects,
        'saved_reports':     saved_reports,
        'total_smells':      int(total_smells),
        'total_refactorings': total_refactorings,
        'recent_activity':   activity,
    })


# ── PUT /api/dashboard/change-password ───────────────────────────────────────

@dashboard_bp.route('/change-password', methods=['PUT'])
@token_required
def change_password():
    """Change current user's password after verifying the current one."""
    data = request.get_json() or {}
    current_pw  = data.get('current_password', '').strip()
    new_pw      = data.get('new_password', '').strip()

    if not current_pw or not new_pw:
        return jsonify({'error': 'current_password and new_password are required'}), 400

    if len(new_pw) < 6:
        return jsonify({'error': 'New password must be at least 6 characters'}), 400

    # Fetch full user doc (includes hashed password)
    username   = request.current_user['username']
    user_doc   = _user_model.get_user_by_username(username)
    if not user_doc:
        return jsonify({'error': 'User not found'}), 404

    # Verify current password
    if not _auth_service.verify_password(current_pw, user_doc['password']):
        return jsonify({'error': 'Current password is incorrect'}), 401

    # Hash & save new password
    new_hashed = _auth_service.hash_password(new_pw)
    _user_model.users.update_one(
        {'username': username},
        {'$set': {'password': new_hashed}}
    )

    return jsonify({'message': 'Password changed successfully'})
