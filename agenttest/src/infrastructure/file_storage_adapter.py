"""JSON file-based storage adapter."""
import json
import os
import threading
from typing import Any, Dict, List, Optional

from common.exceptions import StorageException
from infrastructure.storage_adapter import StorageAdapter


class FileStorageAdapter(StorageAdapter):
    """Simple JSON-backed storage for local development."""

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.primary_file_path = file_path
        self.fallback_file_path = self._build_fallback_path(file_path)
        self.lock = threading.Lock()
        self.data: Dict[str, Dict[str, Dict[str, Any]]] = {}
        self._connected = False

    def connect(self) -> bool:
        try:
            file_dir = os.path.dirname(self.file_path)
            if file_dir and not os.path.exists(file_dir):
                os.makedirs(file_dir, exist_ok=True)

            if os.path.exists(self.file_path):
                with open(self.file_path, "r", encoding="utf-8") as f:
                    self.data = json.load(f) or {}
            else:
                self.data = {}
                self._save_to_file()

            self._connected = True
            return True
        except OSError:
            self.file_path = self.fallback_file_path
            try:
                file_dir = os.path.dirname(self.file_path)
                if file_dir and not os.path.exists(file_dir):
                    os.makedirs(file_dir, exist_ok=True)
                if os.path.exists(self.file_path):
                    with open(self.file_path, "r", encoding="utf-8") as f:
                        self.data = json.load(f) or {}
                else:
                    self.data = {}
                    self._save_to_file()
                self._connected = True
                return True
            except Exception as e:
                raise StorageException(f"Failed to connect file storage: {str(e)}", e)
        except Exception as e:
            raise StorageException(f"Failed to connect file storage: {str(e)}", e)

    def disconnect(self) -> bool:
        self._connected = False
        return True

    def save(self, entity_type: str, entity_id: str, data: Dict[str, Any]) -> bool:
        self._ensure_connected()
        with self.lock:
            if entity_type not in self.data:
                self.data[entity_type] = {}
            self.data[entity_type][entity_id] = data
            self._save_to_file()
            return True

    def find_by_id(self, entity_type: str, entity_id: str) -> Optional[Dict[str, Any]]:
        self._ensure_connected()
        with self.lock:
            if entity_type not in self.data:
                return None
            return self.data[entity_type].get(entity_id)

    def find_all(self, entity_type: str, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        self._ensure_connected()
        with self.lock:
            entities = list(self.data.get(entity_type, {}).values())
            return self._apply_filters(entities, filters or {})

    def update(self, entity_type: str, entity_id: str, data: Dict[str, Any]) -> bool:
        self._ensure_connected()
        with self.lock:
            if entity_id not in self.data.get(entity_type, {}):
                return False
            self.data[entity_type][entity_id].update(data)
            self._save_to_file()
            return True

    def delete(self, entity_type: str, entity_id: str) -> bool:
        self._ensure_connected()
        with self.lock:
            if entity_id not in self.data.get(entity_type, {}):
                return False
            del self.data[entity_type][entity_id]
            self._save_to_file()
            return True

    def exists(self, entity_type: str, entity_id: str) -> bool:
        self._ensure_connected()
        with self.lock:
            return entity_id in self.data.get(entity_type, {})

    def count(self, entity_type: str, filters: Optional[Dict[str, Any]] = None) -> int:
        return len(self.find_all(entity_type, filters))

    def begin_transaction(self):
        return None

    def commit(self):
        return None

    def rollback(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r", encoding="utf-8") as f:
                self.data = json.load(f) or {}

    def _ensure_connected(self):
        if not self._connected:
            raise StorageException("Storage is not connected")

    def _save_to_file(self):
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
        except OSError:
            if self.file_path != self.fallback_file_path:
                self.file_path = self.fallback_file_path
                with open(self.file_path, "w", encoding="utf-8") as f:
                    json.dump(self.data, f, ensure_ascii=False, indent=2)
                return
            raise
        except Exception as e:
            raise StorageException(f"Failed to save data file: {str(e)}", e)

    def _apply_filters(self, entities: List[Dict[str, Any]], filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        if not filters:
            return entities

        result: List[Dict[str, Any]] = []
        for entity in entities:
            match = True
            for key, value in filters.items():
                if key == "tags":
                    expected = value if isinstance(value, list) else [value]
                    entity_tags = entity.get("tags", [])
                    if not all(tag in entity_tags for tag in expected):
                        match = False
                        break
                elif entity.get(key) != value:
                    match = False
                    break
            if match:
                result.append(entity)
        return result

    def _build_fallback_path(self, file_path: str) -> str:
        runtime_root = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "runtime_data"))
        if not os.path.exists(runtime_root):
            os.makedirs(runtime_root, exist_ok=True)
        filename = os.path.basename(file_path)
        name, ext = os.path.splitext(filename)
        return os.path.join(runtime_root, f"{name}.runtime{ext or '.json'}")
