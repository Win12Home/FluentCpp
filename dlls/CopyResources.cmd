@echo off
title 补齐文件
copy "libgcc_s_seh-1.dll" "%windir%\system32"
copy "libstdc++-6.dll" "%windir%\system32"
copy "libwinpthread-1.dll" "%windir%\system32"
exit
