"""Repository for ad agent workflow runs and action executions."""
from typing import Any, Dict, List, Optional

from common.ad_types import ActionExecutionRecord, AdAgentRunResult
from common.exceptions import StorageException
from infrastructure.storage_adapter import StorageAdapter


class AdWorkflowRepository:
    RUN_ENTITY_TYPE = "ad_agent_runs"
    EXECUTION_ENTITY_TYPE = "ad_action_executions"

    def __init__(self, storage_adapter: StorageAdapter):
        self.storage = storage_adapter

    def save_run(self, run: AdAgentRunResult) -> bool:
        try:
            return self.storage.save(self.RUN_ENTITY_TYPE, run.run_id, run.to_dict())
        except Exception as e:
            raise StorageException(f"Failed to save ad agent run: {str(e)}", e)

    def list_runs(self, filters: Optional[Dict[str, Any]] = None) -> List[AdAgentRunResult]:
        data_list = self.storage.find_all(self.RUN_ENTITY_TYPE, filters)
        return [AdAgentRunResult.from_dict(data) for data in data_list]

    def save_execution(self, execution: ActionExecutionRecord) -> bool:
        try:
            return self.storage.save(self.EXECUTION_ENTITY_TYPE, execution.execution_id, execution.to_dict())
        except Exception as e:
            raise StorageException(f"Failed to save action execution: {str(e)}", e)

    def list_executions(self, filters: Optional[Dict[str, Any]] = None) -> List[ActionExecutionRecord]:
        data_list = self.storage.find_all(self.EXECUTION_ENTITY_TYPE, filters)
        return [ActionExecutionRecord(**data) for data in data_list]
