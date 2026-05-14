"""批量操作服务"""
from typing import Dict, List, Any, Optional
from common.types import User, Result, BatchResult, UserStatus
from common.utils import generate_uuid, timestamp_now
from common.validator import Validator
from repositories.user_repository import UserRepository
from repositories.log_repository import LogRepository
from infrastructure.logger import Logger
from services.rule_engine import RuleEngine
from services.config_service import ConfigService


class BatchService:
    """批量操作服务"""
    
    def __init__(
        self,
        user_repository: UserRepository,
        log_repository: LogRepository,
        config_service: ConfigService,
        rule_engine: RuleEngine,
        validator: Validator,
        logger: Logger
    ):
        """初始化批量操作服务
        
        Args:
            user_repository: 用户仓储
            log_repository: 日志仓储
            config_service: 配置服务
            rule_engine: 规则引擎
            validator: 校验器
            logger: 日志器
        """
        self.user_repo = user_repository
        self.log_repo = log_repository
        self.config_service = config_service
        self.rule_engine = rule_engine
        self.validator = validator
        self.logger = logger
    
    def batch_create(self, users_data: List[Dict[str, Any]], atomic: bool = True, operator: str = "system") -> Result[BatchResult]:
        """批量创建用户
        
        Args:
            users_data: 用户数据列表
            atomic: 是否原子操作
            operator: 操作人
            
        Returns:
            批量操作结果
        """
        start_time = timestamp_now()
        config = self.config_service.get_config()
        
        try:
            self.rule_engine.check_batch_limit(len(users_data), config.max_batch_size)
            
            success_count = 0
            failure_count = 0
            failures = []
            created_users = []
            
            for idx, user_data in enumerate(users_data):
                try:
                    if idx % 100 == 0:
                        self.logger.info(f"批量创建进度: {idx}/{len(users_data)}")
                    
                    self.validator.validate_user_data(user_data)
                    
                    user_id = user_data.get("user_id") or generate_uuid()
                    
                    if self.user_repo.exists(user_id):
                        raise ValueError(f"用户已存在: {user_id}")
                    
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
                    created_users.append(user)
                    success_count += 1
                    
                except Exception as e:
                    failure_count += 1
                    failures.append({
                        "index": idx,
                        "data": user_data,
                        "error": str(e)
                    })
                    
                    if atomic:
                        self.logger.error(f"批量创建失败（原子模式）: {str(e)}")
                        raise
            
            self.logger.info(
                f"批量创建完成: 成功 {success_count}, 失败 {failure_count}",
                operator=operator
            )
            
            result = BatchResult(
                total=len(users_data),
                success_count=success_count,
                failure_count=failure_count,
                failures=failures
            )
            
            return Result.ok(result)
            
        except Exception as e:
            self.logger.error(f"批量创建失败: {str(e)}", operator=operator)
            return Result.error(
                error_code=getattr(e, 'error_code', 1010),
                message=str(e)
            )
    
    def batch_update(self, updates: List[Dict[str, Any]], atomic: bool = True, operator: str = "system") -> Result[BatchResult]:
        """批量更新用户
        
        Args:
            updates: 更新数据列表 [{"user_id": "xxx", "data": {...}}, ...]
            atomic: 是否原子操作
            operator: 操作人
            
        Returns:
            批量操作结果
        """
        start_time = timestamp_now()
        config = self.config_service.get_config()
        
        try:
            self.rule_engine.check_batch_limit(len(updates), config.max_batch_size)
            
            success_count = 0
            failure_count = 0
            failures = []
            
            for idx, update_item in enumerate(updates):
                try:
                    if idx % 100 == 0:
                        self.logger.info(f"批量更新进度: {idx}/{len(updates)}")
                    
                    user_id = update_item.get("user_id")
                    update_data = update_item.get("data", {})
                    
                    if not user_id:
                        raise ValueError("缺少user_id")
                    
                    user = self.user_repo.find_by_id(user_id)
                    if not user:
                        raise ValueError(f"用户不存在: {user_id}")
                    
                    update_data["updated_at"] = timestamp_now()
                    self.user_repo.update(user_id, update_data)
                    success_count += 1
                    
                except Exception as e:
                    failure_count += 1
                    failures.append({
                        "index": idx,
                        "user_id": update_item.get("user_id"),
                        "error": str(e)
                    })
                    
                    if atomic:
                        raise
            
            self.logger.info(
                f"批量更新完成: 成功 {success_count}, 失败 {failure_count}",
                operator=operator
            )
            
            result = BatchResult(
                total=len(updates),
                success_count=success_count,
                failure_count=failure_count,
                failures=failures
            )
            
            return Result.ok(result)
            
        except Exception as e:
            self.logger.error(f"批量更新失败: {str(e)}", operator=operator)
            return Result.error(
                error_code=getattr(e, 'error_code', 1010),
                message=str(e)
            )
    
    def batch_delete(self, user_ids: List[str], logical: bool = True, atomic: bool = True, operator: str = "system") -> Result[BatchResult]:
        """批量删除用户
        
        Args:
            user_ids: 用户ID列表
            logical: 是否逻辑删除
            atomic: 是否原子操作
            operator: 操作人
            
        Returns:
            批量操作结果
        """
        start_time = timestamp_now()
        config = self.config_service.get_config()
        
        try:
            self.rule_engine.check_batch_limit(len(user_ids), config.max_batch_size)
            
            success_count = 0
            failure_count = 0
            failures = []
            
            for idx, user_id in enumerate(user_ids):
                try:
                    if idx % 100 == 0:
                        self.logger.info(f"批量删除进度: {idx}/{len(user_ids)}")
                    
                    user = self.user_repo.find_by_id(user_id)
                    if not user:
                        raise ValueError(f"用户不存在: {user_id}")
                    
                    if logical:
                        self.user_repo.update(user_id, {
                            "status": UserStatus.DELETED.value,
                            "updated_at": timestamp_now()
                        })
                    else:
                        self.user_repo.delete(user_id)
                    
                    success_count += 1
                    
                except Exception as e:
                    failure_count += 1
                    failures.append({
                        "index": idx,
                        "user_id": user_id,
                        "error": str(e)
                    })
                    
                    if atomic:
                        raise
            
            self.logger.info(
                f"批量删除完成: 成功 {success_count}, 失败 {failure_count}",
                operator=operator,
                logical=logical
            )
            
            result = BatchResult(
                total=len(user_ids),
                success_count=success_count,
                failure_count=failure_count,
                failures=failures
            )
            
            return Result.ok(result)
            
        except Exception as e:
            self.logger.error(f"批量删除失败: {str(e)}", operator=operator)
            return Result.error(
                error_code=getattr(e, 'error_code', 1010),
                message=str(e)
            )
    
    def import_from_file(self, file_path: str, file_format: str = "json", operator: str = "system") -> Result[BatchResult]:
        """从文件批量导入用户
        
        Args:
            file_path: 文件路径
            file_format: 文件格式 (json/csv)
            operator: 操作人
            
        Returns:
            批量操作结果
        """
        import json
        import csv
        
        try:
            users_data = []
            
            if file_format == "json":
                with open(file_path, 'r', encoding='utf-8') as f:
                    users_data = json.load(f)
                    
            elif file_format == "csv":
                with open(file_path, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    users_data = list(reader)
            else:
                raise ValueError(f"不支持的文件格式: {file_format}")
            
            if not isinstance(users_data, list):
                users_data = [users_data]
            
            self.logger.info(f"从文件导入 {len(users_data)} 条用户数据", file_path=file_path)
            
            return self.batch_create(users_data, atomic=False, operator=operator)
            
        except Exception as e:
            self.logger.error(f"导入文件失败: {str(e)}", file_path=file_path)
            return Result.error(
                error_code=getattr(e, 'error_code', 1010),
                message=str(e)
            )
