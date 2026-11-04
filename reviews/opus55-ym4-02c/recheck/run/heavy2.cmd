@echo off
set E=C:\tmp\opus55\recheck-02c-20261103\rust\rp5.exe
set O=C:\tmp\opus55\recheck-02c-20261103\out
start "" /belownormal /b /wait %E% witness Q8 13 9 -1 11 11 1 1 1 -1 -1 1 4 > %O%\witness.out 2>&1
start "" /belownormal /b /wait %E% witness Q8 17 9 1 9 9 1 1 1 -1 -1 1 4 >> %O%\witness.out 2>&1
start "" /belownormal /b /wait %E% witness Q8 15 19 5 5 5 2 -2 0 0 0 1 4 >> %O%\witness.out 2>&1
start "" /belownormal /b /wait %E% witness Q8 -13 -9 1 -11 -11 1 1 1 -1 -1 1 4 >> %O%\witness.out 2>&1
start "" /belownormal /b /wait %E% witness Q8 -7 -3 3 3 3 1 1 1 -1 -1 1 4 >> %O%\witness.out 2>&1
start "" /belownormal /b /wait %E% witness Z2 1 3 1 -1 3 4 >> %O%\witness.out 2>&1
start "" /belownormal /b /wait %E% witness S3 11 9 5 1 -1 1 1 1 4 >> %O%\witness.out 2>&1
start "" /belownormal /b /wait %E% thm2 S3 11 1 1 4 > %O%\thm2b.out 2>&1
start "" /belownormal /b /wait %E% thm2 S3 12 2 1 2 >> %O%\thm2b.out 2>&1
echo done > %O%\heavy2.done
