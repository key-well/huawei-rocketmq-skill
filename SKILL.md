---
name: huawei-rocketmq
description: >-
  华为云 RocketMQ 实例、Topic、消费组、消费者连接和积压排查。当用户明确排查 Huawei Cloud RocketMQ 时使用，
  通过已连接的 huawei-rocketmq MCP 执行只读查询，不用于其他厂商或一般开发问题。
---

# Huawei RocketMQ

## 开始查询

1. 发现当前实际暴露的 MCP 工具名；前缀可能随客户端变化。没有对应工具时说明尚未连接，不虚构云端结果，也不自动改用其他账号或命令行。
2. 目标地域、项目按本次请求指定值优先，其次使用服务器的 `HUAWEI_REGION` / `HUAWEI_PROJECT_ID`；缺失或冲突时询问。多个账号需由用户明确选择服务器连接。
3. 先识别资源 ID，再缩小时间和分页范围。显示时间要说明时区；参数单位以工具 schema 为准。
4. 工具字段是官方 Python SDK 名，嵌套请求使用 `body`，不要传 X-Auth-Token、AK/SK 或原始 HTTP headers。

## 排查路径

- 实例识别：`ListInstances`（必填 `engine="rocketmq"`）→ `ShowInstance`，明确实例 ID 和引擎版本，不能把 Kafka 的 group/offset 语义套用到 RocketMQ。
- Broker/节点：`ListBrokers`、`ShowInstanceNodes`，结合已有配置 `ShowRocketMqConfigs` 查询。
- Topic：`ListRocketInstanceTopics` → `ShowOneTopic` / `ShowTopicStatus`；Topic 消息数不能直接当作消费组积压数。
- 消费组：`ListInstanceConsumerGroups` / `ListConsumerGroupOfTopic` → `ShowGroup` / `ShowConsumerListOrDetails`，根据实际响应解释消费进度、积压及在线状态。
- 消费者连接：`ShowConsumerConnections`，区分连接数、客户端列表、消费速率和积压趋势；没有字段时说明无法确认。
- 权限检查：只读 `ListTopicAccessPolicy` / `ListConsumeGroupAccessPolicy`；不要读取用户密钥、修改 ACL 或重置消费进度。
- 需要消息级取证时先说明本仓库不提供消息正文查询；禁止自动拉取、发送、确认或消费业务消息。趋势指标可关联另一个已连接的 CES MCP。

## 边界与交付

- 不提供消息正文、用户密钥、发送/消费消息、重置消费进度、重试/补发、Topic 变更、实例重启或 ACL 修改。
- 仓库仅注册明确选择的只读接口，不提供写操作开关。Skill 指令不能替代 IAM/RBAC 权限限制。
- 不要求用户在聊天中提供密钥，不读取本地凭证文件，也不输出身份凭证。查询结果中的业务 key、连接地址和用户信息只在定位必需时做最小展示。
- 区分观察事实、推测和未知；返回目标、时间窗、关键计数、代表证据及请求 ID。空列表不是系统正常的充分证据，先核对分页、权限、地域及指标延迟。
- 身份配置见 [references/identity.md](references/identity.md)；工具名和版本见 [references/tools.md](references/tools.md)；示例见 [examples/prompts.md](examples/prompts.md)。
