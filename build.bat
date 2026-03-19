@echo off
echo Building SAA Learning Hub...
echo.
python -m PyInstaller --noconfirm --distpath "./compiled" --workpath "./build_temp" SAA_Learning_Hub.spec
echo.
echo Build complete! Check the 'compiled' folder for SAA_Learning_Hub.exe
pause
