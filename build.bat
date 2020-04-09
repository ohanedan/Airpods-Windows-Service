@echo off
pyinstaller -F --clean --distpath build -n airpods-windows-service --workpath temp --hiddenimport win32timezone --add-data dll/BleakUWPBridge.dll;. src/service.py
@RD /S /Q temp
del "airpods-windows-service.spec" /s /f /q
@RD /S /Q "src/__pycache__"
set /p DUMMY=Press ENTER to continue...