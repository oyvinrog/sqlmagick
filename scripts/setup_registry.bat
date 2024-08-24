@echo off
setlocal

rem Find the Python executable
for /f "delims=" %%i in ('where python') do set "python_exe=%%i" & goto found_python
:found_python

rem Find the VS Code executable (code.cmd)
for /f "delims=" %%i in ('where code') do set "code_cmd=%%i" & goto found_code
:found_code

rem Define the path to the Python script
set "script=%~dp0open_with_jupyter.py"

rem Add registry entry for all file types (*)
reg add "HKEY_CLASSES_ROOT\*\shell\OpenWithVSCodeJupyter" /ve /d "Query with SQLMagick (VS Code)" /f
reg add "HKEY_CLASSES_ROOT\*\shell\OpenWithVSCodeJupyter\command" /ve /d "\"%python_exe%\" \"%script%\" \"%%1\"" /f

echo Registry entry added successfully.
pause

endlocal
