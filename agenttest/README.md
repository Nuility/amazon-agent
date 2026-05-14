# 用户管理智能体系统

一个智能化、可扩展的用户管理解决方案，支持与大模型API集成实现智能化决策。

---

## 项目简介

用户管理智能体系统提供以下核心功能：

- **用户管理**: 创建、查询、更新、删除用户的完整生命周期管理
- **批量操作**: 支持批量创建、更新、删除，以及从文件导入用户数据
- **智能分析**: 统计分析、异常检测、优化建议生成
- **配置管理**: 灵活的配置系统，支持热更新
- **大模型集成**: 预留OpenAI、华为云盘古等大模型API接口（需开发者自行配置）

---

## 核心功能

### ✅ 用户管理
- 创建用户（支持扩展属性和标签）
- 查询用户详情和列表
- 更新用户信息
- 删除用户（逻辑删除/物理删除）
- 状态流转管理

### ✅ 批量操作
- 批量创建用户（支持事务）
- 批量更新用户
- 批量删除用户
- 从JSON/CSV文件导入

### ✅ 智能分析
- 用户统计数据
- 状态分布分析
- 标签分布分析
- 异常数据检测
- 操作优化建议

### ✅ 配置管理
- YAML/JSON配置文件支持
- 环境变量覆盖
- 配置验证
- 热更新机制

### ✅ 大模型集成（预留）
- OpenAI客户端接口
- 华为云盘古客户端接口
- 降级策略支持

---

## 技术栈

- **语言**: Python 3.8+
- **架构**: 分层架构（接口层、业务逻辑层、数据访问层、基础设施层）
- **存储**: 文件存储（JSON）
- **日志**: Python logging + 日志轮转
- **配置**: YAML配置文件

---

## 项目结构

```
agenttest/
├── src/                      # 源代码
│   ├── common/              # 公共组件
│   │   ├── types.py        # 数据模型定义
│   │   ├── exceptions.py   # 异常定义
│   │   ├── validator.py    # 数据校验器
│   │   └── utils.py        # 工具函数
│   ├── infrastructure/      # 基础设施层
│   │   ├── logger.py       # 日志管理器
│   │   ├── storage_adapter.py       # 存储适配器接口
│   │   ├── file_storage_adapter.py  # 文件存储实现
│   │   ├── config_validator.py      # 配置验证器
│   │   └── llm_client.py   # 大模型客户端
│   ├── repositories/        # 数据访问层
│   │   ├── user_repository.py    # 用户仓储
│   │   ├── log_repository.py     # 日志仓储
│   │   └── config_repository.py  # 配置仓储
│   ├── services/            # 业务逻辑层
│   │   ├── rule_engine.py      # 规则引擎
│   │   ├── user_service.py     # 用户管理服务
│   │   ├── batch_service.py    # 批量操作服务
│   │   ├── analysis_service.py # 智能分析服务
│   │   └── config_service.py   # 配置管理服务
│   ├── interface/           # 接口层
│   │   └── cli.py          # 命令行接口
│   └── main.py             # 主程序入口
├── tests/                   # 测试代码
├── config/                  # 配置文件
│   └── config.yaml         # 默认配置
├── data/                    # 数据存储目录
├── logs/                    # 日志目录
├── requirements.txt         # 核心依赖
├── requirements-dev.txt     # 开发依赖
├── 使用手册.md             # 详细使用手册
├── 后续开发者任务.md       # 待完成功能清单
└── README.md               # 本文档
```

---

## 快速开始

### 1. 环境准备

确保已安装 Python 3.8 或更高版本：

```bash
python --version
```

### 2. 安装依赖

```bash
# 安装核心依赖
pip install -r requirements.txt
```

### 3. 配置系统

配置文件位于 `config/config.yaml`，可根据需要修改：

```yaml
# 批量操作配置
max_batch_size: 1000

# 日志配置
log_level: "INFO"

# 存储配置
data_storage_type: "file"
data_file_path: "./data/users.json"

# 大模型配置（可选）
enable_llm_integration: false
```

### 4. 启动系统

```bash
# 查看帮助
python -m agenttest --help

# 或使用主程序
python src/main.py --help
```

---

## 基本使用示例

### 创建用户

```bash
python -m agenttest create --username "张三" --email "zhangsan@example.com" --phone "13800138000"
```

### 查询用户

```bash
python -m agenttest get <user_id>
```

### 更新用户

```bash
python -m agenttest update <user_id> --username "新名字" --status inactive
```

### 删除用户

```bash
python -m agenttest delete <user_id>
```

### 查询用户列表

```bash
python -m agenttest list --status active --page 1 --page-size 20
```

### 批量导入

```bash
# JSON格式
python -m agenttest batch-create --file users.json --format json

# CSV格式
python -m agenttest batch-create --file users.csv --format csv
```

### 统计分析

```bash
python -m agenttest stats
```

### 智能分析

```bash
python -m agenttest analyze --type anomalies
```

---

## 文档链接

- **使用手册**: [使用手册.md](./使用手册.md) - 详细的安装、配置和使用说明
- **开发者任务**: [后续开发者任务.md](./后续开发者任务.md) - 待完成功能和扩展指南

---

## 系统特性

### 🎯 类型安全
使用Python类型注解，保证类型安全，提高代码可维护性。

### 🔌 可扩展架构
分层架构设计，支持自定义存储适配器、大模型客户端等扩展。

### 🛡️ 降级策略
大模型API不可用时自动降级为本地统计分析，保证系统可用性。

### 📝 操作审计
完整的操作日志记录，支持审计和追溯。

### 🔒 数据脱敏
敏感信息自动脱敏保护。

### ⚡ 性能优化
- 批量操作优化
- 文件锁机制
- 日志轮转

---

## 配置大模型API（可选）

系统预留了大模型API接口，可根据需要配置：

### OpenAI配置

```yaml
enable_llm_integration: true
llm_api_config:
  provider: "openai"
  api_key: "your-api-key"
  api_endpoint: "https://api.openai.com/v1"
  model: "gpt-3.5-turbo"
```

### 华为云盘古配置

```yaml
enable_llm_integration: true
llm_api_config:
  provider: "pangu"
  api_key: "your-api-key"
  api_endpoint: "your-endpoint"
  model: "pangu-model"
```

**注意**: 当前版本大模型客户端为预留接口，需开发者自行实现具体调用逻辑。详见[后续开发者任务.md](./后续开发者任务.md)。

---

## 开发指南

### 运行测试

```bash
# 安装开发依赖
pip install -r requirements-dev.txt

# 运行测试
pytest tests/

# 生成覆盖率报告
pytest --cov=src tests/
```

### 代码风格

```bash
# 代码格式化
black src/

# 代码检查
flake8 src/

# 类型检查
mypy src/
```

---

## 贡献指南

欢迎贡献代码、报告问题或提出建议！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

---

## 许可证

本项目采用 MIT 许可证。

---

## 更新日志

### v1.0.0 (2026-05-14)

**首次发布**

- ✅ 完整的用户管理功能
- ✅ 批量操作支持
- ✅ 智能分析功能
- ✅ 配置管理系统
- ✅ 命令行接口
- ✅ 操作日志记录
- ✅ 大模型API预留接口

---

**开发者**: 华为云码道（CodeArts）代码智能体  
**版本**: v1.0.0  
**更新日期**: 2026-05-14
