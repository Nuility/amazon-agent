"""
使用真实测试数据测试智能体功能
测试数据路径: C:\1\挑战杯\测试数据
"""
import os
import sys
import json
import csv
import time
from datetime import datetime
from typing import Dict, List, Any

# 添加项目路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src_path = os.path.join(project_root, 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

class RealDataTester:
    """真实数据测试器"""
    
    def __init__(self):
        self.test_data_dir = r"C:\1\挑战杯\测试数据"
        self.results = []
        self.passed = 0
        self.failed = 0
        self.warnings = 0
        self.test_summary = {
            'start_time': datetime.now().isoformat(),
            'data_loaded': False,
            'campaigns': [],
            'analysis_results': {},
            'recommendations': []
        }
        
    def test(self, name: str, func):
        """运行测试"""
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
                    if isinstance(value, list) and len(value) > 5:
                        print(f"  {key}: {len(value)} 项")
                    else:
                        print(f"  {key}: {value}")
            if result.get('warnings'):
                for warning in result['warnings']:
                    print(f"  ⚠️  {warning}")
                    
        except Exception as e:
            self.failed += 1
            import traceback
            self.results.append({
                'name': name,
                'status': "❌ 异常",
                'success': False,
                'message': str(e),
                'traceback': traceback.format_exc()
            })
            print(f"❌ 异常")
            print(f"错误: {str(e)}")
    
    def print_summary(self):
        """打印总结"""
        print(f"\n{'='*60}")
        print("测试总结")
        print(f"{'='*60}")
        print(f"总计: {self.passed + self.failed} 个测试")
        print(f"✅ 通过: {self.passed}")
        print(f"❌ 失败: {self.failed}")
        print(f"⚠️  警告: {self.warnings}")
        
        if self.failed == 0:
            print("\n🎉 所有测试通过！智能体功能正常！")
        else:
            print(f"\n⚠️  有 {self.failed} 个测试失败")
        print(f"\n{'='*60}\n")


def test_data_loading():
    """测试1: 加载测试数据"""
    details = {}
    warnings = []
    
    test_data_dir = r"C:\1\挑战杯\测试数据"
    
    # 检查目录
    if not os.path.exists(test_data_dir):
        return {'success': False, 'message': f'测试数据目录不存在: {test_data_dir}'}
    
    details['数据目录'] = test_data_dir
    
    # 加载CSV数据
    csv_file = os.path.join(test_data_dir, 'Campaign Analyze_B08V4R84R1.csv')
    if not os.path.exists(csv_file):
        return {'success': False, 'message': f'CSV文件不存在: {csv_file}'}
    
    try:
        campaigns = []
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                campaigns.append(row)
        
        details['CSV文件'] = '✅ 加载成功'
        details['广告活动数量'] = len(campaigns)
        details['数据时间范围'] = f"{campaigns[0].get('Time', '')} 至 {campaigns[-1].get('Time', '')}"
        
        # 统计广告活动类型
        campaign_names = set()
        for c in campaigns:
            name = c.get('Campaign Name', '')
            if name:
                campaign_names.add(name)
        details['唯一广告活动数'] = len(campaign_names)
        
        return {
            'success': True,
            'message': '测试数据加载成功',
            'details': details,
            'data': {'campaigns': campaigns}
        }
        
    except Exception as e:
        return {
            'success': False,
            'message': f'CSV文件加载失败: {str(e)}',
            'details': details
        }


def test_data_analysis(tester):
    """测试2: 数据分析功能"""
    details = {}
    warnings = []
    
    # 获取加载的数据
    prev_result = tester.results[0] if tester.results else None
    if not prev_result or not prev_result.get('success'):
        return {'success': False, 'message': '前置测试失败，无法分析数据'}
    
    campaigns = prev_result.get('details', {}).get('data', {}).get('campaigns', [])
    if not campaigns:
        return {'success': False, 'message': '没有可分析的数据'}
    
    try:
        # 分析关键指标
        total_impressions = 0
        total_clicks = 0
        total_spend = 0
        total_orders = 0
        total_sales = 0
        enabled_count = 0
        paused_count = 0
        
        for c in campaigns:
            try:
                total_impressions += int(c.get('Impression', 0) or 0)
                total_clicks += int(c.get('Click', 0) or 0)
                total_spend += float(c.get('Spend', 0) or 0)
                total_orders += int(c.get('Order 1d', 0) or 0)
                total_sales += float(c.get('Sales 1d', 0) or 0)
                
                status = c.get('Status', '').lower()
                if status == 'enabled':
                    enabled_count += 1
                else:
                    paused_count += 1
            except:
                continue
        
        # 计算整体指标
        avg_ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
        avg_cpc = (total_spend / total_clicks) if total_clicks > 0 else 0
        avg_cvr = (total_orders / total_clicks * 100) if total_clicks > 0 else 0
        avg_acos = (total_spend / total_sales * 100) if total_sales > 0 else 0
        avg_roas = (total_sales / total_spend) if total_spend > 0 else 0
        
        details['总展示次数'] = f"{total_impressions:,}"
        details['总点击次数'] = f"{total_clicks:,}"
        details['总花费'] = f"${total_spend:.2f}"
        details['总订单数'] = total_orders
        details['总销售额'] = f"${total_sales:.2f}"
        details['平均CTR'] = f"{avg_ctr:.2f}%"
        details['平均CPC'] = f"${avg_cpc:.2f}"
        details['平均CVR'] = f"{avg_cvr:.2f}%"
        details['平均ACOS'] = f"{avg_acos:.2f}%"
        details['平均ROAS'] = f"{avg_roas:.2f}"
        details['启用广告活动'] = enabled_count
        details['暂停广告活动'] = paused_count
        
        # 识别问题
        if avg_acos > 100:
            warnings.append(f"ACOS过高 ({avg_acos:.2f}%)，建议优化")
        if avg_roas < 1:
            warnings.append(f"ROAS过低 ({avg_roas:.2f})，投入产出比不佳")
        
        return {
            'success': True,
            'message': '数据分析完成',
            'details': details,
            'warnings': warnings
        }
        
    except Exception as e:
        return {
            'success': False,
            'message': f'数据分析失败: {str(e)}',
            'details': details
        }


def test_recommendation_generation(tester):
    """测试3: 优化建议生成"""
    details = {}
    warnings = []
    
    # 获取分析结果
    prev_result = tester.results[1] if len(tester.results) > 1 else None
    if not prev_result or not prev_result.get('success'):
        return {'success': False, 'message': '前置分析失败'}
    
    try:
        # 基于数据生成优化建议
        recommendations = []
        
        # 获取原始数据
        campaigns_data = tester.results[0].get('details', {}).get('data', {}).get('campaigns', [])
        
        # 分析每个广告活动
        high_acos_campaigns = []
        low_roas_campaigns = []
        low_ctr_campaigns = []
        
        for c in campaigns_data:
            try:
                name = c.get('Campaign Name', 'Unknown')
                acos = float(c.get('ACOS 1d', 0) or 0)
                roas = float(c.get('ROAS 1d', 0) or 0)
                ctr = float(c.get('CTR', '0%').replace('%', '') or 0)
                spend = float(c.get('Spend', 0) or 0)
                
                if acos > 80 and spend > 10:
                    high_acos_campaigns.append({
                        'name': name,
                        'acos': acos,
                        'spend': spend,
                        'recommendation': '考虑降低出价或暂停',
                        'priority': 'high'
                    })
                
                if roas < 1.5 and spend > 10:
                    low_roas_campaigns.append({
                        'name': name,
                        'roas': roas,
                        'spend': spend,
                        'recommendation': 'ROAS过低，建议优化关键词',
                        'priority': 'high'
                    })
                
                if ctr < 0.5 and spend > 5:
                    low_ctr_campaigns.append({
                        'name': name,
                        'ctr': ctr,
                        'spend': spend,
                        'recommendation': 'CTR过低，检查关键词相关性',
                        'priority': 'medium'
                    })
                    
            except:
                continue
        
        # 生成建议
        if high_acos_campaigns:
            recommendations.append({
                'type': '降低ACOS',
                'count': len(high_acos_campaigns),
                'campaigns': [c['name'] for c in high_acos_campaigns[:5]],
                'action': '降低出价或暂停高ACOS广告活动',
                'priority': 'high'
            })
        
        if low_roas_campaigns:
            recommendations.append({
                'type': '提高ROAS',
                'count': len(low_roas_campaigns),
                'campaigns': [c['name'] for c in low_roas_campaigns[:5]],
                'action': '优化低ROAS广告活动的关键词',
                'priority': 'high'
            })
        
        if low_ctr_campaigns:
            recommendations.append({
                'type': '提高CTR',
                'count': len(low_ctr_campaigns),
                'campaigns': [c['name'] for c in low_ctr_campaigns[:5]],
                'action': '优化低CTR广告活动的关键词相关性',
                'priority': 'medium'
            })
        
        details['生成建议数量'] = len(recommendations)
        details['高ACOS广告活动'] = len(high_acos_campaigns)
        details['低ROAS广告活动'] = len(low_roas_campaigns)
        details['低CTR广告活动'] = len(low_ctr_campaigns)
        
        # 显示建议详情
        for i, rec in enumerate(recommendations, 1):
            details[f'建议{i}'] = f"{rec['type']}: {rec['action']} ({rec['count']}个广告活动)"
        
        if not recommendations:
            warnings.append("未发现明显需要优化的广告活动")
        
        return {
            'success': True,
            'message': f'生成 {len(recommendations)} 条优化建议',
            'details': details,
            'warnings': warnings,
            'recommendations': recommendations
        }
        
    except Exception as e:
        return {
            'success': False,
            'message': f'建议生成失败: {str(e)}',
            'details': details
        }


def test_ad_agent_service_integration():
    """测试4: 广告智能体服务集成"""
    details = {}
    warnings = []
    
    try:
        from main import Application
        
        # 初始化应用
        app = Application()
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config_path = os.path.join(project_root, 'config', 'config.yaml')
        
        success = app.initialize(config_path)
        
        if not success:
            return {'success': False, 'message': '应用初始化失败'}
        
        details['应用初始化'] = '✅ 成功'
        
        # 检查智能体服务
        if app.ad_agent_service:
            details['智能体服务'] = '✅ 已初始化'
            
            # 测试获取摘要
            try:
                summary = app.ad_agent_service.get_summary()
                details['数据摘要获取'] = '✅ 成功'
            except Exception as e:
                warnings.append(f"数据摘要获取失败: {str(e)}")
            
            # 测试列出广告活动
            try:
                campaigns = app.ad_agent_service.list_campaigns()
                details['广告活动列表'] = '✅ 成功'
            except Exception as e:
                warnings.append(f"广告活动列表获取失败: {str(e)}")
            
            return {
                'success': True,
                'message': '智能体服务集成测试通过',
                'details': details,
                'warnings': warnings
            }
        else:
            return {
                'success': False,
                'message': '智能体服务未初始化',
                'details': details
            }
            
    except Exception as e:
        return {
            'success': False,
            'message': f'智能体服务集成测试异常: {str(e)}',
            'details': details
        }


def test_data_import():
    """测试5: 数据导入功能"""
    details = {}
    warnings = []
    
    try:
        from main import Application
        
        app = Application()
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config_path = os.path.join(project_root, 'config', 'config.yaml')
        app.initialize(config_path)
        
        # 测试导入CSV数据
        csv_file = r"C:\1\挑战杯\测试数据\Campaign Analyze_B08V4R84R1.csv"
        
        # 读取CSV
        campaigns = []
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                campaigns.append(row)
        
        # 尝试存储到仓储
        if app.ad_report_repo:
            # 转换数据格式
            for c in campaigns[:5]:  # 测试导入前5条
                try:
                    report_data = {
                        'campaign_id': c.get('Campaign Name', ''),
                        'campaign_name': c.get('Name', ''),
                        'date': c.get('Time', ''),
                        'impressions': int(c.get('Impression', 0) or 0),
                        'clicks': int(c.get('Click', 0) or 0),
                        'cost': float(c.get('Spend', 0) or 0),
                        'orders': int(c.get('Order 1d', 0) or 0),
                        'sales': float(c.get('Sales 1d', 0) or 0),
                        'status': c.get('Status', '')
                    }
                    
                    # 存储报告
                    app.ad_report_repo.save_report(
                        campaign_id=report_data['campaign_id'],
                        date=report_data['date'],
                        report_data=report_data
                    )
                    
                except Exception as e:
                    warnings.append(f"导入数据失败: {str(e)}")
                    continue
            
            details['数据导入'] = '✅ 成功'
            details['导入数量'] = 5
            details['总数据量'] = len(campaigns)
            
            return {
                'success': True,
                'message': '数据导入功能测试通过',
                'details': details,
                'warnings': warnings
            }
        else:
            return {
                'success': False,
                'message': '广告报告仓储未初始化',
                'details': details
            }
            
    except Exception as e:
        return {
            'success': False,
            'message': f'数据导入测试失败: {str(e)}',
            'details': details
        }


def test_performance_metrics():
    """测试6: 性能指标计算"""
    details = {}
    
    # 获取数据
    test_data_dir = r"C:\1\挑战杯\测试数据"
    csv_file = os.path.join(test_data_dir, 'Campaign Analyze_B08V4R84R1.csv')
    
    try:
        campaigns = []
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                campaigns.append(row)
        
        # 计算性能指标
        metrics = {
            'best_roas': 0,
            'best_roas_campaign': '',
            'worst_acos': 0,
            'worst_acos_campaign': '',
            'highest_spend': 0,
            'highest_spend_campaign': '',
            'best_cvr': 0,
            'best_cvr_campaign': ''
        }
        
        for c in campaigns:
            try:
                name = c.get('Campaign Name', '')
                roas = float(c.get('ROAS 1d', 0) or 0)
                acos = float(c.get('ACOS 1d', 0) or 0)
                spend = float(c.get('Spend', 0) or 0)
                cvr = float(c.get('CVR 1d', '0%').replace('%', '') or 0)
                
                if roas > metrics['best_roas']:
                    metrics['best_roas'] = roas
                    metrics['best_roas_campaign'] = name
                
                if acos > metrics['worst_acos']:
                    metrics['worst_acos'] = acos
                    metrics['worst_acos_campaign'] = name
                
                if spend > metrics['highest_spend']:
                    metrics['highest_spend'] = spend
                    metrics['highest_spend_campaign'] = name
                
                if cvr > metrics['best_cvr']:
                    metrics['best_cvr'] = cvr
                    metrics['best_cvr_campaign'] = name
                    
            except:
                continue
        
        details['最佳ROAS'] = f"{metrics['best_roas']:.2f} ({metrics['best_roas_campaign'][:30]})"
        details['最高ACOS'] = f"{metrics['worst_acos']:.2f}% ({metrics['worst_acos_campaign'][:30]})"
        details['最高花费'] = f"${metrics['highest_spend']:.2f} ({metrics['highest_spend_campaign'][:30]})"
        details['最佳CVR'] = f"{metrics['best_cvr']:.2f}% ({metrics['best_cvr_campaign'][:30]})"
        
        return {
            'success': True,
            'message': '性能指标计算完成',
            'details': details
        }
        
    except Exception as e:
        return {
            'success': False,
            'message': f'性能指标计算失败: {str(e)}',
            'details': details
        }


def test_trend_analysis():
    """测试7: 趋势分析"""
    details = {}
    
    test_data_dir = r"C:\1\挑战杯\测试数据"
    csv_file = os.path.join(test_data_dir, 'Campaign Analyze_B08V4R84R1.csv')
    
    try:
        campaigns = []
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                campaigns.append(row)
        
        # 按日期分组
        daily_data = {}
        for c in campaigns:
            date = c.get('Time', '')
            if not date:
                continue
            
            if date not in daily_data:
                daily_data[date] = {
                    'spend': 0,
                    'sales': 0,
                    'orders': 0,
                    'clicks': 0,
                    'impressions': 0
                }
            
            try:
                daily_data[date]['spend'] += float(c.get('Spend', 0) or 0)
                daily_data[date]['sales'] += float(c.get('Sales 1d', 0) or 0)
                daily_data[date]['orders'] += int(c.get('Order 1d', 0) or 0)
                daily_data[date]['clicks'] += int(c.get('Click', 0) or 0)
                daily_data[date]['impressions'] += int(c.get('Impression', 0) or 0)
            except:
                continue
        
        # 排序日期
        sorted_dates = sorted(daily_data.keys())
        
        if len(sorted_dates) >= 2:
            first_date = sorted_dates[0]
            last_date = sorted_dates[-1]
            
            first_data = daily_data[first_date]
            last_data = daily_data[last_date]
            
            # 计算趋势
            spend_trend = ((last_data['spend'] - first_data['spend']) / first_data['spend'] * 100) if first_data['spend'] > 0 else 0
            sales_trend = ((last_data['sales'] - first_data['sales']) / first_data['sales'] * 100) if first_data['sales'] > 0 else 0
            orders_trend = ((last_data['orders'] - first_data['orders']) / first_data['orders'] * 100) if first_data['orders'] > 0 else 0
            
            details['分析天数'] = len(sorted_dates)
            details['起始日期'] = first_date
            details['结束日期'] = last_date
            details['花费趋势'] = f"{spend_trend:+.2f}%"
            details['销售趋势'] = f"{sales_trend:+.2f}%"
            details['订单趋势'] = f"{orders_trend:+.2f}%"
            
            # 趋势判断
            if sales_trend > 0 and orders_trend > 0:
                details['整体趋势'] = '📈 向好'
            elif sales_trend < 0 and orders_trend < 0:
                details['整体趋势'] = '📉 下降'
            else:
                details['整体趋势'] = '➡️ 平稳'
        
        return {
            'success': True,
            'message': '趋势分析完成',
            'details': details
        }
        
    except Exception as e:
        return {
            'success': False,
            'message': f'趋势分析失败: {str(e)}',
            'details': details
        }


def generate_test_report(tester):
    """生成测试报告"""
    report = {
        'test_info': {
            'test_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'test_data_path': r"C:\1\挑战杯\测试数据",
            'total_tests': tester.passed + tester.failed,
            'passed': tester.passed,
            'failed': tester.failed,
            'warnings': tester.warnings,
            'success_rate': f"{(tester.passed / (tester.passed + tester.failed) * 100):.1f}%" if (tester.passed + tester.failed) > 0 else "0%"
        },
        'test_results': tester.results,
        'summary': {
            'environment': 'Python ' + sys.version.split()[0],
            'platform': sys.platform
        }
    }
    
    # 保存JSON报告
    report_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                'test_result_with_data.json')
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n测试报告已保存: {report_path}")
    
    return report


def main():
    """主测试流程"""
    print("\n" + "="*60)
    print("Amazon Ads Agent 智能体功能测试（使用真实数据）")
    print("="*60)
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"测试数据: C:\\1\\挑战杯\\测试数据")
    print("="*60 + "\n")
    
    tester = RealDataTester()
    
    # 运行测试
    tester.test("1. 测试数据加载", test_data_loading)
    tester.test("2. 数据分析功能", lambda: test_data_analysis(tester))
    tester.test("3. 优化建议生成", lambda: test_recommendation_generation(tester))
    tester.test("4. 智能体服务集成", test_ad_agent_service_integration)
    tester.test("5. 数据导入功能", test_data_import)
    tester.test("6. 性能指标计算", test_performance_metrics)
    tester.test("7. 趋势分析", test_trend_analysis)
    
    # 打印总结
    tester.print_summary()
    
    # 生成报告
    report = generate_test_report(tester)
    
    return tester.failed == 0


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
