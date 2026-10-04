param(
  [Parameter(Position=0)]
  [string]$Command,
  [Parameter(Position=1)]
  [string]$ProjectPath,
  [ValidateSet("zh", "en")]
  [string]$Lang = "zh",
  [switch]$Force,
  [switch]$All
)

$ErrorActionPreference = "Stop"
$PluginName = if ($Lang -eq "zh") { "company-codex-workflow-v2-zh" } else { "company-codex-workflow-v2" }
$MarkerBegin = "<!-- codex-workflow-kit:company:start -->"
$MarkerEnd = "<!-- codex-workflow-kit:company:end -->"
$LegacyMarkerBegin = "<!-- company-codex-workflow-kit:start -->"
$LegacyMarkerEnd = "<!-- company-codex-workflow-kit:end -->"
$RootDir = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$PluginSrc = Join-Path $RootDir "outputs/$PluginName"
$MarketplaceRoot = Join-Path $HOME ".agents/plugins"
$PluginInstallRoot = Join-Path $HOME "plugins"
$PluginDst = Join-Path $PluginInstallRoot $PluginName
$MarketplaceFile = Join-Path $MarketplaceRoot "marketplace.json"
$ValidatorPath = if ($env:CODEX_PLUGIN_VALIDATOR) {
  $env:CODEX_PLUGIN_VALIDATOR
} else {
  Join-Path $HOME ".codex/skills/.system/plugin-creator/scripts/validate_plugin.py"
}

function Show-Usage {
  Write-Host "Usage:"
  Write-Host "  powershell -ExecutionPolicy Bypass -File scripts/install.ps1 install-plugin [-Lang zh|en] [-Force]"
  Write-Host "  powershell -ExecutionPolicy Bypass -File scripts/install.ps1 uninstall-plugin [-Lang zh|en|-All]"
  Write-Host "  powershell -ExecutionPolicy Bypass -File scripts/install.ps1 bootstrap-project <project-path> [-Lang zh|en] [-Force]"
  Write-Host "  powershell -ExecutionPolicy Bypass -File scripts/install.ps1 migrate-project <project-path> [-Lang zh|en]"
  Write-Host "  powershell -ExecutionPolicy Bypass -File scripts/install.ps1 deactivate-project <project-path> [-Force]"
  Write-Host "  powershell -ExecutionPolicy Bypass -File scripts/install.ps1 update-templates <project-path> [-Lang zh|en] [-Force]"
  Write-Host "  powershell -ExecutionPolicy Bypass -File scripts/install.ps1 install-agents <project-path> [-Lang zh|en] [-Force]"
  Write-Host "  powershell -ExecutionPolicy Bypass -File scripts/install.ps1 generate-index <project-path> [-Lang zh|en] [-Force]"
  Write-Host "  powershell -ExecutionPolicy Bypass -File scripts/install.ps1 expert-preflight <project-path> [-Lang zh|en]"
  Write-Host "  powershell -ExecutionPolicy Bypass -File scripts/install.ps1 generate-asset-boundaries <project-path> [-Lang zh|en] [-Force]"
  Write-Host "  powershell -ExecutionPolicy Bypass -File scripts/install.ps1 accept-asset-boundaries <project-path> [-Lang zh|en]"
  Write-Host "  powershell -ExecutionPolicy Bypass -File scripts/install.ps1 confirm-asset-boundaries <project-path> [-Lang zh|en]"
  Write-Host "  powershell -ExecutionPolicy Bypass -File scripts/install.ps1 check-assets <project-path> [-Lang zh|en]"
  Write-Host "  powershell -ExecutionPolicy Bypass -File scripts/install.ps1 audit-assets <project-path> [-Lang zh|en]"
  Write-Host "  powershell -ExecutionPolicy Bypass -File scripts/install.ps1 all <project-path> [-Lang zh|en] [-Force]"
  Write-Host "  powershell -ExecutionPolicy Bypass -File scripts/install.ps1 verify [-Lang zh|en]"
}

function Get-PluginNameForLang($Code) {
  if ($Code -eq "zh") {
    return "company-codex-workflow-v2-zh"
  }
  if ($Code -eq "en") {
    return "company-codex-workflow-v2"
  }
  throw "Unsupported language: $Code. Use zh or en."
}

function Get-CodexCli {
  if (-not [string]::IsNullOrWhiteSpace($env:CODEX_CLI) -and (Test-Path $env:CODEX_CLI)) {
    return $env:CODEX_CLI
  }
  $command = Get-Command codex -ErrorAction SilentlyContinue
  if ($command) {
    return $command.Source
  }
  $candidates = @(
    (Join-Path $HOME ".local/bin/codex"),
    "/Applications/ChatGPT.app/Contents/Resources/codex",
    "/Applications/Codex.app/Contents/Resources/codex"
  )
  foreach ($candidate in $candidates) {
    if (Test-Path $candidate) {
      return $candidate
    }
  }
  return $null
}

function Refresh-CodexPluginRegistration {
  $codexCli = Get-CodexCli
  if ([string]::IsNullOrWhiteSpace($codexCli)) {
    Write-Warning "Codex CLI not found; plugin source is installed but the Codex cache was not refreshed."
    Write-Warning "After Codex CLI is available, run: codex plugin add $PluginName@personal"
    return
  }
  & $codexCli plugin add "$PluginName@personal" --json
  if ($LASTEXITCODE -ne 0) {
    throw "Codex plugin registration refresh failed for $PluginName@personal"
  }
  Write-Host "Codex plugin registration refreshed: $PluginName@personal"
}

function Copy-DirSafe($Source, $Destination) {
  if ((Test-Path $Destination) -and (-not $Force)) {
    Write-Host "Skip existing: $Destination"
    return
  }
  if (Test-Path $Destination) {
    Remove-Item -Recurse -Force $Destination
  }
  New-Item -ItemType Directory -Force -Path (Split-Path $Destination) | Out-Null
  Copy-Item -Recurse -Force $Source $Destination
  Get-ChildItem -Path $Destination -Recurse -Force -Filter ".DS_Store" | Remove-Item -Force
}

function Copy-FileSafe($Source, $Destination, $GeneratedDestination = $null) {
  if (-not (Test-Path $Source)) {
    throw "Source file not found: $Source"
  }
  if ((Test-Path $Destination) -and (-not $Force)) {
    if (-not [string]::IsNullOrWhiteSpace($GeneratedDestination)) {
      New-Item -ItemType Directory -Force -Path (Split-Path $GeneratedDestination) | Out-Null
      Copy-Item -Force $Source $GeneratedDestination
      Write-Host "Existing file preserved: $Destination"
      Write-Host "Generated updated file for review: $GeneratedDestination"
    } else {
      Write-Host "Skip existing: $Destination"
    }
    return
  }
  New-Item -ItemType Directory -Force -Path (Split-Path $Destination) | Out-Null
  Copy-Item -Force $Source $Destination
  Write-Host "Wrote file: $Destination"
}

function Ensure-RootPluginJson($PluginRoot) {
  $manifest = Join-Path $PluginRoot ".codex-plugin/plugin.json"
  $rootManifest = Join-Path $PluginRoot "plugin.json"
  if (-not (Test-Path $manifest)) {
    throw "Plugin manifest not found: $manifest"
  }
  Copy-Item -Force $manifest $rootManifest
}

function Review-BundledExperts($PluginRoot, [bool]$Persist = $true) {
  $temporaryRoot = $null
  if ($Persist) {
    $report = Join-Path $PluginRoot "EXPERT-READINESS.md"
    $json = Join-Path $PluginRoot "EXPERT-READINESS.json"
  } else {
    $temporaryRoot = Join-Path ([IO.Path]::GetTempPath()) ("company-expert-review-" + [guid]::NewGuid().ToString("N"))
    New-Item -ItemType Directory -Force -Path $temporaryRoot | Out-Null
    $report = Join-Path $temporaryRoot "EXPERT-READINESS.md"
    $json = Join-Path $temporaryRoot "EXPERT-READINESS.json"
  }
  try {
    python3 (Join-Path $RootDir "scripts/expert_dependencies.py") review `
      --plugin-root $PluginRoot `
      --lang $Lang `
      --output $report `
      --json-output $json
    if ($LASTEXITCODE -ne 0) {
      throw "Expert dependency review failed for $PluginRoot"
    }
  } finally {
    if ($temporaryRoot -and (Test-Path $temporaryRoot)) {
      Remove-Item -Recurse -Force $temporaryRoot
    }
  }
}

function Write-ProjectExpertReadiness($Path) {
  $workflowDir = Join-Path $Path ".codex-workflow"
  New-Item -ItemType Directory -Force -Path $workflowDir | Out-Null
  python3 (Join-Path $RootDir "scripts/expert_dependencies.py") project-report `
    --plugin-root $PluginSrc `
    --project-path $Path `
    --lang $Lang `
    --output (Join-Path $workflowDir "EXPERT-READINESS.md") `
    --json-output (Join-Path $workflowDir "EXPERT-READINESS.json")
}

function Install-AssetBoundaryTool($Path) {
  $destination = Join-Path $Path ".codex-workflow/bin/asset_boundaries.py"
  New-Item -ItemType Directory -Force -Path (Split-Path $destination) | Out-Null
  Copy-Item -Force (Join-Path $RootDir "scripts/asset_boundaries.py") $destination
  Write-Host "Asset boundary checker ready: $destination"
}

function Generate-AssetBoundaries($Path) {
  Install-AssetBoundaryTool $Path
  $scriptArgs = @(
    (Join-Path $RootDir "scripts/asset_boundaries.py"),
    "generate",
    $Path,
    "--lang",
    $Lang
  )
  if ($Force) {
    $scriptArgs += "--force"
  }
  python3 @scriptArgs
  if ($LASTEXITCODE -ne 0) {
    throw "Asset boundary generation failed for $Path"
  }
}

function Confirm-AssetBoundaries($Path) {
  Install-AssetBoundaryTool $Path
  python3 (Join-Path $Path ".codex-workflow/bin/asset_boundaries.py") confirm $Path --lang $Lang
  if ($LASTEXITCODE -ne 0) {
    throw "Asset boundary confirmation failed for $Path"
  }
}

function Accept-AssetBoundaries($Path) {
  Install-AssetBoundaryTool $Path
  python3 (Join-Path $Path ".codex-workflow/bin/asset_boundaries.py") accept-generated $Path --lang $Lang
  if ($LASTEXITCODE -ne 0) {
    throw "Asset boundary candidate acceptance failed for $Path"
  }
}

function Check-Assets($Path, [bool]$AuditAll = $false) {
  Install-AssetBoundaryTool $Path
  $scope = if ($AuditAll) { "--all" } else { "--changed" }
  python3 (Join-Path $Path ".codex-workflow/bin/asset_boundaries.py") check $Path --lang $Lang $scope
  if ($LASTEXITCODE -ne 0) {
    throw "Asset placement check failed for $Path"
  }
}

function Install-Plugin {
  if (-not (Test-Path (Join-Path $PluginSrc ".codex-plugin"))) {
    throw "Plugin source not found: $PluginSrc"
  }
  Ensure-RootPluginJson $PluginSrc
  Review-BundledExperts $PluginSrc $false
  if ((Test-Path $PluginDst) -and (-not $Force)) {
    Write-Host "Plugin already installed: $PluginDst"
    Write-Host "Use -Force to replace it."
  } else {
    Copy-DirSafe $PluginSrc $PluginDst
    Write-Host "Installed plugin: $PluginDst"
  }
  if (Test-Path $PluginDst) {
    Ensure-RootPluginJson $PluginDst
    Review-BundledExperts $PluginDst $true
  }
  New-Item -ItemType Directory -Force -Path $MarketplaceRoot | Out-Null
  New-Item -ItemType Directory -Force -Path $PluginInstallRoot | Out-Null
  if (Test-Path $MarketplaceFile) {
    $data = Get-Content -Raw $MarketplaceFile | ConvertFrom-Json
  } else {
    $data = [pscustomobject]@{
      name = "personal"
      interface = [pscustomobject]@{ displayName = "Personal" }
      plugins = @()
    }
  }
  if (-not $data.interface) {
    $data | Add-Member -NotePropertyName interface -NotePropertyValue ([pscustomobject]@{ displayName = "Personal" })
  }
  if (-not $data.plugins) {
    $data | Add-Member -NotePropertyName plugins -NotePropertyValue @()
  }
  $entry = [pscustomobject]@{
    name = $PluginName
    source = [pscustomobject]@{ source = "local"; path = "./plugins/$PluginName" }
    policy = [pscustomobject]@{ installation = "AVAILABLE"; authentication = "ON_INSTALL" }
    category = "Productivity"
  }
  $plugins = @($data.plugins | Where-Object { $_.name -ne $PluginName })
  $data.plugins = @($plugins + $entry)
  $data | ConvertTo-Json -Depth 8 | Set-Content -Encoding UTF8 $MarketplaceFile
  Write-Host "Marketplace updated: $MarketplaceFile"
  Refresh-CodexPluginRegistration
  Write-Host "Language: $Lang"
}

function Uninstall-PluginName($Name) {
  $destination = Join-Path $PluginInstallRoot $Name
  if (Test-Path $destination) {
    Remove-Item -Recurse -Force $destination
    Write-Host "Removed plugin directory: $destination"
  } else {
    Write-Host "Plugin directory not found: $destination"
  }
  $legacyDestination = Join-Path $MarketplaceRoot "plugins/$Name"
  if (Test-Path $legacyDestination) {
    Remove-Item -Recurse -Force $legacyDestination
    Write-Host "Removed legacy plugin directory: $legacyDestination"
  }
  if (Test-Path $MarketplaceFile) {
    $data = Get-Content -Raw $MarketplaceFile | ConvertFrom-Json
    $data.plugins = @($data.plugins | Where-Object { $_.name -ne $Name })
    $data | ConvertTo-Json -Depth 8 | Set-Content -Encoding UTF8 $MarketplaceFile
  }
  Write-Host "Marketplace entry removed if present: $Name"
}

function Uninstall-Plugin {
  if ($All) {
    Uninstall-PluginName (Get-PluginNameForLang "zh")
    Uninstall-PluginName (Get-PluginNameForLang "en")
  } else {
    Uninstall-PluginName $PluginName
  }
}

function Test-UnmarkedLegacyAgents($Content) {
  if ($Content.Contains($MarkerBegin) -or $Content.Contains($LegacyMarkerBegin)) {
    return $false
  }
  $normalized = $Content.TrimStart()
  $signatures = @(
    @("# 公司 Codex 工作流", "## 上下文优先", "## 阶段边界", "## Superpowers"),
    @("# Company Codex Workflow", "## Context First", "## Phase Boundaries", "## Superpowers"),
    @("# Codex 公司项目工作流", "## 上下文加载", "## 阶段边界", "## 验证规则"),
    @("# Codex Company Workflow", "## Context Loading", "## Phase Boundaries", "## Verification Rules")
  )
  foreach ($signature in $signatures) {
    if (-not $normalized.Contains($signature[0])) {
      continue
    }
    $matches = 0
    foreach ($part in $signature[1..3]) {
      if ($Content.Contains($part)) {
        $matches += 1
      }
    }
    if ($matches -ge 2) {
      return $true
    }
  }
  return $false
}

function Get-NormalizedAgentsSha256($Content) {
  $normalized = $Content.TrimStart([char]0xFEFF).Replace("`r`n", "`n").TrimEnd() + "`n"
  $bytes = [Text.Encoding]::UTF8.GetBytes($normalized)
  $sha = [Security.Cryptography.SHA256]::Create()
  try {
    return ([BitConverter]::ToString($sha.ComputeHash($bytes))).Replace("-", "").ToLowerInvariant()
  } finally {
    $sha.Dispose()
  }
}

function Get-KnownLegacyAgentsHashes {
  $hashes = @(
    "ac01db91a51c2bac541714e9f2c90353f344dd8b1bfb38d64a64388c2b9eb3de",
    "2b1dbe6fec8b753788833de2be7917c07e8006e73efe46ae25b59382bf0050d0"
  )
  $starterName = if ($Lang -eq "zh") {
    "company-codex-workflow-template-zh"
  } else {
    "company-codex-workflow-template"
  }
  $starter = Join-Path $RootDir "outputs/$starterName/AGENTS.md"
  if (Test-Path $starter) {
    $hashes += Get-NormalizedAgentsSha256 (Get-Content -Raw $starter)
  }
  $currentFull = Join-Path $PluginSrc "AGENTS.md"
  if (Test-Path $currentFull) {
    $hashes += Get-NormalizedAgentsSha256 (Get-Content -Raw $currentFull)
  }
  return $hashes
}

function Append-AgentsBlock($Target, [string]$Mode = "safe") {
  $content = if (Test-Path $Target) { Get-Content -Raw $Target } else { "" }
  $source = (Get-Content -Raw (Join-Path $PluginSrc "AGENTS.md")).TrimEnd()
  $block = "$MarkerBegin`n$source`n$MarkerEnd"
  $pairs = @(
    @($MarkerBegin, $MarkerEnd),
    @($LegacyMarkerBegin, $LegacyMarkerEnd)
  )
  $beginCount = 0
  $endCount = 0
  foreach ($pair in $pairs) {
    $beginCount += ([regex]::Matches($content, [regex]::Escape($pair[0]))).Count
    $endCount += ([regex]::Matches($content, [regex]::Escape($pair[1]))).Count
  }
  if ($beginCount -gt 1 -or $endCount -gt 1 -or $beginCount -ne $endCount) {
    throw "AGENTS.md contains duplicate or unbalanced company workflow markers; resolve them manually before updating templates."
  }
  foreach ($pair in $pairs) {
    $start = $content.IndexOf($pair[0])
    if ($start -lt 0) {
      continue
    }
    $finish = $content.IndexOf($pair[1], $start)
    if ($finish -lt 0) {
      throw "AGENTS.md managed block has no closing marker: $($pair[1])"
    }
    $finish += $pair[1].Length
    $prefix = $content.Substring(0, $start).TrimEnd()
    $suffix = $content.Substring($finish).TrimStart()
    $parts = @($prefix, $block, $suffix) | Where-Object { -not [string]::IsNullOrWhiteSpace($_) }
    Set-Content -Encoding UTF8 $Target (($parts -join "`n`n").TrimEnd() + "`n")
    Write-Host "Updated managed company workflow block in AGENTS.md."
    return
  }
  if (Test-UnmarkedLegacyAgents $content) {
    if ($Mode -eq "migrate") {
      $backupDir = Join-Path (Split-Path $Target) ".codex-workflow/backups"
      New-Item -ItemType Directory -Force -Path $backupDir | Out-Null
      $stamp = [DateTimeOffset]::UtcNow.ToString("yyyyMMddTHHmmssfffffffZ")
      $backup = Join-Path $backupDir "AGENTS.$stamp.bak"
      Copy-Item -Force $Target $backup
      $contentHash = Get-NormalizedAgentsSha256 $content
      if ((Get-KnownLegacyAgentsHashes) -notcontains $contentHash) {
        $candidate = Join-Path (Split-Path $Target) "AGENTS.generated.md"
        Set-Content -Encoding UTF8 $candidate ($block.TrimEnd() + "`n")
        Write-Host "Backed up unrecognized legacy AGENTS.md: $backup"
        Write-Host "Generated current managed rules for manual merge: $candidate"
        throw "Migration stopped: legacy AGENTS.md contains unknown or project-local changes. Preserve those rules and merge the generated candidate manually."
      }
      Set-Content -Encoding UTF8 $Target ($block.TrimEnd() + "`n")
      $candidate = Join-Path (Split-Path $Target) "AGENTS.generated.md"
      if (Test-Path $candidate) {
        Remove-Item -Force $candidate
      }
      Write-Host "Backed up legacy AGENTS.md: $backup"
      Write-Host "Migrated unmarked legacy company workflow rules to the managed block."
    } else {
      $candidate = Join-Path (Split-Path $Target) "AGENTS.generated.md"
      Set-Content -Encoding UTF8 $candidate ($block.TrimEnd() + "`n")
      Write-Host "Legacy unmarked AGENTS.md preserved: $Target"
      Write-Host "Generated current managed rules for review: $candidate"
      Write-Host "Run migrate-project to back up and replace the legacy workflow rules safely."
    }
    return
  }
  $parts = @($content.TrimEnd(), $block) | Where-Object { -not [string]::IsNullOrWhiteSpace($_) }
  Set-Content -Encoding UTF8 $Target (($parts -join "`n`n").TrimEnd() + "`n")
  Write-Host "Added managed company workflow block to AGENTS.md."
}

function Write-InstallManifest($Path) {
  $workflowDir = Join-Path $Path ".codex-workflow"
  New-Item -ItemType Directory -Force -Path $workflowDir | Out-Null
  $manifest = [pscustomobject]@{
    kit = "codex-company-workflow-kit"
    profile = "company"
    plugin = $PluginName
    language = $Lang
    installedAt = [DateTimeOffset]::UtcNow.ToString("o")
    managedMarkers = [pscustomobject]@{
      agentsBegin = $MarkerBegin
      agentsEnd = $MarkerEnd
    }
    managedPaths = @(
      "AGENTS.md marker block",
      "BUNDLES.md",
      "EXPERTS.lock.md",
      ".codex/agents/ (optional via install-agents)",
      "specs/global/assets/",
      "specs/global/assets.generated/",
      ".codex-workflow/asset-boundaries.json",
      ".codex-workflow/asset-boundaries.generated.json",
      ".codex-workflow/asset-boundaries.backup.json",
      ".codex-workflow/bin/asset_boundaries.py",
      ".codex-workflow/backups/",
      ".codex-workflow/install.json"
    )
    preservedProjectAssets = @(
      "specs/features/",
      "specs/global/INDEX.md",
      "specs/global/INDEX.generated.md"
    )
  }
  $manifest | ConvertTo-Json -Depth 8 | Set-Content -Encoding UTF8 (Join-Path $workflowDir "install.json")
  Write-Host "Install manifest written: $(Join-Path $workflowDir "install.json")"
}

function Ensure-ProjectGovernanceFiles($Path) {
  Copy-FileSafe (Join-Path $PluginSrc "BUNDLES.md") (Join-Path $Path "BUNDLES.md") (Join-Path $Path "BUNDLES.generated.md")
  Copy-FileSafe (Join-Path $PluginSrc "EXPERTS.lock.md") (Join-Path $Path "EXPERTS.lock.md") (Join-Path $Path "EXPERTS.lock.generated.md")
}

function Ensure-LocalGitExcludes($Path) {
  $gitCommand = Get-Command git -ErrorAction SilentlyContinue
  if (-not $gitCommand) {
    return
  }
  $excludeRelative = git -C $Path rev-parse --git-path info/exclude 2>$null
  if ($LASTEXITCODE -ne 0 -or -not $excludeRelative) {
    return
  }
  $excludePath = $excludeRelative.Trim()
  if (-not [System.IO.Path]::IsPathRooted($excludePath)) {
    $excludePath = Join-Path $Path $excludePath
  }
  New-Item -ItemType Directory -Force -Path (Split-Path $excludePath) | Out-Null
  if (-not (Test-Path $excludePath)) {
    New-Item -ItemType File -Force -Path $excludePath | Out-Null
  }
  $pattern = ".codex-workflow/backups/"
  $hasPattern = Get-Content -Path $excludePath | Where-Object { $_.Trim() -eq $pattern }
  if (-not $hasPattern) {
    Add-Content -Encoding UTF8 $excludePath $pattern
  }
}

function Ensure-ProjectTemplates($Path) {
  $source = Join-Path $PluginSrc "specs/global/assets"
  $destination = Join-Path $Path "specs/global/assets"
  if (-not (Test-Path $source)) {
    throw "Template source not found: $source"
  }
  New-Item -ItemType Directory -Force -Path (Join-Path $Path "specs/global") | Out-Null
  if ((Test-Path $destination) -and (-not $Force)) {
    Write-Host "Project templates already present: $destination"
  } else {
    if (Test-Path $destination) {
      if ($Force) {
        $backupRoot = Join-Path $Path ".codex-workflow/backups"
        New-Item -ItemType Directory -Force -Path $backupRoot | Out-Null
        $backupStamp = [DateTime]::UtcNow.ToString("yyyyMMddTHHmmssfffffffZ")
        $backupDestination = Join-Path $backupRoot "assets.$backupStamp"
        Copy-Item -Recurse -Force $destination $backupDestination
        Ensure-LocalGitExcludes $Path
        Write-Host "Backed up project templates: $backupDestination"
        Get-ChildItem -Path $source -Force | ForEach-Object {
          Copy-Item -Recurse -Force $_.FullName $destination
        }
      }
    } else {
      Copy-Item -Recurse -Force $source $destination
    }
    Get-ChildItem -Path $destination -Recurse -Force -Filter ".DS_Store" | Remove-Item -Force
    Write-Host "Project templates ready: $destination"
  }
}

function Install-ProjectAgents($Path) {
  if ([string]::IsNullOrWhiteSpace($Path)) {
    Show-Usage
    exit 1
  }
  $source = Join-Path $PluginSrc ".codex/agents"
  $destination = Join-Path $Path ".codex/agents"
  $reviewDestination = Join-Path $Path ".codex/agents.generated"
  if (-not (Test-Path $source)) {
    throw "Custom agent source not found: $source"
  }
  New-Item -ItemType Directory -Force -Path (Join-Path $Path ".codex") | Out-Null
  if ((Test-Path $destination) -and (-not $Force)) {
    if (Test-Path $reviewDestination) {
      Remove-Item -Recurse -Force $reviewDestination
    }
    Copy-Item -Recurse -Force $source $reviewDestination
    Get-ChildItem -Path $reviewDestination -Recurse -Force -Filter ".DS_Store" | Remove-Item -Force
    Write-Host "Existing custom agents preserved: $destination"
    Write-Host "Generated updated custom agents for review: $reviewDestination"
    Write-Host "Next: compare agents and agents.generated, then rerun with -Force if you approve replacement."
  } else {
    if (Test-Path $destination) {
      Remove-Item -Recurse -Force $destination
    }
    Copy-Item -Recurse -Force $source $destination
    Get-ChildItem -Path $destination -Recurse -Force -Filter ".DS_Store" | Remove-Item -Force
    Write-Host "Project custom agents ready: $destination"
  }
}

function Generate-Index($Path, $OutputPath, [bool]$Overwrite) {
  if ([string]::IsNullOrWhiteSpace($Path)) {
    Show-Usage
    exit 1
  }
  $scriptArgs = @(
    (Join-Path $RootDir "scripts/generate_index.py"),
    $Path,
    "--lang",
    $Lang,
    "--output",
    $OutputPath
  )
  if ($Overwrite -or $Force) {
    $scriptArgs += "--force"
  }
  python3 @scriptArgs
}

function Bootstrap-Project($Path) {
  if ([string]::IsNullOrWhiteSpace($Path)) {
    Show-Usage
    exit 1
  }
  New-Item -ItemType Directory -Force -Path $Path | Out-Null
  $agents = Join-Path $Path "AGENTS.md"
  $indexPath = Join-Path $Path "specs/global/INDEX.md"
  $indexExisted = Test-Path $indexPath
  if (Test-Path $agents) {
    Append-AgentsBlock $agents
    Write-Host "Merged AGENTS.md: $agents"
  } else {
    New-Item -ItemType File -Force -Path $agents | Out-Null
    Append-AgentsBlock $agents
    Write-Host "Created AGENTS.md: $agents"
  }
  Ensure-ProjectTemplates $Path
  Ensure-ProjectGovernanceFiles $Path
  Generate-AssetBoundaries $Path
  Write-Host "Project workflow assets ready: $(Join-Path $Path "specs")"
  if ((-not $indexExisted) -or $Force) {
    Generate-Index $Path $indexPath $true
  } else {
    $generatedPath = Join-Path $Path "specs/global/INDEX.generated.md"
    Generate-Index $Path $generatedPath $true
    Write-Host "Existing INDEX.md preserved. Review INDEX.generated.md before replacing it."
  }
  Write-InstallManifest $Path
  Write-ProjectExpertReadiness $Path
  Write-Host "Next: review the generated INDEX draft and confirm project context."
}

function Deactivate-Project($Path) {
  if ([string]::IsNullOrWhiteSpace($Path)) {
    Show-Usage
    exit 1
  }
  $agents = Join-Path $Path "AGENTS.md"
  $workflowDir = Join-Path $Path ".codex-workflow"
  $report = Join-Path $workflowDir "deactivation-report.md"
  New-Item -ItemType Directory -Force -Path $workflowDir | Out-Null
  if (Test-Path $agents) {
    $content = Get-Content -Raw $agents
    $start = $content.IndexOf($MarkerBegin)
    if ($start -ge 0) {
      $finish = $content.IndexOf($MarkerEnd, $start)
      if ($finish -ge 0) {
        $finish += $MarkerEnd.Length
        $newContent = ($content.Substring(0, $start).TrimEnd() + "`n" + $content.Substring($finish).TrimStart()).TrimEnd() + "`n"
        Set-Content -Encoding UTF8 $agents $newContent
        Write-Host "Removed company workflow block from AGENTS.md."
      }
    } else {
      Write-Host "No managed company workflow marker found in AGENTS.md; left it unchanged."
    }
  } else {
    Write-Host "AGENTS.md not found; nothing to update."
  }
  if ($Force) {
    foreach ($relative in @("specs/global/assets", "specs/global/assets.generated")) {
      $target = Join-Path $Path $relative
      if (Test-Path $target) {
        Remove-Item -Recurse -Force $target
      }
    }
    foreach ($relative in @(
      ".codex-workflow/asset-boundaries.json",
      ".codex-workflow/asset-boundaries.generated.json",
      ".codex-workflow/asset-boundaries.backup.json",
      ".codex-workflow/bin/asset_boundaries.py"
    )) {
      $target = Join-Path $Path $relative
      if (Test-Path $target) {
        Remove-Item -Force $target
      }
    }
    Write-Host "Removed managed template directories."
  } else {
    Write-Host "Project specs preserved. Use -Force to remove managed template directories only."
  }
  $removedTemplates = if ($Force) { "yes" } else { "no" }
  $body = @"
# Company Workflow Deactivation Report

- Deactivated at: $([DateTimeOffset]::UtcNow.ToString("o"))
- AGENTS.md marker block: removed when present
- Template directories removed: $removedTemplates

## Preserved by default

- specs/features/
- specs/global/INDEX.md
- specs/global/INDEX.generated.md

## Notes

Project requirement, design, task, and verification documents are treated as project assets and are not deleted by this command.
"@
  Set-Content -Encoding UTF8 $report $body
  Write-Host "Deactivation report written: $report"
}

function Update-Templates($Path) {
  if ([string]::IsNullOrWhiteSpace($Path)) {
    Show-Usage
    exit 1
  }
  $source = Join-Path $PluginSrc "specs/global/assets"
  $destination = Join-Path $Path "specs/global/assets"
  $reviewDestination = Join-Path $Path "specs/global/assets.generated"
  if (-not (Test-Path $source)) {
    throw "Template source not found: $source"
  }
  New-Item -ItemType Directory -Force -Path (Join-Path $Path "specs/global") | Out-Null
  if ((Test-Path $destination) -and (-not $Force)) {
    if (Test-Path $reviewDestination) {
      Remove-Item -Recurse -Force $reviewDestination
    }
    Copy-Item -Recurse -Force $source $reviewDestination
    Get-ChildItem -Path $reviewDestination -Recurse -Force -Filter ".DS_Store" | Remove-Item -Force
    Write-Host "Existing templates preserved: $destination"
    Write-Host "Generated updated templates for review: $reviewDestination"
    Write-Host "Next: compare assets and assets.generated, then rerun with -Force if you approve replacement."
  } else {
    if (Test-Path $destination) {
      if ($Force) {
        $backupRoot = Join-Path $Path ".codex-workflow/backups"
        New-Item -ItemType Directory -Force -Path $backupRoot | Out-Null
        $backupStamp = [DateTime]::UtcNow.ToString("yyyyMMddTHHmmssfffffffZ")
        $backupDestination = Join-Path $backupRoot "assets.$backupStamp"
        Copy-Item -Recurse -Force $destination $backupDestination
        Ensure-LocalGitExcludes $Path
        Write-Host "Backed up project templates: $backupDestination"
        Get-ChildItem -Path $source -Force | ForEach-Object {
          Copy-Item -Recurse -Force $_.FullName $destination
        }
      }
    } else {
      Copy-Item -Recurse -Force $source $destination
    }
    Get-ChildItem -Path $destination -Recurse -Force -Filter ".DS_Store" | Remove-Item -Force
    Write-Host "Updated project templates: $destination"
  }
  Append-AgentsBlock (Join-Path $Path "AGENTS.md")
  $indexPath = Join-Path $Path "specs/global/INDEX.md"
  if (Test-Path $indexPath) {
    $generatedPath = Join-Path $Path "specs/global/INDEX.generated.md"
    Generate-Index $Path $generatedPath $true
    Write-Host "Existing INDEX.md preserved. Review INDEX.generated.md for new baseline fields."
  } else {
    Generate-Index $Path $indexPath $true
  }
  Ensure-ProjectGovernanceFiles $Path
  Generate-AssetBoundaries $Path
  Write-InstallManifest $Path
  Write-ProjectExpertReadiness $Path
}

function Migrate-Project($Path) {
  if ([string]::IsNullOrWhiteSpace($Path) -or (-not (Test-Path $Path -PathType Container))) {
    throw "Project path not found: $Path"
  }
  if ($Force) {
    throw "migrate-project does not accept -Force; protected project assets must remain review-only."
  }
  Append-AgentsBlock (Join-Path $Path "AGENTS.md") "migrate"
  Update-Templates $Path
  Write-Host "Legacy project workflow migration completed: $Path"
  Write-Host "Existing project documents and source code were preserved. Review generated candidates before accepting them."
}

function Verify-Kit {
  Ensure-RootPluginJson $PluginSrc
  $validated = $false
  if (Test-Path $ValidatorPath) {
    python3 $ValidatorPath $PluginSrc
    $validated = ($LASTEXITCODE -eq 0)
  }
  if (-not $validated) {
    Write-Host "Codex validator unavailable in this environment; running basic plugin manifest check."
    $manifest = Join-Path $PluginSrc ".codex-plugin/plugin.json"
    $data = Get-Content -Raw $manifest | ConvertFrom-Json
    foreach ($field in @("name", "version", "description", "skills", "interface")) {
      if (-not $data.$field) {
        throw "Missing plugin manifest field: $field"
      }
    }
    $skillsPath = Join-Path $PluginSrc ($data.skills.Trim("./"))
    if (-not (Test-Path $skillsPath)) {
      throw "Skills directory not found: $skillsPath"
    }
  }
  $legacyPattern = "t" + "rae"
  $legacy = rg -n -i --hidden --glob '!.git/**' $legacyPattern $RootDir
  if ($LASTEXITCODE -eq 0) {
    Write-Error "Unexpected legacy source branding found.`n$legacy"
  }
  $riskPattern = "TO" + "DO|TB" + "D|\[TO" + "DO|place" + "holder|待" + "补|待" + "定|高压" + "红线|恐惧" + "诱导|Invoke " + "Tool|必须" + "调用|第一步" + "必须|严禁" + "自行处理"
  $risk = rg -n $riskPattern (Join-Path $RootDir "README.md") (Join-Path $RootDir "CHANGELOG.md") (Join-Path $RootDir "docs") $PluginSrc
  if ($LASTEXITCODE -eq 0) {
    Write-Error "Unexpected disallowed wording found.`n$risk"
  }
  $null = [scriptblock]::Create((Get-Content -Raw (Join-Path $RootDir "scripts/install.ps1")))
  python3 (Join-Path $RootDir "tests/test_asset_boundaries.py")
  if ($LASTEXITCODE -ne 0) {
    throw "Asset boundary regression tests failed"
  }
  python3 (Join-Path $RootDir "tests/test_document_templates.py")
  if ($LASTEXITCODE -ne 0) {
    throw "Document template regression tests failed"
  }
  python3 (Join-Path $RootDir "tests/test_document_ownership.py")
  if ($LASTEXITCODE -ne 0) {
    throw "Document ownership regression tests failed"
  }
  python3 (Join-Path $RootDir "tests/test_quality_validation_workflow.py")
  if ($LASTEXITCODE -ne 0) {
    throw "Quality validation workflow regression tests failed"
  }
  python3 (Join-Path $RootDir "tests/test_human_output.py")
  if ($LASTEXITCODE -ne 0) { throw "Human output regression tests failed" }
  python3 (Join-Path $RootDir "tests/test_target_clients_and_human_summary.py")
  if ($LASTEXITCODE -ne 0) {
    throw "Target client and human summary regression tests failed"
  }
  python3 (Join-Path $RootDir "tests/test_legacy_project_migration.py")
  if ($LASTEXITCODE -ne 0) {
    throw "Legacy project migration regression tests failed"
  }
  Review-BundledExperts $PluginSrc $false | Out-Null
  Write-Host "Verification passed."
}

switch ($Command) {
  "install-plugin" { Install-Plugin }
  "uninstall-plugin" { Uninstall-Plugin }
  "bootstrap-project" { Bootstrap-Project $ProjectPath }
  "migrate-project" { Migrate-Project $ProjectPath }
  "deactivate-project" { Deactivate-Project $ProjectPath }
  "update-templates" { Update-Templates $ProjectPath }
  "install-agents" { Install-ProjectAgents $ProjectPath }
  "generate-index" { Generate-Index $ProjectPath (Join-Path $ProjectPath "specs/global/INDEX.md") $Force }
  "expert-preflight" { Write-ProjectExpertReadiness $ProjectPath }
  "generate-asset-boundaries" { Generate-AssetBoundaries $ProjectPath }
  "accept-asset-boundaries" { Accept-AssetBoundaries $ProjectPath }
  "confirm-asset-boundaries" { Confirm-AssetBoundaries $ProjectPath }
  "check-assets" { Check-Assets $ProjectPath $false }
  "audit-assets" { Check-Assets $ProjectPath $true }
  "all" {
    Install-Plugin
    Bootstrap-Project $ProjectPath
    Verify-Kit
  }
  "verify" { Verify-Kit }
  default {
    Show-Usage
    exit 1
  }
}
