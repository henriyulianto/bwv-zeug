# Instalasi Dependencies bwv-zeug

## Prerequisites
- **Python 3.8+** (sesuai `pyproject.toml`)
- Git untuk clone repository
- Koneksi internet untuk download dependencies

---

## Metode 1: Menggunakan uv (Direkomendasikan)

### 1. Install uv
```bash
pip install uv
```

### 2. Install Dependencies
```bash
cd backend/bwv-zeug
uv pip install -r requirements.txt
```

### 3. Verifikasi Installation
```bash
python -c "import librosa, madmom, scipy, pandas, numpy; print('All dependencies installed successfully!')"
```

### Troubleshooting dengan uv
Jika ada error build madmom:
```bash
# Install build dependencies dulu
uv pip install Cython setuptools wheel numpy

# Kemudian install requirements
uv pip install -r requirements.txt --no-build-isolation
```

---

## Metode 2: Menggunakan pip (Tanpa uv)

### 1. Setup Virtual Environment (Disarankan)
```bash
# Buat virtual environment
python -m venv venv

# Aktifkan virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Update pip
pip install --upgrade pip
```

### 2. Install Dependencies
```bash
cd backend/bwv-zeug
pip install -r requirements.txt
```

### 3. Jika ada masalah dengan madmom build
```bash
# Install build dependencies dulu
pip install Cython setuptools wheel numpy

# Kemudian install requirements
pip install -r requirements.txt --no-build-isolation
```

### 4. Alternative: Install secara bertahap
```bash
# Install core packages dulu
pip install pandas numpy matplotlib

# Install audio processing
pip install librosa soundfile scipy

# Install MIDI tools  
pip install mido midi2audio

# Install beat detection
pip install madmom

# Install remaining packages
pip install invoke antlr4-python3-runtime PyYAML lxml
```

### 5. Verifikasi Installation
```bash
python -c "import librosa, madmom, scipy, pandas, numpy; print('All dependencies installed successfully!')"
```

---

## Platform-Specific Requirements

### Windows
- Install **Visual Studio Build Tools** (untuk kompilasi package)
- Pastikan Python dan pip ada di PATH

### macOS
- Install **Xcode Command Line Tools**:
```bash
xcode-select --install
```

### Linux
- Install development tools:
```bash
# Ubuntu/Debian:
sudo apt-get install python3-dev build-essential

# CentOS/RHEL:
sudo yum install python3-devel gcc gcc-c++
```

---

## Informasi Dependencies

### Total Packages: ~46 packages

### Core Dependencies:
- **pandas** (>=3.0.0) - Data processing
- **numpy** (>=1.24.0) - Numerical computing
- **matplotlib** (>=3.7.0) - Visualization

### Audio Processing:
- **librosa** (>=0.10.0) - Audio analysis
- **soundfile** (>=0.12.0) - Audio I/O
- **madmom** (>=0.16.0) - Beat detection
- **scipy** (>=1.9.0) - Signal processing

### MIDI Tools:
- **mido** (>=0.2.0) - MIDI processing
- **midi2audio** (>=0.1.1) - MIDI to audio conversion

### Build System:
- **invoke** (>=2.2.0) - Task management
- **antlr4-python3-runtime** (>=4.9.0) - ANTLR runtime

### File Format Support:
- **PyYAML** (>=6.0.0) - YAML parsing
- **lxml** (>=4.9.0) - XML processing

---

## Testing Installation

Setelah instalasi, test beberapa critical imports:

```python
# Test audio processing
import librosa
import madmom
import scipy

# Test data processing
import pandas
import numpy

# Test MIDI tools
import mido
import midi2audio

print("All critical dependencies working!")
```

---

## Common Issues & Solutions

### 1. Madmom Build Error
**Problem**: `ModuleNotFoundError: No module named 'Cython'`
**Solution**: Install Cython terlebih dahulu, kemudian install dengan `--no-build-isolation`

### 2. Visual Studio Build Tools Missing (Windows)
**Problem**: Error kompilasi C extension
**Solution**: Install Visual Studio Build Tools dengan C++ compiler

### 3. Permission Error
**Problem**: Tidak bisa install package
**Solution**: Gunakan virtual environment atau `--user` flag

### 4. Network Timeout
**Problem**: Download gagal
**Solution**: Coba lagi atau gunakan mirror lokal

---

## Performance Notes

- **uv**: Lebih cepat (2-10x) dan lebih efisien memory
- **pip**: Lebih lambat untuk package yang perlu kompilasi
- **Build time**: Madmom memerlukan 1-2 menit untuk kompilasi
- **Storage**: Total install size ~500MB-1GB

---

## Support

Jika mengalami masalah instalasi:
1. Pastikan Python 3.8+ terinstall
2. Gunakan virtual environment
3. Install build dependencies terlebih dahulu
4. Coba dengan `--no-build-isolation` untuk package yang bermasalah
