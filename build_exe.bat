@echo off
REM ============================================================
REM  Builds "Repo Downloader.exe" from repo_downloader.py
REM  Put this file in the same folder as repo_downloader.py
REM  (or repo_downloader.pyw) and double-click it.
REM  You only need Python for this one-off build step.
REM ============================================================

cd /d "%~dp0"

set SCRIPT=repo_downloader.py
if not exist "%SCRIPT%" set SCRIPT=repo_downloader.pyw
if not exist "%SCRIPT%" (
    echo Could not find repo_downloader.py in this folder.
    goto error
)

REM Find a Python that actually runs ("where python" can find the
REM Microsoft Store placeholder, which isn't a real Python)
set PY=
py -c "import sys" >nul 2>&1 && set PY=py
if not defined PY python -c "import sys" >nul 2>&1 && set PY=python
if not defined PY (
    echo Could not find a working Python.
    goto error
)

echo.
echo [1/2] Installing the packaging tool (PyInstaller)...
%PY% -m pip install --upgrade pyinstaller || goto error

echo.
echo [2/2] Building the .exe - this takes a minute...
%PY% -m PyInstaller --onefile --windowed --clean --noconfirm --name "Repo Downloader" "%SCRIPT%" || goto error

echo.
echo ============================================================
echo  Done! Your app is:  dist\Repo Downloader.exe
echo  Copy that one file anywhere - the other folders can be deleted.
echo ============================================================
explorer dist
pause
exit /b 0

:error
echo.
echo Build failed - see the messages above.
echo Check Python is installed (python.org, tick "Add Python to PATH").
pause
exit /b 1
