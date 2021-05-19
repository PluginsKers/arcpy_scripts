@echo off
echo Start loading %1
cd /d %~dp0
python ./lib/core.py %1
pause