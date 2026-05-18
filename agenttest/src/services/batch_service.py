"""Batch operations for users."""
import csv
import json
from typing import Any, Dict, List

from common.types import BatchResult, Result, User, UserStatus
from common.utils import generate_uuid, timestamp_now
from common.validator import Validator
from infrastructure.logger import Logger
from repositories.log_repository import LogRepository
from repositories.user_repository import UserRepository
from services.config_service import ConfigService
from services.rule_engine import RuleEngine


class BatchService:
    def __init__(
        self,
        user_repository: UserRepository,
        log_repository: LogRepository,
        config_service: ConfigService,
        rule_engine: RuleEngine,
        validator: Validator,
        logger: Logger,
    ):
        self.user_repo = user_repository
        self.log_repo = log_repository
        self.config_service = config_service
        self.rule_engine = rule_engine
        self.validator = validator
        self.logger = logger

    def batch_create(self, users_data: List[Dict[str, Any]], atomic: bool = True, operator: str = "system") -> Result[BatchResult]:
        try:
            config = self.config_service.get_config()
            self.rule_engine.check_batch_limit(len(users_data), config.max_batch_size)

            success_count = 0
            failure_count = 0
            failures: List[Dict[str, Any]] = []

            for idx, user_data in enumerate(users_data):
                try:
                    self.validator.validate_user_data(user_data)
                    user_id = user_data.get("user_id") or generate_uuid()
                    if self.user_repo.exists(user_id):
                        raise ValueError(f"User already exists: {user_id}")

                    now = timestamp_now()
                    self.user_repo.save(
                        User(
                            user_id=user_id,
                            username=user_data["username"],
                            email=user_data["email"],
                            phone=user_data.get("phone"),
                            status=UserStatus(user_data.get("status", UserStatus.ACTIVE.value)),
                            attributes=user_data.get("attributes", {}),
                            tags=user_data.get("tags", []),
                            created_at=now,
                            updated_at=now,
                            created_by=operator,
                        )
                    )
                    success_count += 1
                except Exception as e:
                    failure_count += 1
                    failures.append({"index": idx, "data": user_data, "error": str(e)})
                    if atomic:
                        raise

            return Result.ok(
                BatchResult(
                    total=len(users_data),
                    success_count=success_count,
                    failure_count=failure_count,
                    failures=failures,
                )
            )
        except Exception as e:
            self.logger.error(f"Batch create failed: {str(e)}")
            return Result.error(getattr(e, "error_code", 1010), str(e))

    def batch_update(self, updates: List[Dict[str, Any]], atomic: bool = True, operator: str = "system") -> Result[BatchResult]:
        try:
            config = self.config_service.get_config()
            self.rule_engine.check_batch_limit(len(updates), config.max_batch_size)

            success_count = 0
            failure_count = 0
            failures: List[Dict[str, Any]] = []

            for idx, update_item in enumerate(updates):
                try:
                    user_id = update_item.get("user_id")
                    payload = update_item.get("data", {})
                    if not user_id:
                        raise ValueError("user_id is required")
                    if not self.user_repo.find_by_id(user_id):
                        raise ValueError(f"User does not exist: {user_id}")
                    payload["updated_at"] = timestamp_now()
                    self.user_repo.update(user_id, payload)
                    success_count += 1
                except Exception as e:
                    failure_count += 1
                    failures.append({"index": idx, "user_id": update_item.get("user_id"), "error": str(e)})
                    if atomic:
                        raise

            return Result.ok(
                BatchResult(
                    total=len(updates),
                    success_count=success_count,
                    failure_count=failure_count,
                    failures=failures,
                )
            )
        except Exception as e:
            self.logger.error(f"Batch update failed: {str(e)}")
            return Result.error(getattr(e, "error_code", 1010), str(e))

    def batch_delete(
        self,
        user_ids: List[str],
        logical: bool = True,
        atomic: bool = True,
        operator: str = "system",
    ) -> Result[BatchResult]:
        try:
            config = self.config_service.get_config()
            self.rule_engine.check_batch_limit(len(user_ids), config.max_batch_size)

            success_count = 0
            failure_count = 0
            failures: List[Dict[str, Any]] = []

            for idx, user_id in enumerate(user_ids):
                try:
                    if not self.user_repo.find_by_id(user_id):
                        raise ValueError(f"User does not exist: {user_id}")
                    if logical:
                        self.user_repo.update(user_id, {"status": UserStatus.DELETED.value, "updated_at": timestamp_now()})
                    else:
                        self.user_repo.delete(user_id)
                    success_count += 1
                except Exception as e:
                    failure_count += 1
                    failures.append({"index": idx, "user_id": user_id, "error": str(e)})
                    if atomic:
                        raise

            return Result.ok(
                BatchResult(
                    total=len(user_ids),
                    success_count=success_count,
                    failure_count=failure_count,
                    failures=failures,
                )
            )
        except Exception as e:
            self.logger.error(f"Batch delete failed: {str(e)}")
            return Result.error(getattr(e, "error_code", 1010), str(e))

    def import_from_file(self, file_path: str, file_format: str = "json", operator: str = "system") -> Result[BatchResult]:
        try:
            if file_format == "json":
                with open(file_path, "r", encoding="utf-8") as f:
                    users_data = json.load(f)
            elif file_format == "csv":
                with open(file_path, "r", encoding="utf-8") as f:
                    users_data = list(csv.DictReader(f))
            else:
                raise ValueError(f"Unsupported file format: {file_format}")

            if not isinstance(users_data, list):
                users_data = [users_data]

            self.logger.info(f"Imported {len(users_data)} rows from {file_path}")
            return self.batch_create(users_data, atomic=False, operator=operator)
        except Exception as e:
            self.logger.error(f"Import from file failed: {str(e)}")
            return Result.error(getattr(e, "error_code", 1010), str(e))
