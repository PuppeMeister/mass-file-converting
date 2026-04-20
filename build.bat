@echo off
setlocal
echo === Mass File Converter — Build ===
echo.

echo [1/3] Installing runtime dependencies...
pip install -r requirements.txt
if errorlevel 1 goto :error

echo.
echo [2/3] Installing PyInstaller...
pip install "pyinstaller>=6.0"
if errorlevel 1 goto :error

echo.
echo [3/3] Building portable executable...
pyinstaller mass_converter.spec --clean --noconfirm
if errorlevel 1 goto :error

echo.
echo ============================================
echo  Build complete!
echo  Executable: dist\MassFileConverter.exe
echo ============================================
goto :end

:error
echo.
echo Build failed. See errors above.
exit /b 1

:end
pause
