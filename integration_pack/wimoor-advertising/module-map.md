# Wimoor 广告投放模块地图

## 模块边界

广告投放后端核心位于 Wimoor ERP 的 `wimoor-amazon-adv` 模块。它是本整合包的 ERP 主体来源。

建议提取边界：

- 广告活动、广告组、广告、关键词、投放、否定关键词、预算、竞价策略等投放管理能力。
- 广告报表、广告概览、店铺广告统计、汇总指标、趋势数据。
- Amazon Advertising API 调用、授权、profile、站点/店铺上下文。
- 广告模块运行所需的公共实体、工具、权限注解、分页、异常、MyBatis 映射、配置。

不建议纳入：

- 订单、采购、库存、财务、物流等 ERP 非广告域。
- Wimoor 完整后台框架和全部菜单。
- 与广告无关的 Amazon 商品、仓储和运营模块，除非某个广告接口明确依赖。

## 后端结构

可确认的后端模块结构：

```text
wimoor-amazon-adv/
├─ amazon-adv-api/
│  └─ 广告领域接口、实体、Mapper、Service API
└─ amazon-adv-boot/
   └─ 广告模块启动实现、Controller、Service 实现、Amazon Ads API 调用
```

`amazon-adv-api` 更适合作为后续 agent 项目的“领域模型来源”，`amazon-adv-boot` 更适合作为“业务行为与接口来源”。

## 已确认的广告统计链路

前端入口：

- `wimoor-ui/src/views/amazon/advertisement/overview/index.vue`
- `overview/components/adStatistics.vue`
- `overview/components/adFunnel.vue`
- `overview/components/roasRank.vue`
- `overview/components/indicator_detail.vue`
- `overview/components/indicator.vue`

后端入口：

- `AdvertReportController.java`：广告报表控制，包含 `getSumProductAction()`、`getMonthSumAction()` 等。
- `AdvertManagerController.java`：广告管理控制。
- `IAmzAdvSumProductAdsService`：商品广告汇总，包含 `getSumProduct()`、`getMonthSumProduct()`、`getDaysSumProduct()`。
- `IAmazonReportAdvSummaryService`：广告报表汇总，包含 `findAdvert()`。

已确认接口：

- `GET /api/v1/advSummary`
- `GET /api/v1/advSummary/warning`
- `POST /api/v1/advReport/getsumproduct`
- `POST /api/v1/advReport/getmonthsum`

## 需要保留的能力分组

- **投放管理**：campaign、ad group、product ad、keyword、targeting、negative keyword、bid、budget、portfolio。
- **报表分析**：广告概览、店铺汇总、广告活动表现、关键词表现、搜索词表现、ASIN/商品表现。
- **优化动作**：暂停/启用、预算调整、竞价调整、关键词新增/否定、投放对象新增/排除。
- **上下文依赖**：店铺、站点、profile、marketplace、用户权限、广告授权 token。

## 与 agent 的关系

Wimoor 广告模块适合沉淀为 agent 的“工具层”和“业务数据层”：

- 查询工具：获取广告账户、活动列表、报表、关键词表现、趋势。
- 分析工具：计算 ACOS、ROAS、CTR、CPC、CVR、花费占比、异常波动。
- 执行动作：创建或修改广告活动、调预算、调竞价、暂停低效关键词。
- 审批动作：高风险操作先进入 CopilotKit/AG-UI 的人类确认流程。
