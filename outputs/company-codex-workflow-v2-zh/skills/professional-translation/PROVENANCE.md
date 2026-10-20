# 来源与受控适配

2026-10-11。公司维护的 Codex 专业文档翻译技能，以 MIT 许可的 fidelity-translator 为方法参考并重新编写中文执行协议。

- 上游：https://github.com/Tasdax123/claude-fidelity-translator
- 固定提交：c9f0651b007b547bdfae103235a4567fa1acd75e
- 参考文件：plugins/fidelity-translator/skills/fidelity-translator/SKILL.md
- 采用：文档术语约束、逐块忠实性检查、结构/数值检查、已有双语资料建立候选词表、术语提案与已确认术语分离。
- 未引入：上游脚本、模型或 API 依赖、默认并行、强制 Word 样式、模型费用估算、embedding 阈值验收、强制重复确认、验证失败仍视作完成。
- 随附上游 LICENSE；这是一份受控适配协议，不声称安装或运行了上游完整翻译管线，也不继承其语言测试声明。
- 审查范围为此目录全部文件；纯 Markdown，无可执行脚本、自动网络调用或新增运行时依赖。
- 版本随公司插件；更新时重做来源、安全、真实样本与误报检查。不是 antigravity-awesome-skills 的一个条目。

## 2026-10-14 incremental-path integration

Company-authored Codex instructions add a conditional Markdown incremental path while retaining the full workflow. Mechanism reference: DeepSeek Harness dsh-translate-docs, reviewed at d74326738864 in CW-AUTO-20261007/T-037; no upstream code, scripts or dependencies copied. T-038–T-040 used one real Chinese revision and a reconstructed English baseline, three runs per arm: no confirmed quality difference, median time 20.1% lower, first incremental run slower. This is limited-sample evidence, not universal superiority or community endorsement. T-041–T-043 covers integration, routing and activation. Existing fidelity reference and MIT license remain unchanged.
