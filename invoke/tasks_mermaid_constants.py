#!/usr/bin/env python3
"""
Constants for Tasks Mermaid Generator
Contains path configurations and execution settings
"""

from pathlib import Path

# Base directory (relative ke file ini)
BASE_DIR = Path(__file__).parent.parent

# Path configurations (absolute paths with fallbacks)


def safe_resolve(path: Path, fallback: str = None) -> Path:
    """Safely resolve path with fallback if resolution fails."""
    try:
        return path.resolve()
    except (OSError, RuntimeError):
        if fallback:
            # Expand shell variables (e.g., $HOME, $USER) in fallback
            import os
            expanded_fallback = os.path.expandvars(fallback)
            return Path(expanded_fallback)
        return path


def get_lilypond_bin() -> Path:
    """Get lilypond binary path, checking system PATH first."""
    import shutil
    import os
    import platform

    # First check if lilypond is available in PATH
    lilypond_in_path = shutil.which('lilypond')
    if lilypond_in_path:
        return "lilypond"

    # If not in PATH, use the defined path with fallback
    # Add .exe extension on Windows
    lilypond_binary = 'lilypond.exe' if platform.system() == 'Windows' else 'lilypond'

    return safe_resolve(
        BASE_DIR.parent / f"lilypond-{LILYPOND_VER}" / "bin" / lilypond_binary,
        f"$HOME/lilypond/lilypond-{LILYPOND_VER}/bin/{lilypond_binary}"
    )


# Sesuaikan SOLMISASI_LIB_NAME dengan yang digunakan
# Jika menggunakan solmisasi-lily, ganti dengan
# "solmisasi-lily/lib"
SOLMISASI_LIB_NAME = "solmisasi-ly"
SOLMISASI_LIB_ABS_PATH = safe_resolve(
    # Expected: ../solmisasi-ly or ../solmisasi-lily/lib
    BASE_DIR.parent / SOLMISASI_LIB_NAME,
    f"$HOME/projects/{SOLMISASI_LIB_NAME}"  # Your fallback
)

PARTITUR_DATA_ABS_PATH = safe_resolve(
    BASE_DIR.parent.parent / "data",  # Expected: ../../data
    "$HOME/projects/partitur-data"  # Your fallback
)

LILYPOND_VER = "2.25.34"
LILYPOND_BIN = get_lilypond_bin()  # Auto-detect: PATH first, then defined paths

# Execution configuration
USE_BWV_LILYPOND_INCLUDES = False
USE_DOCKER_FOR_LILYPOND = False  # False = use local Lilypond, True = use Docker
