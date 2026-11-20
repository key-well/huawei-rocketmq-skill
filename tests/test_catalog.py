from dataclasses import replace
import pytest
from jsonschema import Draft202012Validator
from huawei_rocketmq_mcp.catalog import TOOL_SPECS
from huawei_rocketmq_mcp.service import client_class, model_module
from scripts.generate_tools import validate_catalog


def test_catalog_matches_sdk_and_has_only_explicit_queries():
    assert validate_catalog() == []
    for spec in TOOL_SPECS:
        Draft202012Validator.check_schema(spec.input_schema)
        cls = getattr(model_module(spec.api_version), spec.request_class)
        info = getattr(client_class(spec.api_version), "_" + spec.sdk_method + "_http_info")(cls())
        assert info["method"] == "GET" or spec.name in {"BatchListMetricData", "ListNotificationMasks"}
        assert not any(word in spec.name for word in ("Password", "Certificate", "Delete", "Create", "Update", "Reset"))


def test_catalog_excludes_credentials_and_message_content():
    names = {spec.name for spec in TOOL_SPECS}
    assert not names & {"ListMessages", "ShowUser", "ShowChartValues", "ShowRelease", "ListBackupFileLinks", "ScanClients", "ExecuteCommandMobilization"}
