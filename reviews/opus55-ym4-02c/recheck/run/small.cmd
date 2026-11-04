@echo off
set E=C:\tmp\opus55\recheck-02c-20261103\rust\rp5.exe
set O=C:\tmp\opus55\recheck-02c-20261103\out
start "" /belownormal /b /wait %E% thm2 Q8 1 1 1 2 > %O%\thm2d.out 2>&1
start "" /belownormal /b /wait %E% thm2 Q8 2 1 1 2 one >> %O%\thm2d.out 2>&1
start "" /belownormal /b /wait %E% thm2 S3 3 1 1 2 >> %O%\thm2d.out 2>&1
start "" /belownormal /b /wait %E% thm2 S3 4 1 1 2 one >> %O%\thm2d.out 2>&1
start "" /belownormal /b /wait %E% thm2 Z2 5 2 1 2 >> %O%\thm2d.out 2>&1
start "" /belownormal /b /wait %E% thm2 Z2 6 2 2 2 >> %O%\thm2d.out 2>&1
start "" /belownormal /b /wait %E% thm2 Z2 7 1 1 4 >> %O%\thm2d.out 2>&1
start "" /belownormal /b /wait %E% thm2 S3 8 2 2 >> %O%\thm2d.out 2>&1
start "" /belownormal /b /wait %E% thm2 S3 9 1 4 >> %O%\thm2d.out 2>&1
start "" /belownormal /b /wait %E% thm2 S3 10 1 4 one >> %O%\thm2d.out 2>&1
start "" /belownormal /b /wait %E% witness Z2 1 3 1 -1 1 6 >> %O%\witness2.out 2>&1
start "" /belownormal /b /wait %E% witness Z2 1 3 1 -1 1 4 >> %O%\witness2.out 2>&1
start "" /belownormal /b /wait %E% witness Z2 1 3 1 -1 1 1 4 >> %O%\witness2.out 2>&1
start "" /belownormal /b /wait %E% witness Z2 3 1 1 -1 1 4 >> %O%\witness2.out 2>&1
