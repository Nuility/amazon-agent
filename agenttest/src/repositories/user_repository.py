"""用户仓储"""
from typing import Dict, List, Optional, Any
from common.types import User
from common.exceptions import UserNotFoundException, StorageException
from infrastructure.storage_adapter import StorageAdapter


class UserRepository:
    """用户仓储"""
    
    ENTITY_TYPE = "users"
    
    def __init__(self, storage_adapter: StorageAdapter):
        """初始化用户仓储
        
        Args:
            storage_adapter: 存储适配器
        """
        self.storage = storage_adapter
    
    def save(self, user: User) -> bool:
        """保存用户
        
        Args:
            user: 用户实体
            
        Returns:
            保存是否成功
        """
        try:
            return self.storage.save(
                self.ENTITY_TYPE,
                user.user_id,
                user.to_dict()
            )
        except Exception as e:
            raise StorageException(f"保存用户失败: {str(e)}", e)
    
    def find_by_id(self, user_id: str) -> Optional[User]:
        """根据ID查询用户
        
        Args:
            user_id: 用户ID
            
        Returns:
            用户实体
        """
        data = self.storage.find_by_id(self.ENTITY_TYPE, user_id)
        if data:
            return User.from_dict(data)
        return None
    
    def find_all(self, filters: Optional[Dict[str, Any]] = None) -> List[User]:
        """查询用户列表
        
        Args:
            filters: 过滤条件
            
        Returns:
            用户列表
        """
        data_list = self.storage.find_all(self.ENTITY_TYPE, filters)
        return [User.from_dict(data) for data in data_list]
    
    def find_by_username(self, username: str) -> Optional[User]:
        """根据用户名查询用户
        
        Args:
            username: 用户名
            
        Returns:
            用户实体
        """
        users = self.find_all()
        for user in users:
            if user.username == username:
                return user
        return None
    
    def find_by_email(self, email: str) -> Optional[User]:
        """根据邮箱查询用户
        
        Args:
            email: 邮箱
            
        Returns:
            用户实体
        """
        users = self.find_all()
        for user in users:
            if user.email == email:
                return user
        return None
    
    def update(self, user_id: str, data: Dict[str, Any]) -> bool:
        """更新用户
        
        Args:
            user_id: 用户ID
            data: 更新数据
            
        Returns:
            更新是否成功
        """
        try:
            return self.storage.update(self.ENTITY_TYPE, user_id, data)
        except Exception as e:
            raise StorageException(f"更新用户失败: {str(e)}", e)
    
    def delete(self, user_id: str) -> bool:
        """删除用户
        
        Args:
            user_id: 用户ID
            
        Returns:
            删除是否成功
        """
        try:
            return self.storage.delete(self.ENTITY_TYPE, user_id)
        except Exception as e:
            raise StorageException(f"删除用户失败: {str(e)}", e)
    
    def exists(self, user_id: str) -> bool:
        """检查用户是否存在
        
        Args:
            user_id: 用户ID
            
        Returns:
            是否存在
        """
        return self.storage.exists(self.ENTITY_TYPE, user_id)
    
    def count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        """统计用户数量
        
        Args:
            filters: 过滤条件
            
        Returns:
            数量
        """
        return self.storage.count(self.ENTITY_TYPE, filters)
