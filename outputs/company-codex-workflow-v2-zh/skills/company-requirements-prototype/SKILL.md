---
name: company-requirements-prototype
description: Use when 公司项目仍处于需求阶段，需要创建、预览、修改或确认隔离的 HTML、页面或交互原型，以验证需求而不进入技术设计或生产实现时。
---

# 公司需求原型验证

## 文档归属检查

先读取项目内 `specs/global/assets/document-ownership.md`；缺失时读取插件内置 `../../specs/global/assets/document-ownership.md`。创建或更新阶段文档前，继承已确认归属并选择记录粒度；未验收任务续写原记录，小修复不自动新建根级 features 或完整文档包。必要的专项设计和验证不因记录精简而省略。

## 核心边界

需求原型验证“用户看到什么、如何操作”，不是技术设计或生产实现。文件阶段由验证目的和依赖边界决定，不由 `.html`、`.js` 等扩展名决定。

## 适用判断

适用于需求尚在收敛或已经澄清，但用户希望先画、预览、修改或确认页面/交互原型的场景。

不适用于：

- 技术、架构、性能或第三方库可行性验证：改用 `company-spike-research`。
- 修改生产源码或接入真实系统：必须先取得技术设计和实现授权。
- 非可视化的小需求：继续使用 `company-feature-requirements`，不创建原型产物。

## 执行协议

1. 读取权威需求、关联 `business-rules.md` 和现有原型清单。
2. 明示 `当前阶段：需求阶段`、`生产实现授权：无`，列出本轮验证问题和非目标。
3. 首次原型或实质性 UX/交互变化时，**REQUIRED SUB-SKILL:** Use `superpowers:brainstorming`。方向已确认后的机械调整不重复启动。
4. 非简单 UI 使用 `company-expert-routing`；优先采用 `company-frontend-delivery` bundle，并按需实际调用 `frontend-design`、`webapp-testing`，复杂客户端行为才增加 `frontend-developer`。
5. 只创建自包含、模拟数据、非敏感静态资源的 HTML/CSS/JavaScript。默认草稿目录：

```text
.codex-workflow/prototypes/<feature>/draft/
```

6. 在草稿目录维护 `prototype.json`，至少记录 `feature`、`source_requirements`、`status`、`created_at`、`updated_at`、`owned_files`、`validation_questions`、`browser_verification`。不得擅自修改 `.gitignore`。
7. 只在需求已确认的目标使用终端、视口、浏览器和输入方式下检查关键交互、状态、可访问性和控制台错误；关闭本轮启动的服务与浏览器进程。
8. 原型反馈改变目标、范围、业务规则、文案或验收标准时，先回到 `company-feature-requirements` 更新权威文档，再继续原型迭代。

## 转为需求基线

只有用户明确表达“需求和原型均确认，转为需求基线”或等价意图时才能执行：

1. 把已批准原型复制到权威需求文档同级 `prototype/`。
2. 在需求文档记录状态、版本、路径、确认日期、已验证范围、未承诺内容及入口 HTML 或归档包的 SHA-256。
3. 校验来源和基线内容、链接及校验和。
4. 只清理 `prototype.json` 能证明归属的草稿；不得删除来源不明文件。
5. 停止。不得自动创建技术设计、任务计划、commit 或 push。

用户同时明确说“进入技术设计”时，转为基线后只路由到 `company-feature-design`；仍不得自动进入任务拆分。

## 熔断条件

用户要求真实 API、数据库、认证、生产数据、生产组件、框架迁移、后端、数据库结构、基础设施、性能或技术可行性验证时，立即停止原型修改。说明越界内容，并在 `company-spike-research` 与已授权的 `company-feature-design` 之间重新判断入口。

模糊的“确认”“继续”“下一步”只表示继续当前需求/原型阶段，不构成技术设计或生产实现授权。

## 目标终端门禁

- 原型必须继承权威需求的目标使用终端，不得用专家 skill 的通用响应式建议扩展产品范围。
- 未明确支持移动端时，不得自行增加移动端适配、移动断点、触摸交互、设备外框、移动截图或移动端浏览器测试。
- 用户要求新增终端时，先回 `company-feature-requirements` 更新终端边界和 AC，再继续原型。

## 人类优先输出

先读取 `../../specs/global/assets/human-output-standard.md`，同时尊重项目已确认的读者和交付用途。保留一句话结论和下一步建议；用中文解释结果、依据和影响。以下输出/报告中的内部字段写入已有执行记录，不默认附在用户回复或人类文档中。

### 回复契约门禁

发送前按共享规范复核事实范围、前置条件、责任方、授权、读者及显示效果。普通问答不套固定标题；用户需要详细解释时补充有用依据。未通过阅读检查先重写再发送。
## 输出协议

- 工作流层：`company-requirements-prototype`
- 当前阶段：需求阶段
- 原型状态：草稿迭代 / 待确认 / 已确认 / 已撤回
- 生产实现授权：无
- 实际调用：
- Superpowers 叠加：
- 专家/插件能力：
- 原型验证目标：
- 草稿或基线路径：
- 浏览器验证证据：
- 需求反馈与文档漂移：
- 未验证项与剩余风险：
- 下一步：继续需求/原型迭代 / 转为需求基线 / 等待用户明确进入技术设计

需求或原型尚未确认时，不得建议任务拆分。

## 文档质量门禁

创建或实质修改正式文档前，先读取项目内 `specs/global/assets/document-standard.md`；缺失时读取插件内置 `../../specs/global/assets/document-standard.md`。本 skill 负责检查 `DOC-G01`、`DOC-G04`、`DOC-G05`、`DOC-G06`、`DOC-G07`、`DOC-G08`、`DOC-G09`、`DOC-G10`、`DOC-G11`、`DOC-G12`。
