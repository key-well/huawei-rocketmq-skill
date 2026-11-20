from __future__ import annotations

from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkcore.http.http_config import HttpConfig

from .config import RocketMQConfig as Config, RocketMQScope as Scope
from .service import client_class, region_class


def build_client(config: Config, scope: Scope, version: str = 'v2'):
    credentials = BasicCredentials(ak=config.access_key, sk=config.secret_key, project_id=scope.project_id)
    http = HttpConfig.get_default_config()
    http.timeout = (10, 30)
    # 不启用 HTTP 调试日志；请求由 SDK 签名并使用默认 TLS 证书校验。
    return (client_class(version).new_builder().with_credentials(credentials)
            .with_region(region_class(version).value_of(scope.region))
            .with_http_config(http).build())
