"""日志仓储"""
from typing import Dict, List, Optional, Any
from common.types import OperationLog
from common.exceptions import StorageException
from infrastructure.storage_adapter import StorageAdapter


class LogRepository:
    """日志仓储"""
    
    ENTITY_TYPE = "logs"
    
    def __init__(self, storage_adapter: StorageAdapter):
        """初始化日志仓储
        
        Args:
            storage_adapter: 存储适配器
        """
        self.storage = storage_adapter
    
    def save(self, log: OperationLog) -> bool:
        """保存操作日志
        
        Args:
            log: 操作日志实体
            
        Returns:
            保存是否成功
        """
        try:
            return self.storage.save(
                self.ENTITY_TYPE,
                log.log_id,
                log.to_dict()
            )
        except Exception as e:
            raise StorageException(f"保存日志失败: {str(e)}", e)
    
    def find_by_id(self, log_id: str) -> Optional[OperationLog]:
        """查询日志
        
        Args:
            log_id: 日志ID
            
        Returns:
            操作日志实体
        """
        data = self.storage.find_by_id(self.ENTITY_TYPE, log_id)
        if data:
            return OperationLog.from_dict(data)
        return None
    
    def find_by_user(self, user_id: str) -> List[OperationLog]:
        """查询用户的操作日志
        
        Args:
            user_id: 用户ID
            
        Returns:
            操作日志列表
        """
        all_logs = self.storage.find_all(self.ENTITY_TYPE)
        result = []
        for data in all_logs:
            log = OperationLog.from_dict(data)
            if user_id in log.target_users:
                result.append(log)
        return result
    
    def find_by_operation(self, operation_type: str) -> List[OperationLog]:
        """查询特定类型的操作日志
        
        Args:
            operation_type: 操作类型
            
        Returns:
            操作日志列表
        """
        all_logs = self.storage.find_all(self.ENTITY_TYPE)
        result = []
        for data in all_logs:
            log = OperationLog.from_dict(data)
            if log.operation_type == operation_type:
                result.append(log)
        return result
    
    def find_by_time_range(self, start: int, end: int) -> List[OperationLog]:
        """查询时间范围内的日志
        
        Args:
            start: 开始时间戳
            end: 结束时间戳
            
        Returns:
            操作日志列表
        """
        all_logs = self.storage.find_all(self.ENTITY_TYPE)
        result = []
        for data in all_logs:
            log = OperationLog.from_dict(data)
            if start <= log.timestamp <= end:
                result.append(log)
        return result
    
    def find_by_operator(self, operator: str) -> List[OperationLog]:
        """查询操作人的日志
        
        Args:
            operator: 操作人
            
        Returns:
            操作日志列表
        """
        all_logs = self.storage.find_all(self.ENTITY_TYPE)
        result = []
        for data in all_logs:
            log = OperationLog.from_dict(data)
            if log.operator == operator:
                result.append(log)
        return result
    
    def find_all(self, limit: Optional[int] = None) -> List[OperationLog]:
        """查询所有日志
        
        Args:
            limit: 限制数量
            
        Returns:
            操作日志列表
        """
        all_logs = self.storage.find_all(self.ENTITY_TYPE)
        logs = [OperationLog.from_dict(data) for data in all_logs]
        logs.sort(key=lambda x: x.timestamp, reverse=True)
        if limit:
            return logs[:limit]
        return logs
