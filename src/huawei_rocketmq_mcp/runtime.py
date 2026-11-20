from __future__ import annotations

import asyncio
from collections.abc import Callable
from typing import Any

from jsonschema import Draft202012Validator

from .adapter import apply_arguments, to_jsonable
from .catalog import TOOL_BY_NAME, ToolSpec
from .client import build_client
from .config import RocketMQConfig as Config, RocketMQScope as Scope
from .service import model_module

ClientFactory = Callable[[Config, Scope, str], Any]


async def invoke_tool(spec: ToolSpec, arguments: dict[str, Any], *, config: Config,
                      client_factory: ClientFactory = build_client) -> Any:
    # 运行时再次核对白名单，不允许通过构造 ToolSpec 绕过已发布的只读工具集。
    if TOOL_BY_NAME.get(spec.name) != spec:
        raise ValueError("Tool is not in the read-only catalog")
    errors = sorted(Draft202012Validator(spec.input_schema).iter_errors(arguments),
                    key=lambda error: str(list(error.path)))
    if errors:
        # 不回显非法参数值，避免将业务数据或误填的密钥写入错误输出。
        error = errors[0]
        path = ".".join(str(item) for item in error.path) or "arguments"
        raise ValueError(f"Invalid {path}: schema rule {error.validator}")
    params = dict(arguments)
    region = params.pop("region", None)
    project_id = params.pop("project_id", None)
    scope = config.resolve_scope(region=region, project_id=project_id)
    request_cls = getattr(model_module(spec.api_version), spec.request_class)
    request = apply_arguments(request_cls(), params, version=spec.api_version)
    client = client_factory(config, scope, spec.api_version)
    response = await asyncio.to_thread(getattr(client, spec.sdk_method), request)
    return to_jsonable(response)
