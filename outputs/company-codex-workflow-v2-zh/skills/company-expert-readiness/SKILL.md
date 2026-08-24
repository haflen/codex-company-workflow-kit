---
name: company-expert-readiness
description: Use when a company project needs to verify bundled expert skills, check whether external expert dependencies are installed and exposed, or explain expert readiness before workflow use.
---

# 公司专家依赖就绪检查

## 目的

确保公司 workflow 开箱即用：强依赖外部专家必须随插件内置安装、自动审查，并在项目初始化时生成就绪报告。

## 工作流

1. 读取项目根目录 `BUNDLES.md`、`EXPERTS.lock.md` 和 `.codex-workflow/EXPERT-READINESS.md`。
2. 如果报告不存在，建议运行 `bash scripts/install.sh expert-preflight <project-path> --lang zh`。
3. 检查当前会话是否暴露 bundle 所需专家 skill。
4. 如果专家已随插件安装但当前会话不可见，提示用户新开 Codex 线程刷新技能列表。
5. 如果专家缺失，要求重新执行 `install-plugin --force` 或 `all <project-path> --force`。
6. 输出可用专家、缺失专家、受限专家、下一步。


## 人类优先输出

最终回复先使用：`一句话结论`、`这次完成了什么`、`需要你注意什么`、`你现在需要做什么`。用业务结果和用户影响表达，只给一个主要下一步；首次出现的内部术语必须解释。随后把 Superpowers、专家调用、命令、路径、哈希、验证证据和内部 workflow 字段放入 `技术审计附录`，不得把内部 workflow 字段逐项倾倒到人类摘要，也不得用审计字段代替人类摘要。


### 回复契约门禁

- 触发范围：本轮正式完成或阶段收尾、用户明确索要进度总结、阻塞结论或下一步方案，以及包含审计字段的成段回复。
- 1-2 句的工作中更新和普通问答始终不触发固定格式，即使提到当前结果、风险或下一步；但不得在轻量回复中附带完整审计明细。
- 用户要求“详细一点”时，只增加四段正文或 `技术审计附录` 的深度，不得删除、改名或调换四个标题。
- 审计字段只能出现在 `技术审计附录`，不得与四段人类摘要并列或抢在其前。
- 发送前检查四个标题是否齐全且顺序正确、风险是否翻译为实际影响、是否只有一个主要下一步；任一不满足时先重写再发送。

## 输出

- 工作流层：`company-expert-readiness`
- 透明度模式：
- Superpowers 叠加：无；这是安装和依赖诊断。
- 实际调用：
- 专家/插件能力：
- 未调用但采用视角：
- 第一性原理检查：
- 对抗式审查：
- 执行策略：先检查随包内置专家，再检查当前会话暴露状态。
- 验证证据：
- 未验证项：
- 剩余风险：
- Bundle：
- 已安装并可调用：
- 已安装但当前会话未暴露：
- 缺失：
- 安全审查状态：
- 用户下一步：

## 护栏

- 不要求用户逐个安装强依赖专家。
- 不把“锁文件存在”误判为“当前会话可调用”。
- 不静默更新外部 hub；更新必须走公司技能维护和安全审查。
