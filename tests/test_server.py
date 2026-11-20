import pytest
from huawei_rocketmq_mcp.server import create_server
from huawei_rocketmq_mcp.catalog import TOOL_SPECS


@pytest.mark.asyncio
async def test_discovery_needs_no_cloud_credentials_and_marks_queries_read_only():
    server = create_server(env={})
    handler = next(handler for typ, handler in server.request_handlers.items()
                   if typ.__name__ == "ListToolsRequest")
    response = await handler(type("Request", (), {"params": None})())
    assert len(response.root.tools) == len(TOOL_SPECS)
    assert all(tool.annotations.readOnlyHint and not tool.annotations.destructiveHint for tool in response.root.tools)
