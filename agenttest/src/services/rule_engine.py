"""规则引擎"""
from typing import Dict, Any
from common.types import UserStatus
from common.exceptions import (
    ValidationException,
    BatchLimitExceededException,
    InvalidStatusTransitionException
)


class RuleEngine:
    """规则引擎"""
    
    def validate_user_creation(self, user_data: Dict[str, Any]) -> None:
        """验证用户创建规则
        
        Args:
            user_data: 用户数据
            
        Raises:
            ValidationException: 验证失败
        """
        if "username" not in user_data:
            raise ValidationException("用户名不能为空", field="username")
        
        if "email" not in user_data:
            raise ValidationException("邮箱不能为空", field="email")
        
        username = user_data.get("username", "")
        if not username or len(username.strip()) == 0:
            raise ValidationException("用户名不能为空字符串", field="username")
        
        if len(username) > 128:
            raise ValidationException("用户名长度不能超过128字符", field="username")
    
    def validate_user_update(self, user_id: str, update_data: Dict[str, Any]) -> None:
        """验证用户更新规则
        
        Args:
            user_id: 用户ID
            update_data: 更新数据
            
        Raises:
            ValidationException: 验证失败
        """
        if not user_id:
            raise ValidationException("用户ID不能为空", field="user_id")
        
        if not update_data:
            raise ValidationException("更新数据不能为空", field="update_data")
        
        if "username" in update_data:
            username = update_data["username"]
            if not username or len(username.strip()) == 0:
                raise ValidationException("用户名不能为空字符串", field="username")
            if len(username) > 128:
                raise ValidationException("用户名长度不能超过128字符", field="username")
        
        if "status" in update_data:
            status = update_data["status"]
            if status not in [s.value for s in UserStatus]:
                raise ValidationException(f"无效的用户状态: {status}", field="status")
    
    def validate_user_deletion(self, user_id: str) -> None:
        """验证用户删除规则
        
        Args:
            user_id: 用户ID
            
        Raises:
            ValidationException: 验证失败
        """
        if not user_id:
            raise ValidationException("用户ID不能为空", field="user_id")
    
    def validate_status_transition(self, current_status: str, new_status: str) -> None:
        """验证状态流转
        
        Args:
            current_status: 当前状态
            new_status: 新状态
            
        Raises:
            InvalidStatusTransitionException: 无效的状态转换
        """
        valid_transitions = {
            UserStatus.ACTIVE.value: [UserStatus.INACTIVE.value, UserStatus.DELETED.value],
            UserStatus.INACTIVE.value: [UserStatus.ACTIVE.value, UserStatus.DELETED.value],
            UserStatus.DELETED.value: []
        }
        
        if current_status not in valid_transitions:
            raise InvalidStatusTransitionException(current_status, new_status)
        
        if new_status not in valid_transitions[current_status]:
            raise InvalidStatusTransitionException(current_status, new_status)
    
    def check_batch_limit(self, batch_size: int, max_limit: int) -> None:
        """检查批量操作限制
        
        Args:
            batch_size: 批量操作数量
            max_limit: 最大限制
            
        Raises:
            BatchLimitExceededException: 超出限制
        """
        if batch_size <= 0:
            raise ValidationException("批量操作数量必须大于0", field="batch_size")
        
        if batch_size > max_limit:
            raise BatchLimitExceededException(batch_size, max_limit)
    
    def validate_batch_data(self, batch_data: list) -> None:
        """验证批量数据
        
        Args:
            batch_data: 批量数据
            
        Raises:
            ValidationException: 验证失败
        """
        if not batch_data:
            raise ValidationException("批量数据不能为空", field="batch_data")
        
        if not isinstance(batch_data, list):
            raise ValidationException("批量数据必须是列表", field="batch_data")
