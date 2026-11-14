@echo off
cd /d "%~dp0"
python update_data.py
if errorlevel 1 goto end
git add data.json
git commit -m "Update daily ETF data"
git push origin main
:end
pause
