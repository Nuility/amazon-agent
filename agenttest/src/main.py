"""Application entry point and dependency wiring."""
import os
import sys
from typing import Optional

src_dir = os.path.dirname(os.path.abspath(__file__))
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from common.types import SystemConfig
from common.validator import Validator
from infrastructure.config_validator import ConfigValidator
from infrastructure.file_storage_adapter import FileStorageAdapter
from infrastructure.llm_client import create_llm_client
from infrastructure.logger import Logger, init_logger
from interface.cli import CLI
from repositories.ad_report_repository import AdReportRepository
from repositories.ad_workflow_repository import AdWorkflowRepository
from repositories.config_repository import ConfigRepository
from repositories.keyword_rank_repository import KeywordRankRepository
from repositories.log_repository import LogRepository
from repositories.user_repository import UserRepository
from services.ad_agent_service import AdAgentService
from services.analysis_service import AnalysisService
from services.batch_service import BatchService
from services.amazon_ads_service import AmazonAdsService
from services.config_service import ConfigService
from services.prompt_engineering_service import PromptEngineeringService
from services.rule_engine import RuleEngine
from services.user_service import UserService


class Application:
    """Top-level application object."""

    def __init__(self):
        self.logger: Optional[Logger] = None
        self.config: Optional[SystemConfig] = None
        self.storage = None
        self.user_repo: Optional[UserRepository] = None
        self.log_repo: Optional[LogRepository] = None
        self.config_repo: Optional[ConfigRepository] = None
        self.ad_report_repo: Optional[AdReportRepository] = None
        self.keyword_rank_repo: Optional[KeywordRankRepository] = None
        self.ad_workflow_repo: Optional[AdWorkflowRepository] = None
        self.user_service: Optional[UserService] = None
        self.batch_service: Optional[BatchService] = None
        self.analysis_service: Optional[AnalysisService] = None
        self.ad_agent_service: Optional[AdAgentService] = None
        self.prompt_engineering_service: Optional[PromptEngineeringService] = None
        self.config_service: Optional[ConfigService] = None
        self.amazon_ads_service: Optional[AmazonAdsService] = None
        self.cli: Optional[CLI] = None

    def initialize(self, config_path: str = "./config/config.yaml") -> bool:
        """Initialize configuration, storage, repositories, and services."""
        try:
            config_repo = ConfigRepository()
            config_validator = ConfigValidator()
            project_root = os.path.dirname(os.path.dirname(__file__))

            default_config_path = os.path.join(
                project_root,
                "config",
                "config.yaml",
            )
            actual_config_path = config_path if os.path.exists(config_path) else default_config_path

            if os.path.exists(actual_config_path):
                config = config_repo.load(actual_config_path)
            else:
                config = SystemConfig()
                self._create_default_config(actual_config_path, config)

            config.data_file_path = self._resolve_project_path(project_root, config.data_file_path)
            config.log_file_path = self._resolve_project_path(project_root, config.log_file_path)
            config.sqlite_db_path = self._resolve_project_path(project_root, config.sqlite_db_path)

            self.config = config
            self.logger = init_logger(
                name="agenttest",
                log_level=config.log_level,
                log_file_path=config.log_file_path,
                log_max_size=config.log_max_size,
                log_backup_count=config.log_backup_count,
            )
            self.logger.info("Initializing application services")

            self.storage = FileStorageAdapter(config.data_file_path)
            self.storage.connect()

            self.user_repo = UserRepository(self.storage)
            self.log_repo = LogRepository(self.storage)
            self.config_repo = config_repo
            self.ad_report_repo = AdReportRepository(self.storage)
            self.keyword_rank_repo = KeywordRankRepository(self.storage)
            self.ad_workflow_repo = AdWorkflowRepository(self.storage)

            llm_client = create_llm_client(config.llm_api_config)
            rule_engine = RuleEngine()
            validator = Validator()

            self.config_service = ConfigService(
                config_repository=config_repo,
                config_validator=config_validator,
                logger=self.logger,
            )
            self.config_service._config = config
            self.config_service._config_path = actual_config_path

            self.prompt_engineering_service = PromptEngineeringService(
                config_dir=os.path.join(project_root, "config"),
                logger=self.logger,
            )

            self.user_service = UserService(
                user_repository=self.user_repo,
                log_repository=self.log_repo,
                rule_engine=rule_engine,
                logger=self.logger,
                validator=validator,
            )

            self.batch_service = BatchService(
                user_repository=self.user_repo,
                log_repository=self.log_repo,
                config_service=self.config_service,
                rule_engine=rule_engine,
                validator=validator,
                logger=self.logger,
            )

            self.analysis_service = AnalysisService(
                user_repository=self.user_repo,
                llm_client=llm_client,
                config_service=self.config_service,
                logger=self.logger,
            )

            self.ad_agent_service = AdAgentService(
                ad_report_repository=self.ad_report_repo,
                keyword_rank_repository=self.keyword_rank_repo,
                workflow_repository=self.ad_workflow_repo,
                prompt_engineering_service=self.prompt_engineering_service,
                llm_client=llm_client,
                logger=self.logger,
            )

            self.amazon_ads_service = AmazonAdsService(
                config=config,
                ad_report_repository=self.ad_report_repo,
                logger=self.logger,
            )

            self.cli = CLI(
                user_service=self.user_service,
                batch_service=self.batch_service,
                analysis_service=self.analysis_service,
                config_service=self.config_service,
                logger=self.logger,
            )

            self.logger.info("Application initialized successfully")
            return True
        except Exception as e:
            if self.logger:
                self.logger.error(f"Application initialization failed: {str(e)}")
            else:
                print(f"Application initialization failed: {str(e)}")
            return False

    def _create_default_config(self, config_path: str, config: SystemConfig):
        try:
            import yaml

            config_dir = os.path.dirname(config_path)
            if config_dir and not os.path.exists(config_dir):
                os.makedirs(config_dir, exist_ok=True)

            with open(config_path, "w", encoding="utf-8") as f:
                yaml.dump(config.to_dict(), f, allow_unicode=True, default_flow_style=False)
        except Exception as e:
            print(f"Failed to create default config: {str(e)}")

    def _resolve_project_path(self, project_root: str, path_value: str) -> str:
        if not path_value:
            return path_value
        if os.path.isabs(path_value):
            return path_value
        normalized = path_value[2:] if path_value.startswith("./") else path_value
        return os.path.normpath(os.path.join(project_root, normalized))

    def run(self, args: Optional[list] = None):
        if not self.cli:
            print("Application is not initialized")
            sys.exit(1)
        self.cli.run(args)

    def shutdown(self):
        if self.storage:
            self.storage.disconnect()
        if self.logger:
            self.logger.info("Application shutdown complete")


def main():
    app = Application()
    if not app.initialize():
        sys.exit(1)

    try:
        app.run()
    except KeyboardInterrupt:
        print("\nInterrupted by user")
    finally:
        app.shutdown()


if __name__ == "__main__":
    main()
