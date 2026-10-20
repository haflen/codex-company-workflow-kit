# Task Contract Template

This record serves Codex execution and review. When explaining the contract to a user, follow the [human output standard](human-output-standard.md): summarize goal, endpoint and missing decisions without dumping internal JSON.

Extract real facts using the [execution policy](task-execution-policy.md). This is an example schema 1 contract object, not authority for the current task or an existing state.json. Replace references and quotations with actual sources. Reference authoritative specifications and acceptance criteria instead of copying their content.

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

Use explicit project-relative `allowed_paths`; record the actual scope of reads, edits, tests and external actions separately. Multiple real user sources may be cited; each action references only applicable sources. Endpoints are `inspect`, `plan`, `prepare`, `commit`, `deliver`, `merge`, `deploy` and `production_acceptance`; their names never create authority.

For multi-stage tasks, store this object as `contract` in `.codex-workflow/tasks/<task-id>/state.json`; existing execution records keep a link only. Simple tasks may reuse existing records. Do not claim structured state was created when tooling is missing or unavailable. `max_repair_rounds=2` is the workflow default; stricter user or host limits prevail. Other unspecified limits remain null.
