"""Prompt template management for the starter ad agent."""
import json
import os
from typing import Any, Dict

from common.types import Result
from infrastructure.logger import Logger


DEFAULT_PROMPT_TEMPLATE = {
    "system_role": (
        "You are an advertising optimization agent. "
        "Your job is to review campaign performance, identify risks, "
        "spot growth opportunities, and recommend safe next actions."
    ),
    "task_template": (
        "Objective: {objective}\n"
        "Summary: {summary}\n"
        "Recommendations: {recommendations}\n"
        "Return:\n"
        "1. Top risk\n"
        "2. Top opportunity\n"
        "3. Next action\n"
        "4. Why the action is safe"
    ),
    "output_style": "Short operator-facing analysis in bullet-like plain text.",
}


class PromptEngineeringService:
    """Stores and renders prompt templates for the ad agent workflow."""

    def __init__(self, config_dir: str, logger: Logger):
        self.logger = logger
        self.file_path = os.path.join(config_dir, "ad_agent_prompt.json")
        self._ensure_template_file()

    def _ensure_template_file(self) -> None:
        if os.path.exists(self.file_path):
            return

        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_PROMPT_TEMPLATE, f, ensure_ascii=False, indent=2)
        self.logger.info("Created starter ad agent prompt template file")

    def get_template(self) -> Result[Dict[str, Any]]:
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return Result.ok(data)
        except Exception as e:
            return Result.error(error_code=getattr(e, "error_code", 1010), message=str(e))

    def update_template(self, template_data: Dict[str, Any]) -> Result[Dict[str, Any]]:
        try:
            current = DEFAULT_PROMPT_TEMPLATE.copy()
            current.update(template_data or {})
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(current, f, ensure_ascii=False, indent=2)
            self.logger.info("Updated ad agent prompt template")
            return Result.ok(current)
        except Exception as e:
            return Result.error(error_code=getattr(e, "error_code", 1010), message=str(e))

    def render_prompt(self, objective: str, summary: Dict[str, Any], recommendations: str) -> Result[str]:
        template_result = self.get_template()
        if not template_result.success or not template_result.data:
            return Result.error(error_code=1010, message=template_result.error_message or "Prompt template unavailable")

        template = template_result.data
        try:
            rendered = (
                f"{template['system_role']}\n\n"
                + template["task_template"].format(
                    objective=objective,
                    summary=summary,
                    recommendations=recommendations,
                )
                + f"\n\nStyle: {template['output_style']}"
            )
            return Result.ok(rendered)
        except Exception as e:
            return Result.error(error_code=getattr(e, "error_code", 1010), message=str(e))
