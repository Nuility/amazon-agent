param(
    [string]$WorkspaceRoot = "D:\云码道\amazon-agent-feature-ui-enhancement"
)

$ErrorActionPreference = "Stop"

$sourcesDir = Join-Path $WorkspaceRoot ".sources"
$packDir = Join-Path $WorkspaceRoot "integration_pack"
$wimoorRepo = Join-Path $sourcesDir "wimoor"
$copilotkitRepo = Join-Path $sourcesDir "CopilotKit"
$wimoorTarget = Join-Path $packDir "wimoor-advertising\source"
$copilotTarget = Join-Path $packDir "copilotkit-agent-ui\source-reference"

New-Item -ItemType Directory -Force -Path $sourcesDir, $wimoorTarget, $copilotTarget | Out-Null

if (-not (Test-Path $wimoorRepo)) {
    git clone --depth 1 https://github.com/wimoor-erp/wimoor.git $wimoorRepo
}

if (-not (Test-Path $copilotkitRepo)) {
    git clone --depth 1 https://github.com/CopilotKit/CopilotKit.git $copilotkitRepo
}

$wimoorAdv = Join-Path $wimoorRepo "wimoor-amazon-adv"
if (-not (Test-Path $wimoorAdv)) {
    throw "Wimoor advertising module not found: $wimoorAdv"
}

Copy-Item -Recurse -Force $wimoorAdv (Join-Path $wimoorTarget "wimoor-amazon-adv")

$dependencyCandidates = @(
    "pom.xml",
    "wimoor-common",
    "wimoor-system",
    "wimoor-amazon"
)

foreach ($item in $dependencyCandidates) {
    $from = Join-Path $wimoorRepo $item
    if (Test-Path $from) {
        Copy-Item -Recurse -Force $from (Join-Path $wimoorTarget $item)
    }
}

$copilotReferenceItems = @(
    "packages",
    "examples",
    "docs",
    "README.md",
    "package.json",
    "pnpm-workspace.yaml"
)

foreach ($item in $copilotReferenceItems) {
    $from = Join-Path $copilotkitRepo $item
    if (Test-Path $from) {
        Copy-Item -Recurse -Force $from (Join-Path $copilotTarget $item)
    }
}

Write-Host "Sources fetched and copied into integration_pack."

