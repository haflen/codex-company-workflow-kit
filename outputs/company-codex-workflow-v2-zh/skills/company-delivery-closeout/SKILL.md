---
name: company-delivery-closeout
description: Use when 公司项目的任务批次、功能、里程碑或版本阶段已经完成，准备正式收口、本地提交或推送当前业务分支时。
---

# 公司交付收口

## 核心原则

任务完成不等于可交付。必须基于最终待提交状态规整成果、验证证据和 Git 边界；未知归属、失败验证或文档冲突都会阻止提交和推送。

## 模式判断

| 用户意图 | 模式 | Git 动作 |
| --- | --- | --- |
| “开始交付收口” | `prepare` | 不 commit、不 push |
| “收口并提交” | `commit` | 本地 commit，不 push |
| “收口并推送业务分支” | `deliver` | 本地 commit，普通 push 当前业务分支 |

无法判断模式时默认 `prepare`。用户明确说“所有任务已完成，开始交付收口并推送业务分支”即一次性授权 `deliver`；正常路径不重复询问。

## 授权边界

授权仅覆盖当前收口范围内的普通本地 commit 和普通 push。不得扩展为强制推送、rebase、amend、合并、删除分支、发布、部署、删除未知文件或修改范围外工作。

## 阶段一：范围与分支门禁

1. 确认项目根目录、当前分支、上游、远端和权威任务文档。
2. 核对任务均为已完成、明确延期或明确不做；未完成任务不得静默关闭。
3. 列出允许纳入的目录、文件和已有用户改动。
4. `main`、`master`、`develop`、`integration`、`release` 及项目声明的受保护分支禁止 `commit`/`deliver`。
5. 区分“同一里程碑累计改动”与“真实并行冲突”；前者不是阻塞，后者按文件归属判断。

## 阶段二：成果盘点与逐文件分类

使用只读状态和 diff 盘点代码、测试、配置、迁移、文档、资产、生成物和未跟踪文件。每个变更必须归入一种：

- `include`：本次交付应提交。
- `retain-but-exclude`：保留在工作区，但不属于本次提交。
- `cleanup-candidate`：有来源证据的临时产物。
- `blocking-unknown`：归属、用途或安全性不明。

需求原型按来源和状态分类：`prototype.json` 登记且仍处于活动/待确认状态的草稿为 `retain-but-exclude`，并记录延期或后续确认入口；已撤回、被替换，或已完成基线校验的来源草稿才是 `cleanup-candidate`；已确认并位于权威需求同级 `prototype/` 的基线为 `include`；没有清单或需求链接证明归属的原型为 `blocking-unknown`。

出现 `blocking-unknown` 时停止删除、commit 和 push。不得整仓暂存。

## 阶段三：文档与成果规整

1. 对照需求、业务规则、设计、API 契约、任务和最终实现。
2. 只更新项目已有且承担相应职责的权威入口、索引、version/feature README、任务状态和 lifecycle 记录。
3. 保留有审计价值的历史；不把分支局部结果提前写成公共事实。
4. 只修正本次交付直接造成的格式、备注或文档漂移，不做邻近重构。

若代码与文档冲突且无法无歧义收敛，停止 Git 动作并返回对应需求、设计或任务 workflow。

## 阶段四：临时产物 dry-run 与来源证明

删除前先输出候选清单、来源、创建者/命令、是否被跟踪、保留价值和计划动作。

- 仅自动删除当前 workflow 明确创建、有路径记录且不是正式成果的临时文件。
- 原型草稿只能在状态为已撤回/被替换，或基线校验已完成时删除，并且 `prototype.json.owned_files` 必须能证明路径归属。
- 重复产生但应长期忽略的文件，只提出项目级 `.gitignore` 建议。
- 日志证据、数据库、附件、设计资产、嵌套仓库和来源不明文件必须保留并停止确认。

清理后重新运行状态盘点；不得执行无范围清理或破坏性重置。

## 阶段五：最终验证、代码审查与安全检查

1. 按最高风险任务判定 `V0/V1/V2/V3`，在清理和文档规整后的最终候选上重新验证。
2. 执行相关测试、类型检查、lint、构建、必要的浏览器/E2E 检查和 `git diff --check`。
3. 非平凡代码或 L2/L3 交付必须使用 `superpowers:requesting-code-review` 审查最终 diff。
4. 所有正式交付必须使用 `superpowers:verification-before-completion`，只接受本轮新鲜证据。
5. 检查疑似密钥、生产配置、数据库、异常大文件、意外依赖和未验证生成物。
6. 读取 `.codex-workflow/asset-boundaries.json`，运行本次变更资产检查；新增/移动文件出现阻断项时停止 commit/push。全量历史审计只在用户要求或健康检查判定需要时运行。
7. 复杂领域风险存在时才调用 `company-expert-routing`；普通收口不重复路由。

任何失败、未验证关键项或高严重度审查问题都会停止 commit/push。

## 阶段六：精确暂存、commit 与普通 push

1. 展示最终 `include` 清单、删除清单、diff 统计、验证证据、未验证项和建议提交信息。
2. 只按明确文件路径暂存，不得使用整仓暂存。
3. 必须检查：

```bash
git diff --cached --name-status
git diff --cached --check
git diff --cached --stat
```

4. staged 清单必须与 `include` 完全一致，然后创建一次本地 commit 并记录 SHA。
5. `prepare` 到此仍不得 commit；`commit` 在本地 commit 后停止；`deliver` 使用 `git push -u origin HEAD` 普通推送当前业务分支。
6. 普通 push 被拒绝、远端领先、权限/网络不明时停止，不自动改写历史或升级权限。
7. `superpowers:finishing-a-development-branch` 只提供分支收尾检查，不得把已选模式改成 PR、合并、删除 worktree 或其他集成动作。

## 阶段七：交付报告

输出以下字段：

- 工作流层：`company-delivery-closeout`
- 执行模式：`prepare` / `commit` / `deliver`
- 收口范围与权威任务文档：
- 任务完成状态：
- 成果分类：代码 / 测试 / 文档 / 配置 / 资产
- 已删除临时文件：
- 已保留但排除文件：
- 阻塞未知文件：
- 资产落点门禁与检查范围：
- Superpowers 叠加：
- 实际调用：
- 专家能力：实际调用 / 未调用但采用视角
- 验证等级、命令与结果：
- 未验证项与剩余风险：
- staged 文件：
- commit SHA：
- 当前分支、远端与 push 结果：
- 停止原因：
- 下一步建议与推荐用户下一句：

## 停止条件

受保护分支、任务未完成、真实文件归属冲突、未知/范围外文件、不可证明的删除候选、验证或审查失败、文档冲突、疑似敏感/生产/数据库/大文件、staged 不一致、远端领先、普通 push 被拒绝、网络或权限无法确认，均必须停止。

停止报告要说明阻塞项、已完成的安全步骤、未执行的 Git 动作和恢复入口，不得虚假报告 commit 或 push 成功。

## Superpowers 叠加

- 非平凡代码或 L2/L3：**REQUIRED SUB-SKILL:** Use `superpowers:requesting-code-review`。
- 所有正式交付：**REQUIRED SUB-SKILL:** Use `superpowers:verification-before-completion`。
- 进入 Git 收尾：**REQUIRED SUB-SKILL:** Use `superpowers:finishing-a-development-branch`，但服从本 skill 的模式与授权边界。

## 文档质量门禁

创建或实质修改正式文档前，先读取项目内 `specs/global/assets/document-standard.md`；缺失时读取插件内置 `../../specs/global/assets/document-standard.md`。本 skill 负责检查 `DOC-G01`、`DOC-G04`、`DOC-G05`、`DOC-G06`、`DOC-G07`、`DOC-G08`、`DOC-G09`、`DOC-G10`、`DOC-G11`、`DOC-G12`。
