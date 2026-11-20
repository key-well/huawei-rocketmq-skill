# 身份与权限

- MCP 名：`huawei-rocketmq`。凭证只在用户本地客户端配置填写，不放进对话、仓库或日志。
- `HUAWEI_ACCESS_KEY`、`HUAWEI_SECRET_KEY` 必填；`HUAWEI_REGION`、`HUAWEI_PROJECT_ID` 可设默认值，也可由每次工具调用的 `region`、`project_id` 覆盖。
- 安装脚本只写 `REPLACE_WITH_YOUR_*` 占位符。不得将占位符当作可用凭证进行云端测试。
- 使用专用 IAM 用户/委托及所需资源范围的最小只读权限。具体 action 需根据本仓库实际使用的 API 对照华为云当前权限文档配置；本项目不声称某个策略能覆盖所有查询。
- 401/403 时保留 request_id、error_code，核对账号、项目、地域及策略，不以增大权限或自动换账号重试。
- 本版本使用长期 AK/SK 的 BasicCredentials，不宣称已支持临时 STS 令牌或自动轮换。
- CCE 云 API 的 IAM 不等于 Kubernetes RBAC；查询 Pod、日志需要另行授权。本安装不会建立 Kubernetes 连接。
