from __future__ import annotations

import re
from datetime import date, datetime
from enum import Enum
from typing import Any

from .service import model_module


def _coerce(value: Any, type_name: str, version: str) -> Any:
    if value is None:
        return None
    match = re.fullmatch(r"list\[(.+)]", type_name)
    if match and isinstance(value, list):
        return [_coerce(item, match.group(1), version) for item in value]
    match = re.fullmatch(r"dict\([^,]+,\s*(.+)\)", type_name)
    if match and isinstance(value, dict):
        return {key: _coerce(item, match.group(1), version) for key, item in value.items()}
    cls = getattr(model_module(version), type_name, None)
    if cls and isinstance(value, dict):
        return apply_arguments(cls(), value, version=version)
    return value


def apply_arguments(model: Any, arguments: dict[str, Any], *, version: str = 'v2') -> Any:
    known = getattr(model, "openapi_types", {})
    unknown = sorted(set(arguments) - set(known))
    if unknown:
        raise ValueError("Unknown argument(s): " + ", ".join(unknown))
    for name, value in arguments.items():
        setattr(model, name, _coerce(value, known[name], version))
    return model


def to_jsonable(value: Any) -> Any:
    if hasattr(value, "to_dict"):
        return to_jsonable(value.to_dict())
    if isinstance(value, dict):
        return {str(key): to_jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [to_jsonable(item) for item in value]
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return value
