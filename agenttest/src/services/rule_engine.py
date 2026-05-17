"""Business rule validation helpers."""
from typing import Any, Dict

from common.exceptions import BatchLimitExceededException, InvalidStatusTransitionException, ValidationException
from common.types import UserStatus


class RuleEngine:
    def validate_user_creation(self, user_data: Dict[str, Any]) -> None:
        if "username" not in user_data or not str(user_data.get("username", "")).strip():
            raise ValidationException("Username is required", field="username")
        if "email" not in user_data or not str(user_data.get("email", "")).strip():
            raise ValidationException("Email is required", field="email")
        if len(str(user_data["username"])) > 128:
            raise ValidationException("Username must be 128 characters or fewer", field="username")

    def validate_user_update(self, user_id: str, update_data: Dict[str, Any]) -> None:
        if not user_id:
            raise ValidationException("User ID is required", field="user_id")
        if not update_data:
            raise ValidationException("Update data is required", field="update_data")
        if "username" in update_data and not str(update_data["username"]).strip():
            raise ValidationException("Username cannot be empty", field="username")
        if "status" in update_data and update_data["status"] not in [status.value for status in UserStatus]:
            raise ValidationException(f"Invalid user status: {update_data['status']}", field="status")

    def validate_user_deletion(self, user_id: str) -> None:
        if not user_id:
            raise ValidationException("User ID is required", field="user_id")

    def validate_status_transition(self, current_status: str, new_status: str) -> None:
        valid_transitions = {
            UserStatus.ACTIVE.value: [UserStatus.INACTIVE.value, UserStatus.DELETED.value],
            UserStatus.INACTIVE.value: [UserStatus.ACTIVE.value, UserStatus.DELETED.value],
            UserStatus.DELETED.value: [],
        }
        if current_status not in valid_transitions or new_status not in valid_transitions[current_status]:
            raise InvalidStatusTransitionException(current_status, new_status)

    def check_batch_limit(self, batch_size: int, max_limit: int) -> None:
        if batch_size <= 0:
            raise ValidationException("Batch size must be greater than 0", field="batch_size")
        if batch_size > max_limit:
            raise BatchLimitExceededException(batch_size, max_limit)

    def validate_batch_data(self, batch_data: list) -> None:
        if not batch_data:
            raise ValidationException("Batch data cannot be empty", field="batch_data")
        if not isinstance(batch_data, list):
            raise ValidationException("Batch data must be a list", field="batch_data")
