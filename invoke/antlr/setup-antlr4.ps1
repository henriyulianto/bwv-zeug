#!/usr/bin/env pwsh

# ANTLR4 Setup Script - Add to PATH
# This script adds ANTLR4 to system PATH for easy access

Write-Host "🚀 ANTLR4 Setup Script" -ForegroundColor Green
Write-Host "======================" -ForegroundColor Green

# Check if ANTLR4 directory exists
$antlrDir = "C:\antlr4"
if (-not (Test-Path $antlrDir)) {
    Write-Host "❌ ANTLR4 directory not found: $antlrDir" -ForegroundColor Red
    Write-Host "Please create the directory and place antlr-4.13.2-complete.jar inside" -ForegroundColor Yellow
    exit 1
}

# Check if ANTLR4 JAR exists
$antlrJar = Join-Path $antlrDir "antlr-4.13.2-complete.jar"
if (-not (Test-Path $antlrJar)) {
    Write-Host "❌ ANTLR4 JAR not found: $antlrJar" -ForegroundColor Red
    Write-Host "Please download ANTLR4 from https://www.antlr.org/download.html" -ForegroundColor Yellow
    exit 1
}

# Get current PATH
$currentPath = [Environment]::GetEnvironmentVariable("PATH", "User")

# Check if ANTLR4 already in PATH
if ($currentPath -like "*$antlrDir*") {
    Write-Host "✅ ANTLR4 already in PATH" -ForegroundColor Green
} else {
    # Add ANTLR4 to PATH
    $newPath = $currentPath + ";$antlrDir"
    [Environment]::SetEnvironmentVariable("PATH", $newPath, "User")
    Write-Host "✅ Added ANTLR4 to PATH" -ForegroundColor Green
    Write-Host "🔄 Please restart PowerShell to use the updated PATH" -ForegroundColor Yellow
}

# Test ANTLR4 command
Write-Host ""
Write-Host "🧪 Testing ANTLR4 command..." -ForegroundColor Yellow

# Create temporary test grammar
$testGrammar = @'
grammar Test;
prog: ID+;
ID: [a-z]+;
WS: [ \t\r\n]+ -> skip;
'@

Set-Content -Path "Test.g4" -Value $testGrammar

# Test ANTLR4
try {
    & java -jar $antlrJar -version 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ ANTLR4 JAR works correctly" -ForegroundColor Green
        
        # Test grammar generation
        & java -jar $antlrJar Test.g4 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Grammar generation works" -ForegroundColor Green
        } else {
            Write-Host "⚠️  Grammar generation test failed" -ForegroundColor Yellow
        }
        
        # Clean up test files
        Remove-Item -Force -ErrorAction SilentlyContinue Test.g4, Test*.py, Test*.tokens, Test*.interp
    } else {
        Write-Host "❌ ANTLR4 JAR test failed" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ Error testing ANTLR4: $_" -ForegroundColor Red
}

Write-Host ""
Write-Host "🎉 ANTLR4 setup complete!" -ForegroundColor Green
Write-Host "💡 You can now use:" -ForegroundColor Cyan
Write-Host "   - .\antlr4.ps1 -Dlanguage=Python3 MyGrammar.g4" -ForegroundColor Gray
Write-Host "   - .\antlr4.bat -Dlanguage=Python3 MyGrammar.g4" -ForegroundColor Gray
Write-Host "   - java -jar C:\antlr4\antlr-4.13.2-complete.jar -Dlanguage=Python3 MyGrammar.g4" -ForegroundColor Gray
