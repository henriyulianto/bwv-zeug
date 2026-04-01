#!/usr/bin/env pwsh

# Build script for ANTLR grammar files (PowerShell version)
Write-Host "🚀 Building ANTLR Grammar Files" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green

# Clean up old generated files
Write-Host "🧹 Cleaning up old generated files..." -ForegroundColor Yellow
Remove-Item -Force -ErrorAction SilentlyContinue MermaidPipeline*.py, *.tokens, *.interp

# Generate lexer classes
Write-Host "📝 Generating lexer classes..." -ForegroundColor Yellow
.\antlr4.ps1 -Dlanguage=Python3 MermaidPipelineLexer.g4

# Generate parser classes
Write-Host "📝 Generating parser classes..." -ForegroundColor Yellow
.\antlr4.ps1 -Dlanguage=Python3 MermaidPipelineParser.g4

# List generated files
Write-Host "✅ Generated files:" -ForegroundColor Green
Get-ChildItem MermaidPipeline*.py | ForEach-Object {
    Write-Host "  $($_.Name)" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "🎉 Build complete!" -ForegroundColor Green
Write-Host "💡 You can now run: python tasks_mermaid_generator.py -i TASKS.mmd -o tasks_generated.py" -ForegroundColor Cyan
Write-Host ""
Write-Host "📝 Note: Run this script with '.\build_antlr.ps1' in PowerShell" -ForegroundColor Gray
