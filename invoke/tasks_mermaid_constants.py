#!/usr/bin/env python3
"""
Constants for Tasks Mermaid Generator
Contains path configurations and execution settings
"""

from pathlib import Path

# Base directory (relative ke file ini)
BASE_DIR = Path(__file__).parent.parent

# Path configurations (absolute paths)
SOLMISASI_LILY_ABS_PATH = (
    BASE_DIR.parent / "solmisasi-lily" / "lib").resolve()
PARTITUR_ABS_PATH = (BASE_DIR.parent.parent / "data").resolve()
LILYPOND_VER = "2.25.33"
LILYPOND_BIN = (
    BASE_DIR.parent / f"lilypond-{LILYPOND_VER}" / "bin" / "lilypond").resolve()

# Execution configuration
DOCKER_OR_LOCAL = False  # False = use local Lilypond, True = use Docker
