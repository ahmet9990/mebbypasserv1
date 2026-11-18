@echo off
setlocal EnableExtensions
chcp 65001 >nul
cd /d "%~dp0"
set "PYTHONPATH=%~dp0"
set "PYTHONIOENCODING=utf-8"
set "MBP_HOME=%~dp0"

set "CMD=%~1"
if "%CMD%"=="" set "CMD=start"

set "PY="
where py >nul 2>&1 && set "PY=py -3"
if not defined PY where python >nul 2>&1 && set "PY=python"
if not defined PY (
  echo Python bulunamadi.
  echo https://www.python.org/downloads/windows/ adresinden Python 3 kurun.
  echo Kurulumda "Add python.exe to PATH" kutusunu isaretleyin.
  echo.
  echo fatih cracked by Venathra Team
  if not "%MBP_NOPAUSE%"=="1" pause
  exit /b 1
)

if /I "%CMD%"=="start" goto start
if /I "%CMD%"=="baslat" goto start
if /I "%CMD%"=="stop" goto stop
if /I "%CMD%"=="durdur" goto stop
if /I "%CMD%"=="status" goto status
if /I "%CMD%"=="durum" goto status
if /I "%CMD%"=="test" goto test
if /I "%CMD%"=="tani" goto tani
if /I "%CMD%"=="teshis" goto tani
if /I "%CMD%"=="geri-al" goto gerial
if /I "%CMD%"=="gerial" goto gerial
if /I "%CMD%"=="log" goto log
if /I "%CMD%"=="gui" goto gui
goto usage

:start
%PY% -X utf8 -m mebbypass --sistem %2 %3 %4 %5 %6
goto done

:stop
set "PIDF=%USERPROFILE%\.mebbypass\mebbypass.pid"
set "PORTF=%USERPROFILE%\.mebbypass\port"
set "PID="
set "PORT=8080"
if exist "%PIDF%" set /p PID=<"%PIDF%"
if exist "%PORTF%" set /p PORT=<"%PORTF%"
if defined PID (
  taskkill /PID %PID% >nul 2>&1
  timeout /t 2 /nobreak >nul
  taskkill /F /PID %PID% >nul 2>&1
  del /f /q "%PIDF%" >nul 2>&1
)
%PY% -X utf8 -m mebbypass --geri-al -p %PORT%
goto done

:status
%PY% -X utf8 -m mebbypass --durum
goto done

:test
%PY% -X utf8 -m mebbypass --test
goto done

:tani
%PY% -X utf8 -m mebbypass --tani
goto done

:gerial
%PY% -X utf8 -m mebbypass --geri-al
goto done

:log
%PY% -X utf8 -m mebbypass --log-son
goto done

:gui
%PY% -X utf8 -m mebbypass --gui
goto done

:usage
echo Kullanim: mebbypass.bat [start^|stop^|status^|test^|tani^|geri-al^|log^|gui]
echo   BASLAT.bat   proxy + Windows proxy ayari
echo   DURDUR.bat   durdur ve ayari geri al
echo   GUI.bat      pencere
%PY% -X utf8 -c "print('fatih cracked by Venathra Team')"
goto done

:done
if not "%MBP_NOPAUSE%"=="1" pause
exit /b 0
