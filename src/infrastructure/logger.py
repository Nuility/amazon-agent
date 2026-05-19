import json
import logging
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


class StructuredLogger:
    def __init__(
        self,
        name: str,
        log_file: str = "logs/app.log",
        level: str = "INFO",
        sensitive_fields: Optional[List[str]] = None
    ):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, level.upper()))
        
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(getattr(logging, level.upper()))
        
        console_handler = logging.StreamHandler()
        console_handler.setLevel(getattr(logging, level.upper()))
        
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        if not self.logger.handlers:
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)
        
        self.sensitive_fields = sensitive_fields or ["api_key", "token", "password", "secret"]
    
    def _sanitize(self, data: Any) -> Any:
        if isinstance(data, dict):
            sanitized = {}
            for key, value in data.items():
                if key.lower() in [f.lower() for f in self.sensitive_fields]:
                    sanitized[key] = "***REDACTED***"
                else:
                    sanitized[key] = self._sanitize(value)
            return sanitized
        elif isinstance(data, list):
            return [self._sanitize(item) for item in data]
        elif isinstance(data, str):
            for field in self.sensitive_fields:
                pattern = rf'({field}["\s:=]+)([^"\s,}}]+)'
                data = re.sub(pattern, r'\1***REDACTED***', data, flags=re.IGNORECASE)
            return data
        return data
    
    def _format_log(self, operation: str, result: str, **kwargs) -> str:
        log_data = {
            "timestamp": datetime.now().isoformat(),
            "operation": operation,
            "result": result,
            **kwargs
        }
        sanitized_data = self._sanitize(log_data)
        return json.dumps(sanitized_data, ensure_ascii=False)
    
    def info(self, operation: str, result: str = "success", **kwargs) -> None:
        message = self._format_log(operation, result, **kwargs)
        self.logger.info(message)
    
    def error(self, operation: str, result: str = "error", error: Optional[str] = None, **kwargs) -> None:
        log_data = {"error": error} if error else {}
        message = self._format_log(operation, result, **log_data, **kwargs)
        self.logger.error(message)
    
    def warning(self, operation: str, result: str = "warning", **kwargs) -> None:
        message = self._format_log(operation, result, **kwargs)
        self.logger.warning(message)
    
    def debug(self, operation: str, result: str = "debug", **kwargs) -> None:
        message = self._format_log(operation, result, **kwargs)
        self.logger.debug(message)


def get_logger(name: str, **kwargs) -> StructuredLogger:
    return StructuredLogger(name, **kwargs)
