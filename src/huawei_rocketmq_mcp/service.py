from __future__ import annotations

from importlib import import_module

VERSIONS = ['v2']
CLIENT_NAME = 'RocketMQClient'
SERVICE = 'rocketmq'


def model_module(version: str):
    if version not in VERSIONS:
        raise ValueError("Unsupported SDK API version")
    return import_module(f"huaweicloudsdk{SERVICE}.{version}.model")


def client_class(version: str):
    if version not in VERSIONS:
        raise ValueError("Unsupported SDK API version")
    return getattr(import_module(f"huaweicloudsdk{SERVICE}.{version}"), CLIENT_NAME)


def region_class(version: str):
    if version not in VERSIONS:
        raise ValueError("Unsupported SDK API version")
    return getattr(import_module(f"huaweicloudsdk{SERVICE}.{version}.region.{SERVICE}_region"), 'RocketMQRegion')
