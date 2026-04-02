function Invoke-LoggedCommand {
    param(
        [Parameter(Mandatory=$true)]
        [string]$Command,
        
        [Parameter(Mandatory=$false)]
        [string]$LogFile = "build.log",
        
        [Parameter(Mandatory=$false)]
        [switch]$NoDisplay
    )
    
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logEntry = "[$timestamp] $Command"
    
    # Write to log file
    Add-Content -Path $LogFile -Value $logEntry
    
    # Execute and capture output
    try {
        $output = Invoke-Expression $Command
        if ($output) {
            if (-not $NoDisplay) {
                Write-Host $output
            }
            Add-Content -Path $LogFile -Value $output
        }
        
        # Log success
        $successMsg = "[$timestamp] SUCCESS: $Command"
        Add-Content -Path $LogFile -Value $successMsg
        if (-not $NoDisplay) {
            Write-Host $successMsg -ForegroundColor Green
        }
        
        return $output
    }
    catch {
        $errorMsg = "[$timestamp] ERROR: $Command - $_"
        Add-Content -Path $LogFile -Value $errorMsg
        if (-not $NoDisplay) {
            Write-Host $errorMsg -ForegroundColor Red
        }
        throw
    }
}

# Export function
Export-ModuleMember -Function Invoke-LoggedCommand
