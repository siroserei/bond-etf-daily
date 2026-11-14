@echo off
cd /d "%~dp0"
python update_data.py
if errorlevel 1 goto end
git add data.json
git diff --cached --quiet
if not errorlevel 1 (
  echo No new data to publish.
  goto end
)
git commit -m "Update daily ETF data"
if errorlevel 1 goto end
git push origin main
:end
pause
