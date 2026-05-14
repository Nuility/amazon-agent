"""数据校验器"""
import re
from typing import Dict, List, Optional, Any
from .types import UserStatus
from .exceptions import ValidationException


class Validator:
    """数据校验器"""
    
    EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    PHONE_CN_PATTERN = re.compile(r'^1[3-9]\d{9}$')
    PHONE_INTERNATIONAL_PATTERN = re.compile(r'^\+?[1-9]\d{6,14}$')
    UUID_PATTERN = re.compile(r'^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$', re.IGNORECASE)
    
    @classmethod
    def validate_user_id(cls, user_id: str, allow_custom: bool = True) -> bool:
        """校验用户ID格式
        
        Args:
            user_id: 用户ID
            allow_custom: 是否允许自定义格式
            
        Returns:
            校验结果
        """
        if not user_id or not isinstance(user_id, str):
            return False
        
        if cls.UUID_PATTERN.match(user_id):
            return True
        
        if allow_custom:
            if len(user_id) < 1 or len(user_id) > 128:
                return False
            if user_id.isspace():
                return False
            return True
        
        return False
    
    @classmethod
    def validate_username(cls, username: str) -> bool:
        """校验用户名
        
        Args:
            username: 用户名
            
        Returns:
            校验结果
        """
        if not username or not isinstance(username, str):
            return False
        
        if len(username) < 1 or len(username) > 128:
            return False
        
        if username.isspace():
            return False
        
        return True
    
    @classmethod
    def validate_email(cls, email: str) -> bool:
        """校验邮箱格式
        
        Args:
            email: 邮箱地址
            
        Returns:
            校验结果
        """
        if not email or not isinstance(email, str):
            return False
        
        return bool(cls.EMAIL_PATTERN.match(email))
    
    @classmethod
    def validate_phone(cls, phone: str, allow_international: bool = True) -> bool:
        """校验手机号格式
        
        Args:
            phone: 手机号
            allow_international: 是否允许国际格式
            
        Returns:
            校验结果
        """
        if not phone or not isinstance(phone, str):
            return False
        
        phone = phone.strip()
        
        if cls.PHONE_CN_PATTERN.match(phone):
            return True
        
        if allow_international and cls.PHONE_INTERNATIONAL_PATTERN.match(phone):
            return True
        
        return False
    
    @classmethod
    def validate_user_status(cls, status: str) -> bool:
        """校验用户状态
        
        Args:
            status: 状态值
            
        Returns:
            校验结果
        """
        try:
            UserStatus(status)
            return True
        except ValueError:
            return False
    
    @classmethod
    def validate_status_transition(cls, current_status: str, new_status: str) -> bool:
        """校验状态流转合法性
        
        Args:
            current_status: 当前状态
            new_status: 新状态
            
        Returns:
            校验结果
        """
        valid_transitions = {
            UserStatus.ACTIVE.value: [UserStatus.INACTIVE.value, UserStatus.DELETED.value],
            UserStatus.INACTIVE.value: [UserStatus.ACTIVE.value, UserStatus.DELETED.value],
            UserStatus.DELETED.value: []
        }
        
        if current_status not in valid_transitions:
            return False
        
        return new_status in valid_transitions[current_status]
    
    @classmethod
    def validate_attributes(cls, attributes: Dict[str, str]) -> bool:
        """校验扩展属性
        
        Args:
            attributes: 属性字典
            
        Returns:
            校验结果
        """
        if not isinstance(attributes, dict):
            return False
        
        if len(attributes) > 50:
            return False
        
        for key, value in attributes.items():
            if not isinstance(key, str) or not isinstance(value, str):
                return False
            if len(value) > 1024:
                return False
        
        return True
    
    @classmethod
    def validate_tags(cls, tags: List[str]) -> bool:
        """校验标签列表
        
        Args:
            tags: 标签列表
            
        Returns:
            校验结果
        """
        if not isinstance(tags, list):
            return False
        
        if len(tags) > 20:
            return False
        
        for tag in tags:
            if not isinstance(tag, str):
                return False
            if len(tag) > 64:
                return False
        
        return True
    
    @classmethod
    def validate_user_data(cls, user_data: Dict[str, Any]) -> None:
        """校验用户数据完整性
        
        Args:
            user_data: 用户数据
            
        Raises:
            ValidationException: 校验失败
        """
        username = user_data.get("username")
        if not cls.validate_username(username):
            raise ValidationException("用户名格式无效", field="username")
        
        email = user_data.get("email")
        if not cls.validate_email(email):
            raise ValidationException("邮箱格式无效", field="email")
        
        phone = user_data.get("phone")
        if phone and not cls.validate_phone(phone):
            raise ValidationException("手机号格式无效", field="phone")
        
        status = user_data.get("status")
        if status and not cls.validate_user_status(status):
            raise ValidationException("用户状态无效", field="status")
        
        attributes = user_data.get("attributes")
        if attributes and not cls.validate_attributes(attributes):
            raise ValidationException("扩展属性格式无效", field="attributes")
        
        tags = user_data.get("tags")
        if tags and not cls.validate_tags(tags):
            raise ValidationException("标签格式无效", field="tags")
    
    @classmethod
    def validate_batch_size(cls, batch_size: int, max_limit: int) -> bool:
        """校验批量操作数量
        
        Args:
            batch_size: 批量操作数量
            max_limit: 最大限制
            
        Returns:
            校验结果
        """
        return isinstance(batch_size, int) and 0 < batch_size <= max_limit
