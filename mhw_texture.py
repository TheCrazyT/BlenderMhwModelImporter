bl_info = {
    "name": "MHW Texture importer",
    "category": "Import-Export",
    "author": "CrazyT",
    "location": "File > Import"
}
import configparser
import bpy
import bmesh
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator
from mathutils import Vector, Matrix, Euler
from struct import unpack
import tempfile
import os
import subprocess
from os import listdir
from os.path import isfile, join

def writeConfig():
    global config_path,config
    f = open(config_filepath,"w+")
    f.write("[DEFAULT]\n")
    for x in config['DEFAULT']:
        f.write("%s=%s\n" % (x,config['DEFAULT'][x]))
    f.close()
    print("write config:")
    print({section: dict(config[section]) for section in config.sections()})

def init_config():
    global config_filepath,config,PATH,CHUNK_PATH
    config_path = bpy.utils.user_resource('CONFIG', path='scripts', create=True)
    config_filepath = os.path.join(config_path, "mhw_importer.config")
    print("config_filepath: %s" % config_filepath)
    config = configparser.ConfigParser()
    if not os.path.isfile(config_filepath):
        config['DEFAULT']    = "d:\\tmp\\test"
        config['CHUNK_PATH'] = "d:\\tmp\\chunk"
        writeConfig()
    config.read(config_filepath)
    if 'INSTALL_PATH' in config['DEFAULT']:
        PATH = config['DEFAULT']['INSTALL_PATH']
    else:
        PATH = "d:\\tmp\\test"
    if 'CHUNK_PATH' in config['DEFAULT']:
        CHUNK_PATH = config['DEFAULT']['CHUNK_PATH']
    else:
        CHUNK_PATH = "d:\\tmp\\chunk"




init_config()

    
def doImportTex(filePath):
    ScarletPath = "%s\\Scarlet" % PATH
    tempdir  = tempfile.mkdtemp()
    print("tempdir: %s" % tempdir)
    prm = ["%s\\ScarletTestApp.exe"%ScarletPath,filePath,"--output",tempdir]
    print("execute %s" % prm)
    FNULL = open(os.devnull, 'r')
    try:
        subprocess.check_call(prm,stdin=FNULL, shell=False)
    except:
        pass
    
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

class ImportTEX(Operator, ImportHelper):
    bl_idname = "custom_import.import_mhw_tex"
    bl_label = "Load MHW TEX file (.tex)"
 
    filename_ext = ".tex"
 
    filter_glob = StringProperty(default="*.tex", options={'HIDDEN'}, maxlen=255)

    install_path = StringProperty(
            name="Install path.",
            description="Path the contains the Scarlet directory.",
            default=PATH,
    )
    def execute(self, context):
        global PATH,config_filepath,config
        PATH = self.install_path
        if not os.path.isdir(PATH):
            raise Exception("Install path %s not found!" % PATH)
            
        config['DEFAULT']['INSTALL_PATH'] = PATH
        writeConfig()

        filePath = self.filepath
        doImportTex(filePath)
        
        return {'FINISHED'}

# Only needed if you want to add into a dynamic menu
def menu_func_import(self, context):
    self.layout.operator(ImportTEX.bl_idname, text="MHW TEX (.tex)")

def register():
    global PATH,config_filepath
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