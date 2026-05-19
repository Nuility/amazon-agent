import json
import asyncio
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, Optional
import aiofiles


class StorageAdapter(ABC):
    @abstractmethod
    async def connect(self) -> None:
        pass
    
    @abstractmethod
    async def disconnect(self) -> None:
        pass
    
    @abstractmethod
    async def read(self, key: str) -> Optional[Any]:
        pass
    
    @abstractmethod
    async def write(self, key: str, value: Any) -> None:
        pass
    
    @abstractmethod
    async def delete(self, key: str) -> None:
        pass
    
    @abstractmethod
    async def exists(self, key: str) -> bool:
        pass


class JSONFileStorageAdapter(StorageAdapter):
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self._lock = asyncio.Lock()
        self._connected = False
    
    async def connect(self) -> None:
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self._connected = True
    
    async def disconnect(self) -> None:
        self._connected = False
    
    def _get_file_path(self, key: str) -> Path:
        return self.data_dir / f"{key}.json"
    
    async def read(self, key: str) -> Optional[Any]:
        if not self._connected:
            await self.connect()
        
        file_path = self._get_file_path(key)
        
        if not file_path.exists():
            return None
        
        async with self._lock:
            async with aiofiles.open(file_path, mode='r', encoding='utf-8') as f:
                content = await f.read()
                return json.loads(content) if content else None
    
    async def write(self, key: str, value: Any) -> None:
        if not self._connected:
            await self.connect()
        
        file_path = self._get_file_path(key)
        
        async with self._lock:
            async with aiofiles.open(file_path, mode='w', encoding='utf-8') as f:
                await f.write(json.dumps(value, ensure_ascii=False, indent=2))
    
    async def delete(self, key: str) -> None:
        if not self._connected:
            await self.connect()
        
        file_path = self._get_file_path(key)
        
        async with self._lock:
            if file_path.exists():
                file_path.unlink()
    
    async def exists(self, key: str) -> bool:
        if not self._connected:
            await self.connect()
        
        return self._get_file_path(key).exists()
    
    async def list_keys(self) -> list:
        if not self._connected:
            await self.connect()
        
        return [f.stem for f in self.data_dir.glob("*.json")]


class MemoryStorageAdapter(StorageAdapter):
    def __init__(self):
        self._data: Dict[str, Any] = {}
        self._connected = False
    
    async def connect(self) -> None:
        self._connected = True
    
    async def disconnect(self) -> None:
        self._connected = False
        self._data.clear()
    
    async def read(self, key: str) -> Optional[Any]:
        return self._data.get(key)
    
    async def write(self, key: str, value: Any) -> None:
        self._data[key] = value
    
    async def delete(self, key: str) -> None:
        self._data.pop(key, None)
    
    async def exists(self, key: str) -> bool:
        return key in self._data
    
    async def list_keys(self) -> list:
        return list(self._data.keys())
    
    async def clear(self) -> None:
        self._data.clear()
