"""Minimal Amazon Ads API client."""
from __future__ import annotations

import gzip
import io
import json
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from urllib import error, parse, request


class AmazonAdsClientError(Exception):
    """Raised when the Amazon Ads API returns an error."""


@dataclass
class AmazonAdsCredentials:
    client_id: str
    client_secret: str
    refresh_token: str
    region: str = "na"


class AmazonAdsClient:
    TOKEN_URL = "https://api.amazon.com/auth/o2/token"
    REGION_BASE_URLS = {
        "na": "https://advertising-api.amazon.com",
        "eu": "https://advertising-api-eu.amazon.com",
        "fe": "https://advertising-api-fe.amazon.com",
    }

    def __init__(self, credentials: AmazonAdsCredentials, timeout: int = 30):
        self.credentials = credentials
        self.timeout = timeout
        self._access_token: Optional[str] = None
        self._access_token_expires_at: float = 0.0

    @property
    def base_url(self) -> str:
        return self.REGION_BASE_URLS.get(self.credentials.region.lower(), self.REGION_BASE_URLS["na"])

    def validate_credentials(self) -> None:
        missing = []
        if not self.credentials.client_id:
            missing.append("client_id")
        if not self.credentials.client_secret:
            missing.append("client_secret")
        if not self.credentials.refresh_token:
            missing.append("refresh_token")
        if missing:
            raise AmazonAdsClientError(f"Missing Amazon Ads credentials: {', '.join(missing)}")

    def get_access_token(self, force_refresh: bool = False) -> str:
        self.validate_credentials()
        if not force_refresh and self._access_token and time.time() < self._access_token_expires_at - 60:
            return self._access_token

        payload = parse.urlencode(
            {
                "grant_type": "refresh_token",
                "refresh_token": self.credentials.refresh_token,
                "client_id": self.credentials.client_id,
                "client_secret": self.credentials.client_secret,
            }
        ).encode("utf-8")
        req = request.Request(self.TOKEN_URL, data=payload, method="POST")
        req.add_header("Content-Type", "application/x-www-form-urlencoded;charset=UTF-8")
        data = self._load_json(req)
        self._access_token = data["access_token"]
        expires_in = int(data.get("expires_in", 3600))
        self._access_token_expires_at = time.time() + expires_in
        return self._access_token

    def list_profiles(self, access_level: str = "view", api_program: str = "report") -> List[Dict[str, Any]]:
        query = parse.urlencode({"accessLevel": access_level, "apiProgram": api_program})
        return self._api_request("GET", f"/v2/profiles?{query}")

    def list_sp_campaigns(self, profile_id: str, state_filter: Optional[List[str]] = None) -> Dict[str, Any]:
        body: Dict[str, Any] = {}
        if state_filter:
            body["stateFilter"] = {"include": state_filter}
        return self._api_request(
            "POST",
            "/sp/campaigns/list",
            profile_id=profile_id,
            body=body if body else None,
            headers={
                "Accept": "application/vnd.spCampaign.v3+json",
                "Content-Type": "application/vnd.spCampaign.v3+json",
            },
        )

    def create_report(
        self,
        profile_id: str,
        *,
        start_date: str,
        end_date: str,
        report_type_id: str,
        columns: List[str],
        group_by: List[str],
        ad_product: str = "SPONSORED_PRODUCTS",
        time_unit: str = "SUMMARY",
        filters: Optional[List[Dict[str, Any]]] = None,
        name: Optional[str] = None,
    ) -> Dict[str, Any]:
        body: Dict[str, Any] = {
            "name": name or f"{report_type_id}-{start_date}-{end_date}",
            "startDate": start_date,
            "endDate": end_date,
            "configuration": {
                "adProduct": ad_product,
                "groupBy": group_by,
                "columns": columns,
                "reportTypeId": report_type_id,
                "timeUnit": time_unit,
                "format": "GZIP_JSON",
            },
        }
        if filters:
            body["configuration"]["filters"] = filters

        return self._api_request(
            "POST",
            "/reporting/reports",
            profile_id=profile_id,
            body=body,
            headers={"Content-Type": "application/vnd.createasyncreportrequest.v3+json"},
        )

    def get_report(self, report_id: str, profile_id: str) -> Dict[str, Any]:
        return self._api_request("GET", f"/reporting/reports/{report_id}", profile_id=profile_id)

    def download_report(self, url: str) -> List[Dict[str, Any]]:
        req = request.Request(url, method="GET")
        with request.urlopen(req, timeout=self.timeout) as resp:
            raw = resp.read()
            encoding = resp.headers.get("Content-Encoding", "")

        if encoding.lower() == "gzip" or url.endswith(".gz"):
            raw = gzip.decompress(raw)

        text = raw.decode("utf-8")
        parsed = json.loads(text)
        if isinstance(parsed, list):
            return parsed
        if isinstance(parsed, dict) and "rows" in parsed and isinstance(parsed["rows"], list):
            return parsed["rows"]
        raise AmazonAdsClientError("Unexpected report payload format")

    def wait_for_report(
        self,
        report_id: str,
        profile_id: str,
        *,
        max_attempts: int = 12,
        poll_interval_seconds: int = 5,
    ) -> Dict[str, Any]:
        last_payload: Dict[str, Any] = {}
        for _ in range(max_attempts):
            last_payload = self.get_report(report_id, profile_id)
            status = str(last_payload.get("status", "")).upper()
            if status in {"COMPLETED", "SUCCESS"}:
                return last_payload
            if status in {"FAILURE", "FAILED", "CANCELLED"}:
                raise AmazonAdsClientError(f"Amazon Ads report failed with status: {status}")
            time.sleep(poll_interval_seconds)
        raise AmazonAdsClientError(f"Timed out waiting for report {report_id}: last status={last_payload.get('status')}")

    def _api_request(
        self,
        method: str,
        path: str,
        *,
        profile_id: Optional[str] = None,
        body: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Any:
        access_token = self.get_access_token()
        url = f"{self.base_url}{path}"
        payload = json.dumps(body).encode("utf-8") if body is not None else None

        req = request.Request(url, data=payload, method=method)
        req.add_header("Amazon-Advertising-API-ClientId", self.credentials.client_id)
        req.add_header("Authorization", f"Bearer {access_token}")
        req.add_header("Accept", "application/json")
        if profile_id:
            req.add_header("Amazon-Advertising-API-Scope", str(profile_id))
        if body is not None and not headers:
            req.add_header("Content-Type", "application/json")
        for key, value in (headers or {}).items():
            req.add_header(key, value)

        return self._load_json(req)

    def _load_json(self, req: request.Request) -> Any:
        try:
            with request.urlopen(req, timeout=self.timeout) as resp:
                payload = resp.read()
                content_encoding = resp.headers.get("Content-Encoding", "")
                if content_encoding.lower() == "gzip":
                    payload = gzip.decompress(payload)
                text = payload.decode("utf-8")
                return json.loads(text) if text else {}
        except error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            raise AmazonAdsClientError(f"Amazon Ads API HTTP {e.code}: {body}")
        except error.URLError as e:
            raise AmazonAdsClientError(f"Amazon Ads API connection failed: {str(e)}")
        except json.JSONDecodeError as e:
            raise AmazonAdsClientError(f"Amazon Ads API returned invalid JSON: {str(e)}")
