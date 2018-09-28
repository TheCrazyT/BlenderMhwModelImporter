#Ported to blender from "MT Framework tools" https://www.dropbox.com/s/4ufvrgkdsioe3a6/MT%20Framework.mzp?dl=0 
#(https://lukascone.wordpress.com/2017/06/18/mt-framework-tools/)

content=bytes("","UTF-8")
bl_info = {
    "name": "MHW Model importer",
    "category": "Import-Export",
    "author": "CrazyT",
    "location": "File > Import"
}
 
 
import base64
import zlib 
import bpy
from .operators.mhw_model import ImportMOD3
from .operators.mhw_model import menu_func_import as mhw_model_menu_func_import
from .operators.mhw_model import menu_func_export as mhw_model_menu_func_export
from .operators.mhw_texture import menu_func_import as mhw_texture_menu_func_export
from .operators.mhw_model import ExportMOD3
from .operators.mhw_texture import ImportTEX

def register():
    bpy.utils.register_class(ImportMOD3)
    bpy.utils.register_class(ExportMOD3)
    bpy.utils.register_class(ImportTEX)
    bpy.types.INFO_MT_file_import.append(mhw_model_menu_func_import)
    bpy.types.INFO_MT_file_export.append(mhw_model_menu_func_export)
    bpy.types.INFO_MT_file_import.append(mhw_texture_menu_func_export)
 
 
def unregister():
    bpy.utils.unregister_class(ImportMOD3)
    bpy.utils.unregister_class(ExportMOD3)
    bpy.utils.unregister_class(ImportTEX)
    bpy.types.INFO_MT_file_import.remove(mhw_model_menu_func_import)
    bpy.types.INFO_MT_file_export.remove(mhw_model_menu_func_export)
    bpy.types.INFO_MT_file_import.remove(mhw_texture_menu_func_export)
 

    
if __name__ == "__main__":
    try:
        unregister()
    except:
        pass
    register()