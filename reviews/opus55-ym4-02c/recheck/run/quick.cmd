@echo off
set E=C:\tmp\opus55\recheck-02c-20261103\rust\rp5.exe
set O=C:\tmp\opus55\recheck-02c-20261103\out
start "" /belownormal /b /wait %E% thm2 Z3 21 1 1 4 > %O%\thm2c.out 2>&1
start "" /belownormal /b /wait %E% thm2 Z3 22 2 1 2 >> %O%\thm2c.out 2>&1
start "" /belownormal /b /wait %E% thm2 Z4 23 1 1 4 >> %O%\thm2c.out 2>&1
start "" /belownormal /b /wait %E% thm2 Z3 24 1 1 4 one >> %O%\thm2c.out 2>&1
start "" /belownormal /b /wait %E% thm2 Z4 25 1 1 4 one >> %O%\thm2c.out 2>&1
start "" /belownormal /b /wait %E% thm2 Z4 26 2 1 2 >> %O%\thm2c.out 2>&1
