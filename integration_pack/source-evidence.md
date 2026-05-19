# 已确认来源证据

## Wimoor ERP

Wimoor 官方后台结构文档确认：

- Wimoor 是 Spring Boot + Spring Cloud + Nacos + Seata + Gateway 架构。
- 持久层使用 MyBatis / MyBatis Plus。
- 前端使用 Vue3 + Element Plus。
- 广告模块为 `wimoor-amazon-adv`，功能是亚马逊广告管理。
- `wimoor-amazon-adv` 下含 `amazon-adv-api` 与 `amazon-adv-boot`。
- 数据库按业务拆分，其中广告库为 `db_amazon_adv`。

Wimoor 广告统计文档确认：

- 前端主入口：`wimoor-ui/src/views/amazon/advertisement/overview/index.vue`
- 广告统计组件：`overview/components/adStatistics.vue`
- 漏斗分析组件：`overview/components/adFunnel.vue`
- ROAS 排名组件：`overview/components/roasRank.vue`
- 指标详情组件：`overview/components/indicator_detail.vue`
- 指标设置组件：`overview/components/indicator.vue`
- 后端报表控制器：`AdvertReportController.java`
- 后端广告管理控制器：`AdvertManagerController.java`
- 汇总服务：`AmzAdvSumServiceImpl`
- 商品广告汇总服务：`IAmzAdvSumProductAdsService`
- 广告报表汇总服务：`IAmazonReportAdvSummaryService`
- 核心接口包括 `/api/v1/advSummary`、`/api/v1/advSummary/warning`、`/api/v1/advReport/getsumproduct`、`/api/v1/advReport/getmonthsum`。

## CopilotKit

CopilotKit 仓库与官方页面确认：

- CopilotKit 用于构建 agent-native 应用、Generative UI、共享状态和 human-in-the-loop 工作流。
- CopilotKit 是 AG-UI Protocol 背后的项目方。
- AG-UI 是 agent 与用户界面之间的双向事件连接层。
- AG-UI 支持 shared state、tool-based GenUI、agentic chat、human in the loop、agentic GenUI 等模式。

## 参考链接

- Wimoor GitHub: https://github.com/wimoor-erp/wimoor
- Wimoor 后台结构说明: https://wiki.wimoor.com/books/0584c/page/a8abb
- Wimoor 广告统计说明: https://wiki.wimoor.com/books/d9fc5/page/8e296
- CopilotKit GitHub: https://github.com/CopilotKit/CopilotKit
- CopilotKit AG-UI: https://www.copilotkit.ai/ag-ui
- AG-UI 文档: https://docs.ag-ui.com

