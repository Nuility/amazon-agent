"""User analytics service."""
from collections import Counter
from typing import Any, Dict, List, Optional

from common.types import Result, Statistics, UserStatus
from infrastructure.llm_client import LLMClient
from infrastructure.logger import Logger
from repositories.user_repository import UserRepository
from services.config_service import ConfigService


class AnalysisService:
    def __init__(
        self,
        user_repository: UserRepository,
        llm_client: LLMClient,
        config_service: ConfigService,
        logger: Logger,
    ):
        self.user_repo = user_repository
        self.llm_client = llm_client
        self.config_service = config_service
        self.logger = logger

    def get_statistics(self, filters: Optional[Dict[str, Any]] = None) -> Result[Statistics]:
        try:
            users = self.user_repo.find_all(filters)
            status_distribution = Counter([u.status.value for u in users])
            tag_distribution = Counter()
            attributes_distribution: Dict[str, Dict[str, int]] = {}

            for user in users:
                for tag in user.tags:
                    tag_distribution[tag] += 1
                for key, value in user.attributes.items():
                    attributes_distribution.setdefault(key, {})
                    attributes_distribution[key][value] = attributes_distribution[key].get(value, 0) + 1

            stats = Statistics(
                total_users=len(users),
                status_distribution=dict(status_distribution),
                tag_distribution=dict(tag_distribution),
                attributes_distribution=attributes_distribution,
            )
            self.logger.info(f"Statistics ready for {len(users)} users")
            return Result.ok(stats)
        except Exception as e:
            self.logger.error(f"Failed to compute statistics: {str(e)}")
            return Result.error(getattr(e, "error_code", 1010), str(e))

    def get_classification_suggestions(self, criteria: str, filters: Optional[Dict[str, Any]] = None) -> Result[str]:
        try:
            config = self.config_service.get_config()
            if config.enable_llm_integration and self.llm_client.is_available():
                users = self.user_repo.find_all(filters)
                payload = [u.to_dict() for u in users[:100]]
                try:
                    response = self.llm_client.analyze_users(payload, f"Classify users by: {criteria}")
                    return Result.ok(response)
                except Exception as e:
                    self.logger.warning(f"LLM classification failed, using fallback: {str(e)}")
            return self._local_classification(criteria, filters)
        except Exception as e:
            return Result.error(getattr(e, "error_code", 1010), str(e))

    def _local_classification(self, criteria: str, filters: Optional[Dict[str, Any]] = None) -> Result[str]:
        try:
            users = self.user_repo.find_all(filters)
            groups: Dict[str, List[str]] = {}
            for user in users:
                groups.setdefault(user.status.value, []).append(user.username)

            lines = [f"Local classification for criteria: {criteria}", f"Total users: {len(users)}"]
            for status, usernames in groups.items():
                lines.append(f"{status}: {', '.join(usernames[:10])}")
            return Result.ok("\n".join(lines))
        except Exception as e:
            return Result.error(getattr(e, "error_code", 1010), str(e))

    def detect_anomalies(self) -> Result[Dict[str, Any]]:
        try:
            users = self.user_repo.find_all()
            email_count = Counter([u.email for u in users])
            username_count = Counter([u.username for u in users])

            anomalies = {
                "duplicate_emails": [{"email": email, "count": count} for email, count in email_count.items() if count > 1],
                "duplicate_usernames": [{"username": name, "count": count} for name, count in username_count.items() if count > 1],
                "incomplete_data": [],
                "invalid_status": [],
            }

            for user in users:
                missing = []
                if not user.email:
                    missing.append("email")
                if not user.username:
                    missing.append("username")
                if missing:
                    anomalies["incomplete_data"].append({"user_id": user.user_id, "missing_fields": missing})
                if user.status.value not in {item.value for item in UserStatus}:
                    anomalies["invalid_status"].append({"user_id": user.user_id, "status": user.status.value})

            total_anomalies = sum(len(value) for value in anomalies.values())
            return Result.ok({"anomalies": anomalies, "total_anomalies": total_anomalies})
        except Exception as e:
            self.logger.error(f"Failed to detect anomalies: {str(e)}")
            return Result.error(getattr(e, "error_code", 1010), str(e))

    def get_operation_suggestions(self, operation_context: Dict[str, Any]) -> Result[List[str]]:
        try:
            suggestions: List[str] = []
            stats_result = self.get_statistics()
            if not stats_result.success or not stats_result.data:
                return Result.error(stats_result.error_code, stats_result.error_message)

            stats = stats_result.data
            if stats.total_users > 1000:
                suggestions.append("Use batch operations instead of one-by-one updates for large user sets.")

            inactive_rate = stats.status_distribution.get(UserStatus.INACTIVE.value, 0) / max(stats.total_users, 1)
            if inactive_rate > 0.3:
                suggestions.append("Inactive users exceed 30%; consider a cleanup or reactivation workflow.")

            deleted_count = stats.status_distribution.get(UserStatus.DELETED.value, 0)
            if deleted_count > 100:
                suggestions.append("A large number of deleted users exist; consider physical cleanup if policy allows.")

            if not suggestions:
                suggestions.append("The current dataset looks stable. No immediate operational changes are needed.")

            return Result.ok(suggestions)
        except Exception as e:
            self.logger.error(f"Failed to build operation suggestions: {str(e)}")
            return Result.error(getattr(e, "error_code", 1010), str(e))
