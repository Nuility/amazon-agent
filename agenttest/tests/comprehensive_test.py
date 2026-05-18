"""
Amazon Ads Agent 综合测试脚本
测试所有核心功能和组件
"""
import os
import sys
import json
import time
import traceback
from datetime import datetime
from typing import Dict, List, Any

class TestRunner:
    """测试运行器"""
    
    def __init__(self):
        self.results = []
        self.passed = 0
        self.failed = 0
        self.warnings = 0
        self.project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
    def test(self, name: str, func):
        """运行单个测试"""
        print(f"\n{'='*60}")
        print(f"测试: {name}")
        print(f"{'='*60}")
        
        try:
            result = func()
            if result.get('success', False):
                self.passed += 1
                status = "✅ 通过"
                if result.get('warnings'):
                    self.warnings += len(result['warnings'])
                    status += f" (警告: {len(result['warnings'])})"
            else:
                self.failed += 1
                status = "❌ 失败"
            
            self.results.append({
                'name': name,
                'status': status,
                'success': result.get('success', False),
                'message': result.get('message', ''),
                'details': result.get('details', {}),
                'warnings': result.get('warnings', [])
            })
            
            print(f"{status}")
            if result.get('message'):
                print(f"说明: {result['message']}")
            if result.get('details'):
                for key, value in result['details'].items():
                    print(f"  {key}: {value}")
            if result.get('warnings'):
                for warning in result['warnings']:
                    print(f"  ⚠️  {warning}")
                    
        except Exception as e:
            self.failed += 1
            status = "❌ 异常"
            error_msg = str(e)
            
            self.results.append({
                'name': name,
                'status': status,
                'success': False,
                'message': error_msg,
                'traceback': traceback.format_exc()
            })
            
            print(f"{status}")
            print(f"错误: {error_msg}")
            print(traceback.format_exc())
    
    def print_summary(self):
        """打印测试总结"""
        print(f"\n{'='*60}")
        print("测试总结")
        print(f"{'='*60}")
        print(f"总计: {self.passed + self.failed} 个测试")
        print(f"✅ 通过: {self.passed}")
        print(f"❌ 失败: {self.failed}")
        print(f"⚠️  警告: {self.warnings}")
        
        if self.failed == 0:
            print("\n🎉 所有测试通过！")
        else:
            print(f"\n⚠️  有 {self.failed} 个测试失败，请检查")
            
        print(f"\n{'='*60}\n")


def test_environment():
    """测试1: 环境检查"""
    details = {}
    warnings = []
    
    # Python版本
    py_version = sys.version_info
    details['Python版本'] = f"{py_version.major}.{py_version.minor}.{py_version.micro}"
    
    if py_version.major < 3 or (py_version.major == 3 and py_version.minor < 8):
        return {'success': False, 'message': 'Python版本过低，需要3.8+'}
    
    # 项目目录
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    details['项目根目录'] = project_root
    
    required_dirs = ['src', 'config', 'tests']
    for dir_name in required_dirs:
        dir_path = os.path.join(project_root, dir_name)
        if not os.path.exists(dir_path):
            warnings.append(f"缺少目录: {dir_name}")
    
    return {
        'success': True,
        'message': '环境检查完成',
        'details': details,
        'warnings': warnings
    }


def test_dependencies():
    """测试2: 依赖包检查"""
    details = {}
    warnings = []
    
    required_packages = {
        'yaml': 'PyYAML',
        'dotenv': 'python-dotenv',
        'click': 'Click',
        'fastapi': 'FastAPI',
        'uvicorn': 'Uvicorn',
        'pydantic': 'Pydantic'
    }
    
    missing = []
    for module, package in required_packages.items():
        try:
            __import__(module)
            details[package] = '✅ 已安装'
        except ImportError:
            details[package] = '❌ 未安装'
            missing.append(package)
    
    if missing:
        warnings.append(f"缺少依赖包: {', '.join(missing)}")
        return {
            'success': False,
            'message': '请安装缺失的依赖包',
            'details': details,
            'warnings': warnings
        }
    
    return {
        'success': True,
        'message': '所有核心依赖已安装',
        'details': details
    }


def test_config():
    """测试3: 配置文件检查"""
    details = {}
    warnings = []
    
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(project_root, 'config', 'config.yaml')
    
    # 检查配置文件存在
    if not os.path.exists(config_path):
        return {'success': False, 'message': '配置文件不存在'}
    
    details['配置文件路径'] = config_path
    
    # 尝试加载配置
    try:
        import yaml
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        # 检查关键配置项
        required_keys = ['max_batch_size', 'log_level', 'data_file_path']
        for key in required_keys:
            if key in config:
                details[f'配置项 {key}'] = str(config[key])
            else:
                warnings.append(f"缺少配置项: {key}")
        
        # 检查LLM配置
        if 'llm_api_config' in config:
            llm_config = config['llm_api_config']
            details['LLM提供商'] = llm_config.get('provider', '未配置')
            details['LLM集成'] = '启用' if config.get('enable_llm_integration') else '禁用'
        
        return {
            'success': True,
            'message': '配置文件加载成功',
            'details': details,
            'warnings': warnings
        }
        
    except Exception as e:
        return {
            'success': False,
            'message': f'配置文件解析失败: {str(e)}',
            'warnings': warnings
        }


def test_storage():
    """测试4: 存储系统测试"""
    details = {}
    warnings = []
    
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(project_root, 'data', 'users.json')
    
    # 检查数据目录
    data_dir = os.path.dirname(data_path)
    if not os.path.exists(data_dir):
        os.makedirs(data_dir, exist_ok=True)
        details['数据目录'] = '已创建'
    else:
        details['数据目录'] = '已存在'
    
    # 测试文件存储
    try:
        # 写入测试数据
        test_data = {
            'test_key': {
                'id': 'test_001',
                'name': '测试用户',
                'timestamp': datetime.now().isoformat()
            }
        }
        
        # 如果文件存在，先读取
        if os.path.exists(data_path):
            with open(data_path, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
        else:
            existing_data = {}
        
        # 合并数据
        existing_data.update(test_data)
        
        # 写入文件
        with open(data_path, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, indent=2, ensure_ascii=False)
        
        # 读取验证
        with open(data_path, 'r', encoding='utf-8') as f:
            read_data = json.load(f)
        
        if 'test_key' in read_data:
            details['写入测试'] = '✅ 成功'
            details['读取测试'] = '✅ 成功'
            
            # 清理测试数据
            del existing_data['test_key']
            with open(data_path, 'w', encoding='utf-8') as f:
                json.dump(existing_data, f, indent=2, ensure_ascii=False)
            
            return {
                'success': True,
                'message': '存储系统工作正常',
                'details': details
            }
        else:
            return {
                'success': False,
                'message': '数据读取验证失败',
                'details': details
            }
            
    except Exception as e:
        return {
            'success': False,
            'message': f'存储测试失败: {str(e)}',
            'details': details,
            'warnings': warnings
        }


def test_application_init():
    """测试5: 应用初始化测试"""
    details = {}
    warnings = []
    
    try:
        # 添加src到路径
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        src_path = os.path.join(project_root, 'src')
        if src_path not in sys.path:
            sys.path.insert(0, src_path)
        
        # 导入Application类
        from main import Application
        
        details['Application类'] = '✅ 导入成功'
        
        # 尝试初始化
        app = Application()
        details['Application实例'] = '✅ 创建成功'
        
        # 初始化应用
        config_path = os.path.join(project_root, 'config', 'config.yaml')
        success = app.initialize(config_path)
        
        if success:
            details['应用初始化'] = '✅ 成功'
            details['配置加载'] = '✅ 成功' if app.config else '❌ 失败'
            details['存储初始化'] = '✅ 成功' if app.storage else '❌ 失败'
            details['用户仓储'] = '✅ 成功' if app.user_repo else '❌ 失败'
            details['用户服务'] = '✅ 成功' if app.user_service else '❌ 失败'
            
            return {
                'success': True,
                'message': '应用初始化成功',
                'details': details,
                'warnings': warnings
            }
        else:
            return {
                'success': False,
                'message': '应用初始化失败',
                'details': details,
                'warnings': warnings
            }
            
    except Exception as e:
        return {
            'success': False,
            'message': f'应用初始化异常: {str(e)}',
            'details': details,
            'warnings': warnings
        }


def test_user_service():
    """测试6: 用户服务测试"""
    details = {}
    warnings = []
    
    try:
        # 初始化应用
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        src_path = os.path.join(project_root, 'src')
        if src_path not in sys.path:
            sys.path.insert(0, src_path)
        
        from main import Application
        
        app = Application()
        config_path = os.path.join(project_root, 'config', 'config.yaml')
        app.initialize(config_path)
        
        # 测试创建用户
        test_user_data = {
            'username': f'测试用户_{int(time.time())}',
            'email': f'test_{int(time.time())}@example.com',
            'phone': '13800138000'
        }
        
        create_result = app.user_service.create_user(**test_user_data)
        
        if create_result.success:
            details['创建用户'] = '✅ 成功'
            user_id = create_result.data.user_id
            details['用户ID'] = user_id
            
            # 测试查询用户
            get_result = app.user_service.get_user(user_id)
            if get_result.success:
                details['查询用户'] = '✅ 成功'
                details['用户名'] = get_result.data.username
            else:
                details['查询用户'] = f'❌ 失败: {get_result.error}'
            
            # 测试更新用户
            update_result = app.user_service.update_user(user_id, username='更新后的用户名')
            if update_result.success:
                details['更新用户'] = '✅ 成功'
            else:
                details['更新用户'] = f'❌ 失败: {update_result.error}'
            
            # 测试删除用户
            delete_result = app.user_service.delete_user(user_id)
            if delete_result.success:
                details['删除用户'] = '✅ 成功'
            else:
                details['删除用户'] = f'❌ 失败: {delete_result.error}'
            
            return {
                'success': True,
                'message': '用户服务测试完成',
                'details': details,
                'warnings': warnings
            }
        else:
            return {
                'success': False,
                'message': f'创建用户失败: {create_result.error}',
                'details': details,
                'warnings': warnings
            }
            
    except Exception as e:
        return {
            'success': False,
            'message': f'用户服务测试异常: {str(e)}',
            'details': details,
            'warnings': warnings
        }


def test_statistics():
    """测试7: 统计服务测试"""
    details = {}
    warnings = []
    
    try:
        # 初始化应用
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        src_path = os.path.join(project_root, 'src')
        if src_path not in sys.path:
            sys.path.insert(0, src_path)
        
        from main import Application
        
        app = Application()
        config_path = os.path.join(project_root, 'config', 'config.yaml')
        app.initialize(config_path)
        
        # 获取统计数据
        stats_result = app.analysis_service.get_statistics()
        
        if stats_result.success:
            stats = stats_result.data
            details['用户总数'] = stats.total_users
            details['活跃用户'] = stats.active_users
            details['未活跃用户'] = stats.inactive_users
            details['已删除用户'] = stats.deleted_users
            
            return {
                'success': True,
                'message': '统计服务测试完成',
                'details': details
            }
        else:
            return {
                'success': False,
                'message': f'获取统计数据失败: {stats_result.error}',
                'details': details
            }
            
    except Exception as e:
        return {
            'success': False,
            'message': f'统计服务测试异常: {str(e)}',
            'details': details,
            'warnings': warnings
        }


def test_api_server():
    """测试8: API服务器测试"""
    details = {}
    warnings = []
    
    try:
        # 检查API文件
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        server_path = os.path.join(project_root, 'src', 'api', 'server.py')
        
        if not os.path.exists(server_path):
            return {
                'success': False,
                'message': 'API服务器文件不存在',
                'warnings': warnings
            }
        
        details['服务器文件'] = '✅ 存在'
        
        # 检查UI文件
        ui_files = ['index.html', 'app.js', 'styles.css']
        ui_path = os.path.join(project_root, 'src', 'api', 'ui')
        
        for ui_file in ui_files:
            file_path = os.path.join(ui_path, ui_file)
            if os.path.exists(file_path):
                size = os.path.getsize(file_path)
                details[f'UI文件 {ui_file}'] = f'✅ {size} bytes'
            else:
                warnings.append(f"UI文件缺失: {ui_file}")
        
        # 尝试导入FastAPI应用
        api_path = os.path.join(project_root, 'src', 'api')
        if api_path not in sys.path:
            sys.path.insert(0, api_path)
        
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location("server", server_path)
            server_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(server_module)
            
            if hasattr(server_module, 'app'):
                details['FastAPI应用'] = '✅ 加载成功'
            else:
                warnings.append("FastAPI app对象未找到")
                
        except Exception as e:
            warnings.append(f"FastAPI应用加载异常: {str(e)}")
        
        return {
            'success': True,
            'message': 'API服务器检查完成',
            'details': details,
            'warnings': warnings
        }
        
    except Exception as e:
        return {
            'success': False,
            'message': f'API服务器测试异常: {str(e)}',
            'details': details,
            'warnings': warnings
        }


def test_llm_client():
    """测试9: LLM客户端测试"""
    details = {}
    warnings = []
    
    try:
        # 初始化应用
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        src_path = os.path.join(project_root, 'src')
        if src_path not in sys.path:
            sys.path.insert(0, src_path)
        
        from main import Application
        
        app = Application()
        config_path = os.path.join(project_root, 'config', 'config.yaml')
        app.initialize(config_path)
        
        # 检查LLM客户端
        if app.config and app.config.llm_api_config:
            llm_config = app.config.llm_api_config
            details['LLM提供商'] = llm_config.get('provider', '未配置')
            details['LLM模型'] = llm_config.get('model', '未配置')
            
            # 检查LLM客户端是否可用
            try:
                from infrastructure.llm_client import create_llm_client
                client = create_llm_client(llm_config)
                
                if client.is_available():
                    details['LLM客户端状态'] = '✅ 可用'
                else:
                    details['LLM客户端状态'] = '⚠️ 不可用（Mock模式）'
                    warnings.append("LLM客户端不可用，将使用Mock模式")
                
                return {
                    'success': True,
                    'message': 'LLM客户端检查完成',
                    'details': details,
                    'warnings': warnings
                }
            except Exception as e:
                warnings.append(f"LLM客户端创建异常: {str(e)}")
                return {
                    'success': True,
                    'message': 'LLM配置检查完成',
                    'details': details,
                    'warnings': warnings
                }
        else:
            return {
                'success': True,
                'message': 'LLM未配置（将使用Mock模式）',
                'details': details,
                'warnings': ['LLM未配置，将使用Mock模式']
            }
            
    except Exception as e:
        return {
            'success': False,
            'message': f'LLM客户端测试异常: {str(e)}',
            'details': details,
            'warnings': warnings
        }


def test_ad_agent_service():
    """测试10: 广告智能体服务测试"""
    details = {}
    warnings = []
    
    try:
        # 初始化应用
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        src_path = os.path.join(project_root, 'src')
        if src_path not in sys.path:
            sys.path.insert(0, src_path)
        
        from main import Application
        
        app = Application()
        config_path = os.path.join(project_root, 'config', 'config.yaml')
        app.initialize(config_path)
        
        # 检查智能体服务
        if app.ad_agent_service:
            details['智能体服务'] = '✅ 已初始化'
            
            # 测试获取摘要
            try:
                summary = app.ad_agent_service.get_summary()
                details['数据摘要'] = '✅ 可获取'
            except Exception as e:
                warnings.append(f"获取数据摘要失败: {str(e)}")
            
            # 测试列出广告活动
            try:
                campaigns = app.ad_agent_service.list_campaigns()
                details['广告活动列表'] = '✅ 可获取'
            except Exception as e:
                warnings.append(f"获取广告活动失败: {str(e)}")
            
            return {
                'success': True,
                'message': '广告智能体服务检查完成',
                'details': details,
                'warnings': warnings
            }
        else:
            return {
                'success': False,
                'message': '广告智能体服务未初始化',
                'details': details,
                'warnings': warnings
            }
            
    except Exception as e:
        return {
            'success': False,
            'message': f'广告智能体服务测试异常: {str(e)}',
            'details': details,
            'warnings': warnings
        }


def main():
    """运行所有测试"""
    print("\n" + "="*60)
    print("Amazon Ads Agent 综合测试")
    print("="*60)
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60 + "\n")
    
    runner = TestRunner()
    
    # 运行所有测试
    runner.test("1. 环境检查", test_environment)
    runner.test("2. 依赖包检查", test_dependencies)
    runner.test("3. 配置文件检查", test_config)
    runner.test("4. 存储系统测试", test_storage)
    runner.test("5. 应用初始化测试", test_application_init)
    runner.test("6. 用户服务测试", test_user_service)
    runner.test("7. 统计服务测试", test_statistics)
    runner.test("8. API服务器测试", test_api_server)
    runner.test("9. LLM客户端测试", test_llm_client)
    runner.test("10. 广告智能体服务测试", test_ad_agent_service)
    
    # 打印总结
    runner.print_summary()
    
    # 生成测试报告
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    report_path = os.path.join(project_root, 'test_report.json')
    
    report = {
        'timestamp': datetime.now().isoformat(),
        'total': runner.passed + runner.failed,
        'passed': runner.passed,
        'failed': runner.failed,
        'warnings': runner.warnings,
        'results': runner.results
    }
    
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"测试报告已保存: {report_path}")
    
    return runner.failed == 0


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
