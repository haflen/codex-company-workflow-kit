# 任务约定模板

读者为执行和复核任务的 Codex；向用户说明约定时遵守 [表达规范](human-output-standard.md)，简述目标、终点与缺失决定，不直接倾倒内部 JSON。

按 [执行约定](task-execution-policy.md) 提取真实信息。以下是 schema 1 的 contract 对象示例，不是本任务授权，也不是已创建的 state.json。替换来源引用与原话；保留权威规格和验收引用，不复制业务正文。

```json
{
  "goal": "Fix normalize and verify the existing tests",
  "allowed_paths": [
    "labels.py"
  ],
  "excluded": [
    "commit",
    "push",
    "deploy"
  ],
  "spec_refs": [
    "TASK.md"
  ],
  "acceptance": [
    {
      "id": "AC-001",
      "reference": "TASK.md",
      "required": true
    }
  ],
  "delivery_endpoint": "prepare",
  "authorization": {
    "sources": [
      {
        "id": "USER-001",
        "reference": "Example only: replace with the actual retrievable user message",
        "quote": "Fix normalize in labels.py and run existing tests. Do not commit or push."
      }
    ],
    "actions": [
      {
        "action": "read",
        "scope": [
          "TASK.md",
          "labels.py",
          "test_labels.py"
        ],
        "source_ids": [
          "USER-001"
        ]
      },
      {
        "action": "edit",
        "scope": [
          "labels.py"
        ],
        "source_ids": [
          "USER-001"
        ]
      },
      {
        "action": "test",
        "scope": [
          "python3 -B -m unittest -v"
        ],
        "source_ids": [
          "USER-001"
        ]
      }
    ]
  },
  "decision_points": [],
  "required_artifacts": [
    "labels.py"
  ],
  "limits": {
    "max_repair_rounds": 2,
    "token_budget": null,
    "deadline": null
  }
}
```

`allowed_paths` 使用明确的项目相对路径；读取、编辑、测试和外部动作分别记录实际范围。`sources` 可包含多个真实用户来源，动作只引用适用来源。`inspect`、`plan`、`prepare`、`commit`、`deliver`、`merge`、`deploy`、`production_acceptance` 分别表示约定终点，不允许根据名称自行补授权。

多阶段任务将本对象保存在 `.codex-workflow/tasks/<task-id>/state.json` 的 `contract` 中；已有执行记录只保存链接。简单任务可复用已有记录。工具未安装或尚不可用时，不宣称结构化状态已创建。`max_repair_rounds=2` 是工作流默认，用户或宿主更严格限制优先；其他未提供限制保持 null。
