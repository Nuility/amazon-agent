"""文件存储适配器"""
import json
import os
import threading
from typing import Dict, List, Optional, Any
from infrastructure.storage_adapter import StorageAdapter
from common.exceptions import StorageException


class FileStorageAdapter(StorageAdapter):
    """文件存储适配器"""
    
    def __init__(self, file_path: str):
        """初始化文件存储适配器
        
        Args:
            file_path: 数据文件路径
        """
        self.file_path = file_path
        self.lock = threading.Lock()
        self.data: Dict[str, Dict[str, Dict[str, Any]]] = {}
        self._connected = False
    
    def connect(self) -> bool:
        """建立连接"""
        try:
            file_dir = os.path.dirname(self.file_path)
            if file_dir and not os.path.exists(file_dir):
                os.makedirs(file_dir, exist_ok=True)
            
            if os.path.exists(self.file_path):
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
            else:
                self.data = {}
                self._save_to_file()
            
            self._connected = True
            return True
        except Exception as e:
            raise StorageException(f"连接文件存储失败: {str(e)}", e)
    
    def disconnect(self) -> bool:
        """断开连接"""
        self._connected = False
        return True
    
    def save(self, entity_type: str, entity_id: str, data: Dict[str, Any]) -> bool:
        """保存实体"""
        if not self._connected:
            raise StorageException("存储未连接")
        
        with self.lock:
            if entity_type not in self.data:
                self.data[entity_type] = {}
            
            self.data[entity_type][entity_id] = data
            self._save_to_file()
            return True
    
    def find_by_id(self, entity_type: str, entity_id: str) -> Optional[Dict[str, Any]]:
        """根据ID查询实体"""
        if not self._connected:
            raise StorageException("存储未连接")
        
        with self.lock:
            if entity_type not in self.data:
                return None
            return self.data[entity_type].get(entity_id)
    
    def find_all(self, entity_type: str, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """查询所有实体"""
        if not self._connected:
            raise StorageException("存储未连接")
        
        with self.lock:
            if entity_type not in self.data:
                return []
            
            entities = list(self.data[entity_type].values())
            
            if filters:
                entities = self._apply_filters(entities, filters)
            
            return entities
    
    def update(self, entity_type: str, entity_id: str, data: Dict[str, Any]) -> bool:
        """更新实体"""
        if not self._connected:
            raise StorageException("存储未连接")
        
        with self.lock:
            if entity_type not in self.data or entity_id not in self.data[entity_type]:
                return False
            
            self.data[entity_type][entity_id].update(data)
            self._save_to_file()
            return True
    
    def delete(self, entity_type: str, entity_id: str) -> bool:
        """删除实体"""
        if not self._connected:
            raise StorageException("存储未连接")
        
        with self.lock:
            if entity_type not in self.data or entity_id not in self.data[entity_type]:
                return False
            
            del self.data[entity_type][entity_id]
            self._save_to_file()
            return True
    
    def exists(self, entity_type: str, entity_id: str) -> bool:
        """检查实体是否存在"""
        if not self._connected:
            raise StorageException("存储未连接")
        
        with self.lock:
            if entity_type not in self.data:
                return False
            return entity_id in self.data[entity_type]
    
    def count(self, entity_type: str, filters: Optional[Dict[str, Any]] = None) -> int:
        """统计实体数量"""
        return len(self.find_all(entity_type, filters))
    
    def _save_to_file(self):
        """保存到文件"""
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            raise StorageException(f"保存文件失败: {str(e)}", e)
    
    def _apply_filters(self, entities: List[Dict[str, Any]], filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        """应用过滤条件"""
        result = []
        for entity in entities:
            match = True
            for key, value in filters.items():
                if key == "status":
                    if entity.get("status") != value:
                        match = False
                        break
                elif key == "tags":
                    if not isinstance(value, list):
                        value = [value]
                    entity_tags = entity.get("tags", [])
                    if not all(tag in entity_tags for tag in value):
                        match = False
                        break
                elif key in entity:
                    if entity[key] != value:
                        match = False
                        break
            
            if match:
                result.append(entity)
        
        return result
    
    def begin_transaction(self):
        """开始事务"""
        pass
    
    def commit(self):
        """提交事务"""
        pass
    
    def rollback(self):
        """回滚事务"""
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
