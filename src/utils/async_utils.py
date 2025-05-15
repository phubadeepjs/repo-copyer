from functools import wraps
from typing import Any, Callable, TypeVar, cast

T = TypeVar('T')

def async_lru_cache(maxsize: int = 128, typed: bool = False) -> Callable:
    """Async LRU cache decorator.
    
    Args:
        maxsize: Maximum size of the cache
        typed: If True, arguments of different types will be cached separately
        
    Returns:
        Decorated async function with caching
    """
    cache = {}
    
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            key = str(args) + str(kwargs)
            if key not in cache:
                cache[key] = await func(*args, **kwargs)
            return cache[key]
        return cast(Callable[..., Any], wrapper)
    return decorator
