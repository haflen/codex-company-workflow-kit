# 公司 Codex 工作流内部培训文档

这份文档用于给公司用户介绍如何在 Codex 中使用公司工作流。目标不是让每个人记住所有 skill 名称，而是让用户知道遇到不同工作场景时该怎么开始、怎么确认、怎么回退。

## 1. 这套工作流解决什么问题

公司项目里使用 AI 编程时，常见问题不是 AI 不会写代码，而是：

- 需求没有澄清就开始实现。
- 设计、实现和验证之间缺少追溯。
- 不同人使用 Codex 的方式不一致。
- 旧项目接入时上下文太散，AI 容易读错或读多。
- 专家技能更新没有审查和回滚路径。

这套 workflow kit 提供的是轻量护栏：

- 让 Codex 知道什么时候做需求、设计、任务、实现、bugfix、hotfix、spike。
- 让项目保留 `AGENTS.md`、`specs/`、`INDEX.md` 这些可交接资产。
- 让专家技能通过 bundle 自动路由，减少用户记忆成本。
- 让升级、停用、卸载都有安全路径。

## 2. 用户需要记住的最小心智模型

用户只需要理解三件事：

1. 全局插件让 Codex 具备公司 workflow skills。
2. 项目初始化让某个业务项目带上公司规范和模板。
3. 遇到不确定场景时，先让 Codex 判断入口。

推荐第一句话：

```text
我现在该走哪个流程？背景是：<当前情况>
```

Codex 应自动判断进入需求、设计、任务、实现、bugfix、hotfix、spike、旧项目接入或技能升级。

## 3. 安装路径

### 全局安装

适合每位公司用户在自己的电脑上安装一次：

```bash
bash scripts/install.sh install-plugin --lang zh
```

效果：

- 安装中文公司版 Codex workflow 插件。
- 以后任何项目里都可以唤起公司 skills。

### 项目安装

适合给某个业务项目接入公司规范：

```bash
bash scripts/install.sh bootstrap-project /path/to/company-project --lang zh
```

效果：

- 创建或合并 `AGENTS.md`。
- 复制 `specs/` 模板。
- 生成 `specs/global/INDEX.md` 草稿。
- 写入 `.codex-workflow/install.json` 安装清单。

### 组合安装

如果是第一次使用，推荐一次完成：

```bash
bash scripts/install.sh all /path/to/company-project --lang zh
```

## 4. 空项目怎么开始

空项目或需求雏形阶段，不要直接让 Codex 写代码。推荐先说：

```text
我现在是项目发起人，这还是一个空项目，需求只有雏形。请帮我走公司需求澄清流程，先不要写代码。
```

Codex 应优先帮助用户沉淀：

- 项目目标。
- 目标用户和核心场景。
- MVP 范围。
- 暂不做范围。
- 验收标准。
- 风险、依赖和待确认问题。

推荐第一份需求文档：

```text
specs/features/project-kickoff/requirements.md
```

## 5. 旧项目怎么接入

旧项目不要一次性补齐所有历史文档。推荐节奏：

```text
项目安装
-> 确认 INDEX.md 草稿
-> 选择一个小功能、bugfix 或 spike 试点
-> 复盘流程成本和验证质量
-> 再扩大到团队默认流程
```

推荐唤起语：

```text
请帮我把这个旧项目接入公司 Codex 工作流
```

旧项目已有规则优先保留。公司 workflow 只追加约束段落，不覆盖原有团队规范。

## 6. 一次完整功能流程示例

### 第一步：需求澄清

```text
帮我梳理这个功能需求：客户需要在后台查看订单状态变更记录。
```

期望产物：

```text
specs/features/order-status-audit/requirements.md
```

确认后说：

```text
需求已确认，进入技术设计
```

### 第二步：技术设计

Codex 应输出 API、数据流、权限、边界条件、验证策略和风险。

确认后说：

```text
方案已确认，进入任务拆解
```

### 第三步：任务拆解

Codex 应把设计拆成可执行任务，并标注验证点。

确认后说：

```text
任务已确认，开始实现
```

### 第四步：实现和验证

Codex 应按任务执行，必要时复用 Superpowers 的 TDD、debugging、verification 能力。

完成时必须说明：

- 改了什么。
- 哪些文件受影响。
- 跑了什么验证命令。
- 还有什么风险。

## 7. Bugfix、Hotfix 和 Spike

Bugfix：

```text
开始 bugfix：<问题描述>
```

Hotfix：

```text
/hotfix <线上事故>
```

Spike：

```text
/spike <技术问题>
```

原则：

- bugfix 先复现或形成证据链。
- hotfix 先止血，再补偿记录。
- spike 做最小实验，输出结论，不默认进入生产代码。

## 8. 专家技能如何参与

普通用户不需要手动点名专家。

工作流会根据当前任务自动通过 `BUNDLES.md` 选择组合。例如：

- 前端交互：偏向前端 bundle。
- Java 后端：偏向后端 bundle。
- 测试策略：偏向 QA 和验证 bundle。
- AI/RAG：偏向 AI feature bundle。

用户也可以显式说：

```text
这个任务请重点使用 Java 后端专家和测试专家。
```

显式请求优先，但不能绕过安全、验证和项目规范。

## 9. 和 Superpowers 的关系

公司 workflow 负责公司项目的阶段边界、文档资产、专家路由和治理。

Superpowers 负责通用工程方法，例如：

- brainstorming
- test-driven-development
- systematic-debugging
- verification-before-completion
- requesting-code-review

用户不需要同时记两套指令。正常说业务目标即可，Codex 应在合适节点自动结合使用。

## 10. 模板更新、停用和卸载

更新已初始化项目里的模板：

```bash
bash scripts/install.sh update-templates /path/to/company-project --lang zh
```

默认只生成 `specs/global/assets.generated/` 供对比。确认后再覆盖：

```bash
bash scripts/install.sh update-templates /path/to/company-project --lang zh --force
```

停用项目内 workflow：

```bash
bash scripts/install.sh deactivate-project /path/to/company-project
```

默认保留项目资产，只移除 `AGENTS.md` 里的 workflow marker 段落。

卸载本机全局插件：

```bash
bash scripts/install.sh uninstall-plugin --lang zh
```

同时卸载中英文插件：

```bash
bash scripts/install.sh uninstall-plugin --all
```

## 11. 培训建议

第一次内部培训建议 45 分钟：

- 5 分钟：说明为什么需要 workflow。
- 10 分钟：演示全局安装和项目初始化。
- 10 分钟：演示空项目需求澄清。
- 10 分钟：演示一次 bugfix 或 spike。
- 5 分钟：说明模板更新、停用、卸载。
- 5 分钟：答疑和收集试点反馈。

培训验收标准：

- 用户知道从哪句话开始。
- 用户知道什么时候不能直接写代码。
- 用户知道如何确认需求、设计和任务。
- 用户知道如何更新、停用和卸载。
- 用户知道项目资料会被保留，不会被默认删除。
