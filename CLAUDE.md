# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

PyQt5 desktop application for mass file conversion. Converts `jpg↔png` (via Pillow) and `txt↔md` (content-preserving copy). Produces a portable single-file `.exe` via PyInstaller.

## Environment

Conda environment: `massconvertingtool`

```bash
conda activate massconvertingtool
```

All commands below assume this environment is active (or use `conda run -n massconvertingtool <cmd>`).

## Commands

```bash
# Run app from source
python main.py

# Run all tests
pytest

# Run a single test file
pytest tests/test_converters.py

# Run a single test
pytest tests/test_converters.py::TestJpgToPng::test_output_format_is_png

# Build portable exe (Windows)
build.bat
# Output: dist\MassFileConverter.exe
```

## Architecture

```
app/
  converters.py     — ConversionPair dataclass + jpg_to_png / png_to_jpg / copy_content
                      functions + CONVERSIONS registry dict (the single source of truth
                      for all supported conversion types)
  scanner.py        — scan_files(): collects files by extension from a list of paths/dirs
  worker.py         — ConversionWorker(QThread): runs conversions in background,
                      emits progress / log_message / finished signals
  ui/
    main_window.py  — MainWindow assembles source picker, options panel,
                      progress bar, and log panel
```

**Data flow:** `MainWindow` calls `scan_files()` to count/list files, then passes them to `ConversionWorker` which calls the converter function and emits signals back to the UI.

**Adding a new conversion type:** add a function to `app/converters.py` and register a new `ConversionPair` in `CONVERSIONS`. No other files need changing.

## Build Notes

- `mass_converter.spec` — one-file, windowed (no console window), Pillow hidden imports included
- `*.spec` is gitignored by default; `!mass_converter.spec` exception is already in `.gitignore`
- `dist/` and `build/` are gitignored
