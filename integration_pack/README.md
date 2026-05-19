# 广告投放 Agent 整合包说明

## 这个整合包的意义

本整合包把两个开源项目中对“广告投放 Agent”有价值的部分先做成独立资料与接口包，后续可以再融合进你的 agent 项目，而不用一开始就把两个大型系统整体搬进去。

- **Wimoor ERP** 提供亚马逊广告投放业务域：广告活动、广告组、关键词、投放、预算、竞价、报表、汇总统计、店铺/权限/数据源等 ERP 侧上下文。
- **CopilotKit** 提供 agent 前端交互与人机协同模式：聊天侧栏、前端 action、共享状态、生成式 UI、人类确认、AG-UI 风格事件流。
- **本包的定位** 是“可接入代码包的前置整合层”：先明确模块边界、接口契约、数据对象和后续融合路径，避免后续直接合并时把 ERP 全量依赖、UI monorepo 或无关业务一起卷入。

## 当前包内容

```text
integration_pack/
├─ README.md
├─ SOURCES.md
├─ source-evidence.md
├─ fetch_sources.ps1
├─ wimoor-advertising/
│  ├─ module-map.md
│  ├─ source-manifest.yaml
│  └─ api-contract-notes.md
├─ copilotkit-agent-ui/
│  ├─ integration-notes.md
│  └─ source-manifest.yaml
├─ contracts/
│  ├─ advertising-agent-contract.yaml
│  └─ copilotkit-ui-events.yaml
└─ handoff/
   └─ agent-fusion-blueprint.md
```

## 整合原则

- ERP 只取广告投放闭包，不引入订单、采购、仓储、财务等非广告模块。
- 广告模块以 `wimoor-amazon-adv` 为后端主来源，保留其运行所需的公共模型、权限、店铺、配置、Amazon SP/API 与广告 API 依赖说明。
- CopilotKit 不整包迁入，只吸收 agent UI 和交互协议思想，后续按目标项目技术栈选择 React 组件或协议适配。
- 先沉淀跨系统接口契约，再决定 Java 服务、Python agent、前端 UI 之间的具体部署方式。

## 重要限制

当前会话的命令行网络仍无法直连 GitHub/Gitee，因此未能完整克隆两个仓库。这个包基于可访问的公开仓库页面、官方/项目文档和当前工作区已有 agent 结构整理，保留了待完整拉取源码后的清单和落点。后续网络可用时，运行 `fetch_sources.ps1` 即可把源码快照补齐到本包。
