from collections import defaultdict
from importlib import import_module
from typing import Any, DefaultDict

__all__ = ("resolve_module_function",)


# Singleton constant mapping (module name, function name) -> function.
CACHE: DefaultDict[str, DefaultDict[str, Any]] = defaultdict(
    lambda: defaultdict(lambda: None)
)


def resolve_module_function(module_name: str, function_name: str) -> Any:
    # Check if it's already in our cache.
    if func := CACHE[module_name][function_name]:
        return func

    # If not, attempt to resolve it dynamically.
    module = import_module(module_name)
    func = getattr(module, function_name)
    CACHE[module_name][function_name] = func
    return func
