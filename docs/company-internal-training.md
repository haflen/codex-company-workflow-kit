# Codex 公司工作流内部培训手册

本手册用于第一次内部培训。目标不是把大家训练成“会背流程的人”，而是让团队能在 Codex 里用同一套轻量工作流完成需求澄清、技术设计、任务拆解、实现验证、问题修复和技术预研。

建议培训时长：45-60 分钟。

适用对象：

- 项目发起人、产品或业务负责人。
- 技术负责人、架构负责人。
- 开发、测试、Reviewer。
- 需要把旧项目接入 Codex 工作流的项目成员。

## 1. 为什么需要这套 workflow

公司项目里使用 AI 编程，最大的问题通常不是“AI 会不会写代码”，而是：

- 需求没有说清楚，AI 很快写出了错误方向的代码。
- 项目上下文散落在聊天记录、代码、口头说明和旧文档里，无法稳定复用。
- 实现过程缺少验证证据，PR 很难判断是否真的满足需求。
- 旧项目接入时，Codex 不知道项目边界、架构禁区和已有规范。
- 专家技能来自开源或内部沉淀，如果没有版本、审查、更新流程，长期会失控。

这套 workflow 的定位是“护栏”，不是“轨道”：

- 需求和设计阶段先把问题说清楚，避免过早写代码。
- 实现阶段强调任务拆解、最小改动和验证证据。
- bugfix、hotfix、spike 允许快速进入特殊通道，不被完整流程拖慢。
- 通过项目上下文索引减少重复解释，让 Codex 更快进入项目状态。
- 通过技能维护和安全审查，控制外部技能、专家技能、自进化技能带来的风险。

最重要的一句话：小任务不必写重文档，大任务不能跳过确认。

## 2. 怎么安装到 Codex

安装分三种模式。培训时建议先讲清楚这三种模式，因为很多安装问题都来自把占位路径当成真实路径，或者混淆“全局插件”和“项目初始化”。

### 2.1 全局安装

全局安装是把公司工作流作为 Codex 插件安装到本机。安装后，在任意项目里都可以唤起公司工作流技能。

在 kit 仓库目录执行：

```bash
cd /path/to/codex-company-workflow-kit
bash scripts/install.sh install-plugin --lang zh
```

也可以使用 npm 入口：

```bash
npx codex-company-workflow install-plugin --lang zh
```

全局安装完成后，预期可以在 Codex 插件列表里看到公司插件，并且 `codex plugin list` 中能看到类似：

```text
company-codex-workflow-v2-zh@personal installed, enabled
```

### 2.2 项目安装

项目安装是把公司项目规范和模板写入某个具体业务项目目录。它会创建或合并：

- `AGENTS.md`
- `specs/global/INDEX.md`
- `specs/global/assets/` 下的需求、设计、任务、spike、hotfix 等模板

命令示例：

```bash
cd /path/to/codex-company-workflow-kit
bash scripts/install.sh bootstrap-project /path/to/your-project --lang zh
```

注意：`/path/to/your-project` 是占位符，必须替换成真实项目目录。例如：

```bash
bash scripts/install.sh bootstrap-project /Users/alex/Projects/order-platform --lang zh
```

### 2.3 组合安装

组合安装会先安装全局插件，再初始化指定项目。推荐新试点项目使用这种方式。

```bash
cd /path/to/codex-company-workflow-kit
bash scripts/install.sh all /path/to/your-project --lang zh
```

### 2.4 安装后的三种使用入口

安装完成后，用户可以通过三种方式使用：

1. 自然语言入口：

```text
我现在不知道该走哪个流程，请帮我判断下一步。
```

2. 明确点名公司工作流入口：

```text
$company-workflow-help
我现在要做一个新功能，请帮我判断应该从需求、设计还是实现开始。
```

3. Codex 插件或技能菜单：

在 Codex 支持技能菜单展示的环境里，可以从菜单里选择公司工作流相关技能。当前更可靠的方式仍然是自然语言入口和 `$company-workflow-help`。

说明：界面里看到的 `/company-...` 类名称可以作为提示语参考，但不要把它理解成所有 Codex 版本都 guaranteed 支持的应用级 slash command。真正稳定的是“自然语言 + skill 触发规则”。

## 3. 空项目怎么从需求雏形开始

空项目最容易犯的错误是：项目还没有边界，就让 Codex 创建工程、选技术栈、写代码。

正确做法是先进入需求澄清，而不是实现。

### 3.1 初始化空项目

如果这是一个空目录，先执行项目安装：

```bash
cd /path/to/codex-company-workflow-kit
bash scripts/install.sh bootstrap-project /path/to/empty-project --lang zh
```

安装后，Codex 会生成项目上下文索引草稿：

```text
specs/global/INDEX.md
```

空项目里的 `INDEX.md` 一开始可以很短，很多内容可以标注为“待确认”。重点是先建立项目入口，而不是一次写完整。

### 3.2 推荐启动语

在 Codex 中打开这个空项目，然后输入：

```text
我现在是项目发起人，这还是一个空项目，需求只有雏形。请帮我走公司需求澄清流程，先不要写代码。
```

如果你已经知道一个初始想法，可以这样说：

```text
我想做一个面向内部运营人员的订单管理系统，目前只有初步想法。请先帮我澄清目标用户、核心场景、MVP 范围、验收标准和风险，不要写代码。
```

### 3.3 空项目第一阶段应该产出什么

第一阶段不追求完整 PRD，而是形成最小可确认需求：

- 项目目标：这个项目解决什么问题。
- 目标用户：谁会实际使用。
- 核心流程：用户最关键的 1-3 个操作路径。
- MVP 范围：第一版必须有、可以没有、明确不做。
- 验收标准：怎样算完成。
- 风险与假设：哪些地方还不确定。

建议把第一次需求沉淀到：

```text
specs/features/project-kickoff/requirements.md
```

确认需求后，再进入技术设计；不要在需求雏形阶段直接进入代码实现。

## 4. 旧项目怎么接入

旧项目接入的原则是渐进式，不要一上来重写全部文档，也不要让 workflow 改变项目既有结构。

### 4.1 接入旧项目的目标

旧项目接入主要解决三件事：

- 让 Codex 快速理解项目结构、命令、技术栈和关键目录。
- 把团队约束写入 `AGENTS.md`，减少每次重复说明。
- 选择一个小范围任务试点，验证这套流程是否适合该项目。

### 4.2 初始化旧项目

```bash
cd /path/to/codex-company-workflow-kit
bash scripts/install.sh bootstrap-project /path/to/existing-project --lang zh
```

如果旧项目已有 `AGENTS.md`，安装脚本会追加公司工作流段落，不会覆盖原有内容。

如果旧项目已有 `specs/global/INDEX.md`，默认不会覆盖，通常会生成待确认版本，供项目负责人审阅。

### 4.3 推荐启动语

```text
请帮我把这个旧项目接入公司 Codex 工作流。先阅读项目结构、README、package 配置和已有规范，生成项目上下文索引草稿，不要改业务代码。
```

生成后，项目负责人或技术负责人需要确认：

- 项目技术栈是否识别正确。
- 启动、测试、构建命令是否正确。
- 关键目录和边界是否正确。
- 哪些模块是高风险区域。
- 哪些历史约束不能被 Codex 随意修改。

### 4.4 旧项目试点建议

旧项目不要第一个任务就选大重构。建议从以下三类任务里选一个：

- 一个边界清楚的小 feature。
- 一个可复现、影响范围小的 bugfix。
- 一个不会直接进入生产代码的 spike。

用一次小任务跑通流程，比一次性补齐全部文档更有效。

## 5. 一个 feature 怎么走

标准 feature 流程是：

```text
需求澄清 -> 技术设计 -> 任务拆解 -> 实现验证
```

### 5.1 需求澄清

适用场景：

- 新功能只有想法，还没有明确验收标准。
- 需求涉及多个角色、多个边界条件。
- 需求可能影响接口、数据结构、权限或流程。

推荐启动语：

```text
帮我梳理这个功能需求：<描述你的功能想法>。请先输出目标、范围、验收标准、边界条件和待确认问题，不要写代码。
```

确认后，可以让 Codex 写入：

```text
specs/features/<feature-name>/requirements.md
```

### 5.2 技术设计

需求确认后再进入技术设计：

```text
需求已确认，进入技术设计。请结合当前项目结构，输出实现方案、接口变化、数据流、风险和测试策略。
```

技术设计应重点回答：

- 改哪些模块。
- 新增或修改哪些接口。
- 数据结构是否变化。
- 权限、兼容性、性能、安全是否有风险。
- 需要哪些测试。
- 是否需要调用专家技能或查官方文档。

### 5.3 任务拆解

技术方案确认后再拆任务：

```text
方案已确认，进入任务拆解。请把工作拆成可执行任务，并为每个任务标注验证方式。
```

好的任务拆解应该满足：

- 每个任务可以独立执行和验证。
- 先做低风险基础改动，再做业务逻辑，再做 UI 或集成。
- 每一步都有测试、构建、手工验证或代码检查证据。

### 5.4 实现验证

任务确认后再实现：

```text
任务已确认，开始实现。请按任务顺序修改代码，并在完成后给出验证证据。
```

实现阶段要注意：

- 只改和当前任务相关的文件。
- 遇到需求或设计不清楚时，回到确认，不要自行扩大范围。
- 完成后必须给出验证证据，例如测试命令、构建命令、关键截图或手工验证步骤。

## 6. 一个 bugfix 怎么走

bugfix 的目标不是“先猜一个修复”，而是先复现、定位、最小修复、回归验证。

推荐启动语：

```text
开始 bugfix：<问题现象>。
复现步骤：<如何复现>。
期望行为：<应该怎样>。
实际行为：<现在怎样>。
请先定位原因并说明验证方式，不要扩大修改范围。
```

bugfix 流程：

1. 判断这是 bug、需求变更还是环境问题。
2. 尝试复现或找到证据。
3. 定位最可能的根因。
4. 做最小修复。
5. 运行回归验证。
6. 总结影响范围和验证证据。

如果问题复杂，可以显式结合 Superpowers：

```text
请结合 Superpowers systematic-debugging 排查这个问题，先定位根因，再提出最小修复方案。
```

bugfix 不应该顺手重构大块代码。发现无关问题可以记录，但不要在同一次修复里扩大范围。

## 7. 一个 spike 怎么走

spike 是技术预研，不是正式实现。它适用于：

- 技术可行性不确定。
- 需要比较第三方库或方案。
- 需要验证性能、兼容性、接口能力。
- 需要降低架构设计前的不确定性。

推荐启动语：

```text
开始 spike：我想验证 <技术问题>。请限定时间和范围，设计最小实验，输出结论、证据、风险和下一步建议，不要直接改生产代码。
```

好的 spike 输出应该包括：

- 要验证的问题。
- 实验范围和不做什么。
- 使用的资料来源或官方文档。
- 最小实验过程。
- 结论：可行、不可行、需要进一步验证。
- 风险和建议。

spike 完成后，如果决定进入正式开发，应重新回到 feature 的需求或设计阶段，而不是直接把实验代码合并进主线。

## 8. 这套 workflow、Codex 和 Superpowers 的关系

培训时需要把三者关系讲清楚，否则团队容易误解为“装了公司 workflow 就不用 Codex 自带能力”，或者“有 Superpowers 就不需要公司流程”。实际上三者是分层协作关系，不是互相替代。

### 8.1 三层能力模型

可以用三层来理解：

| 层级 | 代表能力 | 主要解决什么问题 | 培训时怎么解释 |
| --- | --- | --- | --- |
| Codex 基础能力层 | 读代码、改代码、运行命令、调用工具、理解项目上下文 | 让 AI 真正进入工程现场，完成代码和文档任务 | Codex 是工作台和执行引擎 |
| Superpowers 工程方法层 | brainstorming、TDD、systematic-debugging、writing-plans、verification-before-completion | 让 Codex 更像资深工程师一样思考、计划、验证 | Superpowers 是通用工程纪律 |
| 公司 workflow 治理层 | requirements、design、planning、implementation、bugfix、spike、legacy onboarding、skill governance | 让 Codex 按公司项目流程协作，产出可审计、可交接、可复用的结果 | 公司 workflow 是团队协作护栏 |

一句话版本：

```text
Codex 负责执行，Superpowers 负责工程方法，公司 workflow 负责公司项目流程和团队治理。
```

### 8.2 三者不是谁替代谁

Codex 自带能力很强，能直接读项目、改代码、跑测试。但如果没有工作流约束，它可能在需求没确认时过早实现，也可能缺少团队需要的交付痕迹。

Superpowers 提供了很好的通用工程方法，例如先 brainstorm、复杂问题先系统调试、实现前做 TDD、完成前做验证。但它默认不理解你公司的需求模板、项目接入方式、专家技能治理、技能升级安全流程。

公司 workflow 不是重写 Codex，也不是重写 Superpowers。它做的是把公司协作习惯放到 Codex 里：

- 什么时候该先澄清需求。
- 什么时候必须做技术设计。
- 什么时候可以直接 bugfix 或 spike。
- 什么时候要调用专家路由。
- 什么时候要做技能升级、安全审查和版本比对。
- 产出应该沉淀到项目里的什么位置。

### 8.3 实际使用时谁先触发

实际使用时，用户不需要手动思考三层怎么组合。建议顺序是：

1. 用户用自然语言说清当前目标。
2. 公司 workflow 先判断这是需求、设计、实现、bugfix、spike、旧项目接入还是技能维护。
3. 如果任务需要通用工程方法，公司 workflow 会结合 Superpowers 的方法论。
4. 如果任务需要改代码或查项目，Codex 使用自身工程能力执行。
5. 如果任务需要外部知识或专家判断，再进入专家路由、官方文档或技能安全审查。

例如用户说：

```text
我要做订单筛选导出功能，请帮我开始。
```

理想链路不是马上写代码，而是：

```text
公司 workflow 判断：这是 feature
-> 进入需求澄清
-> 必要时结合 Superpowers brainstorming
-> 需求确认后进入技术设计
-> 设计确认后拆任务
-> 实现阶段结合 Codex 工程能力和 Superpowers TDD/verification
```

### 8.4 什么时候用户需要显式点名 Superpowers

大多数时候不用显式点名。直接说：

```text
我现在不知道该走哪个流程，请帮我判断下一步。
```

或者：

```text
帮我梳理这个功能需求，先不要写代码。
```

只有在下面几种情况下，建议显式点名 Superpowers：

- 你希望 Codex 更深入地和你一起梳理方案。
- 你遇到复杂 bug，希望强制走系统化调试。
- 你希望实现阶段更严格地按 TDD 推进。
- 你准备收尾，希望强制做完成前验证。
- 你发现 Codex 太快进入实现，需要把它拉回思考和验证。

### 8.5 常见组合方式

如果你希望更明确，可以这样组合。

需求和方案还模糊：

```text
请结合 Superpowers brainstorming，帮我澄清这个功能的目标、范围、验收标准和风险。
```

适用技能：

- `company-feature-requirements`
- `superpowers:brainstorming`

要写实现计划：

```text
请结合 Superpowers writing-plans，把已经确认的设计拆成可执行任务和验证点。
```

适用技能：

- `company-feature-planning`
- `superpowers:writing-plans`

要实现功能：

```text
请结合 Superpowers test-driven-development，按已确认任务实现这个功能，并给出验证证据。
```

适用技能：

- `company-implementation-runner`
- `superpowers:test-driven-development`

要排查问题：

```text
请结合 Superpowers systematic-debugging 排查这个 bug，先复现和定位，不要直接猜修复。
```

适用技能：

- `company-bugfix-runner`
- `superpowers:systematic-debugging`

完成前验证：

```text
请结合 Superpowers verification-before-completion，检查这次改动是否已经满足需求、测试和验证要求。
```

适用技能：

- `company-implementation-runner`
- `superpowers:verification-before-completion`

### 8.6 给团队的使用建议

对普通团队成员，不要求记住所有技能名。培训时只需要记住三类提示：

```text
我不知道该走哪个流程，请帮我判断下一步。
```

```text
请先澄清需求/设计/任务，不要写代码。
```

```text
请结合 Superpowers 做 brainstorming / systematic-debugging / test-driven-development / verification-before-completion。
```

对技术负责人和 Reviewer，需要额外关注：

- Codex 是否过早进入实现。
- 公司 workflow 是否留下了需求、设计、任务、验证证据。
- Superpowers 是否在复杂问题上发挥了工程纪律作用。
- 专家技能是否通过公司 workflow 的专家路由和安全审查，而不是被随意复制使用。

最终原则：公司 workflow 决定“该走哪条业务流程”，Superpowers 强化“怎么把工程动作做扎实”，Codex 负责“把确认后的动作执行到位”。

## 9. 模板更新、停用和卸载怎么做

### 9.1 更新项目模板

当公司 workflow kit 更新了模板，而某个项目已经初始化过，可以执行：

```bash
cd /path/to/codex-company-workflow-kit
bash scripts/install.sh update-templates /path/to/your-project --lang zh
```

默认是安全模式，不会直接覆盖项目已有模板，通常会写入：

```text
specs/global/assets.generated/
```

项目负责人确认无误后，如确实需要覆盖：

```bash
bash scripts/install.sh update-templates /path/to/your-project --lang zh --force
```

### 9.2 停用某个项目的工作流

如果项目暂时不想继续使用这套 workflow，可以停用项目级配置：

```bash
cd /path/to/codex-company-workflow-kit
bash scripts/install.sh deactivate-project /path/to/your-project
```

停用会尽量保留项目资产，不会删除已产生的需求、设计、任务文档。它会生成停用报告：

```text
.codex-workflow/deactivation-report.md
```

### 9.3 卸载本机全局插件

如果只想卸载本机 Codex 插件：

```bash
cd /path/to/codex-company-workflow-kit
bash scripts/install.sh uninstall-plugin --lang zh
```

如果中英文版本都安装过，需要全部卸载：

```bash
bash scripts/install.sh uninstall-plugin --all
```

注意：卸载全局插件不会自动删除业务项目里的 `AGENTS.md` 和 `specs/`，因为这些属于项目资产。

## 10. 第一次培训演练脚本

培训时可以用下面顺序做一个 15-20 分钟演示。

### 10.1 安装演示

```bash
cd /path/to/codex-company-workflow-kit
bash scripts/install.sh all /path/to/demo-project --lang zh
```

讲解点：

- `all` 等于全局插件安装 + 项目初始化。
- `/path/to/demo-project` 必须换成真实路径。
- 初始化后重点看 `AGENTS.md` 和 `specs/global/INDEX.md`。

### 10.2 空项目需求演示

在 Codex 输入：

```text
我现在是项目发起人，这是一个空项目，需求只有雏形：我要做一个内部订单管理工具。请帮我走公司需求澄清流程，先不要写代码。
```

讲解点：

- 空项目不要直接写代码。
- 先确认目标用户、核心场景、MVP、验收标准。
- 输出可以落到 `specs/features/project-kickoff/requirements.md`。

### 10.3 feature 演示

```text
帮我梳理这个功能需求：运营人员可以按客户名称、订单状态和创建时间筛选订单，并导出当前筛选结果。请先输出范围、验收标准和边界条件。
```

确认后继续：

```text
需求已确认，进入技术设计。请结合当前项目结构，输出接口、数据流、风险和测试策略。
```

再继续：

```text
方案已确认，进入任务拆解。请把工作拆成可执行任务，并为每个任务标注验证方式。
```

最后：

```text
任务已确认，开始实现，并在完成后给出验证证据。
```

### 10.4 bugfix 演示

```text
开始 bugfix：订单列表按状态筛选后，翻到第二页会丢失筛选条件。
复现步骤：选择状态为已完成，点击下一页。
期望行为：第二页仍然只展示已完成订单。
实际行为：第二页展示了全部订单。
请先定位原因并说明验证方式，不要扩大修改范围。
```

讲解点：

- 先复现和定位，再修。
- bugfix 不顺手做大重构。
- 完成后要给回归验证证据。

### 10.5 spike 演示

```text
开始 spike：我想验证当前项目是否适合使用某个表格虚拟滚动库来支持 10 万行订单展示。请限定范围，设计最小实验，输出结论、证据、风险和建议，不要直接改生产代码。
```

讲解点：

- spike 是降低不确定性。
- spike 结果不是生产实现。
- 结论确认后再进入正式 feature 流程。

## 11. 角色分工和验收标准

### 11.1 项目发起人或业务负责人

负责确认：

- 需求目标是否正确。
- MVP 范围是否合理。
- 验收标准是否能判断完成。
- 哪些内容必须现在做，哪些可以后续做。

### 11.2 技术负责人

负责确认：

- 技术设计是否符合项目架构。
- 接口、数据流、权限、安全、性能风险是否可控。
- 是否需要专家技能或官方文档。
- 任务拆解是否能被开发执行。

### 11.3 开发

负责执行：

- 按已确认任务实现。
- 保持最小改动范围。
- 运行测试、构建、手工验证。
- 给出清晰的验证证据。

### 11.4 Reviewer

负责检查：

- PR 是否能追溯到需求、设计和任务。
- 改动是否超出范围。
- 验证证据是否充分。
- 是否引入隐性风险。

## 12. 常见误区

### 12.1 把占位路径当成真实路径

错误示例：

```bash
bash scripts/install.sh bootstrap-project /path/to/project --lang zh
```

正确做法是替换成真实路径：

```bash
bash scripts/install.sh bootstrap-project /Users/alex/Projects/order-platform --lang zh
```

### 12.2 需求没确认就开始写代码

如果 Codex 在需求雏形阶段准备改代码，应提醒：

```text
先停止实现。请先完成需求澄清和验收标准确认。
```

### 12.3 小任务过度文档化

小任务可以轻量处理。只要目标、范围、验收标准和验证方式清楚，不需要为了流程而写很重的文档。

### 12.4 把 spike 当成正式实现

spike 的产出是结论和证据，不是直接上线的代码。决定采用后，应回到正式设计和实现流程。

### 12.5 误以为必须手动点名每个专家技能

通常不用。公司 workflow 的专家路由会根据任务类型判断是否需要专家技能、官方文档或安全审查。用户只需要说清业务目标。

需要强制指定时，可以这样说：

```text
这次请显式走公司专家路由，判断需要哪些专家技能、知识源和验证方式。
```

### 12.6 技能升级不做审查

外部技能、专家技能、自进化建议都不能直接覆盖。应该先 dry-run、比对差异、安全审查，再由用户确认。

## 13. 一页速查

### 安装

```bash
bash scripts/install.sh install-plugin --lang zh
bash scripts/install.sh bootstrap-project /path/to/project --lang zh
bash scripts/install.sh all /path/to/project --lang zh
```

### 不知道走什么流程

```text
我现在不知道该走哪个流程，请帮我判断下一步。
```

### 空项目需求雏形

```text
我现在是项目发起人，这还是一个空项目，需求只有雏形。请帮我走公司需求澄清流程，先不要写代码。
```

### 旧项目接入

```text
请帮我把这个旧项目接入公司 Codex 工作流。先生成项目上下文索引草稿，不要改业务代码。
```

### Feature

```text
帮我梳理这个功能需求：<功能想法>。请先输出目标、范围、验收标准、边界条件和待确认问题，不要写代码。
```

### Bugfix

```text
开始 bugfix：<问题现象>。复现步骤：<步骤>。期望行为：<期望>。实际行为：<实际>。请先定位原因并说明验证方式。
```

### Spike

```text
开始 spike：我想验证 <技术问题>。请限定范围，设计最小实验，输出结论、证据、风险和建议。
```

### Superpowers 配合

```text
请结合 Superpowers brainstorming 帮我澄清这个方案。
请结合 Superpowers systematic-debugging 排查这个问题。
请结合 Superpowers test-driven-development 实现这个任务。
请结合 Superpowers verification-before-completion 做完成前验证。
```

### 更新、停用、卸载

```bash
bash scripts/install.sh update-templates /path/to/project --lang zh
bash scripts/install.sh deactivate-project /path/to/project
bash scripts/install.sh uninstall-plugin --lang zh
```

## 14. 培训结束后的落地建议

第一次培训后，不建议全公司所有项目同时切换。更稳妥的方式是：

1. 选择一个新项目或一个旧项目的小模块试点。
2. 先跑通一个 feature、一个 bugfix、一个 spike。
3. 收集团队使用中的卡点，例如提示语不清、模板太重、专家路由不准。
4. 通过技能维护流程提出改进，不直接手工改散落的项目模板。
5. 试点稳定后，再推广到更多项目。

验收标准很简单：团队成员不用记复杂流程，也能在 Codex 中自然进入正确的工作流；项目产出能追溯、能验证、能交接。
