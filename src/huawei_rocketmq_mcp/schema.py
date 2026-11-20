from __future__ import annotations

import ast
import inspect
import re
import textwrap
from typing import Any

from .service import model_module

PRIMITIVES = {"str": {"type": "string"}, "int": {"type": "integer"},
              "float": {"type": "number"}, "bool": {"type": "boolean"}, "object": {}}


def required_fields(model_class: type) -> list[str]:
    # SDK 构造函数中无条件赋值的参数为必填；可选参数在 if 分支内赋值。
    tree = ast.parse(textwrap.dedent(inspect.getsource(model_class.__init__)))
    fields = set(getattr(model_class, "openapi_types", {}))
    required = []
    for statement in tree.body[0].body:
        if not isinstance(statement, ast.Assign) or not isinstance(statement.value, ast.Name):
            continue
        for target in statement.targets:
            if (isinstance(target, ast.Attribute) and target.attr in fields
                    and isinstance(target.value, ast.Name) and target.value.id == "self"
                    and target.attr == statement.value.id):
                required.append(target.attr)
    return required


def type_schema(type_name: str, version: str, seen: frozenset[str]) -> dict[str, Any]:
    if type_name in PRIMITIVES:
        return dict(PRIMITIVES[type_name])
    match = re.fullmatch(r"list\[(.+)]", type_name)
    if match:
        return {"type": "array", "items": type_schema(match.group(1), version, seen)}
    match = re.fullmatch(r"dict\([^,]+,\s*(.+)\)", type_name)
    if match:
        return {"type": "object", "additionalProperties": type_schema(match.group(1), version, seen)}
    if type_name in seen:
        return {"type": "object"}
    cls = getattr(model_module(version), type_name, None)
    return model_schema(cls, version, seen | {type_name}) if cls else {}


def model_schema(model_class: type, version: str, seen: frozenset[str] = frozenset()) -> dict[str, Any]:
    # SDK 部分枚举是空模型类，实际请求应发送枚举标量，不能生成空对象 schema。
    enum_values = [value for name, value in vars(model_class).items()
                   if (name.isupper() or re.fullmatch(r"_[0-9]+", name))
                   and isinstance(value, (str, int, float, bool))]
    if not getattr(model_class, "openapi_types", {}) and enum_values:
        enum_type = {str: "string", int: "integer", float: "number", bool: "boolean"}[type(enum_values[0])]
        return {"type": enum_type, "enum": enum_values}
    # 保留 SDK 参数名（例如 CES 的 _from），避免 HTTP 字段名与 SDK 名混用。
    doc = inspect.getdoc(model_class.__init__) or ""
    descriptions = dict(re.findall(r":param (\w+): (.*?)(?=\n\s*:type |\Z)", doc, re.S))
    properties = {}
    for name, type_name in getattr(model_class, "openapi_types", {}).items():
        item = type_schema(type_name, version, seen)
        if descriptions.get(name):
            item["description"] = descriptions[name].strip()
        properties[name] = item
    schema = {"type": "object", "properties": properties, "additionalProperties": False}
    required = required_fields(model_class)
    if required:
        schema["required"] = required
    return schema
