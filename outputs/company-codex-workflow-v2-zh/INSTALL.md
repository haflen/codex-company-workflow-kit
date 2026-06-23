# 安装公司 Codex 工作流 V2 中文版

第一次使用建议先看仓库根目录下的 `docs/company-quickstart.md` 或 `docs/codex-usage-guide.md`。

## 项目级使用

1. 将 `AGENTS.md` 合并到公司项目根目录的 `AGENTS.md`。
2. 将 `specs/global/assets/` 模板复制到公司项目的 `specs/global/assets/`。
3. 使用安装脚本生成 `specs/global/INDEX.md` 草稿，并由项目负责人确认技术栈、命令、当前版本和活跃里程碑。
4. 将 `BUNDLES.md` 和 `EXPERTS.lock.md` 放到公司项目根目录，用于专家组合和专家依赖锁定。
5. 按公司实际技术栈调整 `BUNDLES.md`。
6. 按可信专家技能来源调整 `EXPERTS.lock.md`。
7. 先用一个功能和一个 bugfix 试点，再设为团队强制流程。

推荐命令：

```bash
bash scripts/install.sh bootstrap-project /path/to/project --lang zh
```

只生成或刷新索引草稿：

```bash
bash scripts/install.sh generate-index /path/to/project --lang zh
```

旧项目已有 `INDEX.md` 时默认不覆盖，会生成 `specs/global/INDEX.generated.md` 供对比确认。

如果项目提示找不到模板、`BUNDLES.md` 或 `EXPERTS.lock.md`，执行：

```bash
bash scripts/install.sh update-templates /path/to/project --lang zh
```

已有文件默认不会覆盖，会生成 `.generated` 文件供对比确认。

## 插件级使用

使用仓库根目录脚本：

```bash
bash scripts/install.sh install-plugin --lang zh
```

Windows：

```powershell
powershell -ExecutionPolicy Bypass -File scripts/install.ps1 install-plugin -Lang zh
```

## 技能更新

外部专家技能属于依赖。它们应在 `EXPERTS.lock.md` 中固定版本，使用前经过审查，并通过 dry-run 升级流程更新，而不是从 hub 自动拉取。

技能更新默认 dry-run。说 `检查专家技能更新` 或使用 `company-skill-upgrade-runner`；Codex 应比对新旧版本、完成安全审查，并等待明确确认后再覆盖生产技能。
