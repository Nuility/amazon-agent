"""智能分析服务"""
from typing import Dict, List, Any, Optional
from collections import Counter
from common.types import Statistics, Result, UserStatus
from repositories.user_repository import UserRepository
from infrastructure.llm_client import LLMClient, MockLLMClient
from infrastructure.logger import Logger
from services.config_service import ConfigService


class AnalysisService:
    """智能分析服务"""
    
    def __init__(
        self,
        user_repository: UserRepository,
        llm_client: LLMClient,
        config_service: ConfigService,
        logger: Logger
    ):
        """初始化智能分析服务
        
        Args:
            user_repository: 用户仓储
            llm_client: 大模型客户端
            config_service: 配置服务
            logger: 日志器
        """
        self.user_repo = user_repository
        self.llm_client = llm_client
        self.config_service = config_service
        self.logger = logger
    
    def get_statistics(self, filters: Optional[Dict[str, Any]] = None) -> Result[Statistics]:
        """获取用户统计数据
        
        Args:
            filters: 过滤条件
            
        Returns:
            统计结果
        """
        try:
            users = self.user_repo.find_all(filters)
            
            total_users = len(users)
            
            status_distribution = Counter([u.status.value for u in users])
            
            tag_distribution = Counter()
            for user in users:
                for tag in user.tags:
                    tag_distribution[tag] += 1
            
            attributes_distribution = {}
            for user in users:
                for key, value in user.attributes.items():
                    if key not in attributes_distribution:
                        attributes_distribution[key] = {}
                    if value not in attributes_distribution[key]:
                        attributes_distribution[key][value] = 0
                    attributes_distribution[key][value] += 1
            
            stats = Statistics(
                total_users=total_users,
                status_distribution=dict(status_distribution),
                tag_distribution=dict(tag_distribution),
                attributes_distribution=attributes_distribution
            )
            
            self.logger.info(f"统计完成: 总用户数 {total_users}")
            
            return Result.ok(stats)
            
        except Exception as e:
            self.logger.error(f"统计失败: {str(e)}")
            return Result.error(
                error_code=getattr(e, 'error_code', 1010),
                message=str(e)
            )
    
    def get_classification_suggestions(self, criteria: str, filters: Optional[Dict[str, Any]] = None) -> Result[str]:
        """获取用户分类建议
        
        Args:
            criteria: 分类标准描述
            filters: 过滤条件
            
        Returns:
            分类建议
        """
        try:
            config = self.config_service.get_config()
            
            if not config.enable_llm_integration or not self.llm_client.is_available():
                self.logger.warning("大模型API不可用，使用本地分析")
                return self._local_classification(criteria, filters)
            
            users = self.user_repo.find_all(filters)
            users_data = [u.to_dict() for u in users[:100]]
            
            try:
                result = self.llm_client.analyze_users(users_data, f"根据以下标准进行用户分类: {criteria}")
                self.logger.info("大模型分类建议生成成功")
                return Result.ok(result)
                
            except Exception as e:
                self.logger.warning(f"大模型调用失败，降级为本地分析: {str(e)}")
                return self._local_classification(criteria, filters)
            
        except Exception as e:
            self.logger.error(f"分类建议生成失败: {str(e)}")
            return Result.error(
                error_code=getattr(e, 'error_code', 1010),
                message=str(e)
            )
    
    def _local_classification(self, criteria: str, filters: Optional[Dict[str, Any]] = None) -> Result[str]:
        """本地分类分析（降级策略）
        
        Args:
            criteria: 分类标准
            filters: 过滤条件
            
        Returns:
            分类结果
        """
        try:
            users = self.user_repo.find_all(filters)
            
            status_groups = {}
            for user in users:
                status = user.status.value
                if status not in status_groups:
                    status_groups[status] = []
                status_groups[status].append(user.username)
            
            result_lines = [f"基于状态的用户分类（共 {len(users)} 个用户）:"]
            for status, usernames in status_groups.items():
                result_lines.append(f"\n{status} 状态用户 ({len(usernames)} 个):")
                result_lines.extend([f"  - {name}" for name in usernames[:10]])
                if len(usernames) > 10:
                    result_lines.append(f"  ... 还有 {len(usernames) - 10} 个")
            
            result = "\n".join(result_lines)
            return Result.ok(result)
            
        except Exception as e:
            return Result.error(
                error_code=getattr(e, 'error_code', 1010),
                message=str(e)
            )
    
    def detect_anomalies(self) -> Result[Dict[str, Any]]:
        """检测异常数据
        
        Returns:
            异常检测结果
        """
        try:
            users = self.user_repo.find_all()
            
            anomalies = {
                "duplicate_emails": [],
                "duplicate_usernames": [],
                "incomplete_data": [],
                "invalid_status": []
            }
            
            email_count = Counter([u.email for u in users])
            anomalies["duplicate_emails"] = [
                {"email": email, "count": count}
                for email, count in email_count.items()
                if count > 1
            ]
            
            username_count = Counter([u.username for u in users])
            anomalies["duplicate_usernames"] = [
                {"username": username, "count": count}
                for username, count in username_count.items()
                if count > 1
            ]
            
            for user in users:
                incomplete = []
                if not user.email:
                    incomplete.append("email")
                if not user.username:
                    incomplete.append("username")
                
                if incomplete:
                    anomalies["incomplete_data"].append({
                        "user_id": user.user_id,
                        "missing_fields": incomplete
                    })
            
            total_anomalies = (
                len(anomalies["duplicate_emails"]) +
                len(anomalies["duplicate_usernames"]) +
                len(anomalies["incomplete_data"]) +
                len(anomalies["invalid_status"])
            )
            
            self.logger.info(f"异常检测完成: 发现 {total_anomalies} 个异常")
            
            return Result.ok({
                "anomalies": anomalies,
                "total_anomalies": total_anomalies
            })
            
        except Exception as e:
            self.logger.error(f"异常检测失败: {str(e)}")
            return Result.error(
                error_code=getattr(e, 'error_code', 1010),
                message=str(e)
            )
    
    def get_operation_suggestions(self, operation_context: Dict[str, Any]) -> Result[List[str]]:
        """获取操作优化建议
        
        Args:
            operation_context: 操作上下文
            
        Returns:
            优化建议列表
        """
        try:
            suggestions = []
            
            stats_result = self.get_statistics()
            if not stats_result.success:
                return Result.error(
                    error_code=stats_result.error_code,
                    message=stats_result.error_message
                )
            
            stats = stats_result.data
            
            if stats.total_users > 1000:
                suggestions.append("建议使用批量操作代替单个操作以提高性能")
            
            inactive_rate = stats.status_distribution.get(UserStatus.INACTIVE.value, 0) / stats.total_users if stats.total_users > 0 else 0
            if inactive_rate > 0.3:
                suggestions.append(f"检测到 {inactive_rate*100:.1f}% 的用户处于非活跃状态，建议清理或重新激活")
            
            deleted_count = stats.status_distribution.get(UserStatus.DELETED.value, 0)
            if deleted_count > 100:
                suggestions.append(f"有 {deleted_count} 个已删除用户，建议定期清理物理删除")
            
            if not suggestions:
                suggestions.append("当前系统运行良好，暂无优化建议")
            
            self.logger.info(f"生成 {len(suggestions)} 条优化建议")
            
            return Result.ok(suggestions)
            
        except Exception as e:
            self.logger.error(f"生成优化建议失败: {str(e)}")
            return Result.error(
                error_code=getattr(e, 'error_code', 1010),
                message=str(e)
            )
