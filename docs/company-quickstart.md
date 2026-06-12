# Company Quickstart

这份文档面向公司项目用户。用户不需要理解所有 skill，只需要知道在什么场景说什么。

如果你是第一次使用，建议先看：

- [Codex 使用完整说明](codex-usage-guide.md)
- [常用唤起语](common-prompts.md)
- [公司试点手册](pilot-playbook.md)
- [旧项目迁移指南](legacy-project-migration.md)

## 第一次放进项目

推荐使用一键脚本：

```bash
bash scripts/install.sh all /path/to/project --lang zh
```

Windows：

```powershell
powershell -ExecutionPolicy Bypass -File scripts/install.ps1 all C:\path\to\project -Lang zh
```

英文版本使用 `--lang en` 或 `-Lang en`。

手工方式：

1. 把 `outputs/company-codex-workflow-v2-zh/AGENTS.md` 合并到目标项目根目录的 `AGENTS.md`。
2. 把 `outputs/company-codex-workflow-v2-zh/specs/` 复制到目标项目。
3. 运行 `bash scripts/install.sh generate-index /path/to/project --lang zh` 生成 `specs/global/INDEX.md` 草稿。
4. 检查并确认产品名称、当前版本、里程碑、技术栈、启动/测试/构建命令和主要源码入口。
5. 根据公司实际技术栈调整 `BUNDLES.md`。
6. 根据实际可信专家技能调整 `EXPERTS.lock.md`。

旧项目已有 `INDEX.md` 时，项目初始化默认不会覆盖。脚本会生成 `specs/global/INDEX.generated.md`，先由项目负责人确认，再决定是否替换原索引。

## 空项目或需求雏形

如果项目还是空目录，或者还在需求梳理阶段，`bootstrap-project` 仍然适合先执行。它会先放入 `AGENTS.md` 和 `specs/`，让 Codex 有统一的需求沉淀位置。

这种阶段不要急着进入技术设计或实现。建议先说：

```text
我现在是项目发起人，这还是一个空项目，需求只有雏形。请帮我走公司需求澄清流程，先不要写代码。
```

然后让 Codex 产出或维护：

- 项目愿景和业务目标。
- 目标用户和核心场景。
- MVP 范围。
- 暂不做范围。
- 验收标准。
- 关键风险和待确认问题。

推荐把第一版需求放在：

```text
specs/features/project-kickoff/requirements.md
```

`specs/global/INDEX.md` 在空项目里会有很多“待用户确认”，这是正常的。先确认产品名、业务边界和当前阶段即可；技术栈、启动命令、测试命令可以等技术方案确定后再补。

## 做一个普通功能

如果不知道入口，可以先说：

```text
我现在该走哪个流程？背景是：<当前情况>
```

用户可以这样说：

```text
帮我梳理这个功能需求：<功能描述>
```

Codex 应该输出目标、范围、验收标准、边界条件。确认后继续：

```text
需求已确认，进入技术设计
```

设计确认后：

```text
方案已确认，进入任务拆解
```

任务确认后：

```text
任务已确认，开始实现
```

## 修 bug

```text
开始 bugfix：<现象、复现步骤、期望行为>
```

Codex 应该先判断这是 bug 还是需求变更，再复现或收集证据，然后做最小修复和回归验证。

## 线上 hotfix

```text
/hotfix <事故描述>
```

Codex 应该优先止血，记录原因、修复、验证和后续补偿任务。hotfix 不应该顺手加入新功能。

## 技术 spike

```text
/spike <需要验证的技术问题>
```

Codex 应该做最小实验，输出结论、推荐方案和后续风险。spike 代码默认不是生产代码。

## 专家技能自动路由

用户不需要说“请调用 frontend-developer”。工作流会根据任务自动选择 `BUNDLES.md` 里的组合。

示例：

- 前端交互：自动偏向 `company-frontend-delivery`。
- Java 后端：自动偏向 `company-backend-java`。
- AI/RAG：自动偏向 `company-ai-feature`。
- 紧急缺陷：自动偏向 `company-hotfix`。
- 技能更新：自动偏向 `company-skill-governance`。

用户仍然可以显式点名专家；显式请求优先，但不能绕过安全和验证要求。

## 技能更新

默认先 dry-run：

```text
检查专家技能更新
对比并升级 java-pro，先不要覆盖
```

确认报告后再说：

```text
确认覆盖 java-pro
```

完整说明见 [技能升级 dry-run 工作流](skill-upgrade-dry-run.md)。

## 常见安装问题

### `/path/to/project` 可以直接复制吗？

不可以。`/path/to/project` 是占位符，要替换成真实项目路径。

错误示例：

```bash
bash scripts/install.sh bootstrap-project /path/to/company-trade-platform --lang zh
```

正确示例：

```bash
bash scripts/install.sh bootstrap-project /absolute/path/to/company-trade-platform --lang zh
```

### `bash: scripts/install.sh: No such file or directory` 是什么原因？

说明你当前目录不是 workflow kit 仓库。`scripts/install.sh` 在 `codex-company-workflow-kit` 里，不在业务项目里。

推荐方式：

```bash
cd /absolute/path/to/codex-company-workflow-kit
bash scripts/install.sh bootstrap-project /absolute/path/to/company-trade-platform --lang zh
```

如果已经在业务项目目录，也可以用绝对路径调用脚本：

```bash
bash /absolute/path/to/codex-company-workflow-kit/scripts/install.sh bootstrap-project /absolute/path/to/company-trade-platform --lang zh
```
