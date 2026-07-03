---
name: company-feature-design
description: Use when company feature requirements are confirmed and a technical design, architecture decision, API contract, data flow, or test strategy is needed before task planning.
---

# 公司功能技术设计

## 目的

在任务拆解前产出技术方案、契约、数据流、风险和测试策略。

## 工作流

1. 确认需求已存在，并包含验收标准。
2. 阅读项目上下文、现有模式和相关源文件；如果需求判定需要 `business-rules.md`，必须先读取业务规则与计算口径。
3. 执行方案对比分级判定：L1 小改动可跳过但必须说明原因；L2/L3 命中触发条件时必须比较 2-3 个方案。
4. 需要方案对比时，显式叠加 `superpowers:brainstorming`，输出推荐方案、备选方案、取舍和用户确认点。
5. 对非平凡架构、框架、数据、UI 或测试决策使用 `company-expert-routing`，由它自动选择技术栈 bundle。
6. 对非平凡架构、数据、权限、性能、安全、外部 API、前端渲染或跨服务边界执行第一性原理检查。
7. 设计不得重新发明业务公式；只能把 `business-rules.md` 中的操作逻辑、状态流转、字段口径和计算公式映射到模块、接口、数据结构和测试策略。
8. 输出设计、契约、风险说明、反例场景和测试策略。
9. 涉及前后端或服务边界时，任务拆解前先产出 API 契约。
10. 如果本轮设计来自实现阶段中发现的范围变化，必须标记 `实现授权状态：已失效，需要用户确认后再编码`，并说明旧任务授权不覆盖新范围。
11. L2/L3 方案对比触发后，必须获得用户对推荐方案的确认，才能进入任务拆解。
12. 设计阶段结束后停止，除非用户给出任务拆解交接口令。

## Superpowers 叠加

- 默认：方案存在不确定性或命中 L2/L3 方案对比触发条件时叠加 `superpowers:brainstorming`，用于比较 2-3 个设计路径。
- 高风险设计：叠加 `company-expert-routing` 后，可按专家结果继续使用 `superpowers:brainstorming` 收敛方案。
- 设计已经唯一且风险低时：可以不叠加，但输出必须写明原因。

## 方案对比触发条件

命中以下任一条件时，必须做方案对比，并在任务拆解前让用户确认推荐方案：

- 新增较大的功能模块、核心页面、核心流程或子系统。
- 涉及前后端边界、服务边界、数据模型、权限、安全、性能、缓存、并发或外部 API。
- 涉及 `business-rules.md`、计算口径、状态机、审批流、任务流或复杂数据映射。
- 存在“快速交付”和“长期可维护”之间的明显取舍。
- 方案会影响扩展性、迁移成本、测试策略、发布/回滚或团队协作边界。
- 用户提到“比较大、模块、架构、方案、技术路线、要不要这样做、对比一下”。

未命中时可以跳过，但必须写明：`方案对比：跳过，原因：L1 小改动，技术路径唯一，风险低。`

## 产物

使用模板时按以下顺序查找：

1. 项目内：`specs/global/assets/design-template.md`；跨边界工作使用 `specs/global/assets/api-contract-template.md`。
2. 插件内置 fallback：相对当前 skill 目录读取 `../../specs/global/assets/design-template.md` 或 `../../specs/global/assets/api-contract-template.md`。

如需求阶段链接了 `business-rules.md`，设计产物必须在“使用的上下文”中列出它，并说明每条关键规则映射到哪里实现或验证。

## 边界

设计工作不得编辑实现代码。

范围变化后的设计工作不得直接接回实现；必须先进入任务拆解，并等待用户确认新任务范围。

## 输出格式

- 工作流层：`company-feature-design`
- 透明度模式：
- Superpowers 叠加：
- 实际调用：
- 专家/插件能力：
- 未调用但采用视角：
- 第一性原理检查：
- 对抗式审查：
- 执行策略：
- 验证证据：
- 未验证项：
- 剩余风险：
- 推荐设计：
- 实现授权状态：
- 方案对比判定：
- 备选方案和取舍：
- 用户确认点：
- 业务规则映射：
- 底层事实和最小成立条件：
- 关键反例场景：
- 风险：
- 测试策略：
- 下一步：L2/L3 已确认推荐方案后才能进入 `company-feature-planning`。
