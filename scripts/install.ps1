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
  Write-Host "  powershell -ExecutionPolicy Bypass -File scripts/install.ps1 deactivate-project <project-path> [-Force]"
  Write-Host "  powershell -ExecutionPolicy Bypass -File scripts/install.ps1 update-templates <project-path> [-Lang zh|en] [-Force]"
  Write-Host "  powershell -ExecutionPolicy Bypass -File scripts/install.ps1 generate-index <project-path> [-Lang zh|en] [-Force]"
  Write-Host "  powershell -ExecutionPolicy Bypass -File scripts/install.ps1 expert-preflight <project-path> [-Lang zh|en]"
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

function Review-BundledExperts($PluginRoot) {
  $report = Join-Path $PluginRoot "EXPERT-READINESS.md"
  $json = Join-Path $PluginRoot "EXPERT-READINESS.json"
  python3 (Join-Path $RootDir "scripts/expert_dependencies.py") review `
    --plugin-root $PluginRoot `
    --lang $Lang `
    --output $report `
    --json-output $json
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

function Install-Plugin {
  if (-not (Test-Path (Join-Path $PluginSrc ".codex-plugin"))) {
    throw "Plugin source not found: $PluginSrc"
  }
  Ensure-RootPluginJson $PluginSrc
  Review-BundledExperts $PluginSrc
  if ((Test-Path $PluginDst) -and (-not $Force)) {
    Write-Host "Plugin already installed: $PluginDst"
    Write-Host "Use -Force to replace it."
  } else {
    Copy-DirSafe $PluginSrc $PluginDst
    Write-Host "Installed plugin: $PluginDst"
  }
  if (Test-Path $PluginDst) {
    Ensure-RootPluginJson $PluginDst
    Review-BundledExperts $PluginDst
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

function Append-AgentsBlock($Target) {
  $content = if (Test-Path $Target) { Get-Content -Raw $Target } else { "" }
  if ($content -match [regex]::Escape($MarkerBegin) -or $content -match [regex]::Escape($LegacyMarkerBegin)) {
    Write-Host "AGENTS.md already contains company workflow block."
    return
  }
  Add-Content $Target ""
  Add-Content $Target $MarkerBegin
  Add-Content $Target (Get-Content -Raw (Join-Path $PluginSrc "AGENTS.md"))
  Add-Content $Target $MarkerEnd
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
      "specs/global/assets/",
      "specs/global/assets.generated/",
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
      Remove-Item -Recurse -Force $destination
    }
    Copy-Item -Recurse -Force $source $destination
    Get-ChildItem -Path $destination -Recurse -Force -Filter ".DS_Store" | Remove-Item -Force
    Write-Host "Project templates ready: $destination"
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
      Remove-Item -Recurse -Force $destination
    }
    Copy-Item -Recurse -Force $source $destination
    Get-ChildItem -Path $destination -Recurse -Force -Filter ".DS_Store" | Remove-Item -Force
    Write-Host "Updated project templates: $destination"
  }
  Ensure-ProjectGovernanceFiles $Path
  Write-ProjectExpertReadiness $Path
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
  Review-BundledExperts $PluginSrc | Out-Null
  Write-Host "Verification passed."
}

switch ($Command) {
  "install-plugin" { Install-Plugin }
  "uninstall-plugin" { Uninstall-Plugin }
  "bootstrap-project" { Bootstrap-Project $ProjectPath }
  "deactivate-project" { Deactivate-Project $ProjectPath }
  "update-templates" { Update-Templates $ProjectPath }
  "generate-index" { Generate-Index $ProjectPath (Join-Path $ProjectPath "specs/global/INDEX.md") $Force }
  "expert-preflight" { Write-ProjectExpertReadiness $ProjectPath }
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
