#Ported to blender from "MT Framework tools" https://www.dropbox.com/s/4ufvrgkdsioe3a6/MT%20Framework.mzp?dl=0 
#(https://lukascone.wordpress.com/2017/06/18/mt-framework-tools/)

content=bytes("","UTF-8")
bl_info = {
    "name": "MHW Model importer",
    "category": "Import-Export",
    "author": "CrazyT",
    "location": "File > Import"
}
 
 

 
import bpy
import bmesh
import os
import configparser
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator
from mathutils import Vector, Matrix, Euler
from struct import unpack, pack
x64=64

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

class MODVertexBuffer818904dc:
    def __init__(self,headerref,vertexcount):
        print("MODVertexBuffer818904dc %d" % vertexcount)
        self.vertarray   = []
        self.headerref   = headerref
        self.vertexcount = vertexcount
        for i in range(0,vertexcount):
            if headerref.bendian:
                self.vertarray.append([ReadBEFloat(headerref.fl),ReadBEFloat(headerref.fl),ReadBEFloat(headerref.fl)])
            else:
                self.vertarray.append([ReadFloat(headerref.fl),ReadFloat(headerref.fl),ReadFloat(headerref.fl)])
            Read8s(headerref.fl)
            Read8s(headerref.fl)
            Read8s(headerref.fl)
            ReadByte(headerref.fl)
            ReadLong(headerref.fl)
            ReadHalfFloat(headerref.fl)
            ReadHalfFloat(headerref.fl)
            ReadLong(headerref.fl)

class MODVertexBufferf06033f:
    def __init__(self,headerref,vertexcount):
        print("MODVertexBufferf06033f %d" % vertexcount)
        self.vertarray   = []
        self.headerref   = headerref
        self.vertexcount = vertexcount
        for i in range(0,vertexcount):
            if headerref.bendian:
                self.vertarray.append([ReadBEFloat(headerref.fl),ReadBEFloat(headerref.fl),ReadBEFloat(headerref.fl)])
            else:
                self.vertarray.append([ReadFloat(headerref.fl),ReadFloat(headerref.fl),ReadFloat(headerref.fl)])
            Read8s(headerref.fl)
            Read8s(headerref.fl)
            Read8s(headerref.fl)
            ReadByte(headerref.fl)
            ReadLong(headerref.fl)
            ReadHalfFloat(headerref.fl)
            ReadHalfFloat(headerref.fl)
            ReadLong(headerref.fl)
            ReadByte(headerref.fl)
            
            ReadByte(headerref.fl)
            ReadByte(headerref.fl)
            ReadByte(headerref.fl)
           
class MODVertexBuffer81f58067:
    def __init__(self,headerref,vertexcount):
        print("MODVertexBuffer81f58067 %d" % vertexcount)
        self.vertarray   = []
        self.headerref   = headerref
        self.vertexcount = vertexcount
        for i in range(0,vertexcount):
            if headerref.bendian:
                self.vertarray.append([ReadBEFloat(headerref.fl),ReadBEFloat(headerref.fl),ReadBEFloat(headerref.fl)])
            else:
                self.vertarray.append([ReadFloat(headerref.fl),ReadFloat(headerref.fl),ReadFloat(headerref.fl)])
            Read8s(headerref.fl)
            Read8s(headerref.fl)
            Read8s(headerref.fl)
            ReadByte(headerref.fl)
            ReadLong(headerref.fl)
            ReadHalfFloat(headerref.fl)
            ReadHalfFloat(headerref.fl)
            ReadLong(headerref.fl)
            ReadByte(headerref.fl)
            ReadByte(headerref.fl)
            ReadByte(headerref.fl)
            ReadByte(headerref.fl)
            ReadByte(headerref.fl)
            
            ReadByte(headerref.fl)
            ReadByte(headerref.fl)
            ReadByte(headerref.fl)
            ReadByte(headerref.fl)
            ReadByte(headerref.fl)
            ReadByte(headerref.fl)
            ReadByte(headerref.fl)
class MODVertexBufferf471fe45:
    def __init__(self,headerref,vertexcount):
        print("MODVertexBufferf471fe45 %d" % vertexcount)
        raise Exception("ToDo")
        self.vertarray   = []
        self.headerref   = headerref
        self.vertexcount = vertexcount
        for i in range(0,vertexcount):
            if headerref.bendian:
                self.vertarray.append([ReadBEFloat(headerref.fl),ReadBEFloat(headerref.fl),ReadBEFloat(headerref.fl)])
            else:
                self.vertarray.append([ReadFloat(headerref.fl),ReadFloat(headerref.fl),ReadFloat(headerref.fl)])
            Read8s(headerref.fl)
            Read8s(headerref.fl)
            Read8s(headerref.fl)
            ReadByte(headerref.fl)
            ReadLong(headerref.fl)
            ReadHalfFloat(headerref.fl)
            ReadHalfFloat(headerref.fl)
            ReadLong(headerref.fl)
class MODVertexBuffer3c730760:
    def __init__(self,headerref,vertexcount):
        print("MODVertexBuffer3c730760 %d" % vertexcount)
        self.vertarray   = []
        self.headerref   = headerref
        self.vertexcount = vertexcount
        for i in range(0,vertexcount):
            if headerref.bendian:
                self.vertarray.append([ReadBEFloat(headerref.fl),ReadBEFloat(headerref.fl),ReadBEFloat(headerref.fl)])
            else:
                self.vertarray.append([ReadFloat(headerref.fl),ReadFloat(headerref.fl),ReadFloat(headerref.fl)])
            Read8s(headerref.fl)
            Read8s(headerref.fl)
            Read8s(headerref.fl)
            ReadByte(headerref.fl)
            ReadLong(headerref.fl)
            ReadHalfFloat(headerref.fl)
            ReadHalfFloat(headerref.fl)
            ReadLong(headerref.fl)
            ReadByte(headerref.fl)
            
            ReadByte(headerref.fl)
            ReadByte(headerref.fl)
            ReadByte(headerref.fl)
            
            ReadByte(headerref.fl)
            
            ReadByte(headerref.fl)
            ReadByte(headerref.fl)
            ReadByte(headerref.fl)
class MODVertexBufferb2fc0083:
    def __init__(self,headerref,vertexcount):
        print("MODVertexBufferb2fc0083 %d" % vertexcount)
        raise Exception("ToDo")
        self.vertarray   = []
        self.headerref   = headerref
        self.vertexcount = vertexcount
        for i in range(0,vertexcount):
            if headerref.bendian:
                self.vertarray.append([ReadBEFloat(headerref.fl),ReadBEFloat(headerref.fl),ReadBEFloat(headerref.fl)])
            else:
                self.vertarray.append([ReadFloat(headerref.fl),ReadFloat(headerref.fl),ReadFloat(headerref.fl)])
            Read8s(headerref.fl)
            Read8s(headerref.fl)
            Read8s(headerref.fl)
            ReadByte(headerref.fl)
            ReadLong(headerref.fl)
            ReadHalfFloat(headerref.fl)
            ReadHalfFloat(headerref.fl)
            ReadLong(headerref.fl)
class MODVertexBuffer366995a7:
    def __init__(self,headerref,vertexcount):
        print("MODVertexBuffer366995a7 %d" % vertexcount)
        self.vertarray   = []
        self.headerref   = headerref
        self.vertexcount = vertexcount
        for i in range(0,vertexcount):
            if headerref.bendian:
                self.vertarray.append([ReadBEFloat(headerref.fl),ReadBEFloat(headerref.fl),ReadBEFloat(headerref.fl)])
            else:
                self.vertarray.append([ReadFloat(headerref.fl),ReadFloat(headerref.fl),ReadFloat(headerref.fl)])
            Read8s(headerref.fl)
            Read8s(headerref.fl)
            Read8s(headerref.fl)
            ReadByte(headerref.fl)
            ReadLong(headerref.fl)
            ReadHalfFloat(headerref.fl)
            ReadHalfFloat(headerref.fl)
            ReadLong(headerref.fl)
            Read8s(headerref.fl)
            Read8s(headerref.fl)
            Read8s(headerref.fl)
            Read8s(headerref.fl)
            for b in range(0,8):
                Read8s(headerref.fl)
            ReadLong(headerref.fl)

class MODVertexBufferc9690ab8:
    def __init__(self,headerref,vertexcount):
        print("MODVertexBufferc9690ab8 %d" % vertexcount)
        raise Exception("ToDo")
        self.vertarray   = []
        self.headerref   = headerref
        self.vertexcount = vertexcount
        for i in range(0,vertexcount):
            if headerref.bendian:
                self.vertarray.append([ReadBEFloat(headerref.fl),ReadBEFloat(headerref.fl),ReadBEFloat(headerref.fl)])
            else:
                self.vertarray.append([ReadFloat(headerref.fl),ReadFloat(headerref.fl),ReadFloat(headerref.fl)])
            Read8s(headerref.fl)
            Read8s(headerref.fl)
            Read8s(headerref.fl)
            ReadByte(headerref.fl)
            ReadLong(headerref.fl)
            ReadHalfFloat(headerref.fl)
            ReadHalfFloat(headerref.fl)
            ReadLong(headerref.fl)
class MODVertexBuffer5e7f202d:
    def __init__(self,headerref,vertexcount):
        print("MODVertexBuffer5e7f202d %d" % vertexcount)
        raise Exception("ToDo")
        self.vertarray   = []
        self.headerref   = headerref
        self.vertexcount = vertexcount
        for i in range(0,vertexcount):
            if headerref.bendian:
                self.vertarray.append([ReadBEFloat(headerref.fl),ReadBEFloat(headerref.fl),ReadBEFloat(headerref.fl)])
            else:
                self.vertarray.append([ReadFloat(headerref.fl),ReadFloat(headerref.fl),ReadFloat(headerref.fl)])
            Read8s(headerref.fl)
            Read8s(headerref.fl)
            Read8s(headerref.fl)
            ReadByte(headerref.fl)
            ReadLong(headerref.fl)
            ReadHalfFloat(headerref.fl)
            ReadHalfFloat(headerref.fl)
            ReadLong(headerref.fl)
class MODVertexBufferd829702c:
    def __init__(self,headerref,vertexcount):
        print("MODVertexBufferd829702c %d" % vertexcount)
        self.vertarray   = []
        self.headerref   = headerref
        self.vertexcount = vertexcount
        for i in range(0,vertexcount):
            if headerref.bendian:
                self.vertarray.append([ReadBEFloat(headerref.fl),ReadBEFloat(headerref.fl),ReadBEFloat(headerref.fl)])
            else:
                self.vertarray.append([ReadFloat(headerref.fl),ReadFloat(headerref.fl),ReadFloat(headerref.fl)])
            Read8s(headerref.fl)
            Read8s(headerref.fl)
            Read8s(headerref.fl)
            ReadByte(headerref.fl)
            ReadLong(headerref.fl)
            ReadHalfFloat(headerref.fl)
            ReadHalfFloat(headerref.fl)
class MODVertexBufferb8e69244:
    def __init__(self,headerref,vertexcount):
        print("MODVertexBufferd829702c %d" % vertexcount)
        self.vertarray   = []
        self.headerref   = headerref
        self.vertexcount = vertexcount
        for i in range(0,vertexcount):
            if headerref.bendian:
                self.vertarray.append([ReadBEFloat(headerref.fl),ReadBEFloat(headerref.fl),ReadBEFloat(headerref.fl)])
            else:
                self.vertarray.append([ReadFloat(headerref.fl),ReadFloat(headerref.fl),ReadFloat(headerref.fl)])
            Read8s(headerref.fl)
            Read8s(headerref.fl)
            Read8s(headerref.fl)
            ReadByte(headerref.fl)
            ReadLong(headerref.fl)
            ReadHalfFloat(headerref.fl)
            ReadHalfFloat(headerref.fl)
            ReadLong(headerref.fl)
            ReadByte(headerref.fl)
            ReadByte(headerref.fl)
            ReadByte(headerref.fl)
            ReadByte(headerref.fl)
            for b in range(1,9):
                ReadByte(headerref.fl)
            ReadLong(headerref.fl)
            
            ReadByte(headerref.fl)
            ReadByte(headerref.fl)
            ReadByte(headerref.fl)
            ReadByte(headerref.fl)
MODVertexBuffera5104ca0 = MODVertexBuffer5e7f202d
MODVertexBufferf637401c = MODVertexBufferf06033f
MODVertexBuffera756f2f9 = MODVertexBufferd829702c


pos = {}
def ReadByte(fl):
    global pos,content
    res = unpack("B",content[pos[fl]:pos[fl]+1])[0]
    pos[fl]+=1
    return res
def ReadLong(fl):
    global pos,content
    res = unpack("I",content[pos[fl]:pos[fl]+4])[0]
    pos[fl]+=4
    return res
def ReadShort(fl):
    global pos,content
    res = unpack("H",content[pos[fl]:pos[fl]+2])[0]
    pos[fl]+=2
    return res
def ReadBELong(fl):
    global pos,content
    res = unpack(">I",content[pos[fl]:pos[fl]+4])[0]
    pos[fl]+=4
    return res
def ReadBEShort(fl):
    global pos,content
    res = unpack(">H",content[pos[fl]:pos[fl]+2])[0]
    pos[fl]+=2
    return res
def _rdhf(v):
    #TODO
    pass
def Read8s(fl):
    return ReadByte(fl)*0.0078125
def ReadHalfFloat(fl):
    return _rdhf(ReadShort(fl))
def ReadFloat(fl):
    global pos,content
    res = unpack("f",content[pos[fl]:pos[fl]+4])[0]
    pos[fl]+=4
    return res
def ReadBEFloat(fl):
    global pos,content
    res = unpack(">f",content[pos[fl]:pos[fl]+4])[0]
    pos[fl]+=4
    return res
def ReadPointer(fl,size):
    global pos,content,x64
    if(size==x64):
        res = unpack("Q",content[pos[fl]:pos[fl]+8])[0]
        pos[fl]+=8
        return res
    return None
def ReadVector3(fl):
    global pos,content
    res = unpack("fff",content[pos[fl]:pos[fl]+4*3])
    pos[fl]+=4*3
    return res
def CollectStrips(fl,modf=1):
    print("CollectStrips")

    resarray = []
    f1t = ReadShort(fl)
    f2t = ReadShort(fl) 
    f = 2
    while f < num:
        cf = ReadShort(fl) 
        if cf == 0xffff:
            f1t = ReadShort(fl)
            f2t = ReadShort(fl) 
            f += 3
        else:
            if (f % 2) == 1:
                cfa = [cf,f2t,f1t]
            else:
                cfa = [f1t,f2t,cf]
            resarray.append([x+modf for x in cfa])
            f1t = f2t
            f2t = cf
            f += 1
    return resarray
def CollectTris(fl,num,modf=1):
    print("CollectTris %d" % num)
    res = []
    for i in range(0 ,num):
        res.append([x+modf for x in [ReadShort(fl) , ReadShort(fl) ,ReadShort(fl)]])
    return res
def CollectBETris(fl,num,modf=1):
    print("CollectBETris %d" % num)
    res = []
    for i in range(0 ,num):
        res.append([x+modf for x in [ReadBEShort(fl) , ReadBEShort(fl) ,ReadBEShort(fl)]])
    return res
def CollectBEStrips(fl,modf=1):
    print("CollectBEStrips")
    resarray = []
    f1t = ReadBEShort(fl)
    f2t = ReadBEShort(fl) 
    f = 2
    while f < num:
        cf = ReadBEShort(fl) 
        if cf == 0xffff:
            f1t = ReadBEShort(fl)
            f2t = ReadBEShort(fl) 
            f += 3
        else:
            if (f % 2) == 1:
                cfa = [cf,f2t,f1t]
            else:
                cfa = [f1t,f2t,cf]
            resarray.append(cfa+modf)
            f1t = f2t
            f2t = cf
            f += 1
    return resarray
def Seek(fl,offset):
    global pos,content_file
    pos[fl]=offset
def fseek(fl,roffset):
    global pos,content_file
    pos[fl]+=roffset
    
    
class MeshPart:
    def __init__(self,
            id,
            Material,
            LOD,
            BlockSize,
            BlockType,
            VertexSub,
            VertexCount,
            VertexOffset,
            FaceOffset,
            FaceCount,
            FaceAdd,
            meshdata,
            boneremapid,
            headerref,
            loadmeshdata):
            self.id = id
            self.Material = Material
            self.LOD = LOD
            self.BlockSize = BlockSize
            self.BlockType = BlockType
            self.VertexSub = VertexSub
            self.VertexCount = VertexCount
            self.VertexOffset = VertexOffset
            self.FaceOffset = FaceOffset
            self.FaceCount = FaceCount
            self.FaceAdd = FaceAdd
            self.meshdata = meshdata
            self.boneremapid = boneremapid
            self.headerref = headerref
            self.loadmeshdataF = loadmeshdata
    def loadmeshdata(self):
        self.loadmeshdataF(self)

class ImportMOD3(Operator, ImportHelper):
    bl_idname = "custom_import.import_mhw"
    bl_label = "Load MHW MOD file (.mod3)"
 
    # ImportHelper mixin class uses this
    filename_ext = ".mod3"
 
    filter_glob = StringProperty(default="*.mod3", options={'HIDDEN'}, maxlen=255)
    
    
    chunk_path = StringProperty(
        name="Chunk path",
        description="Path to chunk folder (containing template.mrl3 for example)",
        default=CHUNK_PATH,
    )
    install_path = StringProperty(
            name="Install path.",
            description="Path the contains the Scarlet directory.",
            default=PATH,
    )
    use_layers = BoolProperty(
            name="Use layers for mesh parts.",
            description="If we find multiple mesh parts, try to move every mesh in a seperate layer.",
            default=True,
    )
    import_textures = BoolProperty(
            name="Import textures.",
            description="Looks automatically for the *.mrl3 file and imports the *.tex files.",
            default=False,
    )
    only_import_lod_1 = BoolProperty(
            name="Only import high LOD-parts.",
            description="Skip meshparts with low level of detail.",
            default=True,
    )

    def readHeader(self):
        fl = self.fl
        self.bendian = False
        self.ID = ReadLong(fl);
        if self.ID!=0x444f4d:
            raise Exception("Invalid Header")
        self.Version = ReadByte(fl) #unsigned
        self.Version2 = ReadByte(fl) 
        self.BoneCount = ReadShort(fl) #unsigned
        self.MeshCount = ReadShort(fl) #unsigned
        self.MaterialCount = ReadShort(fl) #unsigned
        self.VertexCount = ReadLong(fl) #unsigned
        self.FaceCount = ReadLong(fl) #unsigned
        self.VertexIds = ReadLong(fl) #unsigned
        self.VertexBufferSize = ReadLong(fl) #unsigned
        self.SecondBufferSize = ReadLong(fl) #unsigned
        if self.Version < 190:
            self.TextureCount = ReadLong(fl) #unsigned
        self.GroupCount = ReadPointer(fl,x64)
        if self.Version < 190 or self.Version > 220: 
            self.BoneMapCount = ReadPointer(fl,x64)
        self.BonesOffset = ReadPointer(fl,x64)
        self.GroupOffset = ReadPointer(fl,x64)
        self.TextureOffset = ReadPointer(fl,x64)
        self.MeshOffset = ReadPointer(fl,x64)
        self.VertexOffset =ReadPointer(fl,x64)
        if self.Version < 190:
            self.Vertex2Offset = ReadLong(fl) #unsigned
        self.FacesOffset = ReadPointer(fl,x64)
        self.UnkOffset = ReadPointer(fl,x64)
        if self.Version < 190:
            self.unkOffset2 = ReadLong(fl) #unsigned
            self.bbsphereposition = ReadVector3(fl)
            self.bbsphereradius = ReadFloat(fl)
            self.bbmin = ReadVector3(fl)
            ReadLong(fl)
            self.bbmax = ReadVector3(fl)
            ReadLong(fl)
            for s  in range(1,4+1):
                self.vtbuffscale[s] = self.bbmax[s]-self.bbmin[s]

        if self.Version == 237:
            self.BoneMapCount = None
    
    def readBones(self):
        fl = self.fl
        Seek(fl,self.BonesOffset)
    
    
    def loadmeshdatav1(self,meshPart):
        f = eval("MODVertexBuffer%08x" % meshPart.BlockType)
        headerref = meshPart.headerref
        if f != None:
            Seek(headerref.fl,((headerref.VertexOffset+meshPart.VertexOffset)+(BlockSize*(meshPart.VertexSub+meshPart.FaceAdd)))) #seek_set
            meshPart.meshdata = f(headerref,meshPart.VertexCount)
            Seek(headerref.fl,(headerref.FacesOffset+FaceOffset*2)) #seek_set
            if headerref.bendian:
                meshPart.meshdata.facearray = CollectBEStrips(headerref.fl,meshPart.FaceCount,(0-meshPart.VertexSub))
            else:
                meshPart.meshdata.facearray = CollectStrips(headerref.fl,meshPart.FaceCount,(0-meshPart.VertexSub))
        else:
            raise Exception("Unknown block hash [%08x] for MTF v1 model format.\n" % meshPart.BlockType)
    def loadmeshdatav1(self):
        raise Exception("NotImplementedError")
    def loadmeshdatav3(self,meshPart):
        f = eval("MODVertexBuffer%08x" % meshPart.BlockType)
        headerref = meshPart.headerref
        if f != None:
            VOFF=headerref.VertexOffset+meshPart.VertexOffset
            BOFF=meshPart.VertexSub+meshPart.FaceAdd
            Seek(headerref.fl,(VOFF+meshPart.BlockSize*BOFF)) #seek_set
            meshPart.meshdata = f(headerref,meshPart.VertexCount)
            Seek(headerref.fl,(headerref.FacesOffset+meshPart.FaceOffset*2)) #seek_set
            meshPart.FaceCount = int(meshPart.FaceCount/3)
            if headerref.bendian:
                meshPart.meshdata.facearray = CollectBETris(headerref.fl,meshPart.FaceCount,0-meshPart.VertexSub)
            else:
                meshPart.meshdata.facearray = CollectTris(headerref.fl,meshPart.FaceCount,0-meshPart.VertexSub)
        else:
            raise Exception("Unknown block hash [%08x] for MTF v1 model format.\n" % meshPart.BlockType)

    def readMeshPartv1(self):
        if self.bendian:
            fl = self.fl
            id = ReadBEShort(fl)
            Material = ReadBEShort(fl )
            ReadByte(fl) #unsigned
            LOD = ReadByte(fl) #unsigned
            readshort(fl)
            BlockSize = ReadByte(fl) #unsigned
            BlockType = ReadByte(fl) #unsigned
            fseek(fl,2) #seek_cur
            VertexCount = ReadBEShort(fl) 
            ReadShort(fl)
            VertexSub = ReadBELong(fl)
            VertexOffset = ReadBELong(fl) 
            fseek(fl,4) #seek_cur
            FaceOffset = ReadBELong(fl)
            FaceCount = ReadBELong(fl)
            FaceAdd = ReadBELong(fl)
            fseek(fl,6) #seek_cur
            boneremapid = ReadByte(fl)+1
            fseek(fl,5) #seek_cur
        else:
            fl = self.fl
            id = ReadShort(fl)
            Material = ReadShort(fl )
            ReadByte(fl) #unsigned
            LOD = ReadByte(fl) #unsigned
            readshort(fl)
            BlockSize = ReadByte(fl) #unsigned
            BlockType = ReadByte(fl) #unsigned
            fseek(fl,2) #seek_cur
            VertexCount = ReadShort(fl) 
            ReadShort(fl)
            VertexSub = ReadLong(fl)
            VertexOffset = ReadLong(fl) 
            fseek(fl,4) #seek_cur
            FaceOffset = ReadLong(fl) 
            FaceCount = ReadLong(fl)
            FaceAdd = ReadLong(fl) 
            fseek(fl,6) #seek_cur
            boneremapid = ReadByte(fl)+1
            fseek(fl,5) #seek_cur
        return MeshPart(id,
            Material,
            LOD,
            BlockSize,
            BlockType,
            VertexSub,
            VertexCount,
            VertexOffset,
            FaceOffset,
            FaceCount,
            FaceAdd,
            None,
            boneremapid,
            self,
            self.loadmeshdatav1)


    def readMeshPartv2(self):
        raise Exception("readMeshPartv2 not implemented")
    def readMeshPartv3(self):
        headerref = self.headerref
        ReadShort(headerref.fl) #unsigned
        VertexCount = ReadShort(headerref.fl) #unsigned     
        id = ReadShort(headerref.fl) #unsigned
        ReadShort(headerref.fl) #unsigned
        lod = ReadLong(headerref.fl) #unsigned
        ReadShort(headerref.fl) #unsigned
        BlockSize = ReadByte(headerref.fl) #unsigned
        ReadByte(headerref.fl)
        VertexSub = ReadLong(headerref.fl) #unsigned
        VertexOffset = ReadLong(headerref.fl) #unsigned
        BlockType = ReadLong(headerref.fl) #unsigned
        FaceOffset = ReadLong(headerref.fl) #unsigned
        FaceCount = ReadLong(headerref.fl) #unsigned
        FaceAdd = ReadLong(headerref.fl) #unsigned
        boneremapid = ReadByte(headerref.fl)+1
        fseek(headerref.fl,39) #seek_cur
        return MeshPart(id,
            None,
            lod,
            BlockSize,
            BlockType,
            VertexSub,
            VertexCount,
            VertexOffset,
            FaceOffset,
            FaceCount,
            FaceAdd,
            None,
            boneremapid,
            self,
            self.loadmeshdatav3)
    
    def readMeshParts(self):
        Seek(self.fl,self.MeshOffset)
        if(self.Version == 237):
            readMeshPart = self.readMeshPartv3
        elif(self.Version < 190):
            readMeshPart = self.readMeshPartv1
        else:
            readMeshPart = self.readMeshPartv2
        for i in range(0,self.MeshCount):
           self.parts.append(readMeshPart())

    def readVertexes(self):
        Seek(self.fl,self.VertexOffset)
        for m in self.parts:
            m.loadmeshdata()

    def parseMrl3(self,filepath):
        global PATH,CHUNK_PATH,content
        
        import mhw_texture
        mhw_texture.PATH = PATH
        mhw_texture.CHUNK_PATH = CHUNK_PATH
        
        if not os.path.isfile(filepath):
            print("%s not found" % filepath)
            return
        
        if not os.path.isdir(CHUNK_PATH):
            raise Exception("Chunkdirectory %s does not exist!" % CHUNK_PATH)
        
        with open(filepath, 'rb') as content_file:
            content = content_file.read()

        fl      = 1
        pos[fl] = 0
        ReadLong(fl)
        for u in range(0,12):
            ReadByte(fl)
        marerialCount = ReadLong(fl)
        textureCount = ReadLong(fl)
        for i in range(0,4):
            ReadLong(fl)
        
        for i in range(0,textureCount):
            ReadLong(fl)
            for i in range(0,12):
                ReadByte(fl)
            tex = ""
            for i in range(0,256):
                b = ReadByte(fl)
                if b != 0:
                    by = chr(b)
                    tex = "%s%s"  % (tex,by)
            texpath = "%s\\%s.tex" % (CHUNK_PATH,tex)
            print("importing texture: %s" % (texpath))
            mhw_texture.doImportTex(texpath)
    
    def execute(self, context):
        global content,CHUNK_PATH
        CHUNK_PATH = self.chunk_path
        if CHUNK_PATH[len(CHUNK_PATH)-1] == '\\':
            CHUNK_PATH = CHUNK_PATH[0:len(CHUNK_PATH)-1]
        PATH = self.install_path
        if not os.path.isdir(PATH):
            raise Exception("Install path %s not found!" % PATH)
            
        config['DEFAULT']['INSTALL_PATH'] = PATH
        config['DEFAULT']['CHUNK_PATH'] = CHUNK_PATH
        writeConfig()
        if(self.import_textures):
            self.parseMrl3(self.filepath.replace(".mod3",".mrl3"))
        if(self.use_layers):
            print("using layers")
        with open(self.filepath, 'rb') as content_file:
            fl = 0
            content = content_file.read()
        self.fl = fl
        self.headerref = self
        self.parts = []
        pos[fl] = 0
            
        self.readHeader()
        self.readBones()
        self.readMeshParts()
        self.readVertexes()
        
        fi = 0
        pi = 0
        for m in self.parts:
            if (self.only_import_lod_1) and (m.LOD!=1):
                continue
            if m.meshdata != None:
                bm = bmesh.new()
                mesh = bpy.data.meshes.new("mesh")  # add a new mesh
                obj = bpy.data.objects.new("MyObject.%05d.%08x" % (pi,m.BlockType), mesh)  # add a new object using the mesh
                #print("%d     %d" % (m.VertexCount,len(m.meshdata.vertarray)))
                verts  = []
                verts2 = []
                faces = []
                for v in m.meshdata.vertarray:
                    #print(v)
                    verts2.append(v)
                    verts.append(bm.verts.new(v))
                for f in m.meshdata.facearray:
                    addFace=True
                    for x in f:
                        if x>=len(verts):
                            addFace = False
                            #print("%d not in verts [%d]" % (x,len(verts)))
                    if addFace:
                        #if fi<30:
                        vts  = [verts[x] for x in f]
                        vts2 = [verts2[x] for x in f]
                        #print(vts)
                        #print(vts2)
                        #print(f)
                        faces.append(vts)
                        fi+=1
                        try:
                            f1 = bm.faces.new(vts)
                        except:
                            pass
                        #pass
                    else:
                        raise Exception("Problem with face:%s [vert len:%d,pos:%08x]" % (f,len(verts),pos[fl]))

                scene = bpy.context.scene
                scene.objects.link(obj)  # put the object into the scene (link)
                if(self.use_layers):
                    for i in range(19):
                        obj.layers[1+i] = (i == (pi % 19)) # we only have 20 layers available ... sadly
                scene.objects.active = obj  # set as the active object in the scene
                obj.select = True  # select object

                mesh = bpy.context.object.data


                # make the bmesh the object's mesh
                bm.to_mesh(mesh)  
                bm.free()  # always do this when finished

            pi += 1
            #break


        return {'FINISHED'}
# Only needed if you want to add into a dynamic menu
def menu_func_import(self, context):
    self.layout.operator(ImportMOD3.bl_idname, text="MHW MOD (.mod3)")


def register():
    bpy.utils.register_class(ImportMOD3)
    bpy.types.INFO_MT_file_import.append(menu_func_import)
 
 
def unregister():
    bpy.utils.unregister_class(ImportMOD3)
    bpy.types.INFO_MT_file_import.remove(menu_func_import)
 
 
if __name__ == "__main__":
    try:
        unregister()
    except:
        pass
    register()