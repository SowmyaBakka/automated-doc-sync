param(
    [string]$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")),
    [string]$IssueKey,
    [switch]$DryRun
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Write-HookLog {
    param([string]$Message)

    $logPath = Join-Path $RepoRoot ".github\hooks\sdlc-hook.log"
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Add-Content -Path $logPath -Value "[$timestamp] $Message"
}

function Read-JsonHashtable {
    param([string]$Path)

    return Get-Content -Raw -Path $Path | ConvertFrom-Json -AsHashtable
}

function Get-HeadChangedFiles {
    $files = git diff-tree --no-commit-id --name-only -r HEAD
    if ($LASTEXITCODE -ne 0) {
        throw "Unable to inspect changed files for HEAD"
    }

    return @($files | Where-Object { -not [string]::IsNullOrWhiteSpace($_) })
}

function Get-IssueKeyFromChangedFiles {
    param([string[]]$ChangedFiles)

    foreach ($file in $ChangedFiles) {
        $normalizedPath = $file -replace "\\", "/"
        $match = [regex]::Match($normalizedPath, "^\.sdlc/([A-Z]+-\d+)/")
        if ($match.Success) {
            return $match.Groups[1].Value
        }
    }

    return $null
}

function Get-StageConfig {
    param(
        [hashtable[]]$Stages,
        [string]$StageId
    )

    foreach ($stage in $Stages) {
        if ($stage.id -eq $StageId) {
            return $stage
        }
    }

    return $null
}

function Get-CompletionArtifactPath {
    param(
        [hashtable]$State,
        [hashtable]$Stage,
        [string]$IssueKey
    )

    if ($State.ContainsKey("artifacts") -and $State.artifacts.ContainsKey($Stage.id)) {
        return $State.artifacts[$Stage.id]
    }

    if ($Stage.ContainsKey("completionArtifact") -and -not [string]::IsNullOrWhiteSpace($Stage.completionArtifact)) {
        return ".sdlc/$IssueKey/$($Stage.completionArtifact)"
    }

    return $null
}

function Test-ImplementationStageReadyForHandoff {
    param(
        [hashtable]$State,
        [string]$IssueKey
    )

    $summaryPath = Join-Path $RepoRoot ".sdlc/$IssueKey/implementation-summary.md"
    if (Test-Path $summaryPath) {
        return $true
    }

    $requiredArtifacts = @("implementation-source", "implementation-tests")
    foreach ($artifactKey in $requiredArtifacts) {
        if (-not ($State.ContainsKey("artifacts") -and $State.artifacts.ContainsKey($artifactKey))) {
            Write-HookLog "State not ready: missing fallback artifact '$artifactKey' for implementation handoff"
            return $false
        }

        $artifactPath = $State.artifacts[$artifactKey]
        $absoluteArtifactPath = Join-Path $RepoRoot $artifactPath
        if (-not (Test-Path $absoluteArtifactPath)) {
            Write-HookLog "State not ready: fallback artifact missing at $absoluteArtifactPath"
            return $false
        }
    }

    Write-HookLog "Implementation summary missing; using implementation-source and implementation-tests as fallback handoff evidence"
    return $true
}

function Test-StateReadyForHandoff {
    param(
        [hashtable]$State,
        [hashtable]$Stage,
        [string]$IssueKey
    )

    if ($State.status -ne "completed") {
        Write-HookLog "State not ready: status='$($State.status)' for stage '$($State.currentStage)'"
        return $false
    }

    if ($State.ContainsKey("approved") -and -not $State.approved) {
        Write-HookLog "State not ready: stage '$($State.currentStage)' is not approved"
        return $false
    }

    if ($Stage.id -eq "implementation") {
        return (Test-ImplementationStageReadyForHandoff -State $State -IssueKey $IssueKey)
    }

    $artifactPath = Get-CompletionArtifactPath -State $State -Stage $Stage -IssueKey $IssueKey
    if ([string]::IsNullOrWhiteSpace($artifactPath)) {
        Write-HookLog "State not ready: no completion artifact configured for stage '$($Stage.id)'"
        return $false
    }

    $absoluteArtifactPath = Join-Path $RepoRoot $artifactPath
    if (-not (Test-Path $absoluteArtifactPath)) {
        Write-HookLog "State not ready: completion artifact missing at $absoluteArtifactPath"
        return $false
    }

    return $true
}

function Invoke-Agent {
    param(
        [string]$AgentName,
        [string]$Prompt
    )

    Write-HookLog "Invoking agent @$AgentName with prompt: $Prompt"
    if ($DryRun) {
        Write-HookLog "Dry run enabled: agent invocation skipped"
        return
    }

    code chat -m agent "@$AgentName $Prompt" --reuse-window | Out-Null
}

try {
    Set-Location $RepoRoot

    $configPath = Join-Path $RepoRoot ".github\hooks\sdlc-pipeline.json"
    if (-not (Test-Path $configPath)) {
        Write-HookLog "No pipeline config found at $configPath"
        exit 0
    }

    $pipeline = Read-JsonHashtable -Path $configPath
    $changedFiles = @(Get-HeadChangedFiles)
    if ($changedFiles.Count -eq 0) {
        Write-HookLog "No changed files found for HEAD"
        exit 0
    }

    $headCommit = (git rev-parse --short HEAD).Trim()
    Write-HookLog "Evaluating HEAD $headCommit with changed files: $($changedFiles -join ', ')"

    if (-not $IssueKey) {
        $IssueKey = Get-IssueKeyFromChangedFiles -ChangedFiles $changedFiles
    }

    if ([string]::IsNullOrWhiteSpace($IssueKey)) {
        Write-HookLog "No story-scoped .sdlc changes detected for HEAD"
        exit 0
    }

    $stateFileName = if ($pipeline.ContainsKey("stateFileName")) { $pipeline.stateFileName } else { "pipeline-state.json" }
    $relativeStatePath = ".sdlc/$IssueKey/$stateFileName"
    $statePath = Join-Path $RepoRoot $relativeStatePath
    if (-not (Test-Path $statePath)) {
        Write-HookLog "State file not found at $statePath"
        exit 0
    }

    $normalizedChangedFiles = @($changedFiles | ForEach-Object { $_ -replace "\\", "/" })
    if ($normalizedChangedFiles -notcontains $relativeStatePath) {
        Write-HookLog "State file unchanged in HEAD; skipping orchestration for $IssueKey"
        exit 0
    }

    $state = Read-JsonHashtable -Path $statePath
    if (-not $state.ContainsKey("currentStage") -or [string]::IsNullOrWhiteSpace($state.currentStage)) {
        Write-HookLog "Invalid state file: currentStage is missing"
        exit 0
    }

    $currentStage = Get-StageConfig -Stages $pipeline.stages -StageId $state.currentStage
    if ($null -eq $currentStage) {
        Write-HookLog "Unknown current stage '$($state.currentStage)' in $relativeStatePath"
        exit 0
    }

    if (-not (Test-StateReadyForHandoff -State $state -Stage $currentStage -IssueKey $IssueKey)) {
        exit 0
    }

    $nextStageId = $currentStage.nextStage
    if ([string]::IsNullOrWhiteSpace($nextStageId)) {
        Write-HookLog "Stage '$($currentStage.id)' is terminal; no next agent to invoke"
        exit 0
    }

    $nextStage = Get-StageConfig -Stages $pipeline.stages -StageId $nextStageId
    if ($null -eq $nextStage) {
        Write-HookLog "Pipeline misconfigured: next stage '$nextStageId' was not found"
        exit 0
    }

    $prompt = $currentStage.promptTemplate.Replace("{ISSUE_KEY}", $IssueKey)
    Write-HookLog "State ready for handoff: currentStage='$($currentStage.id)' nextStage='$($nextStage.id)'"
    Invoke-Agent -AgentName $currentStage.agent -Prompt $prompt
    Write-HookLog "Stage handoff to '$($nextStage.id)' executed successfully"
}
catch {
    Write-HookLog "Hook error: $($_.Exception.Message)"
    exit 1
}
