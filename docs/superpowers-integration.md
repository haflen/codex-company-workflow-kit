# Superpowers Integration

这套公司 workflow 不是替代 Superpowers，也不是要求用户每次手动输入 Superpowers skill。

推荐理解成三层：

```text
公司 workflow skills：决定公司流程阶段和交付产物
Superpowers skills：提供工程纪律，如 brainstorming、TDD、debugging、verification
Codex built-in capabilities：读写代码、运行命令、浏览器验证、文件操作、Git
```

## 用户需要怎么唤起

公司用户默认只需要说业务意图：

```text
帮我梳理这个功能需求：...
开始 bugfix：...
任务已确认，开始实现
我现在该走哪个流程？
```

公司 workflow 会在对应节点自动使用或建议 Superpowers 能力。

不建议普通用户写：

```text
/Superpowers /brainstorming
/Superpowers /test-driven-development
```

更推荐在需要显式指定时这样说：

```text
请结合 Superpowers brainstorming 帮我梳理这个方案
请用 Superpowers systematic-debugging 排查这个问题
请用 Superpowers test-driven-development 实现这个任务
```

如果当前 Codex 环境支持 `$superpowers:<skill>` 显式引用，也可以使用：

```text
$superpowers:brainstorming
$superpowers:systematic-debugging
$superpowers:test-driven-development
$superpowers:verification-before-completion
```

但这属于高级用法。公司 workflow 的目标是让用户不用记这些名字。

## 当前映射

| 公司节点 | 默认公司 skill | Superpowers / Codex 能力 |
| --- | --- | --- |
| 不知道入口 | `company-workflow-help` | `brainstorming` only when direction is genuinely open-ended |
| 需求澄清 | `company-feature-requirements` | `brainstorming` for ambiguous product direction |
| 技术设计 | `company-feature-design` | official docs / expert routing / optional `brainstorming` for multiple architecture choices |
| 任务拆解 | `company-feature-planning` | `writing-plans` style task slicing when plan complexity is high |
| 实现 | `company-implementation-runner` | `test-driven-development`, `verification-before-completion` |
| Bugfix | `company-bugfix-runner` | `systematic-debugging`, regression verification |
| 收尾 review | completion report | `requesting-code-review` for major or risky changes |
| 技能更新 | `company-skill-upgrade-runner` | current Codex file/Git tools, security review workflow |

## 使用例子

普通功能：

```text
帮我梳理这个功能需求：客户列表支持按筛选条件导出 CSV
```

公司 workflow 进入 `company-feature-requirements`。如果需求方向仍然开放，Codex 可以使用 `brainstorming` 辅助澄清，但用户不需要手动点名。

实现阶段：

```text
任务已确认，开始实现
```

公司 workflow 进入 `company-implementation-runner`。如果涉及非平凡行为或易出错逻辑，Codex 应使用 `test-driven-development`；完成前应使用 verification discipline，给出真实验证证据。

Bugfix：

```text
开始 bugfix：导出按钮点击后偶发无响应
```

公司 workflow 进入 `company-bugfix-runner`。如果根因不明显，应使用 `systematic-debugging` 先复现和定位，再做最小修复。

## 原则

- 公司 workflow 决定阶段，不让 Superpowers 直接接管公司 SDLC。
- Superpowers 提供工程方法，不重复写进公司 skill。
- 用户可以显式点名 Superpowers，但日常使用不要求记忆。
- 如果 Superpowers skill 不可用，Codex 应说明限制，并使用公司 workflow 的本地规则继续推进。

