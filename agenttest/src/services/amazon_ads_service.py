"""Amazon Ads integration service."""
from __future__ import annotations

import os
from typing import Any, Dict, List, Optional

from common.ad_types import AdReportRecord
from common.types import ErrorCode, Result, SystemConfig
from infrastructure.amazon_ads_client import AmazonAdsClient, AmazonAdsClientError, AmazonAdsCredentials
from infrastructure.logger import Logger
from repositories.ad_report_repository import AdReportRepository


class AmazonAdsService:
    """Fetches real campaign and report data from Amazon Ads."""

    DEFAULT_SEARCH_TERM_COLUMNS = [
        "date",
        "campaignId",
        "campaignName",
        "adGroupId",
        "adGroupName",
        "searchTerm",
        "keyword",
        "keywordId",
        "keywordType",
        "matchType",
        "impressions",
        "clicks",
        "cost",
        "sales7d",
        "sales14d",
        "purchases7d",
        "purchases14d",
        "acosClicks7d",
        "acosClicks14d",
        "roasClicks7d",
        "roasClicks14d",
    ]

    DEFAULT_CAMPAIGN_COLUMNS = [
        "date",
        "campaignId",
        "campaignName",
        "impressions",
        "clicks",
        "cost",
        "sales7d",
        "sales14d",
        "purchases7d",
        "purchases14d",
        "campaignStatus",
    ]

    def __init__(self, config: SystemConfig, ad_report_repository: AdReportRepository, logger: Logger):
        self.config = config
        self.ad_report_repository = ad_report_repository
        self.logger = logger

    def test_connection(self) -> Result[Dict[str, Any]]:
        try:
            client = self._build_client()
            token = client.get_access_token()
            profiles = client.list_profiles(
                access_level=self._config().get("access_level", "view"),
                api_program=self._config().get("api_program", "report"),
            )
            return Result.ok(
                {
                    "connected": True,
                    "region": client.credentials.region,
                    "access_token_preview": token[:12] + "...",
                    "profile_count": len(profiles),
                    "profiles": profiles,
                }
            )
        except AmazonAdsClientError as e:
            return Result.error(ErrorCode.LLM_API_ERROR, str(e))
        except Exception as e:
            return Result.error(ErrorCode.OPERATION_FAILED, str(e))

    def list_profiles(self) -> Result[List[Dict[str, Any]]]:
        try:
            client = self._build_client()
            profiles = client.list_profiles(
                access_level=self._config().get("access_level", "view"),
                api_program=self._config().get("api_program", "report"),
            )
            return Result.ok(profiles)
        except AmazonAdsClientError as e:
            return Result.error(ErrorCode.OPERATION_FAILED, str(e))

    def list_sp_campaigns(self, profile_id: Optional[str] = None) -> Result[Dict[str, Any]]:
        try:
            client = self._build_client()
            resolved_profile_id = str(profile_id or self._config().get("profile_id", "")).strip()
            if not resolved_profile_id:
                return Result.error(ErrorCode.VALIDATION_ERROR, "Amazon Ads profile_id is required")
            data = client.list_sp_campaigns(resolved_profile_id, state_filter=["ENABLED", "PAUSED"])
            return Result.ok(data)
        except AmazonAdsClientError as e:
            return Result.error(ErrorCode.OPERATION_FAILED, str(e))

    def fetch_sp_search_term_report(
        self,
        *,
        profile_id: Optional[str],
        start_date: str,
        end_date: str,
    ) -> Result[Dict[str, Any]]:
        try:
            client = self._build_client()
            resolved_profile_id = str(profile_id or self._config().get("profile_id", "")).strip()
            if not resolved_profile_id:
                return Result.error(ErrorCode.VALIDATION_ERROR, "Amazon Ads profile_id is required")

            created = client.create_report(
                resolved_profile_id,
                start_date=start_date,
                end_date=end_date,
                report_type_id="spSearchTerm",
                columns=self.DEFAULT_SEARCH_TERM_COLUMNS,
                group_by=["searchTerm"],
                name=f"sp-search-term-{start_date}-{end_date}",
            )
            report_id = created.get("reportId") or created.get("report_id")
            if not report_id:
                return Result.error(ErrorCode.OPERATION_FAILED, f"Amazon Ads did not return a report id: {created}")

            report_status = client.wait_for_report(str(report_id), resolved_profile_id)
            location = (
                report_status.get("url")
                or report_status.get("location")
                or (report_status.get("urlExpiresAt") and report_status.get("url"))
            )
            if not location and isinstance(report_status.get("location"), dict):
                location = report_status["location"].get("url")
            if not location:
                url_obj = report_status.get("file") or {}
                location = url_obj.get("url") if isinstance(url_obj, dict) else None
            if not location:
                return Result.error(ErrorCode.OPERATION_FAILED, f"Amazon Ads report completed without a download URL: {report_status}")

            rows = client.download_report(location)
            return Result.ok({"report_id": str(report_id), "status": report_status, "rows": rows})
        except AmazonAdsClientError as e:
            return Result.error(ErrorCode.OPERATION_FAILED, str(e))

    def fetch_sp_campaign_report(
        self,
        *,
        profile_id: Optional[str],
        start_date: str,
        end_date: str,
    ) -> Result[Dict[str, Any]]:
        try:
            client = self._build_client()
            resolved_profile_id = str(profile_id or self._config().get("profile_id", "")).strip()
            if not resolved_profile_id:
                return Result.error(ErrorCode.VALIDATION_ERROR, "Amazon Ads profile_id is required")

            created = client.create_report(
                resolved_profile_id,
                start_date=start_date,
                end_date=end_date,
                report_type_id="spCampaigns",
                columns=self.DEFAULT_CAMPAIGN_COLUMNS,
                group_by=["campaign"],
                name=f"sp-campaigns-{start_date}-{end_date}",
            )
            report_id = created.get("reportId") or created.get("report_id")
            if not report_id:
                return Result.error(ErrorCode.OPERATION_FAILED, f"Amazon Ads did not return a report id: {created}")

            report_status = client.wait_for_report(str(report_id), resolved_profile_id)
            location = report_status.get("url") or report_status.get("location")
            if not location and isinstance(report_status.get("location"), dict):
                location = report_status["location"].get("url")
            if not location:
                url_obj = report_status.get("file") or {}
                location = url_obj.get("url") if isinstance(url_obj, dict) else None
            if not location:
                return Result.error(ErrorCode.OPERATION_FAILED, f"Amazon Ads report completed without a download URL: {report_status}")

            rows = client.download_report(location)
            return Result.ok({"report_id": str(report_id), "status": report_status, "rows": rows})
        except AmazonAdsClientError as e:
            return Result.error(ErrorCode.OPERATION_FAILED, str(e))

    def sync_campaign_report_to_local(
        self,
        *,
        profile_id: Optional[str],
        start_date: str,
        end_date: str,
    ) -> Result[Dict[str, Any]]:
        report_result = self.fetch_sp_campaign_report(profile_id=profile_id, start_date=start_date, end_date=end_date)
        if not report_result.success:
            return Result.error(report_result.error_code, report_result.error_message)

        rows = report_result.data.get("rows", [])
        imported = 0
        for row in rows:
            record = AdReportRecord(
                campaign_id=str(row.get("campaignId", "")),
                campaign_name=str(row.get("campaignName", "")),
                date=str(row.get("date") or end_date),
                impressions=int(float(row.get("impressions", 0) or 0)),
                clicks=int(float(row.get("clicks", 0) or 0)),
                cost=float(row.get("cost", 0) or 0.0),
                orders=int(float(row.get("purchases14d", row.get("purchases7d", 0)) or 0)),
                sales=float(row.get("sales14d", row.get("sales7d", 0)) or 0.0),
                status=str(row.get("campaignStatus", "enabled")).lower(),
                tags=["amazon_ads", "sponsored_products"],
                metadata={
                    "source": "amazon_ads_api",
                    "profile_id": str(profile_id or self._config().get("profile_id", "")),
                    "raw_row": row,
                },
            )
            self.ad_report_repository.save(record)
            imported += 1

        return Result.ok(
            {
                "imported_campaign_rows": imported,
                "report_id": report_result.data.get("report_id"),
                "start_date": start_date,
                "end_date": end_date,
            }
        )

    def _build_client(self) -> AmazonAdsClient:
        cfg = self._config()
        credentials = AmazonAdsCredentials(
            client_id=self._env_or_cfg("AMAZON_ADS_CLIENT_ID", cfg.get("client_id", "")),
            client_secret=self._env_or_cfg("AMAZON_ADS_CLIENT_SECRET", cfg.get("client_secret", "")),
            refresh_token=self._env_or_cfg("AMAZON_ADS_REFRESH_TOKEN", cfg.get("refresh_token", "")),
            region=self._env_or_cfg("AMAZON_ADS_REGION", cfg.get("region", "na")),
        )
        return AmazonAdsClient(credentials)

    def _config(self) -> Dict[str, Any]:
        return self.config.amazon_ads_config or {}

    def _env_or_cfg(self, env_name: str, fallback: str) -> str:
        value = os.environ.get(env_name)
        return value if value is not None and value != "" else fallback
