"""
项目结构验证脚本（无需Python依赖）
检查项目文件和目录结构
"""
import os
import sys

def validate_project():
    """验证项目结构"""
    
    print("="*60)
    print("Amazon Ads Agent 项目结构验证")
    print("="*60)
    print()
    
    # 获取项目根目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    print(f"项目根目录: {project_root}")
    print()
    
    # 定义必需的文件和目录
    required_structure = {
        'directories': [
            'src',
            'src/api',
            'src/api/ui',
            'src/common',
            'src/infrastructure',
            'src/repositories',
            'src/services',
            'src/interface',
            'config',
            'tests',
            'data'
        ],
        'files': [
            'src/main.py',
            'src/api/server.py',
            'src/api/ui/index.html',
            'src/api/ui/app.js',
            'src/api/ui/styles.css',
            'src/common/types.py',
            'src/common/ad_types.py',
            'src/infrastructure/llm_client.py',
            'src/infrastructure/file_storage_adapter.py',
            'src/repositories/user_repository.py',
            'src/services/user_service.py',
            'src/services/ad_agent_service.py',
            'config/config.yaml',
            'requirements.txt',
            'README.md',
            '使用手册.md',
            '后续开发者任务.md'
        ]
    }
    
    # 检查目录
    print("检查目录结构...")
    dir_results = []
    for dir_path in required_structure['directories']:
        full_path = os.path.join(project_root, dir_path)
        exists = os.path.exists(full_path) and os.path.isdir(full_path)
        status = "✅" if exists else "❌"
        dir_results.append((dir_path, exists))
        print(f"  {status} {dir_path}")
    
    # 检查文件
    print("\n检查关键文件...")
    file_results = []
    for file_path in required_structure['files']:
        full_path = os.path.join(project_root, file_path)
        exists = os.path.exists(full_path) and os.path.isfile(full_path)
        status = "✅" if exists else "❌"
        size = os.path.getsize(full_path) if exists else 0
        file_results.append((file_path, exists, size))
        print(f"  {status} {file_path} ({size} bytes)")
    
    # 统计结果
    dir_passed = sum(1 for _, exists in dir_results if exists)
    file_passed = sum(1 for _, exists, _ in file_results if exists)
    
    total_checks = len(dir_results) + len(file_results)
    total_passed = dir_passed + file_passed
    
    print()
    print("="*60)
    print("验证结果")
    print("="*60)
    print(f"目录检查: {dir_passed}/{len(dir_results)} 通过")
    print(f"文件检查: {file_passed}/{len(file_results)} 通过")
    print(f"总计: {total_passed}/{total_checks} 通过")
    print()
    
    # 检查关键配置
    print("关键配置检查:")
    config_path = os.path.join(project_root, 'config', 'config.yaml')
    if os.path.exists(config_path):
        try:
            import yaml
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            
            print(f"  ✅ 配置文件加载成功")
            print(f"  - max_batch_size: {config.get('max_batch_size', '未设置')}")
            print(f"  - log_level: {config.get('log_level', '未设置')}")
            print(f"  - enable_llm_integration: {config.get('enable_llm_integration', False)}")
            
            if 'llm_api_config' in config:
                llm_config = config['llm_api_config']
                print(f"  - LLM提供商: {llm_config.get('provider', '未配置')}")
                print(f"  - LLM模型: {llm_config.get('model', '未配置')}")
        except Exception as e:
            print(f"  ⚠️  配置文件解析失败: {str(e)}")
    else:
        print(f"  ❌ 配置文件不存在")
    
    print()
    
    # 最终结果
    if total_passed == total_checks:
        print("🎉 所有检查通过！项目结构完整。")
        print()
        print("下一步：")
        print("1. 安装依赖: pip install -r requirements.txt")
        print("2. 运行测试: python tests/comprehensive_test.py")
        print("3. 启动服务: python start.py")
        return True
    else:
        print("⚠️  有部分检查未通过，请检查缺失的文件或目录。")
        return False

if __name__ == '__main__':
    success = validate_project()
    print()
    input("按回车键退出...")
    sys.exit(0 if success else 1)
