"""Ad analysis, recommendation, and closed-loop workflow service."""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import uuid4

from common.ad_types import (
    ActionExecutionRecord,
    AdAgentRunResult,
    AdInsightSummary,
    AdReportRecord,
    AgentStep,
    KeywordRankRecord,
    OptimizationRecommendation,
    SearchTermInsight,
)
from common.types import ErrorCode, Result
from infrastructure.llm_client import LLMClient
from infrastructure.logger import Logger
from repositories.ad_report_repository import AdReportRepository
from repositories.ad_workflow_repository import AdWorkflowRepository
from repositories.keyword_rank_repository import KeywordRankRepository
from services.prompt_engineering_service import PromptEngineeringService


class AdAgentService:
    """Service layer for Amazon ads analysis and optimization workflows."""

    def __init__(
        self,
        ad_report_repository: AdReportRepository,
        keyword_rank_repository: KeywordRankRepository,
        workflow_repository: AdWorkflowRepository,
        prompt_engineering_service: PromptEngineeringService,
        llm_client: LLMClient,
        logger: Logger,
    ):
        self.ad_report_repository = ad_report_repository
        self.keyword_rank_repository = keyword_rank_repository
        self.workflow_repository = workflow_repository
        self.prompt_engineering_service = prompt_engineering_service
        self.llm_client = llm_client
        self.logger = logger
        self._ensure_seed_data()

    def _ensure_seed_data(self) -> None:
        if self.ad_report_repository.count() == 0:
            seed_reports = [
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
            self.ad_report_repository.save_many(seed_reports)

        if self.keyword_rank_repository.count() == 0:
            seed_keywords = [
                KeywordRankRecord(
                    keyword="wireless charger",
                    asin="B0CHARGER1",
                    marketplace="US",
                    rank=11,
                    rank_change=4,
                    campaign_id="cmp-001",
                    campaign_name="Sponsored Products - Wireless Charger",
                    match_type="exact",
                    impressions=5200,
                    clicks=188,
                    cost=126.5,
                    sales=620.0,
                    conversions=13,
                    date="2026-05-13",
                ),
                KeywordRankRecord(
                    keyword="iphone case clear",
                    asin="B0CASE001",
                    marketplace="US",
                    rank=37,
                    rank_change=-6,
                    campaign_id="cmp-002",
                    campaign_name="Sponsored Products - Phone Case",
                    match_type="phrase",
                    impressions=6400,
                    clicks=121,
                    cost=118.4,
                    sales=142.0,
                    conversions=5,
                    date="2026-05-13",
                ),
                KeywordRankRecord(
                    keyword="desk lamp office",
                    asin="B0LAMP123",
                    marketplace="US",
                    rank=8,
                    rank_change=2,
                    campaign_id="cmp-003",
                    campaign_name="Sponsored Brands - Desk Lamp",
                    match_type="exact",
                    impressions=3100,
                    clicks=74,
                    cost=52.3,
                    sales=401.0,
                    conversions=9,
                    date="2026-05-13",
                ),
                KeywordRankRecord(
                    keyword="fast wireless charging stand",
                    asin="B0CHARGER1",
                    marketplace="US",
                    rank=29,
                    rank_change=-3,
                    campaign_id="cmp-001",
                    campaign_name="Sponsored Products - Wireless Charger",
                    match_type="broad",
                    impressions=4600,
                    clicks=89,
                    cost=74.1,
                    sales=133.0,
                    conversions=4,
                    date="2026-05-13",
                ),
            ]
            self.keyword_rank_repository.save_many(seed_keywords)

    def list_campaigns(self, filters: Optional[Dict[str, Any]] = None) -> Result[List[Dict[str, Any]]]:
        try:
            records = self.ad_report_repository.find_all(filters)
            return Result.ok([record.to_dict() for record in records])
        except Exception as e:
            return Result.error(getattr(e, "error_code", ErrorCode.OPERATION_FAILED.value), str(e))

    def import_campaign_reports(self, records: List[Dict[str, Any]]) -> Result[Dict[str, Any]]:
        try:
            imported = 0
            for item in records:
                self.ad_report_repository.save(AdReportRecord.from_dict(item))
                imported += 1
            return Result.ok({"imported": imported, "entity": "campaign_reports"})
        except Exception as e:
            return Result.error(getattr(e, "error_code", ErrorCode.OPERATION_FAILED.value), str(e))

    def import_keyword_rankings(self, records: List[Dict[str, Any]]) -> Result[Dict[str, Any]]:
        try:
            imported = 0
            for item in records:
                self.keyword_rank_repository.save(KeywordRankRecord.from_dict(item))
                imported += 1
            return Result.ok({"imported": imported, "entity": "keyword_rankings"})
        except Exception as e:
            return Result.error(getattr(e, "error_code", ErrorCode.OPERATION_FAILED.value), str(e))

    def get_keyword_rankings(self, filters: Optional[Dict[str, Any]] = None) -> Result[List[Dict[str, Any]]]:
        try:
            rankings = self.keyword_rank_repository.find_all(filters)
            rankings.sort(key=lambda item: (item.rank if item.rank > 0 else 999999, item.keyword))
            return Result.ok([item.to_dict() for item in rankings])
        except Exception as e:
            return Result.error(getattr(e, "error_code", ErrorCode.OPERATION_FAILED.value), str(e))

    def get_summary(self, filters: Optional[Dict[str, Any]] = None) -> Result[AdInsightSummary]:
        try:
            records = self.ad_report_repository.find_all(filters)
            keyword_rankings = self.keyword_rank_repository.find_all(filters)

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
                tracked_keywords=len(keyword_rankings),
                top_ranked_keywords=sum(1 for item in keyword_rankings if 0 < item.rank <= 10),
                low_rank_keywords=sum(1 for item in keyword_rankings if item.rank > 20),
            )
            return Result.ok(summary)
        except Exception as e:
            return Result.error(getattr(e, "error_code", ErrorCode.OPERATION_FAILED.value), str(e))

    def analyze_search_terms(self, filters: Optional[Dict[str, Any]] = None) -> Result[List[Dict[str, Any]]]:
        try:
            insights = [self._build_search_term_insight(item) for item in self.keyword_rank_repository.find_all(filters)]
            insights.sort(key=lambda item: item.opportunity_score, reverse=True)
            return Result.ok([item.to_dict() for item in insights])
        except Exception as e:
            return Result.error(getattr(e, "error_code", ErrorCode.OPERATION_FAILED.value), str(e))

    def get_recommendations(self, filters: Optional[Dict[str, Any]] = None) -> Result[List[Dict[str, Any]]]:
        try:
            recommendations: List[OptimizationRecommendation] = []
            insights_result = self.analyze_search_terms(filters)
            if not insights_result.success:
                return Result.error(insights_result.error_code, insights_result.error_message)

            for item in insights_result.data or []:
                priority = "low"
                recommendation_type = "monitor"
                reason = item["insight"]
                action = item["suggested_action"]
                impact = "Improve data quality and preserve account stability."
                guardrail = "Do not change budget by more than 15% per cycle."

                if item["acos"] > 0.45 and item["sales"] > 0:
                    priority = "high"
                    recommendation_type = "bid_down"
                    impact = "Reduce wasted ad spend on expensive terms."
                    guardrail = "Keep the term active if conversion count is still above 3."
                elif item["rank"] and item["rank"] > 20 and item["roas"] > 2.5:
                    priority = "high"
                    recommendation_type = "rank_boost"
                    impact = "Lift ranking on a proven converting term."
                    guardrail = "Increase bids gradually and watch CPC inflation."
                elif item["ctr"] < 0.012:
                    priority = "medium"
                    recommendation_type = "listing_refresh"
                    impact = "Improve click-through rate and traffic quality."
                    guardrail = "Coordinate creative changes with catalog owners."
                elif item["roas"] > 4 and item["rank"] and item["rank"] <= 10:
                    priority = "medium"
                    recommendation_type = "budget_scale"
                    impact = "Capture more profitable volume from a winning keyword."
                    guardrail = "Cap daily budget growth to 20%."

                recommendations.append(
                    OptimizationRecommendation(
                        recommendation_id=f"rec-{uuid4().hex[:10]}",
                        campaign_id=item["campaign_id"],
                        campaign_name=item["campaign_name"],
                        target_keyword=item["keyword"],
                        priority=priority,
                        recommendation_type=recommendation_type,
                        reason=reason,
                        suggested_action=action,
                        expected_impact=impact,
                        guardrail=guardrail,
                    )
                )

            if not recommendations:
                recommendations.append(
                    OptimizationRecommendation(
                        recommendation_id=f"rec-{uuid4().hex[:10]}",
                        campaign_id="portfolio",
                        campaign_name="All Campaigns",
                        target_keyword="",
                        priority="low",
                        recommendation_type="monitor",
                        reason="No immediate optimization opportunities were detected in the current dataset.",
                        suggested_action="Keep collecting data and re-run the workflow after the next reporting cycle.",
                        expected_impact="Maintain stability while waiting for a stronger signal.",
                        guardrail="Avoid changes without statistically meaningful data.",
                    )
                )

            recommendations.sort(key=lambda item: self._priority_weight(item.priority), reverse=True)
            return Result.ok([item.to_dict() for item in recommendations])
        except Exception as e:
            return Result.error(getattr(e, "error_code", ErrorCode.OPERATION_FAILED.value), str(e))

    def execute_recommendations(
        self,
        recommendations: List[Dict[str, Any]],
        dry_run: bool = True,
        limit: Optional[int] = None,
    ) -> Result[List[Dict[str, Any]]]:
        try:
            executions: List[ActionExecutionRecord] = []
            selected = recommendations[:limit] if limit else recommendations
            for item in selected:
                action_payload = {
                    "campaign_id": item.get("campaign_id"),
                    "keyword": item.get("target_keyword"),
                    "recommendation_type": item.get("recommendation_type"),
                    "suggested_action": item.get("suggested_action"),
                }
                message = "Dry-run execution completed. No external API was called."
                if not dry_run:
                    message = "Execution recorded. Connect Amazon Ads APIs here to apply the change for real."
                execution = ActionExecutionRecord(
                    execution_id=f"exe-{uuid4().hex[:10]}",
                    recommendation_id=item.get("recommendation_id", ""),
                    campaign_id=item.get("campaign_id", ""),
                    action_type=item.get("recommendation_type", "unknown"),
                    action_payload=action_payload,
                    dry_run=dry_run,
                    status="simulated" if dry_run else "recorded",
                    message=message,
                    executed_at=self._now_iso(),
                )
                self.workflow_repository.save_execution(execution)
                executions.append(execution)

            return Result.ok([item.to_dict() for item in executions])
        except Exception as e:
            return Result.error(getattr(e, "error_code", ErrorCode.OPERATION_FAILED.value), str(e))

    def list_workflow_runs(self, filters: Optional[Dict[str, Any]] = None) -> Result[List[Dict[str, Any]]]:
        try:
            runs = self.workflow_repository.list_runs(filters)
            runs.sort(key=lambda item: item.created_at, reverse=True)
            return Result.ok([item.to_dict() for item in runs])
        except Exception as e:
            return Result.error(getattr(e, "error_code", ErrorCode.OPERATION_FAILED.value), str(e))

    def list_action_executions(self, filters: Optional[Dict[str, Any]] = None) -> Result[List[Dict[str, Any]]]:
        try:
            items = self.workflow_repository.list_executions(filters)
            items.sort(key=lambda item: item.executed_at, reverse=True)
            return Result.ok([item.to_dict() for item in items])
        except Exception as e:
            return Result.error(getattr(e, "error_code", ErrorCode.OPERATION_FAILED.value), str(e))

    def build_analysis_prompt(
        self,
        objective: str,
        summary: Dict[str, Any],
        insights: List[Dict[str, Any]],
        recommendations: List[Dict[str, Any]],
    ) -> str:
        insight_lines = [
            f"- {item['keyword']} | rank {item['rank']} | acos {item['acos']:.2%} | roas {item['roas']:.2f} | {item['insight']}"
            for item in insights[:5]
        ]
        recommendation_lines = [
            f"- {item['campaign_name']} | {item['target_keyword']} | {item['recommendation_type']} | {item['suggested_action']}"
            for item in recommendations[:5]
        ]

        context_block = (
            "Search term insights:\n"
            + ("\n".join(insight_lines) if insight_lines else "- No search term insights.\n")
            + "\nRecommendations:\n"
            + ("\n".join(recommendation_lines) if recommendation_lines else "- No recommendations.")
        )
        prompt_result = self.prompt_engineering_service.render_prompt(objective, summary, context_block)
        if prompt_result.success and prompt_result.data:
            return prompt_result.data

        return (
            "You are an Amazon ads optimization agent.\n"
            f"Objective: {objective}\n"
            f"Summary: {summary}\n"
            f"{context_block}\n"
        )

    def run_agent_workflow(
        self,
        objective: str = "Improve campaign efficiency while protecting profitable growth.",
        filters: Optional[Dict[str, Any]] = None,
        auto_execute: bool = False,
        execution_limit: int = 3,
        dry_run: bool = True,
    ) -> Result[AdAgentRunResult]:
        try:
            run_id = f"run-{uuid4().hex[:10]}"
            filters = filters or {}
            steps = [
                AgentStep(name="load_reports", status="completed", detail="Loaded campaign reports and keyword ranking records."),
            ]

            summary_result = self.get_summary(filters)
            if not summary_result.success or not summary_result.data:
                return Result.error(ErrorCode.OPERATION_FAILED, summary_result.error_message or "Failed to build summary")
            summary_dict = summary_result.data.to_dict()
            steps.append(
                AgentStep(
                    name="aggregate_metrics",
                    status="completed",
                    detail=(
                        f"Aggregated {summary_dict['total_campaigns']} campaigns, "
                        f"{summary_dict['tracked_keywords']} tracked keywords, "
                        f"ROAS {summary_dict['average_roas']:.2f}."
                    ),
                )
            )

            insights_result = self.analyze_search_terms(filters)
            if not insights_result.success:
                return Result.error(ErrorCode.OPERATION_FAILED, insights_result.error_message or "Failed to build search term insights")
            insights = insights_result.data or []
            steps.append(
                AgentStep(
                    name="search_term_analysis",
                    status="completed",
                    detail=f"Built {len(insights)} keyword-level insights for ranking and efficiency analysis.",
                )
            )

            recommendations_result = self.get_recommendations(filters)
            if not recommendations_result.success:
                return Result.error(ErrorCode.OPERATION_FAILED, recommendations_result.error_message or "Failed to build recommendations")
            recommendations = recommendations_result.data or []
            steps.append(
                AgentStep(
                    name="recommendation_planning",
                    status="completed",
                    detail=f"Generated {len(recommendations)} optimization recommendations.",
                )
            )

            findings = self._build_findings(summary_dict, insights, recommendations)
            prompt = self.build_analysis_prompt(objective, summary_dict, insights, recommendations)

            try:
                llm_output = self.llm_client.call(prompt)
                steps.append(
                    AgentStep(
                        name="llm_reasoning",
                        status="completed",
                        detail="Generated a strategy narrative from the prompt workflow.",
                    )
                )
            except Exception as e:
                llm_output = self._fallback_agent_response(objective, findings, recommendations)
                steps.append(
                    AgentStep(
                        name="llm_reasoning",
                        status="fallback",
                        detail=f"LLM unavailable, used local reasoning fallback: {str(e)}",
                    )
                )

            executed_actions: List[Dict[str, Any]] = []
            if auto_execute:
                execution_result = self.execute_recommendations(recommendations, dry_run=dry_run, limit=execution_limit)
                if execution_result.success:
                    executed_actions = execution_result.data or []
                    steps.append(
                        AgentStep(
                            name="action_execution",
                            status="completed" if dry_run else "recorded",
                            detail=f"Executed {len(executed_actions)} action(s) in {'dry-run' if dry_run else 'recorded'} mode.",
                        )
                    )
                else:
                    steps.append(
                        AgentStep(
                            name="action_execution",
                            status="failed",
                            detail=execution_result.error_message or "Execution step failed.",
                        )
                    )
            else:
                steps.append(
                    AgentStep(
                        name="action_execution",
                        status="pending",
                        detail="Recommendations are ready for human approval or a later execution call.",
                    )
                )

            next_actions = self._build_next_actions(recommendations, auto_execute, dry_run)
            result = AdAgentRunResult(
                run_id=run_id,
                objective=objective,
                workflow_status="completed",
                summary=summary_dict,
                findings=findings,
                search_term_insights=insights,
                recommendations=recommendations,
                executed_actions=executed_actions,
                steps=steps,
                prompt=prompt,
                llm_output=llm_output,
                next_actions=next_actions,
                created_at=self._now_iso(),
                filters=filters,
            )
            self.workflow_repository.save_run(result)
            return Result.ok(result)
        except Exception as e:
            return Result.error(getattr(e, "error_code", ErrorCode.OPERATION_FAILED.value), str(e))

    def _build_search_term_insight(self, record: KeywordRankRecord) -> SearchTermInsight:
        opportunity_score = 0.0
        if record.rank > 0:
            opportunity_score += max(0, 35 - record.rank) * 2
        opportunity_score += min(record.roas, 8) * 8
        opportunity_score += max(record.rank_change, 0) * 3
        opportunity_score -= max(record.acos - 0.35, 0) * 100

        risk_level = "low"
        insight = "Stable performance. Keep monitoring."
        action = "Maintain current bidding and monitor for more data."

        if record.acos > 0.45 and record.sales > 0:
            risk_level = "high"
            insight = "This keyword is converting, but efficiency is weak and spend is too expensive."
            action = "Lower bids 8-12%, review the search term report, and add negatives for waste."
        elif record.rank > 20 and record.roas > 2.5:
            risk_level = "medium"
            insight = "This keyword has healthy returns but weak ranking, so it may be under-supported."
            action = "Increase bid carefully, move the term into exact match, and protect daily budget coverage."
        elif record.ctr < 0.012:
            risk_level = "medium"
            insight = "CTR is weak, which suggests targeting or listing message mismatch."
            action = "Refresh listing hooks, tighten targeting, and split match types for cleaner traffic."
        elif record.rank <= 10 and record.roas > 4:
            risk_level = "low"
            insight = "Strong ranking and strong returns indicate a scale opportunity."
            action = "Scale budget gradually and expand closely related winning terms."

        return SearchTermInsight(
            keyword=record.keyword,
            campaign_id=record.campaign_id,
            campaign_name=record.campaign_name,
            rank=record.rank,
            rank_change=record.rank_change,
            impressions=record.impressions,
            clicks=record.clicks,
            cost=round(record.cost, 2),
            sales=round(record.sales, 2),
            conversions=record.conversions,
            ctr=round(record.ctr, 4),
            cpc=round(record.cpc, 4),
            acos=round(record.acos, 4),
            roas=round(record.roas, 4),
            opportunity_score=round(opportunity_score, 2),
            risk_level=risk_level,
            insight=insight,
            suggested_action=action,
        )

    def _build_findings(
        self,
        summary: Dict[str, Any],
        insights: List[Dict[str, Any]],
        recommendations: List[Dict[str, Any]],
    ) -> List[str]:
        findings = [
            f"Portfolio ROAS is {summary['average_roas']:.2f} and ACOS is {summary['average_acos']:.2%}.",
            f"The system is tracking {summary['tracked_keywords']} keywords, including {summary['top_ranked_keywords']} in the top 10.",
        ]
        if insights:
            top = insights[0]
            findings.append(
                f"Top keyword opportunity is '{top['keyword']}' in {top['campaign_name']} with score {top['opportunity_score']}."
            )
        high_priority = [item for item in recommendations if item.get("priority") == "high"]
        if high_priority:
            findings.append(f"There are {len(high_priority)} high-priority optimization actions ready for review.")
        return findings

    def _build_next_actions(
        self,
        recommendations: List[Dict[str, Any]],
        auto_execute: bool,
        dry_run: bool,
    ) -> List[str]:
        actions = [f"Review {item['campaign_name']} / {item['target_keyword']}: {item['suggested_action']}" for item in recommendations[:3]]
        if auto_execute:
            mode = "dry-run" if dry_run else "recorded"
            actions.append(f"Validate the {mode} execution results before promoting any rule to live Amazon Ads automation.")
        else:
            actions.append("Approve the top recommendations, then call the execution endpoint to continue the loop.")
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
            f"Key findings: {' '.join(findings[:3])}\n"
            "Recommendation: start with the highest-priority items, verify guardrails, and re-run after the next data refresh."
        )

    def _priority_weight(self, priority: str) -> int:
        return {"high": 3, "medium": 2, "low": 1}.get(priority, 0)

    def _now_iso(self) -> str:
        return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
