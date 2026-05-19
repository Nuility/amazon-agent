# CopilotKit 接入说明

## 采用方式

CopilotKit 不建议整仓复制到 agent 项目。它更适合作为前端交互层依赖：

- React 前端使用 CopilotKit 组件提供聊天侧栏或嵌入式 Copilot。
- 前端 action 暴露当前页面状态和可执行动作。
- 后端 agent 暴露广告查询、分析、优化建议和执行工具。
- 高风险广告操作通过人类确认流程落地。

## 对广告投放 Agent 的价值

- **上下文感知**：让 agent 知道当前页面选择的店铺、站点、广告活动、时间范围。
- **工具调用可视化**：把报表查询、预算调整、关键词筛选等工具调用过程展示给用户。
- **生成式 UI**：对广告诊断结果生成表格、卡片、建议列表或确认面板。
- **Human-in-the-loop**：预算、竞价、暂停广告等高风险动作执行前要求用户确认。
- **共享状态**：用户在广告页面筛选条件变化时，agent 同步更新分析上下文。

## 推荐融合层

```text
React UI
  └─ CopilotKit provider/sidebar/action
      └─ Agent API Gateway
          ├─ advertising read tools
          ├─ advertising analysis tools
          ├─ optimization proposal tools
          └─ guarded execution tools
              └─ Wimoor advertising service/API
```

## 不直接迁入的内容

- CopilotKit monorepo 的构建系统、示例全集、站点文档。
- 与广告投放无关的 demo。
- 与目标项目技术栈冲突的样式或路由结构。

