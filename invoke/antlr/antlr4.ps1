#!/usr/bin/env pwsh

# ANTLR4 PowerShell Wrapper Script
# Usage: .\antlr4.ps1 [options] grammar_files...

param(
    [Parameter(ValueFromRemainingArguments=$true)]
    [string[]]$Arguments
)

# ANTLR4 JAR path - adjust if needed
$antlrJar = "C:\antlr4\antlr-4.13.2-complete.jar"

# Check if ANTLR4 JAR exists
if (-not (Test-Path $antlrJar)) {
    Write-Host "❌ ANTLR4 JAR not found at: $antlrJar" -ForegroundColor Red
    Write-Host "Please download ANTLR4 from https://www.antlr.org/download.html" -ForegroundColor Yellow
    Write-Host "And place the JAR file in C:\antlr4\ directory" -ForegroundColor Yellow
    exit 1
}

# Run ANTLR4 with Java
try {
    & java -jar $antlrJar $Arguments
} catch {
    Write-Host "❌ Error running ANTLR4: $_" -ForegroundColor Red
    Write-Host "Make sure Java is installed and in PATH" -ForegroundColor Yellow
    exit 1
}
