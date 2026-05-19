import re
from typing import Dict, Any, List, Optional

from ..domain.session import IntentResult
from ..infrastructure.llm_client import LLMClient
from ..infrastructure.logger import get_logger


class IntentParser:
    def __init__(self, llm_client: Optional[LLMClient] = None):
        self.llm_client = llm_client
        self.logger = get_logger("intent_parser")
        
        self.intent_patterns = {
            "query": [r"查询|查看|显示|获取|列出|找", r"query|show|get|list|find"],
            "create": [r"创建|新建|添加|增加", r"create|add|new"],
            "update": [r"更新|修改|编辑|调整", r"update|modify|edit|change"],
            "delete": [r"删除|移除|清除", r"delete|remove|clear"],
            "analyze": [r"分析|统计|计算|评估", r"analyze|calculate|evaluate"],
            "help": [r"帮助|怎么|如何|使用说明", r"help|how|usage"],
            "greeting": [r"你好|您好|hi|hello|hey"],
            "thanks": [r"谢谢|感谢|thank"],
        }
        
        self.entity_patterns = {
            "campaign_id": r"活动[：:]\s*([a-zA-Z0-9\-]+)",
            "keyword": r"关键词[：:]\s*(.+?)(?:\s|$)",
            "date": r"(\d{4}[-/年]\d{1,2}[-/月]\d{1,2}日?)",
            "amount": r"(\d+(?:\.\d+)?)\s*(?:元|美元|\$|¥)",
        }
    
    async def parse(self, text: str, context: Optional[Dict[str, Any]] = None) -> IntentResult:
        if self.llm_client:
            try:
                llm_result = await self._parse_with_llm(text, context)
                return llm_result
            except Exception as e:
                self.logger.warning(
                    operation="parse",
                    result="llm_failed",
                    error=str(e)
                )
        
        return self._parse_with_rules(text, context)
    
    async def _parse_with_llm(
        self,
        text: str,
        context: Optional[Dict[str, Any]] = None
    ) -> IntentResult:
        prompt = f"""分析以下用户输入，识别意图和实体。

用户输入: {text}

请以JSON格式返回结果，包含以下字段:
- intent: 意图类型（query/create/update/delete/analyze/help/greeting/unknown）
- confidence: 置信度（0-1）
- entities: 提取的实体字典
- suggested_action: 建议的操作（可选）

只返回JSON，不要包含其他内容。"""

        response = await self.llm_client.call(prompt)
        
        import json
        try:
            result_data = json.loads(response)
            return IntentResult(**result_data)
        except:
            return self._parse_with_rules(text, context)
    
    def _parse_with_rules(
        self,
        text: str,
        context: Optional[Dict[str, Any]] = None
    ) -> IntentResult:
        detected_intent = "unknown"
        max_confidence = 0.0
        
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    match_confidence = 0.8 if intent in ["greeting", "thanks"] else 0.7
                    if match_confidence > max_confidence:
                        max_confidence = match_confidence
                        detected_intent = intent
        
        entities = self.extract_entities(text)
        
        clarifications = []
        if detected_intent == "unknown":
            clarifications = ["您想要执行什么操作？", "请提供更明确的指令。"]
        
        self.logger.info(
            operation="parse",
            result="success",
            intent=detected_intent,
            confidence=max_confidence
        )
        
        return IntentResult(
            intent=detected_intent,
            confidence=max_confidence,
            entities=entities,
            clarifications=clarifications
        )
    
    def extract_entities(self, text: str) -> Dict[str, Any]:
        entities = {}
        
        for entity_name, pattern in self.entity_patterns.items():
            matches = re.findall(pattern, text)
            if matches:
                entities[entity_name] = matches[0] if len(matches) == 1 else matches
        
        return entities
