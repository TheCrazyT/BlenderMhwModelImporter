[ ![Download](https://api.bintray.com/packages/thecrazyt/BlenderMhwModelImporter/BlenderMhwModelImporter/images/download.svg) ](https://bintray.com/thecrazyt/BlenderMhwModelImporter/BlenderMhwModelImporter/_latestVersion)
 

Quick install instructions:

 Extract the files and folders of the archive into a new folder and copy that folder to:
 
  c:\Users\YOUR_USERNAME\AppData\Roaming\Blender Foundation\Blender\2.79\scripts\addons\
  
  (replace YOUR_USERNAME with your login name and 2.79 with your blender version)
  
  (Hint: type %APPDATA% in your explorer-window to get to your "Roaming"-directory)
  
  ![install_folder1](screenshoots/install_folder1.png)

  ![install_folder2](screenshoots/install_folder2.png)
  
  Make shure that "Import-Export: MHW Model Importer" in the user-preferences window under the section "add-ons" is checked.


03.10.2018:
  
Started working on weights.

Sadly there are so many different mesh types that only some of them are currently supported. ( [example here](./screenshoots/example6.png) )


02.10.2018:

Added a custom launcher "start.bat" for people with problems on install.

Fixed problem that happens on import of em027_00.mod3. (attention, its a big object, you might need to adjust clippings: N-Key on blender in 3d-view)

Added LOD as custom property for objects. (see: screenshoots/custom_prop.png)


01.10.2018:

Vertex-changes made to the UV-editor now get exported,too

Changed default embed mode to "Reference"

  
30.09.2018:

Started working on UV-Maps.

Currently it selects the first texture it finds, but the UV-map should stay the same if you switch the textures.

To switch texture manually, your object should be in edit (TAB-Key) and face-select mode (cube-icon with highlighted front), hit "a" to select all then you can switch the texture in the UV-window.

Before use check that the *.mrl3 needs to be in same folder and that the chunk path is correct!

Also fixed a bug that can happen if you import on an empty scene (doh!)
  
  
29.09.2018:

Added possibility to import objects with by their lod-level.

Added option to group objects by lod-level into the layers.

Added dropdowns for some options (instead of checkboxes) to make the selection a bit better, because some options don't work together anyway.

Added version number to the addon.

  
28.09.2018:

Added "Reference original data." wich is faster (but if original file is deleted/moved the project can not be exported).

Refractored some redundant code (config).

Added debug-module wich is has disabled debug output on release package (faster).

Cleaned up/structorized code.

  
27.09.2018:

You can now import models with "Embed original data." property on import menu.

This allows you to modify/move some vertices on it and export the same model with the modified data.(it actually only changes the vertice-section, keeping everything else as it is)






  
Screenshoots:

![screenshoot1](screenshoots/example.png)

![screenshoot2](screenshoots/example2.png)

![screenshoot2](screenshoots/example3.png)

![screenshoot2](screenshoots/example4.png)

![screenshoot2](screenshoots/example5.png)