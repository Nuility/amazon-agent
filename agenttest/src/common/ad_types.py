"""Ad-domain models for the Amazon ads agent workflow."""
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class AdReportRecord:
    campaign_id: str
    campaign_name: str
    date: str
    impressions: int
    clicks: int
    cost: float
    orders: int
    sales: float
    status: str = "enabled"
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def ctr(self) -> float:
        return self.clicks / self.impressions if self.impressions > 0 else 0.0

    @property
    def cvr(self) -> float:
        return self.orders / self.clicks if self.clicks > 0 else 0.0

    @property
    def cpc(self) -> float:
        return self.cost / self.clicks if self.clicks > 0 else 0.0

    @property
    def acos(self) -> float:
        return self.cost / self.sales if self.sales > 0 else 0.0

    @property
    def roas(self) -> float:
        return self.sales / self.cost if self.cost > 0 else 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "campaign_id": self.campaign_id,
            "campaign_name": self.campaign_name,
            "date": self.date,
            "impressions": self.impressions,
            "clicks": self.clicks,
            "cost": self.cost,
            "orders": self.orders,
            "sales": self.sales,
            "status": self.status,
            "tags": self.tags,
            "metadata": self.metadata,
            "ctr": self.ctr,
            "cvr": self.cvr,
            "cpc": self.cpc,
            "acos": self.acos,
            "roas": self.roas,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AdReportRecord":
        return cls(
            campaign_id=data.get("campaign_id", ""),
            campaign_name=data.get("campaign_name", ""),
            date=data.get("date", ""),
            impressions=int(data.get("impressions", 0)),
            clicks=int(data.get("clicks", 0)),
            cost=float(data.get("cost", 0.0)),
            orders=int(data.get("orders", 0)),
            sales=float(data.get("sales", 0.0)),
            status=data.get("status", "enabled"),
            tags=list(data.get("tags", [])),
            metadata=dict(data.get("metadata", {})),
        )


@dataclass
class KeywordRankRecord:
    keyword: str
    asin: str
    marketplace: str
    rank: int
    rank_change: int = 0
    campaign_id: str = ""
    campaign_name: str = ""
    match_type: str = "unknown"
    impressions: int = 0
    clicks: int = 0
    cost: float = 0.0
    sales: float = 0.0
    conversions: int = 0
    date: str = ""
    status: str = "tracked"
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def ctr(self) -> float:
        return self.clicks / self.impressions if self.impressions > 0 else 0.0

    @property
    def cpc(self) -> float:
        return self.cost / self.clicks if self.clicks > 0 else 0.0

    @property
    def acos(self) -> float:
        return self.cost / self.sales if self.sales > 0 else 0.0

    @property
    def roas(self) -> float:
        return self.sales / self.cost if self.cost > 0 else 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "keyword": self.keyword,
            "asin": self.asin,
            "marketplace": self.marketplace,
            "rank": self.rank,
            "rank_change": self.rank_change,
            "campaign_id": self.campaign_id,
            "campaign_name": self.campaign_name,
            "match_type": self.match_type,
            "impressions": self.impressions,
            "clicks": self.clicks,
            "cost": self.cost,
            "sales": self.sales,
            "conversions": self.conversions,
            "date": self.date,
            "status": self.status,
            "metadata": self.metadata,
            "ctr": self.ctr,
            "cpc": self.cpc,
            "acos": self.acos,
            "roas": self.roas,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "KeywordRankRecord":
        return cls(
            keyword=data.get("keyword", ""),
            asin=data.get("asin", ""),
            marketplace=data.get("marketplace", ""),
            rank=int(data.get("rank", 0)),
            rank_change=int(data.get("rank_change", 0)),
            campaign_id=data.get("campaign_id", ""),
            campaign_name=data.get("campaign_name", ""),
            match_type=data.get("match_type", "unknown"),
            impressions=int(data.get("impressions", 0)),
            clicks=int(data.get("clicks", 0)),
            cost=float(data.get("cost", 0.0)),
            sales=float(data.get("sales", 0.0)),
            conversions=int(data.get("conversions", 0)),
            date=data.get("date", ""),
            status=data.get("status", "tracked"),
            metadata=dict(data.get("metadata", {})),
        )


@dataclass
class SearchTermInsight:
    keyword: str
    campaign_id: str
    campaign_name: str
    rank: Optional[int]
    rank_change: int
    impressions: int
    clicks: int
    cost: float
    sales: float
    conversions: int
    ctr: float
    cpc: float
    acos: float
    roas: float
    opportunity_score: float
    risk_level: str
    insight: str
    suggested_action: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "keyword": self.keyword,
            "campaign_id": self.campaign_id,
            "campaign_name": self.campaign_name,
            "rank": self.rank,
            "rank_change": self.rank_change,
            "impressions": self.impressions,
            "clicks": self.clicks,
            "cost": self.cost,
            "sales": self.sales,
            "conversions": self.conversions,
            "ctr": self.ctr,
            "cpc": self.cpc,
            "acos": self.acos,
            "roas": self.roas,
            "opportunity_score": self.opportunity_score,
            "risk_level": self.risk_level,
            "insight": self.insight,
            "suggested_action": self.suggested_action,
        }


@dataclass
class AdInsightSummary:
    total_campaigns: int
    total_impressions: int
    total_clicks: int
    total_cost: float
    total_orders: int
    total_sales: float
    average_ctr: float
    average_cvr: float
    average_acos: float
    average_roas: float
    tracked_keywords: int = 0
    top_ranked_keywords: int = 0
    low_rank_keywords: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_campaigns": self.total_campaigns,
            "total_impressions": self.total_impressions,
            "total_clicks": self.total_clicks,
            "total_cost": self.total_cost,
            "total_orders": self.total_orders,
            "total_sales": self.total_sales,
            "average_ctr": self.average_ctr,
            "average_cvr": self.average_cvr,
            "average_acos": self.average_acos,
            "average_roas": self.average_roas,
            "tracked_keywords": self.tracked_keywords,
            "top_ranked_keywords": self.top_ranked_keywords,
            "low_rank_keywords": self.low_rank_keywords,
        }


@dataclass
class OptimizationRecommendation:
    recommendation_id: str
    campaign_id: str
    campaign_name: str
    target_keyword: str
    priority: str
    recommendation_type: str
    reason: str
    suggested_action: str
    expected_impact: str
    guardrail: str
    status: str = "pending"
    source: str = "rule_engine"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "recommendation_id": self.recommendation_id,
            "campaign_id": self.campaign_id,
            "campaign_name": self.campaign_name,
            "target_keyword": self.target_keyword,
            "priority": self.priority,
            "recommendation_type": self.recommendation_type,
            "reason": self.reason,
            "suggested_action": self.suggested_action,
            "expected_impact": self.expected_impact,
            "guardrail": self.guardrail,
            "status": self.status,
            "source": self.source,
        }


@dataclass
class ActionExecutionRecord:
    execution_id: str
    recommendation_id: str
    campaign_id: str
    action_type: str
    action_payload: Dict[str, Any]
    dry_run: bool
    status: str
    message: str
    executed_at: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "execution_id": self.execution_id,
            "recommendation_id": self.recommendation_id,
            "campaign_id": self.campaign_id,
            "action_type": self.action_type,
            "action_payload": self.action_payload,
            "dry_run": self.dry_run,
            "status": self.status,
            "message": self.message,
            "executed_at": self.executed_at,
        }


@dataclass
class AgentStep:
    name: str
    status: str
    detail: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "status": self.status,
            "detail": self.detail,
        }


@dataclass
class AdAgentRunResult:
    run_id: str
    objective: str
    workflow_status: str
    summary: Dict[str, Any]
    findings: List[str]
    search_term_insights: List[Dict[str, Any]]
    recommendations: List[Dict[str, Any]]
    executed_actions: List[Dict[str, Any]]
    steps: List[AgentStep]
    prompt: str
    llm_output: str
    next_actions: List[str]
    created_at: str
    filters: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "run_id": self.run_id,
            "objective": self.objective,
            "workflow_status": self.workflow_status,
            "summary": self.summary,
            "findings": self.findings,
            "search_term_insights": self.search_term_insights,
            "recommendations": self.recommendations,
            "executed_actions": self.executed_actions,
            "steps": [step.to_dict() for step in self.steps],
            "prompt": self.prompt,
            "llm_output": self.llm_output,
            "next_actions": self.next_actions,
            "created_at": self.created_at,
            "filters": self.filters,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AdAgentRunResult":
        return cls(
            run_id=data.get("run_id", ""),
            objective=data.get("objective", ""),
            workflow_status=data.get("workflow_status", "unknown"),
            summary=dict(data.get("summary", {})),
            findings=list(data.get("findings", [])),
            search_term_insights=list(data.get("search_term_insights", [])),
            recommendations=list(data.get("recommendations", [])),
            executed_actions=list(data.get("executed_actions", [])),
            steps=[AgentStep(**step) for step in data.get("steps", [])],
            prompt=data.get("prompt", ""),
            llm_output=data.get("llm_output", ""),
            next_actions=list(data.get("next_actions", [])),
            created_at=data.get("created_at", ""),
            filters=dict(data.get("filters", {})),
        )
