"""Repository for ad performance records."""
from typing import Any, Dict, List, Optional

from common.ad_types import AdReportRecord
from common.exceptions import StorageException
from infrastructure.storage_adapter import StorageAdapter


class AdReportRepository:
    ENTITY_TYPE = "ad_reports"

    def __init__(self, storage_adapter: StorageAdapter):
        self.storage = storage_adapter

    def save(self, record: AdReportRecord) -> bool:
        try:
            entity_id = f"{record.campaign_id}:{record.date}"
            return self.storage.save(self.ENTITY_TYPE, entity_id, record.to_dict())
        except Exception as e:
            raise StorageException(f"Failed to save ad report: {str(e)}", e)

    def save_many(self, records: List[AdReportRecord]) -> None:
        for record in records:
            self.save(record)

    def find_all(self, filters: Optional[Dict[str, Any]] = None) -> List[AdReportRecord]:
        data_list = self.storage.find_all(self.ENTITY_TYPE, filters)
        return [AdReportRecord.from_dict(data) for data in data_list]

    def count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        return self.storage.count(self.ENTITY_TYPE, filters)
