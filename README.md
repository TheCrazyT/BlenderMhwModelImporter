[Download binaries (tar.gz)](https://bintray.com/thecrazyt/BlenderMhwModelImporter/download_file?file_path=0.2%2FMHWImporter.tar.gz)

[Download binaries (zip)](https://bintray.com/thecrazyt/BlenderMhwModelImporter/download_file?file_path=0.2%2FMHWImporter.zip)

If you use texture.py, make shure to setup the Install-Path at the file-import dialog.

27.09.2018:
You can now import models with "Embed original data." property on import menu.
This allows you to modify/move some vertices on it and export the same model with the modified data.(it actually only changes the vertice-section, keeping everything else as it is)

28.09.2018:
Added "Reference original data." wich is faster (but if original file is deleted/moved the project can not be exported).
Refractored some redundant code (config).
Added debug-module wich is has disabled debug output on release package (faster).
Cleaned up/structorized code.


Quick install instructions:
 Extract the files and folders of the archive into a new folder and copy that folder to:
  c:\Users\YOUR_USERNAME\AppData\Roaming\Blender Foundation\Blender\2.79\scripts\addons\
  (replace YOUR_USERNAME with your login name and 2.79 with your blender version)
  (Hint: type %APPDATA% in your explorer-window to get to your "Roaming"-directory)

Screenshoots:

![screenshoot1](screenshoots/example.png)

![screenshoot2](screenshoots/example2.png)