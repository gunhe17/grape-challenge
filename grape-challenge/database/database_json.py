import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
from threading import RLock
import uuid

class JSONDatabase:
    def __init__(self, db_path: str = None):
        # Use environment variable for test database
        if db_path is None:
            if os.environ.get('TEST_MODE') == 'true':
                db_path = os.environ.get('TEST_DB_PATH', '../database/test_db.json')
            else:
                db_path = '../database/db.json'

        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = RLock()
        self._ensure_database()

    def _ensure_database(self):
        """Initialize database file with default structure if it doesn't exist"""
        if not self.db_path.exists():
            default_data = {
                "users": [],
                "sessions": [],
                "fruits": [],
                "missions": [],
                "fruit_templates": [],
                "mission_templates": [],
                "_metadata": {
                    "created_at": datetime.now().isoformat(),
                    "last_modified": datetime.now().isoformat()
                }
            }
            self._write_data(default_data)

    def _read_data(self) -> Dict[str, Any]:
        """Read data from JSON file"""
        try:
            with open(self.db_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self._ensure_database()
            with open(self.db_path, 'r', encoding='utf-8') as f:
                return json.load(f)

    def _write_data(self, data: Dict[str, Any]):
        """Write data to JSON file"""
        if "_metadata" not in data:
            data["_metadata"] = {}
        data["_metadata"]["last_modified"] = datetime.now().isoformat()
        with open(self.db_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def get_table(self, table_name: str) -> List[Dict[str, Any]]:
        """Get all records from a table"""
        with self._lock:
            data = self._read_data()
            return data.get(table_name, [])

    def insert(self, table_name: str, record: Dict[str, Any]) -> Dict[str, Any]:
        """Insert a record into a table"""
        with self._lock:
            data = self._read_data()
            if table_name not in data:
                data[table_name] = []

            # Auto-generate UUID if not provided
            if 'id' not in record:
                record['id'] = str(uuid.uuid4())

            # Add timestamps
            now = datetime.now().isoformat()
            record['created_at'] = record.get('created_at', now)
            record['updated_at'] = now

            data[table_name].append(record)
            self._write_data(data)
            return record

    def find(self, table_name: str, **filters) -> List[Dict[str, Any]]:
        """Find records matching filters"""
        with self._lock:
            records = self.get_table(table_name)
            if not filters:
                return records

            result = []
            for record in records:
                match = True
                for key, value in filters.items():
                    if record.get(key) != value:
                        match = False
                        break
                if match:
                    result.append(record)
            return result

    def find_one(self, table_name: str, **filters) -> Optional[Dict[str, Any]]:
        """Find first record matching filters"""
        results = self.find(table_name, **filters)
        return results[0] if results else None

    def update(self, table_name: str, record_id: Union[str, int], updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update a record by ID"""
        with self._lock:
            data = self._read_data()
            if table_name not in data:
                return None

            # Convert record_id to string for consistent comparison
            record_id_str = str(record_id)

            for i, record in enumerate(data[table_name]):
                if str(record.get('id')) == record_id_str:
                    record.update(updates)
                    record['updated_at'] = datetime.now().isoformat()
                    data[table_name][i] = record
                    self._write_data(data)
                    return record
            return None

    def delete(self, table_name: str, record_id: Union[str, int]) -> bool:
        """Delete a record by ID"""
        with self._lock:
            data = self._read_data()
            if table_name not in data:
                return False

            # Convert record_id to string for consistent comparison
            record_id_str = str(record_id)

            for i, record in enumerate(data[table_name]):
                if str(record.get('id')) == record_id_str:
                    del data[table_name][i]
                    self._write_data(data)
                    return True
            return False

# Global database instance
json_db = JSONDatabase()