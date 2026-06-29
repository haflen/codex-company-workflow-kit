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
