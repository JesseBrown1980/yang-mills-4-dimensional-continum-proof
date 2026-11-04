@echo off
cd /d C:\tmp\opus55\recheck-02c-20261103\run
start "" /belownormal /b /wait python3 -I -X utf8 t.py > base.out 2> base.err
echo exit=%ERRORLEVEL% > base.rc
