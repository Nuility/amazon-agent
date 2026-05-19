import asyncio
from typing import Any, Callable, Optional
from .logger import get_logger


class FallbackStrategy:
    def __init__(self, logger_name: str = "fallback"):
        self.logger = get_logger(logger_name)
    
    async def execute_with_fallback(
        self,
        primary_func: Callable,
        fallback_func: Callable,
        *args,
        **kwargs
    ) -> Any:
        try:
            result = await primary_func(*args, **kwargs)
            self.logger.info(
                operation="execute_with_fallback",
                result="primary_success",
                function=primary_func.__name__
            )
            return result
        except Exception as e:
            self.logger.warning(
                operation="execute_with_fallback",
                result="primary_failed",
                function=primary_func.__name__,
                error=str(e)
            )
            
            try:
                result = await fallback_func(*args, **kwargs)
                self.logger.info(
                    operation="execute_with_fallback",
                    result="fallback_success",
                    function=fallback_func.__name__
                )
                return result
            except Exception as fallback_error:
                self.logger.error(
                    operation="execute_with_fallback",
                    result="fallback_failed",
                    function=fallback_func.__name__,
                    error=str(fallback_error)
                )
                raise fallback_error
    
    async def execute_with_retry(
        self,
        func: Callable,
        max_retries: int = 3,
        delay: float = 1.0,
        *args,
        **kwargs
    ) -> Any:
        last_error = None
        
        for attempt in range(max_retries):
            try:
                result = await func(*args, **kwargs)
                if attempt > 0:
                    self.logger.info(
                        operation="execute_with_retry",
                        result="retry_success",
                        function=func.__name__,
                        attempt=attempt + 1
                    )
                return result
            except Exception as e:
                last_error = e
                self.logger.warning(
                    operation="execute_with_retry",
                    result="attempt_failed",
                    function=func.__name__,
                    attempt=attempt + 1,
                    error=str(e)
                )
                
                if attempt < max_retries - 1:
                    await asyncio.sleep(delay * (2 ** attempt))
        
        self.logger.error(
            operation="execute_with_retry",
            result="all_retries_failed",
            function=func.__name__,
            max_retries=max_retries
        )
        raise last_error
