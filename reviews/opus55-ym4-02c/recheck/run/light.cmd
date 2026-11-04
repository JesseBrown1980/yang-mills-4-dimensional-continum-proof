@echo off
set O=C:\tmp\opus55\recheck-02c-20261103\out
start "" /belownormal /b /wait python3 -I -X utf8 C:\tmp\opus55\recheck-02c-20261103\src\zero_clause.py > %O%\zero_clause.out 2> %O%\zero_clause.err
start "" /belownormal /b /wait python3 -I -X utf8 C:\tmp\opus55\recheck-02c-20261103\src\conj.py -3 3 > %O%\conj3.out 2> %O%\conj3.err
