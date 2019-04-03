This project is **out of date**.

For getting a recent version you should **go to**:

https://github.com/AsteriskAmpersand/Mod3-MHW-Importer

(a complete rework ...)






The version here is just for nostalgia.



Page on Nexus-Mods: https://www.nexusmods.com/monsterhunterworld/mods/242


Snapshot version: [ ![Download](https://api.bintray.com/packages/thecrazyt/BlenderMhwModelImporter/BlenderMhwModelImporter/images/download.svg) ](https://bintray.com/thecrazyt/BlenderMhwModelImporter/BlenderMhwModelImporter/_latestVersion)

Beware, this version might contain editor-breaking things, stable version is always on nexusmods.

Snapshot also means that the files can change without a change of the version number itself! (but you can compare the commit-id to figure out if you are on the newest version)


 

Run start.bat to execute the addon.

14.01.2019:

A lot of improvements about bones/weights/uv.
Also added some more folder checks.
And some smaller bugfixes.


29.10.2018:

fixing start.bat-bug: space-characters inside filepath could prevent running the script.
fixing weight-rounding-bug: blender uses float32, cutting some precision, after recalculation on export int-functions cutted decimal places, resulting in totally different weight-values.

21.10.2018:

Added normals on import and option for exporing normals.
Changed bone model and handling, sadly still problems with downsized monsters (test with replacing poogie).
Added "amatrice"-bonestructure.
Setted X-Ray as default for bone-skeleton.

18.10.2018:

Fixing annoying weight bug (weight information lost on import).
On faces it created a weird problem of skin moving slow with the animation itself.

Also:
Restructurized code.
Fixed bug with install.  
  

14.10.2018:

Trying to remove vertex-count limit.
Sadly still seems to influence UV-mappings.


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
