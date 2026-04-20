# Prompt Documentation

This file records all user prompts and the corresponding actions taken by Claude Code.

---

## Session 1 — 2026-04-20

### Prompt 1

**User:**
> create the pyQT based desktop app to mass convert type files inside a folder or some selected folder or selected files. The converting examples are "jpg -> png", "png -> jpg", "txt -> md", "md -> txt". the final result of the application should be portable .exe file, no need to install the application to the OS. The code should follow the python coding convention and I demand you to do unit testing before finalising the app. Document every prompt I give to you and your related response to "prompt-documentation.md".

**Response / Actions Taken:**

Built a complete PyQt5 desktop application for mass file conversion.

**Architecture:**

| File | Responsibility |
|------|---------------|
| `main.py` | Entry point — creates `QApplication`, shows `MainWindow` |
| `app/converters.py` | `ConversionPair` dataclass + 3 converter functions + `CONVERSIONS` registry dict |
| `app/scanner.py` | `scan_files()` — collects matching files from paths/directories |
| `app/worker.py` | `ConversionWorker(QThread)` — background conversion, emits progress/log/finished signals |
| `app/ui/main_window.py` | `MainWindow(QMainWindow)` — source picker, options, progress bar, log panel |
| `tests/conftest.py` | Shared pytest fixtures (real sample files via `tmp_path`) |
| `tests/test_converters.py` | 17 unit tests for all conversion functions and the registry |
| `tests/test_scanner.py` | 10 unit tests for `scan_files()` |
| `mass_converter.spec` | PyInstaller one-file windowed exe spec |
| `build.bat` | Windows batch build script |

**Conversion methods:**

| From | To | Method |
|------|----|--------|
| JPG | PNG | `PIL.Image.open().save(format="PNG")` |
| PNG | JPG | `PIL.Image.convert("RGB").save(format="JPEG", quality=95)` — handles RGBA |
| TXT | MD | `shutil.copy2` — content-preserving copy with new extension |
| MD | TXT | `shutil.copy2` — content-preserving copy with new extension |

**Test results:** 27/27 passed (Python 3.12.13, pytest 9.0.3, conda env `massconvertingtool`).

---

### Prompt 2

**User:**
> Just tell me, the list of requirements / requirements.txt then I'm gonna create isolate pyenv environment and I'll tell you which environment then you may proceed the work

**Response / Actions Taken:**

Listed runtime deps (`PyQt5>=5.15`, `Pillow>=10.0`), dev deps (`pytest>=8.0`), and build dep (`pyinstaller>=6.0`). Waited for user to set up environment.

---

### Prompt 3

**User:**
> you can install the requirement to a new setup conda environment with this command "conda activate massconvertingtool" so install all required dependencies there and use the environment for the development process.

**Response / Actions Taken:**

Used `conda run -n massconvertingtool` to install all dependencies. All packages were already present. Ran `pytest -v` in the environment — **27/27 tests passed**.
