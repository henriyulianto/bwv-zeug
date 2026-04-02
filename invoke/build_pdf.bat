@echo off
echo 🐳 Building LilyPond PDF...

REM Parse arguments: %1=INCLUDES %2=SONG_TITLE
set "INCLUDES=%1"
set "SONG_TITLE=%2"

REM Run LilyPond
lilypond %INCLUDES% -dno-point-and-click %SONG_TITLE%.ly
if %ERRORLEVEL% NEQ 0 (
    echo ❌ LilyPond failed
    exit /b 1
)

REM Create exports directory and move PDF
if not exist exports mkdir exports
move %SONG_TITLE%.pdf exports
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Move failed
    exit /b 1
)

echo ✅ PDF build complete
exit /b 0
