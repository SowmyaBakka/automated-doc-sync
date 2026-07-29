param(
    [Parameter(Mandatory = $true)]
    [string]$IssueKey,

    [string]$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")),

    [switch]$Force,

    [switch]$DryRun
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

if ($IssueKey -notmatch '^[A-Z]+-\d+$') {
    throw "IssueKey must match the format TEAM-123"
}

function Test-GitRefExists {
    param([string]$Ref)

    git show-ref --verify --quiet $Ref
    return ($LASTEXITCODE -eq 0)
}

function Invoke-GitChecked {
    param([string]$Command)

    Invoke-Expression $Command | Out-Null
    if ($LASTEXITCODE -ne 0) {
        throw "Git command failed: $Command"
    }
}

function Ensure-StoryBranch {
    param([string]$IssueKey)

    $targetBranch = "feature/$($IssueKey.ToLowerInvariant())"
    $currentBranch = (git branch --show-current).Trim()

    if ($currentBranch -eq $targetBranch) {
        Write-Host "Already on story branch $targetBranch"
        return
    }

    if (Test-GitRefExists -Ref "refs/heads/$targetBranch") {
        Invoke-GitChecked -Command "git checkout $targetBranch"
        Write-Host "Switched to existing story branch $targetBranch"
        return
    }

    if (Test-GitRefExists -Ref "refs/heads/main") {
        if ($currentBranch -ne "main") {
            Invoke-GitChecked -Command "git checkout main"
        }

        Invoke-GitChecked -Command "git checkout -b $targetBranch"
        Write-Host "Created story branch $targetBranch from local main"
        return
    }

    if (Test-GitRefExists -Ref "refs/remotes/origin/main") {
        Invoke-GitChecked -Command "git checkout -b $targetBranch origin/main"
        Write-Host "Created story branch $targetBranch from origin/main"
        return
    }

    throw "Cannot create $targetBranch because neither local main nor origin/main exists."
}

function Write-StateFile {
    param(
        [string]$Path,
        [hashtable]$State
    )

    $directory = Split-Path -Parent $Path
    if (-not (Test-Path $directory)) {
        New-Item -ItemType Directory -Path $directory | Out-Null
    }

    $State | ConvertTo-Json -Depth 6 | Set-Content -Path $Path
}

Set-Location $RepoRoot
Ensure-StoryBranch -IssueKey $IssueKey

$storyDirectory = Join-Path $RepoRoot ".sdlc\$IssueKey"
$statePath = Join-Path $storyDirectory "pipeline-state.json"

if ((Test-Path $statePath) -and -not $Force) {
    throw "State file already exists at $statePath. Use -Force to reset it."
}

$state = @{
    issueKey = $IssueKey
    currentStage = "requirements"
    status = "pending"
    approved = $false
    lastAgent = "sdlc-requirements-agent"
    artifacts = @{}
    updatedAt = (Get-Date).ToUniversalTime().ToString("o")
}

Write-StateFile -Path $statePath -State $state
Write-Host "Initialized state file at $statePath"

if ($DryRun) {
    Write-Host "Dry run enabled: kickoff agent launch skipped"
    exit 0
}

code chat -m agent "@sdlc-requirements-agent Capture requirements for $IssueKey" --reuse-window