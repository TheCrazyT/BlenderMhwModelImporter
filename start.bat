@echo off

echo "Version: {VERSION}"
set BLENDER_PATH1="c:\Program Files\Blender Foundation\Blender\blender.exe"
set BLENDER_PATH2="d:\Program Files\Blender Foundation\Blender\blender.exe"
set BLENDER_EXE=""
set FOLDER="%CD%\..\BlenderMhwModelImporter"
if not exist %FOLDER% (
	echo wrong folder name, please rename this folder to: BlenderMhwModelImporter
	pause
	exit
)
if exist %BLENDER_PATH1% (
	set BLENDER_EXE=%BLENDER_PATH1%
	echo %BLENDER_PATH1% found
) else (
	if exist %BLENDER_PATH2% (
		set BLENDER_EXE=%BLENDER_PATH2%
		echo %BLENDER_PATH2% found
	) else (
		echo "Blender not found inside default path!Please modify path inside this file!"
		pause
		exit
	)
)
echo current folder: %CD%
echo path to blender.exe: %BLENDER_EXE%
%BLENDER_EXE% -P %CD%\start.py
pause