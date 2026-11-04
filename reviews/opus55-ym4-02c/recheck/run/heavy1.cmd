@echo off
set E=C:\tmp\opus55\recheck-02c-20261103\rust\rp5.exe
set O=C:\tmp\opus55\recheck-02c-20261103\out
start "" /belownormal /b /wait %E% moved > %O%\moved.out 2> %O%\moved.err
start "" /belownormal /b /wait %E% thm2 Q8 13 1 1 1 2 > %O%\thm2a.out 2>&1
start "" /belownormal /b /wait %E% thm2 Q8 14 2 2 >> %O%\thm2a.out 2>&1
start "" /belownormal /b /wait %E% thm2 Q8 15 1 4 >> %O%\thm2a.out 2>&1
start "" /belownormal /b /wait %E% thm2 Q8 18 1 1 1 2 one >> %O%\thm2a.out 2>&1
start "" /belownormal /b /wait %E% thm2 SL23 16 1 1 2 >> %O%\thm2a.out 2>&1
start "" /belownormal /b /wait %E% thm2 D4 19 1 1 2 >> %O%\thm2a.out 2>&1
start "" /belownormal /b /wait %E% signs Q8 2 2 > %O%\signs.out 2>&1
start "" /belownormal /b /wait %E% signs S3 2 2 >> %O%\signs.out 2>&1
start "" /belownormal /b /wait %E% signs D4 2 2 >> %O%\signs.out 2>&1
start "" /belownormal /b /wait %E% signs Z4 2 2 >> %O%\signs.out 2>&1
start "" /belownormal /b /wait %E% signs A4 2 2 >> %O%\signs.out 2>&1
start "" /belownormal /b /wait %E% signs S4 2 2 >> %O%\signs.out 2>&1
start "" /belownormal /b /wait %E% signs SL23 2 2 >> %O%\signs.out 2>&1
start "" /belownormal /b /wait %E% signs Q8 3 2 >> %O%\signs.out 2>&1
start "" /belownormal /b /wait %E% signs S3 3 2 >> %O%\signs.out 2>&1
start "" /belownormal /b /wait %E% signs S3 3 3 >> %O%\signs.out 2>&1
start "" /belownormal /b /wait %E% signs Z3 2 2 2 >> %O%\signs.out 2>&1
start "" /belownormal /b /wait %E% signs Z2 2 2 2 >> %O%\signs.out 2>&1
start "" /belownormal /b /wait %E% signs Q8 2 1 >> %O%\signs.out 2>&1
start "" /belownormal /b /wait %E% signs Q8 1 1 >> %O%\signs.out 2>&1
start "" /belownormal /b /wait %E% signs S3 2 1 >> %O%\signs.out 2>&1
start "" /belownormal /b /wait %E% signs GL23 2 2 >> %O%\signs.out 2>&1
echo done > %O%\heavy1.done
