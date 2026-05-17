"""用户管理服务"""
from typing import Dict, List, Optional, Any
from common.types import User, Result, UserStatus, OperationLog, OperationType
from common.exceptions import UserNotFoundException, UserAlreadyExistsException
from common.utils import generate_uuid, timestamp_now
from common.validator import Validator
from repositories.user_repository import UserRepository
from repositories.log_repository import LogRepository
from infrastructure.logger import Logger
from services.rule_engine import RuleEngine


class UserService:
    """用户管理服务"""
    
    def __init__(
        self,
        user_repository: UserRepository,
        log_repository: LogRepository,
        rule_engine: RuleEngine,
        logger: Logger,
        validator: Validator
    ):
        """初始化用户管理服务
        
        Args:
            user_repository: 用户仓储
            log_repository: 日志仓储
            rule_engine: 规则引擎
            logger: 日志器
            validator: 校验器
        """
        self.user_repo = user_repository
        self.log_repo = log_repository
        self.rule_engine = rule_engine
        self.logger = logger
        self.validator = validator
    
    def create_user(self, user_data: Dict[str, Any], operator: str = "system") -> Result[User]:
        """创建用户
        
        Args:
            user_data: 用户数据
            operator: 操作人
            
        Returns:
            创建结果
        """
        start_time = timestamp_now()
        
        try:
            self.rule_engine.validate_user_creation(user_data)
            self.validator.validate_user_data(user_data)
            
            user_id = user_data.get("user_id") or generate_uuid()
            
            if self.user_repo.exists(user_id):
                raise UserAlreadyExistsException(user_id)
            
            now = timestamp_now()
            user = User(
                user_id=user_id,
                username=user_data["username"],
                email=user_data["email"],
                phone=user_data.get("phone"),
                status=UserStatus(user_data.get("status", UserStatus.ACTIVE.value)),
                attributes=user_data.get("attributes", {}),
                tags=user_data.get("tags", []),
                created_at=now,
                updated_at=now,
                created_by=operator
            )
            
            self.user_repo.save(user)
            
            self._log_operation(
                operation_type=OperationType.CREATE.value,
                operator=operator,
                target_users=[user_id],
                params=user_data,
                result="success",
                execution_time=timestamp_now() - start_time
            )
            
            self.logger.info(f"用户创建成功: {user_id}", operator=operator)
            
            return Result.ok(user)
            
        except Exception as e:
            self._log_operation(
                operation_type=OperationType.CREATE.value,
                operator=operator,
                target_users=[],
                params=user_data,
                result="failed",
                error_message=str(e),
                execution_time=timestamp_now() - start_time
            )
            
            self.logger.error(f"用户创建失败: {str(e)}", operator=operator)
            
            if isinstance(e, (UserAlreadyExistsException, ValueError)):
                raise
            return Result.error(
                error_code=getattr(e, 'error_code', 1010),
                message=str(e)
            )
    
    def get_user(self, user_id: str) -> Result[User]:
        """查询用户详情
        
        Args:
            user_id: 用户ID
            
        Returns:
            查询结果
        """
        try:
            user = self.user_repo.find_by_id(user_id)
            if not user:
                raise UserNotFoundException(user_id)
            
            return Result.ok(user)
            
        except UserNotFoundException:
            raise
        except Exception as e:
            self.logger.error(f"查询用户失败: {str(e)}", user_id=user_id)
            return Result.error(
                error_code=getattr(e, 'error_code', 1010),
                message=str(e)
            )
    
    def update_user(self, user_id: str, update_data: Dict[str, Any], operator: str = "system") -> Result[User]:
        """更新用户信息
        
        Args:
            user_id: 用户ID
            update_data: 更新数据
            operator: 操作人
            
        Returns:
            更新结果
        """
        start_time = timestamp_now()
        
        try:
            user = self.user_repo.find_by_id(user_id)
            if not user:
                raise UserNotFoundException(user_id)
            
            self.rule_engine.validate_user_update(user_id, update_data)
            
            if "status" in update_data:
                self.rule_engine.validate_status_transition(
                    user.status.value,
                    update_data["status"]
                )
            
            update_data["updated_at"] = timestamp_now()
            self.user_repo.update(user_id, update_data)
            
            updated_user = self.user_repo.find_by_id(user_id)
            
            self._log_operation(
                operation_type=OperationType.UPDATE.value,
                operator=operator,
                target_users=[user_id],
                params=update_data,
                result="success",
                execution_time=timestamp_now() - start_time
            )
            
            self.logger.info(f"用户更新成功: {user_id}", operator=operator)
            
            return Result.ok(updated_user)
            
        except Exception as e:
            self._log_operation(
                operation_type=OperationType.UPDATE.value,
                operator=operator,
                target_users=[user_id],
                params=update_data,
                result="failed",
                error_message=str(e),
                execution_time=timestamp_now() - start_time
            )
            
            self.logger.error(f"用户更新失败: {str(e)}", user_id=user_id, operator=operator)
            
            if isinstance(e, (UserNotFoundException, ValueError)):
                raise
            return Result.error(
                error_code=getattr(e, 'error_code', 1010),
                message=str(e)
            )
    
    def delete_user(self, user_id: str, logical: bool = True, operator: str = "system") -> Result[bool]:
        """删除用户
        
        Args:
            user_id: 用户ID
            logical: 是否逻辑删除
            operator: 操作人
            
        Returns:
            删除结果
        """
        start_time = timestamp_now()
        
        try:
            user = self.user_repo.find_by_id(user_id)
            if not user:
                raise UserNotFoundException(user_id)
            
            self.rule_engine.validate_user_deletion(user_id)
            
            if logical:
                self.user_repo.update(user_id, {
                    "status": UserStatus.DELETED.value,
                    "updated_at": timestamp_now()
                })
            else:
                self.user_repo.delete(user_id)
            
            self._log_operation(
                operation_type=OperationType.DELETE.value,
                operator=operator,
                target_users=[user_id],
                params={"logical": logical},
                result="success",
                execution_time=timestamp_now() - start_time
            )
            
            self.logger.info(f"用户删除成功: {user_id}", operator=operator, logical=logical)
            
            return Result.ok(True)
            
        except Exception as e:
            self._log_operation(
                operation_type=OperationType.DELETE.value,
                operator=operator,
                target_users=[user_id],
                params={"logical": logical},
                result="failed",
                error_message=str(e),
                execution_time=timestamp_now() - start_time
            )
            
            self.logger.error(f"用户删除失败: {str(e)}", user_id=user_id, operator=operator)
            
            if isinstance(e, UserNotFoundException):
                raise
            return Result.error(
                error_code=getattr(e, 'error_code', 1010),
                message=str(e)
            )
    
    def list_users(
        self,
        filters: Optional[Dict[str, Any]] = None,
        page: int = 1,
        page_size: int = 20
    ) -> Result[Dict[str, Any]]:
        """查询用户列表
        
        Args:
            filters: 过滤条件
            page: 页码
            page_size: 每页数量
            
        Returns:
            查询结果
        """
        try:
            all_users = self.user_repo.find_all(filters)
            
            total = len(all_users)
            start_idx = (page - 1) * page_size
            end_idx = start_idx + page_size
            users = all_users[start_idx:end_idx]
            
            return Result.ok({
                "users": [u.to_dict() for u in users],
                "total": total,
                "page": page,
                "page_size": page_size,
                "total_pages": (total + page_size - 1) // page_size if total > 0 else 0
            })
            
        except Exception as e:
            self.logger.error(f"查询用户列表失败: {str(e)}")
            return Result.error(
                error_code=getattr(e, 'error_code', 1010),
                message=str(e)
            )
    
    def _log_operation(
        self,
        operation_type: str,
        operator: str,
        target_users: List[str],
        params: Dict[str, Any],
        result: str,
        error_message: str = "",
        execution_time: int = 0
    ):
        """记录操作日志"""
        log = OperationLog(
            log_id=generate_uuid(),
            operation_type=operation_type,
            operator=operator,
            target_users=target_users,
            operation_params=params,
            result=result,
            error_message=error_message,
            execution_time=execution_time,
            timestamp=timestamp_now()
        )
        self.log_repo.save(log)
