"""
Pipeline Report Archive Model
Stores generated HTML pipeline reports in MongoDB.
"""
from pymongo import MongoClient, DESCENDING
from datetime import datetime
from bson import ObjectId
import os


class PipelineReportModel:
    def __init__(self):
        mongodb_url   = os.getenv('MONGODB_URL', 'mongodb://localhost:27017')
        database_name = os.getenv('DATABASE_NAME', 'pyTestGenie')
        client = MongoClient(mongodb_url)
        db = client[database_name]
        self.reports = db['pipeline_reports']
        self.reports.create_index([('user_id', 1)])
        self.reports.create_index([('created_at', DESCENDING)])

    # ── CRUD ──────────────────────────────────────────────────────────────────

    def save_report(self, user_id: str, title: str, html: str, meta: dict) -> str:
        """Persist a report and return its id."""
        doc = {
            'user_id':    user_id,
            'title':      title,
            'html':       html,
            'meta':       meta,          # stages present, smell count, etc.
            'created_at': datetime.utcnow(),
        }
        result = self.reports.insert_one(doc)
        return str(result.inserted_id)

    def list_reports(self, user_id: str) -> list:
        docs = self.reports.find(
            {'user_id': user_id},
            {'html': 0}                  # exclude heavy HTML from list view
        ).sort('created_at', DESCENDING)
        return [self._fmt(d) for d in docs]

    def get_report(self, report_id: str, user_id: str):
        try:
            doc = self.reports.find_one({'_id': ObjectId(report_id), 'user_id': user_id})
        except Exception:
            return None
        return self._fmt(doc) if doc else None

    def delete_report(self, report_id: str, user_id: str) -> bool:
        try:
            result = self.reports.delete_one({'_id': ObjectId(report_id), 'user_id': user_id})
        except Exception:
            return False
        return result.deleted_count > 0

    # ── Helpers ───────────────────────────────────────────────────────────────

    @staticmethod
    def _fmt(doc: dict) -> dict:
        d = dict(doc)
        d['id'] = str(d.pop('_id'))
        if 'created_at' in d:
            d['created_at'] = d['created_at'].isoformat()
        return d
