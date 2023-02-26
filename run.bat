:: This Bat is created to run test cases directly from bat file and give user options what they want to run .- Gurdeep
@echo off
call venv\Scripts\activate.bat
echo "Virtual Environment is activated"

:begin
echo Select a task:
echo =============
echo -
echo 1) Run Testcase
echo 2) Exit

echo -
set /p op=Type option:
if "%op%"=="1" goto op1
if "%op%"=="2" goto exit


::echo Please Pick an option:
::goto begin

:op1
echo you picked option 1 ,Testcase execution wills start
echo Started at %DATE% %TIME%
pabot --outputdir .\Results .\Tests\paratesting\*.robot
echo -----------------------
echo Execution completed
echo -----------------------
echo Completed at %DATE% %TIME%
goto repeat


:exit
@exit

:repeat
echo Select a task:
echo =============
echo -
echo 1) Run Testcase again
echo 2) Exit
echo -
set /p op=Type option:
if "%op%"=="1" goto op1
if "%op%"=="2" goto exit



::pabot --outputdir .\Results .\Tests\paratesting\*.robot



