@echo off
REM ANTLR4 Batch File Wrapper
REM Usage: antlr4.bat [options] grammar_files...

set ANTLR_JAR=C:\antlr4\antlr-4.13.2-complete.jar

REM Check if ANTLR4 JAR exists
if not exist "%ANTLR_JAR%" (
    echo ❌ ANTLR4 JAR not found at: %ANTLR_JAR%
    echo Please download ANTLR4 from https://www.antlr.org/download.html
    echo And place the JAR file in C:\antlr4\ directory
    exit /b 1
)

REM Run ANTLR4 with Java
java -jar "%ANTLR_JAR%" %*
