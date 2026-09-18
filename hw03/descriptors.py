"""Модуль с дескрипторами атрибутов для задания 3.2.

Вариант 3: Logged, Typed, Observable.

Каждый дескриптор реализует протокол дескриптора:
- __set_name__(self, owner, name)
- __get__(self, obj, objtype=None)
- __set__(self, obj, value)
"""

from __future__ import annotations

import logging
from collections.abc import Callable
from typing import Any

Observer = Callable[[str, Any, Any], None]

logger = logging.getLogger(__name__)


class Validated:
    """Не входит в вариант 3, поэтому не реализован."""

    def __init__(
        self,
        expected_type: type,
        min_value: Any = None,
        max_value: Any = None,
    ) -> None:
        raise NotImplementedError


class Logged:
    """Дескриптор с логированием операций чтения и записи."""

    def __init__(self, default: Any = None) -> None:
        self.default = default
        self.name = ""
        self.storage_name = ""

    def __set_name__(self, owner: type, name: str) -> None:
        self.name = name
        self.storage_name = f"_logged_{name}"

    def __get__(self, obj: Any, objtype: type | None = None) -> Any:
        if obj is None:
            return self
        value = obj.__dict__.get(self.storage_name, self.default)
        logger.info("get %s = %r", self.name, value)
        return value

    def __set__(self, obj: Any, value: Any) -> None:
        logger.info("set %s = %r", self.name, value)
        obj.__dict__[self.storage_name] = value


class Cached:
    """Не входит в вариант 3, поэтому не реализован."""

    def __init__(self, factory: Any) -> None:
        raise NotImplementedError


class Typed:
    """Дескриптор со строгой проверкой типа."""

    def __init__(self, expected_type: type) -> None:
        self.expected_type = expected_type
        self.name = ""
        self.storage_name = ""

    def __set_name__(self, owner: type, name: str) -> None:
        self.name = name
        self.storage_name = f"_typed_{name}"

    def __get__(self, obj: Any, objtype: type | None = None) -> Any:
        if obj is None:
            return self
        try:
            return obj.__dict__[self.storage_name]
        except KeyError:
            raise AttributeError(f"{self.name} is not set") from None

    def __set__(self, obj: Any, value: Any) -> None:
        if not isinstance(value, self.expected_type):
            expected = self.expected_type.__name__
            raise TypeError(f"{self.name} must be {expected}, got {type(value).__name__}")
        obj.__dict__[self.storage_name] = value


class ReadOnly:
    """Не входит в вариант 3, поэтому не реализован."""

    def __init__(self, default: Any = None) -> None:
        raise NotImplementedError


class Observable:
    """Дескриптор с подпиской на изменения значения."""

    def __init__(self, default: Any = None) -> None:
        self.default = default
        self.name = ""
        self.storage_name = ""
        self.observers_name = ""

    def __set_name__(self, owner: type, name: str) -> None:
        self.name = name
        self.storage_name = f"_observable_{name}"
        self.observers_name = f"_observers_{name}"

    def __get__(self, obj: Any, objtype: type | None = None) -> Any:
        if obj is None:
            return self
        if self.storage_name in obj.__dict__:
            return obj.__dict__[self.storage_name]
        if self.default is None:
            raise AttributeError(f"{self.name} is not set")
        return self.default

    def __set__(self, obj: Any, value: Any) -> None:
        old_value = obj.__dict__.get(self.storage_name, self.default)
        obj.__dict__[self.storage_name] = value
        for callback in list(self.observers(obj)):
            callback(self.name, old_value, value)

    def add_observer(self, obj: Any, callback: Observer) -> None:
        """Зарегистрировать callback для отслеживания изменений."""
        self.observers(obj).append(callback)

    def remove_observer(self, obj: Any, callback: Observer) -> None:
        self.observers(obj).remove(callback)

    def observers(self, obj: Any) -> list[Observer]:
        return obj.__dict__.setdefault(self.observers_name, [])
