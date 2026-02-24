"""
Project & Version Model for MongoDB
Handles project history and version management
"""
from pymongo import MongoClient, ASCENDING, DESCENDING
from datetime import datetime
from bson import ObjectId
import os


class ProjectModel:
    def __init__(self):
        mongodb_url = os.getenv('MONGODB_URL', 'mongodb://localhost:27017')
        database_name = os.getenv('DATABASE_NAME', 'pyTestGenie')
        client = MongoClient(mongodb_url)
        db = client[database_name]
        self.projects = db['projects']
        self.versions = db['project_versions']
        self._create_indexes()

    def _create_indexes(self):
        self.projects.create_index([('user_id', ASCENDING)])
        self.versions.create_index([('project_id', ASCENDING)])
        self.versions.create_index([('project_id', ASCENDING), ('version_number', ASCENDING)])

    # ── Projects ──────────────────────────────────────────────────────────────

    def create_project(self, user_id: str, name: str, description: str = '') -> str:
        doc = {
            'user_id': user_id,
            'name': name,
            'description': description,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
        }
        result = self.projects.insert_one(doc)
        return str(result.inserted_id)

    def get_projects(self, user_id: str) -> list:
        docs = self.projects.find({'user_id': user_id}).sort('updated_at', DESCENDING)
        return [self._fmt_project(d) for d in docs]

    def get_project(self, project_id: str, user_id: str):
        try:
            doc = self.projects.find_one({'_id': ObjectId(project_id), 'user_id': user_id})
        except Exception:
            return None
        return self._fmt_project(doc) if doc else None

    def delete_project(self, project_id: str, user_id: str) -> bool:
        try:
            result = self.projects.delete_one({'_id': ObjectId(project_id), 'user_id': user_id})
        except Exception:
            return False
        if result.deleted_count:
            self.versions.delete_many({'project_id': project_id})
            return True
        return False

    def _touch_project(self, project_id: str):
        try:
            self.projects.update_one(
                {'_id': ObjectId(project_id)},
                {'$set': {'updated_at': datetime.utcnow()}}
            )
        except Exception:
            pass

    # ── Versions ──────────────────────────────────────────────────────────────

    def create_version(self, project_id: str, user_id: str,
                       label: str, step: str, data: dict) -> str:
        last = self.versions.find_one(
            {'project_id': project_id},
            sort=[('version_number', DESCENDING)]
        )
        version_number = (last['version_number'] + 1) if last else 1

        doc = {
            'project_id': project_id,
            'user_id': user_id,
            'version_number': version_number,
            'label': label,
            'step': step,
            # source
            'source_filename': data.get('source_filename', ''),
            'source_code':     data.get('source_code', ''),
            # test generation
            'test_code':       data.get('test_code', ''),
            'test_generator':  data.get('test_generator', ''),
            'test_algorithm':  data.get('test_algorithm', ''),
            # smell detection
            'smell_results':   data.get('smell_results', None),
            # refactoring
            'refactored_code': data.get('refactored_code', ''),
            'refactor_model':  data.get('refactor_model', ''),
            'refactor_smell':  data.get('refactor_smell', ''),
            'created_at': datetime.utcnow(),
        }
        result = self.versions.insert_one(doc)
        self._touch_project(project_id)
        return str(result.inserted_id)

    def get_versions(self, project_id: str, user_id: str):
        """Returns list of versions (without heavy code fields for listing)."""
        project = self.get_project(project_id, user_id)
        if not project:
            return None
        docs = self.versions.find(
            {'project_id': project_id},
            projection={'source_code': 0, 'test_code': 0,
                        'refactored_code': 0, 'smell_results': 0}
        ).sort('version_number', ASCENDING)
        return [self._fmt_version(d) for d in docs]

    def get_version(self, version_id: str, user_id: str):
        """Returns full version with all code fields."""
        try:
            doc = self.versions.find_one({'_id': ObjectId(version_id), 'user_id': user_id})
        except Exception:
            return None
        return self._fmt_version(doc) if doc else None

    def delete_version(self, version_id: str, user_id: str):
        try:
            version = self.versions.find_one({'_id': ObjectId(version_id), 'user_id': user_id})
        except Exception:
            return False, 'Version not found'
        if not version:
            return False, 'Version not found'
        count = self.versions.count_documents({'project_id': version['project_id']})
        if count <= 1:
            return False, 'Cannot delete the only version. Delete the project instead.'
        self.versions.delete_one({'_id': ObjectId(version_id)})
        return True, 'Deleted'

    # ── Serializers ───────────────────────────────────────────────────────────

    def _fmt_project(self, doc):
        if not doc:
            return None
        doc['id'] = str(doc.pop('_id'))
        doc['created_at'] = doc['created_at'].isoformat() if doc.get('created_at') else ''
        doc['updated_at'] = doc['updated_at'].isoformat() if doc.get('updated_at') else ''
        return doc

    def _fmt_version(self, doc):
        if not doc:
            return None
        doc['id'] = str(doc.pop('_id'))
        doc['created_at'] = doc['created_at'].isoformat() if doc.get('created_at') else ''
        return doc
