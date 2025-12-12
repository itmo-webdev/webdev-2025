import inspect
from abc import ABC
from typing import Callable, Any
from asyncio import iscoroutinefunction
from functools import wraps
from dataclasses import dataclass

DEPS = {}


def add_dep(typo: type[ABC] | str, release: object):
    DEPS[typo] = release


def get_dep(typo: type[ABC] | str):
    return DEPS[typo]


@dataclass
class Dependency:
    typo: type[ABC] | str | Callable[[], Any]

    async def __call__(self):
        if hasattr(self.typo, "_injectable"):
            return await self.typo()
        return get_dep(self.typo)

    def __hash__(self):
        return hash(self.typo)


def inject(func):
    assert iscoroutinefunction(func), "Function must be async"

    sig = inspect.signature(func)

    need_inject = {}
    for key, param in sig.parameters.items():
        val = param.default
        if isinstance(val, Dependency):
            need_inject[key] = val

    @wraps(func)
    async def wrapper(*args, **kwargs):
        for injection in need_inject:
            if injection not in kwargs:
                kwargs[injection] = await need_inject[injection]()
        return await func(*args, **kwargs)

    wrapper._injectable = True
    return wrapper
