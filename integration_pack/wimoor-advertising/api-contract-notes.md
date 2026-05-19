# Wimoor 广告接口契约笔记

## 推荐抽象方式

后续不要让 agent 直接理解 Wimoor 的全部 Controller 和数据库表。建议先包装成少量广告工具接口：

- `list_campaigns`：按店铺、站点、profile、状态、广告类型查询广告活动。
- `get_campaign_report`：查询活动、广告组、关键词或投放对象的表现数据。
- `get_account_summary`：获取广告账户概览、趋势和关键指标。
- `propose_optimization`：根据规则和模型生成优化建议。
- `apply_optimization`：执行预算、竞价、状态、关键词、投放等修改。

## 核心输入上下文

```yaml
advertising_context:
  tenant_id: string
  user_id: string
  shop_id: string
  marketplace_id: string
  profile_id: string
  timezone: string
```

## 核心指标

```yaml
metrics:
  impressions: integer
  clicks: integer
  spend: decimal
  sales: decimal
  orders: integer
  acos: decimal
  roas: decimal
  ctr: decimal
  cpc: decimal
  cvr: decimal
```

## 风险分级

- 低风险：只读报表、趋势分析、异常解释。
- 中风险：生成建议、批量筛选关键词、预算调整草案。
- 高风险：实际创建/修改/暂停广告活动、预算、关键词、投放对象。

高风险操作必须走确认流程，并记录操作人、旧值、新值、理由和回滚建议。

