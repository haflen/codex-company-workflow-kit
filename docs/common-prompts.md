# Common Prompts

公司用户不需要记 skill 名称。复制下面的句子，把尖括号内容替换成自己的任务即可。

完整技能树见 [Skill Tree](skill-tree.md)。

Superpowers 结合方式见 [Superpowers Integration](superpowers-integration.md)。日常使用不需要手动输入 Superpowers skill 名称。

## 不知道从哪里开始

```text
我现在该走哪个流程？背景是：<当前情况>
```

```text
帮我判断这个任务应该走需求、设计、实现、bugfix、hotfix 还是 spike：<任务描述>
```

## 旧项目接入

```text
请帮我把这个旧项目接入公司 Codex 工作流
```

```text
请生成并检查这个项目的 INDEX.md 草稿
```

```text
请对比 specs/global/INDEX.md 和 specs/global/INDEX.generated.md，告诉我哪些字段需要确认
```

## 空项目启动

```text
我现在是项目发起人，这还是一个空项目，需求只有雏形。请帮我走公司需求澄清流程，先不要写代码。
```

```text
请帮我把这个项目雏形整理成 MVP 范围、暂不做范围、验收标准和待确认问题。
```

```text
请基于当前讨论创建 specs/features/project-kickoff/requirements.md 的第一版草稿。
```

## 新功能

```text
帮我梳理这个功能需求：<功能描述>
```

```text
请结合 Superpowers brainstorming 帮我澄清这个开放方案：<背景>
```

```text
需求已确认，进入技术设计
```

```text
方案已确认，进入任务拆解
```

```text
任务已确认，开始实现
```

## Bugfix 和 Hotfix

```text
开始 bugfix：<现象、复现步骤、期望行为>
```

```text
请用 Superpowers systematic-debugging 排查这个问题：<问题描述>
```

```text
/hotfix <线上事故、影响范围、当前证据>
```

## 技术预研

```text
/spike <需要验证的技术问题>
```

## 专家技能和升级

```text
这个任务需要哪些专家组合？
```

```text
检查专家技能更新
```

```text
对比并升级 <skill-name>，先不要覆盖
```

```text
确认覆盖 <skill-name>
```

## 完成时

```text
请给我本次变更总结、验证证据和剩余风险
```

```text
请在完成前按 Superpowers verification-before-completion 做一次验证检查
```
