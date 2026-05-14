"""命令行接口"""
import argparse
import json
import sys
from typing import Optional
from services.user_service import UserService
from services.batch_service import BatchService
from services.analysis_service import AnalysisService
from services.config_service import ConfigService
from infrastructure.logger import Logger


class CLI:
    """命令行接口"""
    
    def __init__(
        self,
        user_service: UserService,
        batch_service: BatchService,
        analysis_service: AnalysisService,
        config_service: ConfigService,
        logger: Logger
    ):
        """初始化CLI
        
        Args:
            user_service: 用户管理服务
            batch_service: 批量操作服务
            analysis_service: 智能分析服务
            config_service: 配置管理服务
            logger: 日志器
        """
        self.user_service = user_service
        self.batch_service = batch_service
        self.analysis_service = analysis_service
        self.config_service = config_service
        self.logger = logger
    
    def run(self, args: Optional[list] = None):
        """运行CLI
        
        Args:
            args: 命令行参数
        """
        parser = self._create_parser()
        parsed_args = parser.parse_args(args)
        
        if not hasattr(parsed_args, 'command'):
            parser.print_help()
            return
        
        command_handler = getattr(self, f'_handle_{parsed_args.command}', None)
        if command_handler:
            try:
                command_handler(parsed_args)
            except Exception as e:
                self.logger.error(f"命令执行失败: {str(e)}")
                print(f"错误: {str(e)}")
                sys.exit(1)
        else:
            print(f"未知命令: {parsed_args.command}")
            sys.exit(1)
    
    def _create_parser(self) -> argparse.ArgumentParser:
        """创建命令行解析器"""
        parser = argparse.ArgumentParser(
            prog='agenttest',
            description='用户管理智能体系统'
        )
        
        subparsers = parser.add_subparsers(dest='command', help='可用命令')
        
        create_parser = subparsers.add_parser('create', help='创建用户')
        create_parser.add_argument('--username', required=True, help='用户名')
        create_parser.add_argument('--email', required=True, help='邮箱')
        create_parser.add_argument('--phone', help='手机号')
        create_parser.add_argument('--status', default='active', help='用户状态')
        create_parser.add_argument('--tags', help='标签（逗号分隔）')
        create_parser.add_argument('--attributes', help='扩展属性（JSON格式）')
        create_parser.add_argument('--operator', default='cli', help='操作人')
        
        get_parser = subparsers.add_parser('get', help='查询用户')
        get_parser.add_argument('user_id', help='用户ID')
        
        update_parser = subparsers.add_parser('update', help='更新用户')
        update_parser.add_argument('user_id', help='用户ID')
        update_parser.add_argument('--username', help='用户名')
        update_parser.add_argument('--email', help='邮箱')
        update_parser.add_argument('--phone', help='手机号')
        update_parser.add_argument('--status', help='用户状态')
        update_parser.add_argument('--tags', help='标签（逗号分隔）')
        update_parser.add_argument('--attributes', help='扩展属性（JSON格式）')
        update_parser.add_argument('--operator', default='cli', help='操作人')
        
        delete_parser = subparsers.add_parser('delete', help='删除用户')
        delete_parser.add_argument('user_id', help='用户ID')
        delete_parser.add_argument('--physical', action='store_true', help='物理删除')
        delete_parser.add_argument('--operator', default='cli', help='操作人')
        
        list_parser = subparsers.add_parser('list', help='查询用户列表')
        list_parser.add_argument('--status', help='按状态过滤')
        list_parser.add_argument('--tag', help='按标签过滤')
        list_parser.add_argument('--page', type=int, default=1, help='页码')
        list_parser.add_argument('--page-size', type=int, default=20, help='每页数量')
        
        batch_create_parser = subparsers.add_parser('batch-create', help='批量创建用户')
        batch_create_parser.add_argument('--file', required=True, help='数据文件路径')
        batch_create_parser.add_argument('--format', default='json', help='文件格式（json/csv）')
        batch_create_parser.add_argument('--operator', default='cli', help='操作人')
        
        stats_parser = subparsers.add_parser('stats', help='获取统计数据')
        stats_parser.add_argument('--status', help='按状态过滤')
        
        analyze_parser = subparsers.add_parser('analyze', help='智能分析')
        analyze_parser.add_argument('--type', choices=['anomalies', 'suggestions'], default='anomalies', help='分析类型')
        
        config_parser = subparsers.add_parser('config', help='配置管理')
        config_parser.add_argument('--reload', action='store_true', help='重新加载配置')
        config_parser.add_argument('--show', action='store_true', help='显示当前配置')
        
        return parser
    
    def _handle_create(self, args):
        """处理创建用户命令"""
        user_data = {
            'username': args.username,
            'email': args.email,
            'status': args.status
        }
        
        if args.phone:
            user_data['phone'] = args.phone
        
        if args.tags:
            user_data['tags'] = [tag.strip() for tag in args.tags.split(',')]
        
        if args.attributes:
            user_data['attributes'] = json.loads(args.attributes)
        
        result = self.user_service.create_user(user_data, args.operator)
        
        if result.success:
            user = result.data
            print(f"用户创建成功!")
            print(f"用户ID: {user.user_id}")
            print(f"用户名: {user.username}")
            print(f"邮箱: {user.email}")
            print(f"状态: {user.status.value}")
        else:
            print(f"创建失败: {result.error_message}")
    
    def _handle_get(self, args):
        """处理查询用户命令"""
        result = self.user_service.get_user(args.user_id)
        
        if result.success:
            user = result.data
            print(f"用户ID: {user.user_id}")
            print(f"用户名: {user.username}")
            print(f"邮箱: {user.email}")
            print(f"手机: {user.phone or '未设置'}")
            print(f"状态: {user.status.value}")
            print(f"标签: {', '.join(user.tags) if user.tags else '无'}")
            print(f"创建时间: {user.created_at}")
            print(f"创建人: {user.created_by}")
        else:
            print(f"查询失败: {result.error_message}")
    
    def _handle_update(self, args):
        """处理更新用户命令"""
        update_data = {}
        
        if args.username:
            update_data['username'] = args.username
        if args.email:
            update_data['email'] = args.email
        if args.phone:
            update_data['phone'] = args.phone
        if args.status:
            update_data['status'] = args.status
        if args.tags:
            update_data['tags'] = [tag.strip() for tag in args.tags.split(',')]
        if args.attributes:
            update_data['attributes'] = json.loads(args.attributes)
        
        result = self.user_service.update_user(args.user_id, update_data, args.operator)
        
        if result.success:
            user = result.data
            print(f"用户更新成功!")
            print(f"用户ID: {user.user_id}")
            print(f"用户名: {user.username}")
        else:
            print(f"更新失败: {result.error_message}")
    
    def _handle_delete(self, args):
        """处理删除用户命令"""
        result = self.user_service.delete_user(
            args.user_id,
            logical=not args.physical,
            operator=args.operator
        )
        
        if result.success:
            delete_type = "逻辑删除" if not args.physical else "物理删除"
            print(f"用户{delete_type}成功! 用户ID: {args.user_id}")
        else:
            print(f"删除失败: {result.error_message}")
    
    def _handle_list(self, args):
        """处理查询用户列表命令"""
        filters = {}
        if args.status:
            filters['status'] = args.status
        if args.tag:
            filters['tags'] = [args.tag]
        
        result = self.user_service.list_users(filters, args.page, args.page_size)
        
        if result.success:
            data = result.data
            print(f"用户列表 (第 {data['page']}/{data['total_pages']} 页，共 {data['total']} 个用户)")
            print("-" * 80)
            for user in data['users']:
                print(f"ID: {user['user_id'][:8]}... | 用户名: {user['username']} | 邮箱: {user['email']} | 状态: {user['status']}")
        else:
            print(f"查询失败: {result.error_message}")
    
    def _handle_batch_create(self, args):
        """处理批量创建命令"""
        result = self.batch_service.import_from_file(
            args.file,
            args.format,
            args.operator
        )
        
        if result.success:
            batch_result = result.data
            print(f"批量创建完成!")
            print(f"总数: {batch_result.total}")
            print(f"成功: {batch_result.success_count}")
            print(f"失败: {batch_result.failure_count}")
            print(f"成功率: {batch_result.success_rate:.2%}")
            
            if batch_result.failures:
                print("\n失败详情:")
                for failure in batch_result.failures[:5]:
                    print(f"  索引 {failure['index']}: {failure['error']}")
        else:
            print(f"批量创建失败: {result.error_message}")
    
    def _handle_stats(self, args):
        """处理统计命令"""
        filters = {'status': args.status} if args.status else None
        result = self.analysis_service.get_statistics(filters)
        
        if result.success:
            stats = result.data
            print(f"用户统计")
            print("=" * 50)
            print(f"总用户数: {stats.total_users}")
            print(f"\n状态分布:")
            for status, count in stats.status_distribution.items():
                print(f"  {status}: {count}")
            
            if stats.tag_distribution:
                print(f"\n标签分布 (前10):")
                sorted_tags = sorted(stats.tag_distribution.items(), key=lambda x: x[1], reverse=True)
                for tag, count in sorted_tags[:10]:
                    print(f"  {tag}: {count}")
        else:
            print(f"统计失败: {result.error_message}")
    
    def _handle_analyze(self, args):
        """处理分析命令"""
        if args.type == 'anomalies':
            result = self.analysis_service.detect_anomalies()
            
            if result.success:
                data = result.data
                print(f"异常检测")
                print("=" * 50)
                print(f"总异常数: {data['total_anomalies']}")
                
                anomalies = data['anomalies']
                if anomalies['duplicate_emails']:
                    print(f"\n重复邮箱: {len(anomalies['duplicate_emails'])} 个")
                if anomalies['duplicate_usernames']:
                    print(f"重复用户名: {len(anomalies['duplicate_usernames'])} 个")
                if anomalies['incomplete_data']:
                    print(f"不完整数据: {len(anomalies['incomplete_data'])} 个")
            else:
                print(f"分析失败: {result.error_message}")
        
        elif args.type == 'suggestions':
            result = self.analysis_service.get_operation_suggestions({})
            
            if result.success:
                print(f"优化建议")
                print("=" * 50)
                for idx, suggestion in enumerate(result.data, 1):
                    print(f"{idx}. {suggestion}")
            else:
                print(f"分析失败: {result.error_message}")
    
    def _handle_config(self, args):
        """处理配置命令"""
        if args.reload:
            result = self.config_service.reload_config()
            if result.success:
                print("配置重新加载成功!")
            else:
                print(f"配置重新加载失败: {result.error_message}")
        
        elif args.show:
            config = self.config_service.get_config()
            print("当前配置:")
            print("=" * 50)
            config_dict = config.to_dict()
            for key, value in config_dict.items():
                if key != 'llm_api_config':
                    print(f"{key}: {value}")
