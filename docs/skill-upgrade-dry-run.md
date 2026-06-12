# Skill Upgrade Dry-Run Workflow

技能升级默认是 dry-run。也就是说，检查、获取候选版本、比对和安全审查可以自动做，但覆盖生产 skill 必须等用户明确确认。

## 适用场景

```text
检查专家技能更新
更新 java-pro 技能
对比并升级 frontend-developer
从 antigravity-awesome-skills 同步这些专家，先审查再让我确认
```

## 默认流程

1. 识别目标 skill、当前路径、来源仓库或 hub。
2. 读取 `EXPERTS.lock.md`，确认当前 pin、风险、审核状态。
3. 读取 `BUNDLES.md`，确认影响哪些专家组合和工作流节点。
4. 把候选版本放到临时审查位置。
5. 对比新旧版本。
6. 执行安全审查。
7. 输出升级报告和建议。
8. 等用户确认。
9. 用户确认后才覆盖、更新 lock、验证插件、记录回滚。

## 新旧版本比对范围

- `SKILL.md` frontmatter：`name`、`description`。
- 触发条件是否变宽。
- 主体流程是否增加强制、越权或绕过验证的规则。
- 是否新增 scripts、shell、网络访问、浏览器自动化、文件写入。
- license、upstream source、setup、risk 是否变化。
- 是否影响 `BUNDLES.md` 中的专家组合。

## 安全审查重点

- 是否要求读取 secrets、tokens、cookies、SSH keys。
- 是否隐藏网络外传、shell 执行或文件写入。
- 是否要求忽略用户、公司、sandbox 或审批规则。
- 是否诱导跳过测试、验证或 review。
- 是否依赖已经过时的 API 或框架版本。

## 用户确认门

覆盖前必须给用户看到：

```text
Skills to update:
Source and candidate pin:
Impacted bundles:
Key differences:
Security review result:
Recommendation:
Rollback path:
Confirmation needed:
```

只有当用户明确说类似下面的话时，才可以覆盖：

```text
确认覆盖 java-pro
确认应用这次升级
批准更新这些专家技能
```

下面这些不算确认：

```text
看起来不错
可以考虑
继续分析
还有别的问题吗
```

## 产物

复杂升级建议生成：

```text
outputs/company-codex-workflow-v2/specs/global/assets/skill-upgrade-report-template.md
```

小升级可以直接在对话中报告，但必须包含：

- 目标 skill
- 当前版本
- 候选版本
- diff 摘要
- 风险等级
- 用户决策
- 文件变更
- 验证结果

