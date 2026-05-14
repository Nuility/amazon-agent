"""Starter service for ad analysis and optimization recommendations."""
from typing import Any, Dict, List, Optional

from common.ad_types import (
    AdAgentRunResult,
    AdInsightSummary,
    AdReportRecord,
    AgentStep,
    OptimizationRecommendation,
)
from common.types import Result
from infrastructure.llm_client import LLMClient
from infrastructure.logger import Logger
from repositories.ad_report_repository import AdReportRepository
from services.prompt_engineering_service import PromptEngineeringService


class AdAgentService:
    """A first-step ad analysis service built on top of static report data."""

    def __init__(
        self,
        ad_report_repository: AdReportRepository,
        prompt_engineering_service: PromptEngineeringService,
        llm_client: LLMClient,
        logger: Logger,
    ):
        self.ad_report_repository = ad_report_repository
        self.prompt_engineering_service = prompt_engineering_service
        self.llm_client = llm_client
        self.logger = logger
        self._ensure_seed_data()

    def _ensure_seed_data(self) -> None:
        if self.ad_report_repository.count() > 0:
            return

        seed_records = [
            AdReportRecord(
                campaign_id="cmp-001",
                campaign_name="Sponsored Products - Wireless Charger",
                date="2026-05-13",
                impressions=12000,
                clicks=420,
                cost=315.4,
                orders=26,
                sales=1280.0,
                tags=["sponsored_products", "electronics"],
            ),
            AdReportRecord(
                campaign_id="cmp-002",
                campaign_name="Sponsored Products - Phone Case",
                date="2026-05-13",
                impressions=15800,
                clicks=390,
                cost=288.9,
                orders=11,
                sales=512.0,
                tags=["sponsored_products", "accessories"],
            ),
            AdReportRecord(
                campaign_id="cmp-003",
                campaign_name="Sponsored Brands - Desk Lamp",
                date="2026-05-13",
                impressions=8400,
                clicks=165,
                cost=142.7,
                orders=18,
                sales=940.0,
                tags=["sponsored_brands", "home"],
            ),
        ]

        self.ad_report_repository.save_many(seed_records)
        self.logger.info("Seeded starter ad report data for the ad agent workflow")

    def list_campaigns(self, filters: Optional[Dict[str, Any]] = None) -> Result[List[Dict[str, Any]]]:
        try:
            records = self.ad_report_repository.find_all(filters)
            return Result.ok([record.to_dict() for record in records])
        except Exception as e:
            return Result.error(error_code=getattr(e, "error_code", 1010), message=str(e))

    def get_summary(self, filters: Optional[Dict[str, Any]] = None) -> Result[AdInsightSummary]:
        try:
            records = self.ad_report_repository.find_all(filters)
            total_campaigns = len(records)
            total_impressions = sum(record.impressions for record in records)
            total_clicks = sum(record.clicks for record in records)
            total_cost = sum(record.cost for record in records)
            total_orders = sum(record.orders for record in records)
            total_sales = sum(record.sales for record in records)

            summary = AdInsightSummary(
                total_campaigns=total_campaigns,
                total_impressions=total_impressions,
                total_clicks=total_clicks,
                total_cost=round(total_cost, 2),
                total_orders=total_orders,
                total_sales=round(total_sales, 2),
                average_ctr=round(total_clicks / total_impressions, 4) if total_impressions else 0.0,
                average_cvr=round(total_orders / total_clicks, 4) if total_clicks else 0.0,
                average_acos=round(total_cost / total_sales, 4) if total_sales else 0.0,
                average_roas=round(total_sales / total_cost, 4) if total_cost else 0.0,
            )

            return Result.ok(summary)
        except Exception as e:
            return Result.error(error_code=getattr(e, "error_code", 1010), message=str(e))

    def get_recommendations(self, filters: Optional[Dict[str, Any]] = None) -> Result[List[Dict[str, Any]]]:
        try:
            records = self.ad_report_repository.find_all(filters)
            recommendations: List[OptimizationRecommendation] = []

            for record in records:
                if record.acos > 0.4:
                    recommendations.append(
                        OptimizationRecommendation(
                            campaign_id=record.campaign_id,
                            campaign_name=record.campaign_name,
                            priority="high",
                            recommendation_type="bid_control",
                            reason=f"ACOS is high at {record.acos:.2%}",
                            suggested_action="Lower bids on costly keywords and review wasted spend terms.",
                        )
                    )
                elif record.ctr < 0.02:
                    recommendations.append(
                        OptimizationRecommendation(
                            campaign_id=record.campaign_id,
                            campaign_name=record.campaign_name,
                            priority="medium",
                            recommendation_type="creative_refresh",
                            reason=f"CTR is low at {record.ctr:.2%}",
                            suggested_action="Refresh main image, title hooks, and keyword targeting.",
                        )
                    )
                elif record.roas > 4:
                    recommendations.append(
                        OptimizationRecommendation(
                            campaign_id=record.campaign_id,
                            campaign_name=record.campaign_name,
                            priority="medium",
                            recommendation_type="scale_budget",
                            reason=f"ROAS is strong at {record.roas:.2f}",
                            suggested_action="Consider increasing budget and expanding winning terms.",
                        )
                    )

            if not recommendations:
                recommendations.append(
                    OptimizationRecommendation(
                        campaign_id="portfolio",
                        campaign_name="All Campaigns",
                        priority="low",
                        recommendation_type="monitor",
                        reason="No major inefficiencies detected in the starter dataset.",
                        suggested_action="Keep monitoring and collect more data for deeper optimization.",
                    )
                )

            return Result.ok([item.to_dict() for item in recommendations])
        except Exception as e:
            return Result.error(error_code=getattr(e, "error_code", 1010), message=str(e))

    def build_analysis_prompt(
        self,
        objective: str,
        summary: Dict[str, Any],
        recommendations: List[Dict[str, Any]],
    ) -> str:
        recommendation_lines = []
        for item in recommendations[:5]:
            recommendation_lines.append(
                f"- {item['campaign_name']} | {item['recommendation_type']} | {item['reason']} | {item['suggested_action']}"
            )

        rec_block = "\n".join(recommendation_lines) if recommendation_lines else "- No recommendations yet."
        prompt_result = self.prompt_engineering_service.render_prompt(objective, summary, rec_block)
        if prompt_result.success and prompt_result.data:
            return prompt_result.data

        return (
            "You are an advertising optimization agent.\n"
            f"Objective: {objective}\n"
            f"Summary: {summary}\n"
            f"Recommendations: {rec_block}\n"
        )

    def run_agent_workflow(
        self,
        objective: str = "Improve campaign efficiency while protecting profitable growth.",
        filters: Optional[Dict[str, Any]] = None,
    ) -> Result[AdAgentRunResult]:
        try:
            steps = [
                AgentStep(name="load_reports", status="completed", detail="Loaded campaign performance records from local storage."),
            ]

            summary_result = self.get_summary(filters)
            if not summary_result.success or not summary_result.data:
                return Result.error(error_code=1010, message=summary_result.error_message or "Failed to build summary")

            summary_dict = summary_result.data.to_dict()
            steps.append(
                AgentStep(
                    name="aggregate_metrics",
                    status="completed",
                    detail=(
                        f"Aggregated {summary_dict['total_campaigns']} campaigns, spend {summary_dict['total_cost']}, "
                        f"sales {summary_dict['total_sales']}."
                    ),
                )
            )

            recommendations_result = self.get_recommendations(filters)
            if not recommendations_result.success:
                return Result.error(error_code=1010, message=recommendations_result.error_message or "Failed to build recommendations")

            recommendations = recommendations_result.data or []
            steps.append(
                AgentStep(
                    name="rule_screening",
                    status="completed",
                    detail=f"Generated {len(recommendations)} rule-based recommendations.",
                )
            )

            findings = self._build_findings(summary_dict, recommendations)
            prompt = self.build_analysis_prompt(objective, summary_dict, recommendations)

            try:
                llm_output = self.llm_client.call(prompt)
                steps.append(
                    AgentStep(
                        name="llm_reasoning",
                        status="completed",
                        detail="Generated an operator-facing assessment from the workflow prompt.",
                    )
                )
            except Exception as e:
                llm_output = self._fallback_agent_response(objective, findings, recommendations)
                steps.append(
                    AgentStep(
                        name="llm_reasoning",
                        status="fallback",
                        detail=f"LLM unavailable, used local fallback reasoning: {str(e)}",
                    )
                )

            next_actions = self._build_next_actions(recommendations)
            steps.append(
                AgentStep(
                    name="action_planning",
                    status="completed",
                    detail=f"Prepared {len(next_actions)} next actions for review.",
                )
            )

            result = AdAgentRunResult(
                objective=objective,
                workflow_status="completed",
                summary=summary_dict,
                findings=findings,
                recommendations=recommendations,
                steps=steps,
                prompt=prompt,
                llm_output=llm_output,
                next_actions=next_actions,
            )
            return Result.ok(result)
        except Exception as e:
            return Result.error(error_code=getattr(e, "error_code", 1010), message=str(e))

    def _build_findings(self, summary: Dict[str, Any], recommendations: List[Dict[str, Any]]) -> List[str]:
        findings = [
            f"Portfolio ROAS is {summary['average_roas']:.2f} with ACOS at {summary['average_acos']:.2%}.",
            f"Average CTR is {summary['average_ctr']:.2%} across {summary['total_campaigns']} campaigns.",
        ]

        high_priority = [item for item in recommendations if item.get("priority") == "high"]
        if high_priority:
            findings.append(f"There are {len(high_priority)} high-priority optimization items needing immediate attention.")

        scale_candidates = [item for item in recommendations if item.get("recommendation_type") == "scale_budget"]
        if scale_candidates:
            findings.append(f"{len(scale_candidates)} campaign(s) appear strong enough to consider scaling.")

        return findings

    def _build_next_actions(self, recommendations: List[Dict[str, Any]]) -> List[str]:
        actions = []
        for item in recommendations[:3]:
            actions.append(f"Review {item['campaign_name']}: {item['suggested_action']}")
        actions.append("Validate these actions against budget guardrails before any automated execution.")
        return actions

    def _fallback_agent_response(
        self,
        objective: str,
        findings: List[str],
        recommendations: List[Dict[str, Any]],
    ) -> str:
        headline = recommendations[0]["campaign_name"] if recommendations else "current portfolio"
        return (
            f"Objective: {objective}\n"
            f"Primary focus: {headline}\n"
            f"Key findings: {' '.join(findings[:2])}\n"
            "Recommendation: start with the highest-priority item and validate impact after one reporting cycle."
        )
