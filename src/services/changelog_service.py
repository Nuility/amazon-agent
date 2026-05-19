import re
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from ..domain.changelog import ChangeLog
from ..domain.enums import UpdateType
from ..infrastructure.logger import get_logger


class NamingStrategy:
    @staticmethod
    def generate_name(date: datetime, sequence: int = 1) -> str:
        date_str = date.strftime("%y%m%d")
        return f"{date_str}.{sequence}.md"
    
    @staticmethod
    def parse_name(filename: str) -> tuple:
        match = re.match(r'^(\d{6})\.(\d+)\.md$', filename)
        if match:
            date_str = match.group(1)
            sequence = int(match.group(2))
            year = int("20" + date_str[:2])
            month = int(date_str[2:4])
            day = int(date_str[4:6])
            return datetime(year, month, day), sequence
        return None, None


class ChangeLogManager:
    def __init__(self, doc_dir: str = "doc"):
        self.doc_dir = Path(doc_dir)
        self.doc_dir.mkdir(parents=True, exist_ok=True)
        self.logger = get_logger("changelog_manager")
    
    def generate_log(
        self,
        version: str,
        title: str,
        update_type: UpdateType,
        description: str,
        changes: List[str],
        breaking_changes: Optional[List[str]] = None,
        related_docs: Optional[List[str]] = None,
        author: str = "System",
        tags: Optional[List[str]] = None
    ) -> ChangeLog:
        log_id = self._generate_log_id()
        
        log = ChangeLog(
            log_id=log_id,
            version=version,
            title=title,
            update_type=update_type,
            description=description,
            changes=changes,
            breaking_changes=breaking_changes or [],
            related_docs=related_docs or [],
            author=author,
            tags=tags or []
        )
        
        self._save_log(log)
        
        self.logger.info(
            operation="generate_log",
            result="success",
            log_id=log_id,
            version=version
        )
        
        return log
    
    def list_logs(self, limit: int = 10) -> List[ChangeLog]:
        log_files = sorted(
            self.doc_dir.glob("*.md"),
            key=lambda x: x.name,
            reverse=True
        )
        
        logs = []
        for log_file in log_files[:limit]:
            if log_file.name.startswith("upgrade") or log_file.name.startswith("后端"):
                continue
            
            log = self._parse_log_file(log_file)
            if log:
                logs.append(log)
        
        return logs
    
    def get_log(self, log_id: str) -> Optional[ChangeLog]:
        log_file = self.doc_dir / f"{log_id}.md"
        
        if not log_file.exists():
            return None
        
        return self._parse_log_file(log_file)
    
    def _generate_log_id(self) -> str:
        now = datetime.now()
        date_str = now.strftime("%y%m%d")
        
        existing_logs = list(self.doc_dir.glob(f"{date_str}.*.md"))
        
        if not existing_logs:
            sequence = 1
        else:
            sequences = []
            for log_file in existing_logs:
                _, seq = NamingStrategy.parse_name(log_file.name)
                if seq:
                    sequences.append(seq)
            sequence = max(sequences) + 1 if sequences else 1
        
        return f"{date_str}.{sequence}"
    
    def _save_log(self, log: ChangeLog) -> None:
        log_file = self.doc_dir / f"{log.log_id}.md"
        
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write(log.to_markdown())
    
    def _parse_log_file(self, log_file: Path) -> Optional[ChangeLog]:
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            log_id = log_file.stem
            
            version_match = re.search(r'\*\*版本\*\*:\s*(v[\d.]+)', content)
            version = version_match.group(1) if version_match else "v1.0.0"
            
            title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
            title = title_match.group(1) if title_match else "更新日志"
            
            return ChangeLog(
                log_id=log_id,
                version=version,
                title=title,
                update_type=UpdateType.FEATURE,
                description="",
                changes=[]
            )
        except Exception as e:
            self.logger.error(
                operation="parse_log_file",
                result="error",
                file=str(log_file),
                error=str(e)
            )
            return None
    
    def update_related_docs(self, log: ChangeLog) -> None:
        self.logger.info(
            operation="update_related_docs",
            result="success",
            log_id=log.log_id
        )
