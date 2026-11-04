@echo off
set E=C:\tmp\opus55\attack-4d-02c-20261103\rust\brute3.exe
set O=C:\tmp\opus55\recheck-02c-20261103\out
start "" /belownormal /b /wait %E% sitec 1 1 1 -1 -1 > %O%\sitec.out 2>&1
start "" /belownormal /b /wait %E% sitec 3 2 1 -1 2 >> %O%\sitec.out 2>&1
start "" /belownormal /b /wait %E% sitec 3 2 1 -1 -2 >> %O%\sitec.out 2>&1
start "" /belownormal /b /wait %E% sitec 1 -1 1 1 1 >> %O%\sitec.out 2>&1
echo done >> %O%\sitec.out
