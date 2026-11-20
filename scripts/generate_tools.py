#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from huawei_rocketmq_mcp.schema import model_schema
from huawei_rocketmq_mcp.service import client_class, model_module

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "references/operations.json"
OUTPUT = ROOT / "src/huawei_rocketmq_mcp/generated_catalog.json"


def render_catalog() -> list[dict]:
    result = []
    for op in json.loads(SOURCE.read_text(encoding="utf-8")):
        version = op["api_version"]
        client = client_class(version)
        methods = {name.replace("_", "").lower(): name for name in dir(client) if not name.startswith("_")}
        method = methods[op["name"].lower()]
        cls = getattr(model_module(version), op["name"] + "Request")
        info = getattr(client, "_" + method + "_http_info")(cls())
        # 白名单来自逐项选取的官方查询接口；只有批量查询可以使用 POST。
        if info["method"] != "GET" and op["name"] not in ("BatchListMetricData", "ListNotificationMasks"):
            raise ValueError("Non-query operation: " + op["name"])
        schema = model_schema(cls, version)
        if info["method"] == "POST" and "body" in schema["properties"]:
            schema["required"] = sorted(set(schema.get("required", [])) | {"body"})
        schema["properties"] = {
            "region": {"type": "string", "minLength": 1, "description": "Overrides HUAWEI_REGION."},
            "project_id": {"type": "string", "minLength": 1, "description": "Overrides HUAWEI_PROJECT_ID."},
            **schema["properties"],
        }
        result.append({"name": op["name"], "api_version": version,
                       "sdk_method": method, "request_class": cls.__name__,
                       "description": op["description"], "input_schema": schema})
    return result


def validate_catalog() -> list[str]:
    expected = render_catalog()
    if not OUTPUT.exists():
        return ["missing generated catalog"]
    actual = json.loads(OUTPUT.read_text(encoding="utf-8"))
    return [] if actual == expected else ["catalog drift: run scripts/generate_tools.py --write"]


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate explicit read-only SDK bindings.")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    if args.write:
        OUTPUT.write_text(json.dumps(render_catalog(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    errors = validate_catalog()
    for error in errors:
        print(error)
    if not errors:
        print(f"catalog valid: {len(render_catalog())} read-only tools")
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
