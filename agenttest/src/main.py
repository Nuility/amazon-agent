"""主程序入口"""
import os
import sys
from typing import Optional

src_dir = os.path.dirname(os.path.abspath(__file__))
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from common.types import SystemConfig
from common.validator import Validator
from infrastructure.logger import Logger, init_logger
from infrastructure.file_storage_adapter import FileStorageAdapter
from infrastructure.config_validator import ConfigValidator
from infrastructure.llm_client import create_llm_client
from repositories.user_repository import UserRepository
from repositories.log_repository import LogRepository
from repositories.config_repository import ConfigRepository
from services.rule_engine import RuleEngine
from services.user_service import UserService
from services.batch_service import BatchService
from services.analysis_service import AnalysisService
from services.config_service import ConfigService
from interface.cli import CLI


class Application:
    """应用程序主类"""
    
    def __init__(self):
        """初始化应用程序"""
        self.logger: Optional[Logger] = None
        self.config: Optional[SystemConfig] = None
        self.storage = None
        self.user_repo: Optional[UserRepository] = None
        self.log_repo: Optional[LogRepository] = None
        self.config_repo: Optional[ConfigRepository] = None
        self.user_service: Optional[UserService] = None
        self.batch_service: Optional[BatchService] = None
        self.analysis_service: Optional[AnalysisService] = None
        self.config_service: Optional[ConfigService] = None
        self.cli: Optional[CLI] = None
    
    def initialize(self, config_path: str = "./config/config.yaml") -> bool:
        """初始化系统
        
        Args:
            config_path: 配置文件路径
            
        Returns:
            初始化是否成功
        """
        try:
            config_repo = ConfigRepository()
            config_validator = ConfigValidator()
            
            default_config_path = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                "config",
                "config.yaml"
            )
            
            actual_config_path = config_path if os.path.exists(config_path) else default_config_path
            
            if os.path.exists(actual_config_path):
                config = config_repo.load(actual_config_path)
            else:
                config = SystemConfig()
                self._create_default_config(actual_config_path, config)
            
            self.config = config
            
            self.logger = init_logger(
                name="agenttest",
                log_level=config.log_level,
                log_file_path=config.log_file_path,
                log_max_size=config.log_max_size,
                log_backup_count=config.log_backup_count
            )
            
            self.logger.info("初始化用户管理智能体系统...")
            
            self.storage = FileStorageAdapter(config.data_file_path)
            self.storage.connect()
            
            self.user_repo = UserRepository(self.storage)
            self.log_repo = LogRepository(self.storage)
            self.config_repo = config_repo
            
            llm_client = create_llm_client(config.llm_api_config)
            
            rule_engine = RuleEngine()
            validator = Validator()
            
            self.config_service = ConfigService(
                config_repository=config_repo,
                config_validator=config_validator,
                logger=self.logger
            )
            self.config_service._config = config
            self.config_service._config_path = actual_config_path
            
            self.user_service = UserService(
                user_repository=self.user_repo,
                log_repository=self.log_repo,
                rule_engine=rule_engine,
                logger=self.logger,
                validator=validator
            )
            
            self.batch_service = BatchService(
                user_repository=self.user_repo,
                log_repository=self.log_repo,
                config_service=self.config_service,
                rule_engine=rule_engine,
                validator=validator,
                logger=self.logger
            )
            
            self.analysis_service = AnalysisService(
                user_repository=self.user_repo,
                llm_client=llm_client,
                config_service=self.config_service,
                logger=self.logger
            )
            
            self.cli = CLI(
                user_service=self.user_service,
                batch_service=self.batch_service,
                analysis_service=self.analysis_service,
                config_service=self.config_service,
                logger=self.logger
            )
            
            self.logger.info("系统初始化完成")
            
            return True
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"系统初始化失败: {str(e)}")
            else:
                print(f"系统初始化失败: {str(e)}")
            return False
    
    def _create_default_config(self, config_path: str, config: SystemConfig):
        """创建默认配置文件
        
        Args:
            config_path: 配置文件路径
            config: 系统配置
        """
        try:
            import yaml
            config_dir = os.path.dirname(config_path)
            if config_dir and not os.path.exists(config_dir):
                os.makedirs(config_dir, exist_ok=True)
            
            with open(config_path, 'w', encoding='utf-8') as f:
                yaml.dump(config.to_dict(), f, allow_unicode=True, default_flow_style=False)
            
            print(f"已创建默认配置文件: {config_path}")
            
        except Exception as e:
            print(f"创建默认配置文件失败: {str(e)}")
    
    def run(self, args: Optional[list] = None):
        """运行应用
        
        Args:
            args: 命令行参数
        """
        if not self.cli:
            print("系统未初始化")
            sys.exit(1)
        
        self.cli.run(args)
    
    def shutdown(self):
        """关闭应用"""
        if self.storage:
            self.storage.disconnect()
        
        if self.logger:
            self.logger.info("系统已关闭")


def main():
    """主函数"""
    app = Application()
    
    if not app.initialize():
        sys.exit(1)
    
    try:
        app.run()
    except KeyboardInterrupt:
        print("\n用户中断")
    finally:
        app.shutdown()


if __name__ == "__main__":
    main()
