#This path needs to be modified!
PATH = "d:\\Backups_and_projects\\BlenderScripts\\MHW-Model\\"


bl_info = {
    "name": "MHW Texture importer",
    "category": "Import-Export",
    "author": "CrazyT",
    "location": "File > Import"
}
 
import bpy
import bmesh
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator
from mathutils import Vector, Matrix, Euler
from struct import unpack
import tempfile
import os
from os import listdir
from os.path import isfile, join

class ImportTEX(Operator, ImportHelper):
    bl_idname = "custom_import.import_mhw_tex"
    bl_label = "Load MHW TEX file (.tex)"
 
    filename_ext = ".tex"
 
    filter_glob = StringProperty(default="*.tex", options={'HIDDEN'}, maxlen=255)

   
    def execute(self, context):
        filePath = self.filepath
        ScarletPath = "%s\\Scarlet" % PATH
        tempdir  = tempfile.mkdtemp()
        print("tempdir: %s" % tempdir)
        ex = "\"%s\\ScarletTestApp.exe\" %s --output %s < NUL" % (ScarletPath,filePath,tempdir)
        print("execute %s" % ex)
        os.system(ex)
        
        onlyfiles = [f for f in listdir(tempdir) if isfile(join(tempdir, f))]
        
        i = 0
        for f in onlyfiles:
            if "Image 0" in f:
                imgPath = "%s\\%s" % (tempdir,f)
                print("adding image %s" % imgPath)
                img = bpy.data.images.load(imgPath)
                material = bpy.data.materials.new("Mat%d" % i)
                imtex = bpy.data.textures.new('ImageTex%d' % i ,"IMAGE")
                slot = material.texture_slots.add()
                slot.texture = imtex
                i += 1
        
        return {'FINISHED'}

# Only needed if you want to add into a dynamic menu
def menu_func_import(self, context):
    self.layout.operator(ImportTEX.bl_idname, text="MHW TEX (.tex)")


def register():
    bpy.utils.register_class(ImportTEX)
    bpy.types.INFO_MT_file_import.append(menu_func_import)
 
 
def unregister():
    bpy.utils.unregister_class(ImportTEX)
    bpy.types.INFO_MT_file_import.remove(menu_func_import)
 
 
if __name__ == "__main__":
    try:
        unregister()
    except:
        pass
    register()