---
name: company-delivery-closeout
description: Use when 公司项目的任务批次、功能、里程碑或版本阶段已经完成，准备正式收口、本地提交或推送当前业务分支时。
---

# 公司交付收口

## 文档归属检查

先读取项目内 `specs/global/assets/document-ownership.md`；缺失时读取插件内置 `../../specs/global/assets/document-ownership.md`。核对本次记录的归属、引用和当前状态；分开确认提交、合并、部署。仅在路由或阶段变化时更新上层入口，遵守公共文档分支协议。

## 核心原则

任务完成不等于可交付。必须基于最终待提交状态规整成果、验证证据和 Git 边界；未知归属、失败验证或文档冲突都会阻止提交和推送。

## 模式判断

| 用户意图 | 模式 | Git 动作 |
| --- | --- | --- |
| “开始交付收口” | `prepare` | 不 commit、不 push |
| “收口并提交” | `commit` | 本地 commit，不 push |
| “收口并推送业务分支” | `deliver` | 本地 commit，普通 push 当前业务分支 |
| “API 不可用，批准先合入 `<业务分支>`” | `conditional-merge` | 合入指定普通业务分支；按授权决定是否普通 push；保持未交付 |

无法判断模式时默认 `prepare`。用户明确说“所有任务已完成，开始交付收口并推送业务分支”即一次性授权 `deliver`；正常路径不重复询问。

## 授权边界

授权仅覆盖当前收口范围内的普通本地 commit 和普通 push。不得扩展为强制推送、rebase、amend、删除分支、发布、部署、删除未知文件或修改范围外工作。只有 `conditional-merge` 可执行一次明确批准的普通合并，且源候选、目标业务分支和是否 push 都必须逐项记录。

## API 不可用时的条件合入

**有条件合入不等于有条件通过。** 当真实 API 联调是确认范围但 API/环境不可用时，质量验收必须保持 `阻断 / API_PENDING`；本模式只是工程集成决定。

启用 `conditional-merge` 必须同时满足：

1. 用户明确记录批准人、批准时间、源候选与指纹、目标业务分支、允许文件、API 不可用证据、到期条件和补偿任务。
2. 目标只能是普通业务分支；不得进入 main、master、develop、integration、release、受保护分支、发布标签或生产环境，不得发布或部署。
3. API 不可用必须是外部依赖或环境限制，不能用它掩盖已知实现缺陷。
4. 契约、单元、类型、lint、构建、Fixture 隔离和必要浏览器检查通过；生产路径不得静默回退到 Fixture 或 Mock。
5. 原 API 联调与验收任务保持开放，状态依次记录为 `FIXTURE_READY -> API_PENDING -> CONDITIONAL_MERGED`；不得生成 `API_INTEGRATED`、`QUALITY_PASS` 或“已交付”结论。
6. 合并前确认源和目标工作区干净、候选指纹一致，并按项目现有普通合并策略执行；禁止 rebase、强制推送、历史改写和自动冲突裁决。

客户告知必须位于人类摘要前部，不能埋在技术附录：

> 当前仅完成基于 Fixture 的前端开发，并经批准先合入 `<目标业务分支>`。由于 `<API/环境>` 不可用，尚未完成真实 API 联调和真实页面验收。本次合入不代表功能正式交付，也不能证明真实数据、图表或业务计算正确。API 恢复后必须完成 `<补偿任务>`，通过前状态保持“有条件合入 / 未交付”。

## 质量验收状态交接

1. 重新核对独立质量验收触发矩阵，不能只相信上一轮对话中的判断。
2. 判定为不需要时，不要求新增报告；读取实现或 bugfix 的判定依据和完成前验证证据。
3. 判定为 `需要/强制` 时，从权威任务文档同级目录查找 `quality-validation-report.md`，或读取权威任务文档/当前 feature/version README 登记的实际路径。
4. 核对报告结论、用户条件接受记录和候选指纹。候选指纹包括当前分支、HEAD commit、被验收路径、diff SHA-256 与未跟踪文件哈希。
5. 候选指纹一致时复用新鲜验收证据，只补充收口引入的 cleanup、staging、secret、branch 和最终 diff 检查；不得无差别重跑完整测试集。
6. 被验收路径发生漂移时返回 `company-quality-validation`，按原 AC 和范围重新验收。纯文档规整或验收范围外的来源化清理只做增量检查。
7. 状态流只允许 `quality-validation -> delivery-closeout` 或 `delivery-closeout -> quality-validation` 的重新验收路由；不得形成递归调用，quality-validation 不执行 Git 收口，closeout 不冒充独立验收。

## 阶段一：范围与分支门禁

1. 确认项目根目录、当前分支、上游、远端和权威任务文档。
2. 核对任务均为已完成、明确延期或明确不做；未完成任务不得静默关闭。
3. 按“质量验收状态交接”读取实现或 bugfix 的判定。判定为 `需要/强制` 时，必须找到当前交付候选对应的新鲜验收报告和证据。
4. 验收缺失、已过期或为 `blocked` 时停止；`conditional-pass` 仅在风险允许且用户明确接受时继续，高风险 `V3` 不得条件放行。唯一例外是已满足上述六项门禁的 `conditional-merge`，它仍保持阻断和未交付状态。
5. 列出允许纳入的目录、文件和已有用户改动。
6. `main`、`master`、`develop`、`integration`、`release` 及项目声明的受保护分支禁止 `commit`/`deliver`/`conditional-merge`。
7. 区分“同一里程碑累计改动”与“真实并行冲突”；前者不是阻塞，后者按文件归属判断。

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

1. 按最高风险任务判定 `V0/V1/V2/V3`，确认独立质量验收结论仍对应清理和文档规整后的最终候选；若候选发生影响行为的漂移，重新进入 `company-quality-validation`，不要无差别重跑全部测试。
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

## 人类优先输出

先读取 `../../specs/global/assets/human-output-standard.md`，同时尊重项目已确认的读者和交付用途。保留一句话结论和下一步建议；用中文解释结果、依据和影响。以下输出/报告中的内部字段写入已有执行记录，不默认附在用户回复或人类文档中。

### 回复契约门禁

发送前按共享规范复核事实范围、前置条件、责任方、授权、读者及显示效果。普通问答不套固定标题；用户需要详细解释时补充有用依据。未通过阅读检查先重写再发送。
## 阶段七：交付报告

输出以下字段：

- 工作流层：`company-delivery-closeout`
- 执行模式：`prepare` / `commit` / `deliver`
- 收口范围与权威任务文档：
- 任务完成状态：
- 独立质量验收判定与结论：不需要 / pass / conditional-pass / blocked
- 质量验收报告路径与候选指纹：
- 质量验收报告与证据新鲜度：
- 条件通过的用户接受记录：
- 集成处置：正式交付 / `CONDITIONAL_MERGED` 有条件合入且未交付
- API 状态：不适用 / `API_PENDING` / `API_INTEGRATED`
- 条件合入批准人、批准时间、目标业务分支、到期条件与补偿任务：
- 客户告知：不适用 / 已在摘要首部明确 API 不可用且本次只合并分支
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
- 下一步建议与需用户处理的事项（仅确有缺失时）：

## 停止条件

受保护分支、任务未完成、需要质量验收但报告缺失/过期/阻断、未获接受的条件通过、真实文件归属冲突、未知/范围外文件、不可证明的删除候选、验证或审查失败、文档冲突、疑似敏感/生产/数据库/大文件、staged 不一致、远端领先、普通 push 被拒绝、网络或权限无法确认，均必须停止。`conditional-merge` 只能豁免“API 不可用导致验收阻断”和对应 API 任务未完成两项，不能豁免其他停止条件。

停止报告要说明阻塞项、已完成的安全步骤、未执行的 Git 动作和恢复入口，不得虚假报告 commit 或 push 成功。

## Superpowers 叠加

- 非平凡代码或 L2/L3：**REQUIRED SUB-SKILL:** Use `superpowers:requesting-code-review`。
- 所有正式交付：**REQUIRED SUB-SKILL:** Use `superpowers:verification-before-completion`。
- 此处的完成前验证证明收口后的候选、清理和暂存边界正确；质量验收中的同名能力证明 AC 与验收结论成立。两者复用新鲜证据，不默认重复整套测试。
- 进入 Git 收尾：**REQUIRED SUB-SKILL:** Use `superpowers:finishing-a-development-branch`，但服从本 skill 的模式与授权边界。

## 文档质量门禁

创建或实质修改正式文档前，先读取项目内 `specs/global/assets/document-standard.md`；缺失时读取插件内置 `../../specs/global/assets/document-standard.md`。本 skill 负责检查 `DOC-G01`、`DOC-G04`、`DOC-G05`、`DOC-G06`、`DOC-G07`、`DOC-G08`、`DOC-G09`、`DOC-G10`、`DOC-G11`、`DOC-G12`。
