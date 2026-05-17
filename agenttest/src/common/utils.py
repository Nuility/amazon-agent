"""工具函数"""
import uuid
import re
from datetime import datetime
from typing import Any, Dict, Set
import copy


def generate_uuid() -> str:
    """生成UUID"""
    return str(uuid.uuid4())


def timestamp_now() -> int:
    """获取当前时间戳（毫秒）"""
    return int(datetime.now().timestamp() * 1000)


def sanitize_data(data: Dict[str, Any], sensitive_fields: Set[str]) -> Dict[str, Any]:
    """数据脱敏处理
    
    Args:
        data: 原始数据
        sensitive_fields: 敏感字段集合
        
    Returns:
        脱敏后的数据
    """
    result = {}
    for key, value in data.items():
        if key in sensitive_fields:
            result[key] = "***"
        elif isinstance(value, dict):
            result[key] = sanitize_data(value, sensitive_fields)
        else:
            result[key] = value
    return result


def deep_copy(obj: Any) -> Any:
    """深拷贝对象
    
    Args:
        obj: 原始对象
        
    Returns:
        拷贝后的对象
    """
    return copy.deepcopy(obj)


def format_duration(ms: int) -> str:
    """格式化持续时间
    
    Args:
        ms: 毫秒数
        
    Returns:
        格式化的时间字符串
    """
    if ms < 1000:
        return f"{ms}ms"
    elif ms < 60000:
        return f"{ms / 1000:.2f}s"
    else:
        return f"{ms / 60000:.2f}m"


def mask_email(email: str) -> str:
    """邮箱脱敏
    
    Args:
        email: 邮箱地址
        
    Returns:
        脱敏后的邮箱
    """
    if not email or '@' not in email:
        return email
    
    parts = email.split('@')
    username = parts[0]
    domain = parts[1]
    
    if len(username) <= 2:
        masked_username = username[0] + '***'
    else:
        masked_username = username[0] + '***' + username[-1]
    
    return f"{masked_username}@{domain}"


def mask_phone(phone: str) -> str:
    """手机号脱敏
    
    Args:
        phone: 手机号
        
    Returns:
        脱敏后的手机号
    """
    if not phone:
        return phone
    
    if len(phone) <= 7:
        return phone[:3] + '***'
    else:
        return phone[:3] + '***' + phone[-4:]


def is_valid_json_path(path: str) -> bool:
    """检查是否为有效的JSON文件路径
    
    Args:
        path: 文件路径
        
    Returns:
        是否有效
    """
    return path.endswith('.json')


def is_valid_yaml_path(path: str) -> bool:
    """检查是否为有效的YAML文件路径
    
    Args:
        path: 文件路径
        
    Returns:
        是否有效
    """
    return path.endswith('.yaml') or path.endswith('.yml')
