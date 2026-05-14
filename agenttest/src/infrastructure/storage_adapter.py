"""存储适配器抽象基类"""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any


class StorageAdapter(ABC):
    """存储适配器抽象基类"""
    
    @abstractmethod
    def connect(self) -> bool:
        """建立连接
        
        Returns:
            连接是否成功
        """
        pass
    
    @abstractmethod
    def disconnect(self) -> bool:
        """断开连接
        
        Returns:
            断开是否成功
        """
        pass
    
    @abstractmethod
    def save(self, entity_type: str, entity_id: str, data: Dict[str, Any]) -> bool:
        """保存实体
        
        Args:
            entity_type: 实体类型
            entity_id: 实体ID
            data: 实体数据
            
        Returns:
            保存是否成功
        """
        pass
    
    @abstractmethod
    def find_by_id(self, entity_type: str, entity_id: str) -> Optional[Dict[str, Any]]:
        """根据ID查询实体
        
        Args:
            entity_type: 实体类型
            entity_id: 实体ID
            
        Returns:
            实体数据
        """
        pass
    
    @abstractmethod
    def find_all(self, entity_type: str, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """查询所有实体
        
        Args:
            entity_type: 实体类型
            filters: 过滤条件
            
        Returns:
            实体列表
        """
        pass
    
    @abstractmethod
    def update(self, entity_type: str, entity_id: str, data: Dict[str, Any]) -> bool:
        """更新实体
        
        Args:
            entity_type: 实体类型
            entity_id: 实体ID
            data: 更新数据
            
        Returns:
            更新是否成功
        """
        pass
    
    @abstractmethod
    def delete(self, entity_type: str, entity_id: str) -> bool:
        """删除实体
        
        Args:
            entity_type: 实体类型
            entity_id: 实体ID
            
        Returns:
            删除是否成功
        """
        pass
    
    @abstractmethod
    def exists(self, entity_type: str, entity_id: str) -> bool:
        """检查实体是否存在
        
        Args:
            entity_type: 实体类型
            entity_id: 实体ID
            
        Returns:
            是否存在
        """
        pass
    
    @abstractmethod
    def count(self, entity_type: str, filters: Optional[Dict[str, Any]] = None) -> int:
        """统计实体数量
        
        Args:
            entity_type: 实体类型
            filters: 过滤条件
            
        Returns:
            数量
        """
        pass
