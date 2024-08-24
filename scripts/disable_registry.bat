@echo off
setlocal

rem Remove the registry entry for all file types (*)
reg delete "HKEY_CLASSES_ROOT\*\shell\OpenWithVSCodeJupyter" /f

if %errorlevel% equ 0 (
    echo Registry entry removed successfully.
) else (
    echo Failed to remove registry entry or it does not exist.
)

pause
endlocal
