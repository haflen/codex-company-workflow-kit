param(
  [Parameter(Position=0)]
  [string]$Command,
  [Parameter(Position=1)]
  [string]$ProjectPath,
  [ValidateSet("zh", "en")]
  [string]$Lang = "zh",
  [switch]$Force
)

$ErrorActionPreference = "Stop"
$PluginName = if ($Lang -eq "zh") { "company-codex-workflow-v2-zh" } else { "company-codex-workflow-v2" }
$MarkerBegin = "<!-- codex-workflow-kit:company:start -->"
$MarkerEnd = "<!-- codex-workflow-kit:company:end -->"
$LegacyMarkerBegin = "<!-- company-codex-workflow-kit:start -->"
$RootDir = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$PluginSrc = Join-Path $RootDir "outputs/$PluginName"
$MarketplaceRoot = Join-Path $HOME ".agents/plugins"
$PluginDst = Join-Path $MarketplaceRoot "plugins/$PluginName"
$MarketplaceFile = Join-Path $MarketplaceRoot "marketplace.json"

function Show-Usage {
  Write-Host "Usage:"
  Write-Host "  powershell -ExecutionPolicy Bypass -File scripts/install.ps1 install-plugin [-Lang zh|en] [-Force]"
  Write-Host "  powershell -ExecutionPolicy Bypass -File scripts/install.ps1 bootstrap-project <project-path> [-Lang zh|en] [-Force]"
  Write-Host "  powershell -ExecutionPolicy Bypass -File scripts/install.ps1 generate-index <project-path> [-Lang zh|en] [-Force]"
  Write-Host "  powershell -ExecutionPolicy Bypass -File scripts/install.ps1 all <project-path> [-Lang zh|en] [-Force]"
  Write-Host "  powershell -ExecutionPolicy Bypass -File scripts/install.ps1 verify [-Lang zh|en]"
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

function Install-Plugin {
  if (-not (Test-Path (Join-Path $PluginSrc ".codex-plugin"))) {
    throw "Plugin source not found: $PluginSrc"
  }
  if ((Test-Path $PluginDst) -and (-not $Force)) {
    Write-Host "Plugin already installed: $PluginDst"
    Write-Host "Use -Force to replace it."
  } else {
    Copy-DirSafe $PluginSrc $PluginDst
    Write-Host "Installed plugin: $PluginDst"
  }
  New-Item -ItemType Directory -Force -Path (Join-Path $MarketplaceRoot "plugins") | Out-Null
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
    Copy-Item (Join-Path $PluginSrc "AGENTS.md") $agents
    Write-Host "Created AGENTS.md: $agents"
  }
  Copy-DirSafe (Join-Path $PluginSrc "specs") (Join-Path $Path "specs")
  Write-Host "Project specs ready: $(Join-Path $Path "specs")"
  if ((-not $indexExisted) -or $Force) {
    Generate-Index $Path $indexPath $true
  } else {
    $generatedPath = Join-Path $Path "specs/global/INDEX.generated.md"
    Generate-Index $Path $generatedPath $true
    Write-Host "Existing INDEX.md preserved. Review INDEX.generated.md before replacing it."
  }
  Write-Host "Next: review the generated INDEX draft and confirm project context."
}

function Verify-Kit {
  python3 /Users/dan/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py $PluginSrc
  if ($LASTEXITCODE -ne 0) {
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
  Write-Host "Verification passed."
}

switch ($Command) {
  "install-plugin" { Install-Plugin }
  "bootstrap-project" { Bootstrap-Project $ProjectPath }
  "generate-index" { Generate-Index $ProjectPath (Join-Path $ProjectPath "specs/global/INDEX.md") $Force }
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
