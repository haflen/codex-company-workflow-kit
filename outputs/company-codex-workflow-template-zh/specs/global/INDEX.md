# 项目上下文索引

把这个文件作为项目上下文的第一入口。摘要保持简短，只链接会指导后续 Codex 工作的文档。

## 项目快照

- 产品：
- 主要用户：
- 核心业务约束：
- 主要技术栈：
- 测试命令：
- 构建命令：
- 本地启动命令：

## 资产落点门禁

- 配置文件：`.codex-workflow/asset-boundaries.json`
- 确认状态：待确认
- 工程资产根目录：待确认
- 先在需求、设计或计划中声明完整仓库相对路径，再进入实现；交付前检查实际变更文件。
- 项目初始化后确认自动推断结果，不把未确认目录当成正式约束。

## 全局文档

```mermaid
flowchart LR
    A["先读 document-standard"] --> B["选择文档类型模板"]
    B --> C["先写结论和图"]
    C --> D["补关键表格和细节"]
    D --> E["按 DOC-G01~G12 自检"]
```

| 文档 | 用途 | 何时读取 |
| --- | --- | --- |
| `specs/global/INDEX.md` | 上下文地图和命令索引 | 每次任务 |
| `specs/global/assets/document-standard.md` | 正式文档阅读骨架与质量门禁 | 新建或实质修改正式文档 |
| `specs/global/assets/requirements-template.md` | 需求模板 | 创建或细化功能需求 |
| `specs/global/assets/design-template.md` | 技术设计模板 | 设计功能实现 |
| `specs/global/assets/data-model-template.md` | 数据模型与表结构模板 | 设计数据关系、表和字段 |
| `specs/global/assets/business-rules-template.md` | 业务规则与计算口径模板 | 复杂规则、公式或状态流转 |
| `specs/global/assets/api-contract-template.md` | API 契约模板 | 前后端、服务或模块边界工作 |
| `specs/global/assets/tasks-template.md` | 任务规划模板 | 将已确认工作拆成实现步骤 |
| `specs/global/assets/spike-report-template.md` | Spike 报告模板 | `/spike` 工作 |
| `specs/global/assets/hotfix-report-template.md` | Hotfix 报告模板 | `/hotfix` 工作 |
| `specs/global/assets/requirements-prototype-record-template.md` | 需求原型确认记录 | 原型确认并转为需求基线 |
| `specs/global/assets/delivery-closeout-template.md` | 交付收口报告 | 功能、里程碑或版本收口 |

## 功能 Specs

| 功能 | 状态 | 需求 | 设计 | 任务 | 备注 |
| --- | --- | --- | --- | --- | --- |
| 示例 | 草稿 | `specs/features/example/requirements.md` | `specs/features/example/design.md` | `specs/features/example/tasks.md` | 替换为真实功能 |

## 当前风险

- 资产落点配置尚未确认。
