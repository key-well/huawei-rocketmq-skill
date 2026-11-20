# 已注册工具

工具使用 SDK 参数名，具体字段以 MCP 实际返回的 inputSchema 为准。以下 20 个接口均为显式选择的只读查询，不按名称前缀动态放行其他接口。

| 工具 | SDK 版本 | 用途 |
|---|---|---|
| `ListInstances` | `v2` | 查询所有实例列表（只读查询） |
| `ShowInstance` | `v2` | 查询指定实例（只读查询） |
| `ListBrokers` | `v2` | 查询代理列表（只读查询） |
| `ShowInstanceNodes` | `v2` | 查询实例节点（只读查询） |
| `ShowRocketMqConfigs` | `v2` | 查询RocketMQ配置（只读查询） |
| `ListRocketInstanceTopics` | `v2` | 查询主题列表（只读查询） |
| `ShowOneTopic` | `v2` | 查询单个主题（只读查询） |
| `ShowTopicStatus` | `v2` | 查询主题的消息数（只读查询） |
| `ListConsumerGroupOfTopic` | `v2` | 查询主题消费组列表（只读查询） |
| `ListInstanceConsumerGroups` | `v2` | 查询消费组列表（只读查询） |
| `ShowGroup` | `v2` | 查询指定消费组（只读查询） |
| `ShowConsumerListOrDetails` | `v2` | 查询消费列表或详情（只读查询） |
| `ShowConsumerConnections` | `v2` | 查询消费者列表（只读查询） |
| `ListTopicAccessPolicy` | `v2` | 查询主题的授权用户列表（只读查询） |
| `ListConsumeGroupAccessPolicy` | `v2` | 查询消费组的授权用户列表（只读查询） |
| `ListRocketMqMigrationTask` | `v2` | 查询实例下所有迁移任务或查询指定迁移任务信息（只读查询） |
| `ListAvailableZones` | `v2` | 查询可用区信息（只读查询） |
| `ListEngineProducts` | `v2` | 查询产品规格列表（只读查询） |
| `ShowRocketmqTags` | `v2` | 查询实例标签（只读查询） |
| `ShowRocketmqProjectTags` | `v2` | 查询项目标签（只读查询） |

操作名称/简介来源及固定版本见根目录 NOTICE；详细字段由官方 SDK 生成。工具能被列出仅代表 MCP 启动正常，不能证明地域支持、云权限或实际业务结果。
