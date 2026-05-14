"""Ad-domain models used by the starter agent workflow."""
from dataclasses import dataclass, field
from typing import Any, Dict, List


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
            tags=data.get("tags", []),
        )


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
        }


@dataclass
class OptimizationRecommendation:
    campaign_id: str
    campaign_name: str
    priority: str
    recommendation_type: str
    reason: str
    suggested_action: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "campaign_id": self.campaign_id,
            "campaign_name": self.campaign_name,
            "priority": self.priority,
            "recommendation_type": self.recommendation_type,
            "reason": self.reason,
            "suggested_action": self.suggested_action,
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
    objective: str
    workflow_status: str
    summary: Dict[str, Any]
    findings: List[str]
    recommendations: List[Dict[str, Any]]
    steps: List[AgentStep]
    prompt: str
    llm_output: str
    next_actions: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "objective": self.objective,
            "workflow_status": self.workflow_status,
            "summary": self.summary,
            "findings": self.findings,
            "recommendations": self.recommendations,
            "steps": [step.to_dict() for step in self.steps],
            "prompt": self.prompt,
            "llm_output": self.llm_output,
            "next_actions": self.next_actions,
        }
