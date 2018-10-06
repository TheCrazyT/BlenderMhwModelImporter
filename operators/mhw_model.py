#Ported to blender from "MT Framework tools" https://www.dropbox.com/s/4ufvrgkdsioe3a6/MT%20Framework.mzp?dl=0 
#(https://lukascone.wordpress.com/2017/06/18/mt-framework-tools/)

WEIGHTS3_BONES4 = 1
WEIGHTS7_BONES8 = 2
WEIGHTS0_BONES0 = 3

FMT_BONE="Bone.%04d"

EMBED_MODE_NONE = "embed_none"
EMBED_MODE_REFERENCE = "embed_reference"
EMBED_MODE_DATA = "embed_data"

LAYER_MODE_NONE = "layer_none"
LAYER_MODE_PARTS = "layer_parts"
LAYER_MODE_LOD = "layer_lod"

from bpy.types import EnumPropertyItem
ENUM_EMBED_MODE_NONE = (EMBED_MODE_NONE,'None', 'do not embed anything at all.')
ENUM_EMBED_MODE_REFERENCE = (EMBED_MODE_REFERENCE,'Reference original data.','Instead of embedding all data just add the path to the file. This is faster than embed data, but you need to make shure the file never gets deleted,changed or moved.')
ENUM_EMBED_MODE_DATA = (EMBED_MODE_DATA,'Embed original data.','Use this if you share the .blend file with others.')

ENUM_LAYER_MODE_NONE = (LAYER_MODE_NONE,'None', '')
ENUM_LAYER_MODE_PARTS = (LAYER_MODE_PARTS,'mesh parts','Try to move mesh parts evenly accross the layers')
ENUM_LAYER_MODE_LOD = (LAYER_MODE_LOD,'lod-level','Try group mesh parts based on their lod-level evenly accross the layers')

content = bytes("","UTF-8")
contentStream = None

from io import BytesIO
import binascii
import mathutils 
import base64
import zlib 
import bpy
import bmesh
import os
import configparser
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty, IntProperty
from bpy.types import Operator
from mathutils import Vector, Matrix, Euler
from struct import unpack, pack
from ..config import writeConfig, initConfig, setInstallPath, setChunkPath
from ..dbg import dbg

x64=64

(config,CHUNK_PATH,PATH) = initConfig()

WEIGHT_MULTIPLIER = 0.000977517
WEIGHT_MULTIPLIER2 = 0.25
BIT_LENGTH_10 = 0x3ff
def proxima(value1,value2=0,epsilon=0.0001):
    return (value1 <= (value2+epsilon)) and (value1 >= (value2-epsilon))


class matrix3:
    def __init__(self,v):
        self.row1 = [v,v,v]
        self.row2 = [v,v,v]
        self.row3 = [v,v,v]
        self.row4 = [v,v,v]

def readmatrix44(headerref):
    mtx = matrix3(0)
    if headerref.bendian:
        mtx.row1 = ReadBEVector4(headerref.fl)
        mtx.row2 = ReadBEVector4(headerref.fl)
        mtx.row3 = ReadBEVector4(headerref.fl)
        mtx.row4 = ReadBEVector4(headerref.fl)
    else:
        mtx.row1 = ReadVector4(headerref.fl)
        mtx.row2 = ReadVector4(headerref.fl)
        mtx.row3 = ReadVector4(headerref.fl)
        mtx.row4 = ReadVector4(headerref.fl)
    return mtx

def calcBonesAndWeightsArr(cnt,weights,bones):
    weightArrResult = []
    boneArrResult = []
    cwt = []
    cbn = []
    for b in range(0,cnt):
        if (weights[b]>0) and not proxima(weights[b]):
            try:
                fitem = cbn.index(bones[b])
            except:
                fitem = -1
            if fitem > -1:
                cwt[fitem] += weights[b]
            else:
                cbn.append(bones[b])
                cwt.append(weights[b])
    return (cwt,cbn)

def calcBonesAndWeights(cnt,weightVal,weightVal2,bns):
    global WEIGHT_MULTIPLIER
    wt = []
    wt.append((weightVal & BIT_LENGTH_10)*WEIGHT_MULTIPLIER)
    wt.append(((weightVal>>10) & BIT_LENGTH_10)*WEIGHT_MULTIPLIER)
    wt.append(((weightVal>>20) & BIT_LENGTH_10)*WEIGHT_MULTIPLIER)
    
    if cnt > 4:
        wt.append((weightVal2[0]) * WEIGHT_MULTIPLIER2)
        wt.append((weightVal2[0]) * WEIGHT_MULTIPLIER2)
        wt.append((weightVal2[0]) * WEIGHT_MULTIPLIER2)
        wt.append((weightVal2[0]) * WEIGHT_MULTIPLIER2)
        wt.append(1 - wt[0] - wt[1] - wt[2] - wt[3] - wt[4] - wt[5]- wt[6])
        if wt[7] < 0:
            wt[7] = 0
    else:
        wt.append(1 - wt[0] - wt[1] - wt[2])

    
    return calcBonesAndWeightsArr(cnt,wt,bns)


    
################################################################ Vertex Buffers
# TODO: move this shit to separate file
class MODVertexBuffer818904dc:
    def __init__(self,headerref,vertexcount):
        dbg("MODVertexBuffer818904dc %d" % vertexcount)
        self.vertarray   = []
        self.uvs         = []
        self.weights     = []
        self.bones       = []
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
            self.uvs.append((ReadHalfFloat(headerref.fl),1-ReadHalfFloat(headerref.fl)))
            ReadLong(headerref.fl)
    @staticmethod
    def getStructSize():
        return 4+4+4+1+1+1+1+4+2+2+4
    @staticmethod
    def getUVOFFAfterVert():
        return 1+1+1+1+4
    @staticmethod
    def getWeightsOFFAfterUVOFF():
        return -1
    @staticmethod
    def getBonesOFFAfterWeightsOFF():
        return -1

class MODVertexBufferf06033f:
    def __init__(self,headerref,vertexcount):
        dbg("MODVertexBufferf06033f %d" % vertexcount)
        self.vertarray   = []
        self.uvs         = []
        self.weights     = []
        self.bones       = []
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
            self.uvs.append((ReadHalfFloat(headerref.fl),1-ReadHalfFloat(headerref.fl)))
            wts = ReadLong(headerref.fl)
            bns = [ReadByte(headerref.fl),ReadByte(headerref.fl),ReadByte(headerref.fl),ReadByte(headerref.fl)]
            [weights,bones] = calcBonesAndWeights(4,wts,[],bns)
            self.weights.append(weights)
            self.bones.append(bones)
    @staticmethod
    def getStructSize():
        return 4+4+4+1+1+1+1+4+2+2+4+1+ 1+1+1
    @staticmethod
    def getUVOFFAfterVert():
        return 1+1+1+1+4
    @staticmethod
    def getWeightsOFFAfterUVOFF():
        return 0
    @staticmethod
    def getBonesOFFAfterWeightsOFF():
        return 0
    @staticmethod
    def getBoneMode():
        return WEIGHTS3_BONES4
        
class MODVertexBuffer81f58067:
    def __init__(self,headerref,vertexcount):
        dbg("MODVertexBuffer81f58067 %d" % vertexcount)
        self.vertarray   = []
        self.uvs         = []
        self.weights     = []
        self.bones       = []
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
            self.uvs.append((ReadHalfFloat(headerref.fl),1-ReadHalfFloat(headerref.fl)))
            wts = ReadLong(headerref.fl)
            wts2 = [ReadByte(headerref.fl),ReadByte(headerref.fl),ReadByte(headerref.fl),ReadByte(headerref.fl)]            
            bns = [ReadByte(headerref.fl),ReadByte(headerref.fl),ReadByte(headerref.fl),ReadByte(headerref.fl),
                ReadByte(headerref.fl),ReadByte(headerref.fl),ReadByte(headerref.fl),ReadByte(headerref.fl)]
            [weights,bones] = calcBonesAndWeights(8,wts,wts2,bns)
            self.weights.append(weights)
            self.bones.append(bones)

    @staticmethod
    def getStructSize():
        return 4+4+4+1+1+1+1+4+2+2+4+1+1+1+1+1 +1+1+1+1+1+1+1
    @staticmethod
    def getUVOFFAfterVert():
        return 1+1+1+1+4
    @staticmethod
    def getWeightsOFFAfterUVOFF():
        return -1
    @staticmethod
    def getBonesOFFAfterWeightsOFF():
        return -1
    @staticmethod
    def getBoneMode():
        return WEIGHTS7_BONES8
       
class MODVertexBufferf471fe45:
    def __init__(self,headerref,vertexcount):
        dbg("MODVertexBufferf471fe45 %d" % vertexcount)
        self.vertarray   = []
        self.uvs         = []
        self.uvs2        = []
        self.weights     = []
        self.bones       = []
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
            self.uvs.append((ReadHalfFloat(headerref.fl),1-ReadHalfFloat(headerref.fl)))
            self.uvs2.append((ReadHalfFloat(headerref.fl),1-ReadHalfFloat(headerref.fl)))
            wts = ReadLong(headerref.fl)
            bns = [ReadByte(headerref.fl),ReadByte(headerref.fl),ReadByte(headerref.fl),ReadByte(headerref.fl)]
            [weights,bones] = calcBonesAndWeights(4,wts,[],bns)
            self.weights.append(weights)
            self.bones.append(bones)
    @staticmethod
    def getStructSize():
        return 4+4+4+1+1+1+1+4+2+2+4
    @staticmethod
    def getUVOFFAfterVert():
        return 1+1+1+1+4
    @staticmethod
    def getWeightsOFFAfterUVOFF():
        return 0
    @staticmethod
    def getBonesOFFAfterWeightsOFF():
        return 0
    @staticmethod
    def getBoneMode():
        return WEIGHTS3_BONES4

class MODVertexBuffer3c730760:
    def __init__(self,headerref,vertexcount):
        dbg("MODVertexBuffer3c730760 %d" % vertexcount)
        self.vertarray   = []
        self.uvs         = []
        self.weights     = []
        self.bones       = []
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
            self.uvs.append((ReadHalfFloat(headerref.fl),1-ReadHalfFloat(headerref.fl)))
            wts = ReadLong(headerref.fl)
            bns = [ReadByte(headerref.fl),ReadByte(headerref.fl),ReadByte(headerref.fl),ReadByte(headerref.fl)]
            [weights,bones] = calcBonesAndWeights(4,wts,[],bns)
            self.weights.append(weights)
            self.bones.append(bones)
            
            ReadByte(headerref.fl)
            
            ReadByte(headerref.fl)
            ReadByte(headerref.fl)
            ReadByte(headerref.fl)
    @staticmethod
    def getStructSize():
        return 4+4+4+1+1+1+1+4+2+2+4+1+1+1+1+1+1+1+1
    @staticmethod
    def getUVOFFAfterVert():
        return 1+1+1+1+4
    @staticmethod
    def getWeightsOFFAfterUVOFF():
        return 0
    @staticmethod
    def getBonesOFFAfterWeightsOFF():
        return 0      
    @staticmethod
    def getBoneMode():
        return WEIGHTS3_BONES4

class MODVertexBufferb2fc0083:
    def __init__(self,headerref,vertexcount):
        dbg("MODVertexBufferb2fc0083 %d" % vertexcount)
        raise Exception("ToDo")
        self.vertarray   = []
        self.uvs         = []
        self.weights     = []
        self.bones       = []
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
            self.uvs.append((ReadHalfFloat(headerref.fl),1-ReadHalfFloat(headerref.fl)))
            ReadLong(headerref.fl)
    @staticmethod
    def getStructSize():
        return 4+4+4+1+1+1+1+4+2+2+4
    @staticmethod
    def getUVOFFAfterVert():
        return 1+1+1+1+4
    @staticmethod
    def getWeightsOFFAfterUVOFF():
        return -1
    @staticmethod
    def getBonesOFFAfterWeightsOFF():
        return -1
    @staticmethod
    def getBoneMode():
        return WEIGHTS0_BONES0
        
class MODVertexBuffer366995a7:
    def __init__(self,headerref,vertexcount):
        dbg("MODVertexBuffer366995a7 %d" % vertexcount)
        self.vertarray   = []
        self.uvs         = []
        self.weights     = []
        self.bones       = []
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
            self.uvs.append((ReadHalfFloat(headerref.fl),1-ReadHalfFloat(headerref.fl)))
            wts = ReadLong(headerref.fl)
            wts2 = [ReadByte(headerref.fl),ReadByte(headerref.fl),ReadByte(headerref.fl),ReadByte(headerref.fl)]            
            bns = [ReadByte(headerref.fl),ReadByte(headerref.fl),ReadByte(headerref.fl),ReadByte(headerref.fl),
                ReadByte(headerref.fl),ReadByte(headerref.fl),ReadByte(headerref.fl),ReadByte(headerref.fl)]
            [weights,bones] = calcBonesAndWeights(8,wts,wts2,bns)
            self.weights.append(weights)
            self.bones.append(bones)
            ReadLong(headerref.fl)
    @staticmethod
    def getStructSize():
        return 4+4+4+1+1+1+1+4+2+2+4+1+1+1+1 + 8+4
    @staticmethod
    def getUVOFFAfterVert():
        return 1+1+1+1+4
    @staticmethod
    def getWeightsOFFAfterUVOFF():
        return -1
    @staticmethod
    def getBonesOFFAfterWeightsOFF():
        return -1
    @staticmethod
    def getBoneMode():
        return WEIGHTS7_BONES8
        
class MODVertexBufferc9690ab8:
    def __init__(self,headerref,vertexcount):
        dbg("MODVertexBufferc9690ab8 %d" % vertexcount)
        raise Exception("ToDo")
        self.vertarray   = []
        self.uvs         = []
        self.weights     = []
        self.bones       = []
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
            ReadHalfFloat(headerref.fl)
            ReadHalfFloat(headerref.fl)
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
    @staticmethod
    def getStructSize():
        return 4+4+4+1+1+1+1+4+2+2+2+2+1+1+1+1 +1+1+1+1+1+1+1+1
    @staticmethod
    def getUVOFFAfterVert():
        return 1+1+1+1+4
    @staticmethod
    def getWeightsOFFAfterUVOFF():
        return -1
    @staticmethod
    def getBonesOFFAfterWeightsOFF():
        return -1
    @staticmethod
    def getBoneMode():
        return WEIGHTS7_BONES8
        
class MODVertexBuffer5e7f202d:
    def __init__(self,headerref,vertexcount):
        dbg("MODVertexBuffer5e7f202d %d" % vertexcount)
        raise Exception("ToDo")
        self.vertarray   = []
        self.uvs         = []
        self.weights     = []
        self.bones       = []
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
            self.uvs.append((ReadHalfFloat(headerref.fl),1-ReadHalfFloat(headerref.fl)))
            ReadLong(headerref.fl)
    @staticmethod
    def getStructSize():
        return 4+4+4+1+1+1+1+4+2+2+4
    @staticmethod
    def getUVOFFAfterVert():
        return 1+1+1+1+4
    @staticmethod
    def getWeightsOFFAfterUVOFF():
        return -1
    @staticmethod
    def getBonesOFFAfterWeightsOFF():
        return -1
    @staticmethod
    def getBoneMode():
        return WEIGHTS0_BONES0
        
class MODVertexBufferd829702c:
    def __init__(self,headerref,vertexcount):
        dbg("MODVertexBufferd829702c %d" % vertexcount)
        self.vertarray   = []
        self.uvs         = []
        self.weights     = []
        self.bones       = []
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
            self.uvs.append((ReadHalfFloat(headerref.fl),1-ReadHalfFloat(headerref.fl)))
    @staticmethod
    def getStructSize():
        return 4+4+4+1+1+1+1+4+2+2
    @staticmethod
    def getUVOFFAfterVert():
        return 1+1+1+1+4
    @staticmethod
    def getWeightsOFFAfterUVOFF():
        return -1
    @staticmethod
    def getBonesOFFAfterWeightsOFF():
        return -1
    @staticmethod
    def getBoneMode():
        return WEIGHTS0_BONES0  
        
class MODVertexBufferb8e69244:
    def __init__(self,headerref,vertexcount):
        dbg("MODVertexBufferd829702c %d" % vertexcount)
        self.vertarray   = []
        self.uvs         = []
        self.weights     = []
        self.bones       = []
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
            self.uvs.append((ReadHalfFloat(headerref.fl),1-ReadHalfFloat(headerref.fl)))
            wts = ReadLong(headerref.fl)
            wts2 = [ReadByte(headerref.fl),ReadByte(headerref.fl),ReadByte(headerref.fl),ReadByte(headerref.fl)]            
            bns = [ReadByte(headerref.fl),ReadByte(headerref.fl),ReadByte(headerref.fl),ReadByte(headerref.fl),
                ReadByte(headerref.fl),ReadByte(headerref.fl),ReadByte(headerref.fl),ReadByte(headerref.fl)]
            [weights,bones] = calcBonesAndWeights(8,wts,wts2,bns)
            self.weights.append(weights)
            self.bones.append(bones)

            ReadLong(headerref.fl)
            
            ReadByte(headerref.fl)
            ReadByte(headerref.fl)
            ReadByte(headerref.fl)
            ReadByte(headerref.fl)
            
    @staticmethod
    def getStructSize():
        return 4+4+4+1+1+1+1+4+2+2+4+1+1+1+1+1*8+4 +1+1+1+1
    @staticmethod
    def getUVOFFAfterVert():
        return 1+1+1+1+4
    @staticmethod
    def getWeightsOFFAfterUVOFF():
        return -1
    @staticmethod
    def getBonesOFFAfterWeightsOFF():
        return -1
    @staticmethod
    def getBoneMode():
        return WEIGHTS7_BONES8
MODVertexBuffera5104ca0 = MODVertexBuffer5e7f202d
MODVertexBufferf637401c = MODVertexBufferf06033f
MODVertexBuffera756f2f9 = MODVertexBufferd829702c

################################################################ END Vertex Buffers


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
    
#copied this code from http://davidejones.com/blog/1413-python-precision-floating-point/
def _wrhf(float32):
    F16_EXPONENT_BITS = 0x1F
    F16_EXPONENT_SHIFT = 10
    F16_EXPONENT_BIAS = 15
    F16_MANTISSA_BITS = 0x3ff
    F16_MANTISSA_SHIFT =  (23 - F16_EXPONENT_SHIFT)
    F16_MAX_EXPONENT =  (F16_EXPONENT_BITS << F16_EXPONENT_SHIFT)

    a = pack('>f',float32)
    b = binascii.hexlify(a)

    f32 = int(b,16)
    f16 = 0
    sign = (f32 >> 16) & 0x8000
    exponent = ((f32 >> 23) & 0xff) - 127
    mantissa = f32 & 0x007fffff
            
    if exponent == 128:
        f16 = sign | F16_MAX_EXPONENT
        if mantissa:
            f16 |= (mantissa & F16_MANTISSA_BITS)
    elif exponent > 15:
        f16 = sign | F16_MAX_EXPONENT
    elif exponent > -15:
        exponent += F16_EXPONENT_BIAS
        mantissa >>= F16_MANTISSA_SHIFT
        f16 = sign | exponent << F16_EXPONENT_SHIFT | mantissa
    else:
        f16 = sign
    return f16
def _rdhf(float16):
        s = int((float16 >> 15) & 0x00000001)    # sign
        e = int((float16 >> 10) & 0x0000001f)    # exponent
        f = int(float16 & 0x000003ff)            # fraction

        if e == 0:
            if f == 0:
                return int(s << 31)
            else:
                while not (f & 0x00000400):
                    f = f << 1
                    e -= 1
                e += 1
                f &= ~0x00000400
                #print(s,e,f)
        elif e == 31:
            if f == 0:
                return int((s << 31) | 0x7f800000)
            else:
                return int((s << 31) | 0x7f800000 | (f << 13))

        e = e + (127 -15)
        f = f << 13
        return unpack('f',pack('I',int((s << 31) | (e << 23) | f)))[0]

def Read8s(fl):
    return ReadByte(fl)*0.0078125
def ReadHalfFloat(fl):
    s = ReadShort(fl)
    res = _rdhf(s)
    #dbg("S: %08x R: %f" % (s,res))
    return res
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
    
def ReadBEVector3(fl):
    global pos,content
    res = unpack(">fff",content[pos[fl]:pos[fl]+4*3])
    pos[fl]+=4*3
    return list(res)
def ReadVector3(fl):
    global pos,content
    res = unpack("fff",content[pos[fl]:pos[fl]+4*3])
    pos[fl]+=4*3
    return list(res)
    
def ReadBEVector4(fl):
    global pos,content
    res = unpack(">ffff",content[pos[fl]:pos[fl]+4*4])
    pos[fl]+=4*4
    return list(res)
def ReadVector4(fl):
    global pos,content
    res = unpack("ffff",content[pos[fl]:pos[fl]+4*4])
    pos[fl]+=4*4
    return list(res)

def WriteHalfFloats(fl,floats32):
    global pos,content,contentStream
    p = b''
    for f in floats32:
        f16 = _wrhf(f)
        p += pack("<H",f16)
    contentStream.seek(pos[fl])
    contentStream.write(p)
    pos[fl] += 2*len(floats32)
def WriteFloats(fl,floats):
    global pos,content,contentStream
    #dbg("WriteFloats at 0x%08x %s" % (pos[fl],floats))
    if pos[fl]==0:
        raise Exception("Invalid write position")
    p = pack("%df" % len(floats),*floats)
    contentStream.seek(pos[fl])
    contentStream.write(p)
    pos[fl] += len(floats)*4
def WriteBytes(fl,bytes):
    global pos,content,contentStream
    #dbg("WriteBytes at 0x%08x %s" % (pos[fl],bytes))
    if pos[fl]==0:
        raise Exception("Invalid write position")
    p = pack("%dB" % len(bytes),*bytes)
    contentStream.seek(pos[fl])
    contentStream.write(p)
    pos[fl] += len(bytes)
def WriteLongs(fl,longs):
    global pos,content,contentStream
    #dbg("WriteLongs at 0x%08x %s" % (pos[fl],longs))
    if pos[fl]==0:
        raise Exception("Invalid write position")
    p = pack("%dL" % len(longs),*longs)
    contentStream.seek(pos[fl])
    contentStream.write(p)
    pos[fl] += len(longs)*4
def getPos(fl):
    if pos[fl] < 0 :
        raise Exception("invalid pos detected! [%d]" % pos[fl])
    if pos[fl] > 0x100000000 :
        raise Exception("invalid pos detected! [%d]" % pos[fl])
    return pos[fl]

    
def CollectStrips(fl,modf=1):
    dbg("CollectStrips")

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
    dbg("CollectTris %d" % num)
    res = []
    for i in range(0 ,num):
        res.append([x+modf for x in [ReadShort(fl) , ReadShort(fl) ,ReadShort(fl)]])
    return res
def CollectBETris(fl,num,modf=1):
    dbg("CollectBETris %d" % num)
    res = []
    for i in range(0 ,num):
        res.append([x+modf for x in [ReadBEShort(fl) , ReadBEShort(fl) ,ReadBEShort(fl)]])
    return res
def CollectBEStrips(fl,modf=1):
    dbg("CollectBEStrips")
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
            MeshPartOffset,
            uid,
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
            loadmeshdata,
            writemeshdata):
            self.MeshPartOffset = MeshPartOffset
            self.uid = uid
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
            self.writemeshdataF = writemeshdata
    def loadmeshdata(self):
        self.loadmeshdataF(self)
    def writeCustomProperties(self,fl):
        dbg("writeCustomProperties")
        headerref = self.headerref
        n = self.getName()
        if not n in bpy.data.objects:
            dbg("Mesh %s not found!" % n)
            return
        obj = bpy.data.objects[n]
        bm = obj.data
        if "LOD" in bm:
            self.writeLOD(fl,bm["LOD"])
    def writeLOD(self,fl,lod):
        Seek(fl,self.MeshPartOffset+self.getLODOffset())
        WriteLongs(fl,[lod])
    def getLODOffset(self):
        return 8
    def writeVertexes(self,fl):
        dbg("writeVertexes uid:%d" % self.uid)
        headerref = self.headerref
        n = self.getName()
        if not n in bpy.data.objects:
            dbg("Mesh %s not found!" % n)
            return
        obj = bpy.data.objects[n]
        bm = obj.data
        my_id = bm.vertex_layers_int['id']
        verts2 = sorted(bm.vertices, key=lambda v: my_id.data[v.index].value)
        verts = [vert.co for vert in verts2]
        
        
        uvs = {}
        if len(bm.uv_layers)>0:
            vertIdxMap = {}
            i1 = 0
            for i2 in [vert.index for vert in verts2]:
                vertIdxMap[i2] = i1
                i1 += 1
            
            for p in bm.polygons:
                for loop in p.loop_indices:
                    uvs[vertIdxMap[bm.loops[loop].vertex_index]] = bm.uv_layers[0].data[loop].uv
                
        weights = {}
        bones = {}
        vi = 0
        for v in verts2:
            bones[v.index] = [int(obj.vertex_groups[g.group].name.split(".")[1]) for g in v.groups]
            vertWeights = []
            for g in v.groups:
                vertWeights.append(g.weight)
            weights[v.index] = vertWeights
        
        BOFF=self.VertexSub+self.FaceAdd
        dbg("self.VertexOffset %08x" % (headerref.VertexOffset+self.VertexOffset+self.BlockSize*BOFF))
        Seek(fl, (headerref.VertexOffset+self.VertexOffset+self.BlockSize*BOFF))
        self.writemeshdataF(self,fl,verts,uvs,weights,bones)
    def getName(self):
        return "MyObject.%05d.%08x" % (self.uid,self.BlockType)

class MODBoneInfo2:
    def __init__(self,internalId,fl,bendian):
        #self.id = ReadShort(fl)
        #self.internalId = internalId
        ReadShort(fl)
        self.id = internalId
        self.parentid = ReadByte(fl)
        self.child = ReadByte(fl)
        fseek(fl,20)

        

class ExportMOD3(Operator, ImportHelper):
    bl_idname = "custom_import.export_mhw"
    bl_label = "Export MHW MOD file (.mod3)"
 
    # ImportHelper mixin class uses this
    filename_ext = ".mod3"
 
    filter_glob = StringProperty(default="*.mod3", options={'HIDDEN'}, maxlen=255)
    
    #overwrite_lod = BoolProperty(name="Force LOD1 (experimentel)",
    #            description="overwrite the level of detail of the other meshes (for example if you used 'Only import high LOD-parts').",
    #            default=False)
    def execute(self, context):
        global content,pos,contentStream
        if not 'data' in bpy.data.texts:
            raise Exception("Make shure to import with \"Reference/Embed original data.\" first.")
        scene = bpy.context.scene
        for obj in scene.objects:
            if obj.type == 'MESH':
                scene.objects.active = obj
                bpy.ops.object.mode_set(mode='OBJECT')
        dataText = bpy.data.texts['data'].lines[0].body
        if dataText[0:5]=="path:":
            path = dataText[5:]
            dbg("path:%s" % path)
            with open(path, 'rb') as content_file:
                content = content_file.read()
                contentStream = BytesIO(content)
        else:
            data = base64.b64decode(dataText)
            content = zlib.decompress(data)
        i = ImportMOD3(self)
        i.init_main()
        i.fl = 0
        Seek(i.fl,0)
        i.readHeader()
        i.readMeshParts()
        for p in i.parts:
            p.writeVertexes(i.fl)
            p.writeCustomProperties(i.fl)
            
            content = contentStream.getvalue()
        with open(self.filepath, 'wb') as content_file:
            content_file.write(content)
        return {'FINISHED'}
        
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
    use_layers = EnumProperty(
            name="Layer mode",
            description="Chose what mesh should be put to what layer.",
            items=[ENUM_LAYER_MODE_NONE,ENUM_LAYER_MODE_PARTS,ENUM_LAYER_MODE_LOD],
            default=LAYER_MODE_PARTS
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
    only_import_lod = IntProperty(
            name="Only import LOD parts with level:",
            description="If not -1 it imports only parts with a defined level of detail.",
            default=-1,
    )
    embed_mode = EnumProperty(
            name="Embed mode",
            description="Used for beeing able to export the object.",
            items=[ENUM_EMBED_MODE_NONE,ENUM_EMBED_MODE_REFERENCE,ENUM_EMBED_MODE_DATA],
            default=EMBED_MODE_REFERENCE
    )
    do_read_bones = BoolProperty(
            name="Import bones and armature",
            description="Imports bones ... useful for testing poses.",
            default=True)


    def init_main(self):
        self.headerref = self
        self.parts = []

    
    def readHeader(self):
        dbg("readHeader")
        fl = self.fl
        self.bendian = False
        self.ID = ReadLong(fl);
        if self.ID != 0x444f4d:
            raise Exception("Invalid Header")
        self.Version = ReadByte(fl)
        self.Version2 = ReadByte(fl) 
        self.BoneCount = ReadShort(fl)
        self.MeshCount = ReadShort(fl)
        self.MaterialCount = ReadShort(fl)
        self.VertexCount = ReadLong(fl)
        self.FaceCount = ReadLong(fl)
        self.VertexIds = ReadLong(fl)
        self.VertexBufferSize = ReadLong(fl)
        self.SecondBufferSize = ReadLong(fl)
        if self.Version < 190:
            self.TextureCount = ReadLong(fl)
        self.GroupCount = ReadPointer(fl,x64)
        if self.Version < 190 or self.Version > 220: 
            self.BoneMapCount = ReadPointer(fl,x64)
        self.BonesOffset = ReadPointer(fl,x64)
        self.GroupOffset = ReadPointer(fl,x64)
        self.TextureOffset = ReadPointer(fl,x64)
        self.MeshOffset = ReadPointer(fl,x64)
        self.VertexOffset =ReadPointer(fl,x64)
        if self.Version < 190:
            self.Vertex2Offset = ReadLong(fl)
        self.FacesOffset = ReadPointer(fl,x64)
        self.UnkOffset = ReadPointer(fl,x64)
        if self.Version < 190:
            self.unkOffset2 = ReadLong(fl)
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
        dbg("%d" % pos[fl])
    
    
    def addArmature(self,name):
        bpy.ops.object.armature_add()
        ob = bpy.context.scene.objects.active
        #ob.name ="give me a good name!"
        arm = ob.data
        arm.name = name
        return arm
        #bpy.ops.object.mode_set(mode='EDIT')
        #for i in range(3):
        #    bpy.ops.armature.extrude()
        #    bpy.ops.transform.translate(value=(0.0, 0.0, 1.0))
         
        #for i in range(len(arm.edit_bones)):
        #    eb = arm.edit_bones[i]
           # eb.connected = True
        #    eb.roll = i*(20/180*pi)
        #    eb.tail[0] = eb.head[0] + 0.2*(i+1)
        #bpy.ops.object.mode_set(mode='OBJECT')
    
    def addChildBones(self,a,parentBone,id,bones):
        dbg("addChildBones %d" % id)
        i = 0
        for b in bones:
            if ((id == b.parentid)and(b.id != id)):
                dbg("addChildBone %d with parent %d" % (b.id,id))
                #bone2 = bpy.ops.armature.bone_primitive_add(name=FMT_BONE % b.id)
                #bpy.context.scene.objects.active = bone2
                #bpy.ops.armature.select_all(action='DESELECT')
                #parentBone.select_tail = True
                #bpy.ops.armature.extrude()
                #bone2 = a.edit_bones[-1]
                bone2 = a.edit_bones.new(FMT_BONE % b.id)
                bone2.parent = parentBone
                #bone2.head = Vector((1,0,0))
                #bone2.tail = Vector((0,0,0))
                lm = self.lmatrices[i]
                r1 = lm.row1
                r2 = lm.row2
                r3 = lm.row3
                r4 = lm.row4
                #bone2.head = parentBone.tail
                #bone2.tail = parentBone.head+Vector((0.0,0.0,50.0))
                t = Matrix((
                          (r1[0],r1[1],r1[2],r1[3]),
                          (r2[0],r2[1],r2[2],r2[3]),
                          (r3[0],r3[1],r3[2],r3[3]),
                          (r4[0],r4[1],r4[2],r4[3])
                          ))
                #TODO
                bone2.head = parentBone.tail+Vector((10.0*i,0.0,0.0))
                bone2.tail = bone2.head+Vector((0.0,0.0,50.0))
                #bone2.transform(t)

                #bone2.matrix = Matrix((
                #                      (r1[0],r1[1],r1[2],0.0),
                #                      (r2[0],r2[1],r2[2],0.0),
                #                      (r3[0],r3[1],r3[2],0.0),
                #                      (r4[0],r4[1],r4[2],0.0)
                #                      ))
                #bone2.bbone_x = 5.0
                #bone2.bbone_z = 5.0

                self.addChildBones(a,bone2,b.id,bones)
                i += 1
    
    def readBones(self):
        headerref = self.headerref
        fl = self.fl
        Seek(fl,self.BonesOffset)
        _MODBoneInfo = None
        if headerref.Version == 237:
            _MODBoneInfo = MODBoneInfo2
        else:
            raise Exception("not implemented!")
        self.bones = []
        self.lmatrices = []
        self.amatrices = []
        self.remaptable = []
        self.remaptablesize = 0
        for b in range(0,headerref.BoneCount):
            self.bones.append(_MODBoneInfo(b,headerref.fl,headerref.bendian))
        for b in range(0,headerref.BoneCount):
            self.lmatrices.append(readmatrix44(headerref))
        for b in range(0,headerref.BoneCount):
            self.amatrices.append(readmatrix44(headerref))
            self.remaptablesize = 512 if headerref.Version == 137 else 256
        for b in range(0,self.remaptablesize):
            self.remaptable.append(ReadByte(headerref.fl))
        if headerref.BoneMapCount != None:
            raise Exception("not implemented")

    def createBones(self):
        a = self.addArmature("MainArmature")
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.armature.select_all(action='DESELECT')
        a.edit_bones[0].select_tail = True
        dbg("bones: %d" % len(self.bones))
        i = 0
        k = 0
        parentBone = a.edit_bones[-1]
        parentBone.name = FMT_BONE % 255

        for b in self.bones:
            dbg("bone: %d has parent %d" % (b.id,b.parentid))
            if (b.parentid == b.id)or(b.parentid == 255):
                bone = a.edit_bones.new(FMT_BONE % b.id)

                lm = self.lmatrices[i]
                r1 = lm.row1
                r2 = lm.row2
                r3 = lm.row3
                r4 = lm.row4
                t = Matrix((
                    (r1[0],r1[1],r1[2],r1[3]),
                    (r2[0],r2[1],r2[2],r2[3]),
                    (r3[0],r3[1],r3[2],r3[3]),
                    (r4[0],r4[1],r4[2],r4[3])
                ))
                bone.parent = parentBone
                bone.head = parentBone.tail+Vector((10.0*k,0.0,0.0))
                bone.tail = bone.head+Vector((0.0,0.0,50.0))
                #bone.transform(t)
                #TODO
                #bone.tail = Vector((-20.0*k,0.0,1.0))
                #bone.head = Vector((-20.0*k,0.0,0.0))
                #bone.tail = Vector((0.0,0.0,50.0))
                #bone.head = Vector((0.0,0.0,0.0))
                k += 1


                self.addChildBones(a,bone,b.id,self.bones)
            i += 1
        bpy.ops.object.mode_set(mode='OBJECT')
        
        for o in bpy.data.objects:
            if o.type == "MESH":
                bpy.context.scene.objects.active = o
                bpy.ops.object.modifier_add(type='ARMATURE')
                bpy.context.object.modifiers['Armature'].object = bpy.data.objects['Armature']
    
    def writemeshdatav1(self,meshPart,fl,vertices,uvs,weights,bones):
        raise Exception("NotImplementedError")
    def writemeshdatav2(self,meshPart,fl,vertices,uvs,weights,bones):
        raise Exception("NotImplementedError")
    def writemeshdatav3(self,meshPart,fl,vertices,uvs,weights,bones):
        dbg("writemeshdatav3 %s meshPart.VertexCount: %d , vertices: %d" % (meshPart.getName(),meshPart.VertexCount,len(vertices)))
        if meshPart.VertexCount != len(vertices):
            raise Exception("different vertices counts are not (yet) permitted!")
        uvi = 0
        vi = 0
        for v3 in vertices:
            if(len(v3) != 3):
                raise Exception("verticesCount != 3")
            vStartPos = getPos(fl)
            #dbg("vStartPos: %08x" % vStartPos)
            WriteFloats(fl,v3)
            vertexBuffer = eval("MODVertexBuffer%08x" % meshPart.BlockType)
            structSize = vertexBuffer.getStructSize()
            uvOFF = vertexBuffer.getUVOFFAfterVert()
            fseek(fl,uvOFF)
            if len(uvs)>0:
                WriteHalfFloats(fl,[uvs[uvi].x,1-uvs[uvi].y])
                uvi += 1
            else:
                fseek(fl,4)
            weightsOff = vertexBuffer.getWeightsOFFAfterUVOFF()
            bonesOff  = vertexBuffer.getBonesOFFAfterWeightsOFF()
            if (weightsOff != -1) and (bonesOff != -1) and (vi in weights) and (vi in bones):
                fseek(fl,weightsOff)
                if(vertexBuffer.getBoneMode() == WEIGHTS3_BONES4):
                    w1 = 0
                    w2 = 0
                    w3 = 0
                    lw = len(weights[vi])
                    if lw > 0:
                        w1 = weights[vi][0]
                    if lw > 1:
                        w2 = weights[vi][1]
                    if lw > 2:
                        w3 = weights[vi][2]
                    weightVal = int(w1 / WEIGHT_MULTIPLIER) + (int(w2/ WEIGHT_MULTIPLIER)<<10) + (int(w3/ WEIGHT_MULTIPLIER)<<20)
                    WriteLongs(fl,[weightVal])
                    fseek(fl,bonesOff)
                    
                    boneList = bones[vi]
                    while len(bones[vi]) < 4:
                        boneList.append(0)
                    WriteBytes(fl,boneList[0:4])
                elif(vertexBuffer.getBoneMode() == WEIGHTS7_BONES8):
                    w1 = 0
                    w2 = 0
                    w3 = 0

                    w4 = 0
                    w5 = 0
                    w6 = 0
                    w7 = 0


                    lw = len(weights[vi])
                    if lw > 0:
                        w1 = weights[vi][0]
                    if lw > 1:
                        w2 = weights[vi][1]
                    if lw > 2:
                        w3 = weights[vi][2]

                    if lw > 3:
                        w4 = weights[vi][3]
                    if lw > 4:
                        w5 = weights[vi][4]
                    if lw > 5:
                        w6 = weights[vi][5]
                    if lw > 6:
                        w7 = weights[vi][6]
                    weightVal = int(w1 / WEIGHT_MULTIPLIER) + (int(w2/ WEIGHT_MULTIPLIER)<<10) + (int(w3/ WEIGHT_MULTIPLIER)<<20)
                    WriteLongs(fl,[weightVal])

                    WriteBytes(fl,[int(w4 / WEIGHT_MULTIPLIER2) & 0xFF,int(w5 / WEIGHT_MULTIPLIER2) & 0xFF,int(w6 / WEIGHT_MULTIPLIER2) & 0xFF,int(w7 / WEIGHT_MULTIPLIER2) & 0xFF])
                    
                    fseek(fl,bonesOff)
                    boneList = bones[vi]
                    while len(bones[vi]) < 8:
                        boneList.append(0)
                    WriteBytes(fl,boneList[0:8])
                else:
                    weightsOff = 0
                    bonesOff = 0
            else:
                weightsOff = 0
                bonesOff = 0
                
                
                
            #dbg("Next start pos: %08x (structSize: %d)" % (vStartPos+structSize,structSize))
            Seek(fl,vStartPos+structSize) 
            vi += 1
        
    def loadmeshdatav1(self,meshPart):
        f = eval("MODVertexBuffer%08x" % meshPart.BlockType)
        headerref = meshPart.headerref
        if f != None:
            Seek(headerref.fl,((headerref.VertexOffset+meshPart.VertexOffset)+(BlockSize*(meshPart.VertexSub+meshPart.FaceAdd))))
            meshPart.meshdata = f(headerref,meshPart.VertexCount)
            Seek(headerref.fl,(headerref.FacesOffset+FaceOffset*2))
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
            Seek(headerref.fl,(VOFF+meshPart.BlockSize*BOFF))
            meshPart.meshdata = f(headerref,meshPart.VertexCount)
            Seek(headerref.fl,(headerref.FacesOffset+meshPart.FaceOffset*2))
            meshPart.FaceCount = int(meshPart.FaceCount/3)
            if headerref.bendian:
                meshPart.meshdata.facearray = CollectBETris(headerref.fl,meshPart.FaceCount,0-meshPart.VertexSub)
            else:
                meshPart.meshdata.facearray = CollectTris(headerref.fl,meshPart.FaceCount,0-meshPart.VertexSub)
        else:
            raise Exception("Unknown block hash [%08x] for MTF v1 model format.\n" % meshPart.BlockType)

    def readMeshPartv1(self,uid):
        MeshPartOffset = getPos(self.fl)
        if self.bendian:
            fl = self.fl
            id = ReadBEShort(fl)
            Material = ReadBEShort(fl )
            ReadByte(fl)
            LOD = ReadByte(fl)
            readshort(fl)
            BlockSize = ReadByte(fl)
            BlockType = ReadByte(fl)
            fseek(fl,2)
            VertexCount = ReadBEShort(fl) 
            ReadShort(fl)
            VertexSub = ReadBELong(fl)
            VertexOffset = ReadBELong(fl) 
            fseek(fl,4)
            FaceOffset = ReadBELong(fl)
            FaceCount = ReadBELong(fl)
            FaceAdd = ReadBELong(fl)
            fseek(fl,6)
            boneremapid = ReadByte(fl)+1
            fseek(fl,5)
        else:
            fl = self.fl
            id = ReadShort(fl)
            Material = ReadShort(fl )
            ReadByte(fl)
            LOD = ReadByte(fl)
            readshort(fl)
            BlockSize = ReadByte(fl)
            BlockType = ReadByte(fl)
            fseek(fl,2)
            VertexCount = ReadShort(fl) 
            ReadShort(fl)
            VertexSub = ReadLong(fl)
            VertexOffset = ReadLong(fl) 
            fseek(fl,4)
            FaceOffset = ReadLong(fl) 
            FaceCount = ReadLong(fl)
            FaceAdd = ReadLong(fl) 
            fseek(fl,6)
            boneremapid = ReadByte(fl)+1
            fseek(fl,5)
        return MeshPart(
            MeshPartOffset,
            uid,
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
            None,
            boneremapid,
            self,
            self.loadmeshdatav1,
            self.writemeshdatav1)


    def readMeshPartv2(self,uid):
        raise Exception("readMeshPartv2 not implemented")
    def readMeshPartv3(self,uid):
        headerref = self.headerref
        MeshPartOffset = getPos(headerref.fl)
        ReadShort(headerref.fl)
        VertexCount = ReadShort(headerref.fl)     
        id = ReadShort(headerref.fl)
        ReadShort(headerref.fl)
        lod = ReadLong(headerref.fl)
        ReadShort(headerref.fl)
        BlockSize = ReadByte(headerref.fl)
        ReadByte(headerref.fl)
        VertexSub = ReadLong(headerref.fl)
        VertexOffset = ReadLong(headerref.fl)
        BlockType = ReadLong(headerref.fl)
        FaceOffset = ReadLong(headerref.fl)
        FaceCount = ReadLong(headerref.fl)
        FaceAdd = ReadLong(headerref.fl)
        boneremapid = ReadByte(headerref.fl)+1
        fseek(headerref.fl,39)
        return MeshPart(
            MeshPartOffset,
            uid,
            id,
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
            self.loadmeshdatav3,
            self.writemeshdatav3)
    
    def readMeshParts(self):
        dbg("readMeshParts, meshOffset: %08x" % self.MeshOffset)
        Seek(self.fl,self.MeshOffset)
        if(self.Version == 237):
            readMeshPart = self.readMeshPartv3
        elif(self.Version < 190):
            readMeshPart = self.readMeshPartv1
        else:
            readMeshPart = self.readMeshPartv2
        for i in range(0,self.MeshCount):
           self.parts.append(readMeshPart(i))
        dbg("%d %d" % (len(self.parts),self.MeshCount))

    def readVertexes(self):
        Seek(self.fl,self.VertexOffset)
        for m in self.parts:
            m.loadmeshdata()

    def parseMrl3(self,filepath):
        global PATH,CHUNK_PATH,content

        from .mhw_texture import doImportTex

        
        if not os.path.isfile(filepath):
            dbg("%s not found" % filepath)
            return
        
        if not os.path.isdir(CHUNK_PATH):
            raise Exception("Chunkdirectory %s does not exist!" % CHUNK_PATH)
        
        with open(filepath, 'rb') as content_file:
            content = content_file.read()

        fl      = 1
        Seek(fl,0)
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
            dbg("importing texture: %s" % (texpath))
            doImportTex(texpath)
    
    def execute(self, context):
        global content,CHUNK_PATH
        
        self.embed_data = True if self.embed_mode == EMBED_MODE_DATA else False
        self.reference_data = True if self.embed_mode == EMBED_MODE_REFERENCE else False
        self.init_main()
        CHUNK_PATH = self.chunk_path
        if CHUNK_PATH[len(CHUNK_PATH)-1] == '\\':
            CHUNK_PATH = CHUNK_PATH[0:len(CHUNK_PATH)-1]
        PATH = self.install_path
        if not os.path.isdir(PATH):
            raise Exception("Install path %s not found!" % PATH)
            
        setInstallPath(PATH)
        setChunkPath(CHUNK_PATH)
        writeConfig()
        if(self.import_textures):
            self.parseMrl3(self.filepath.replace(".mod3",".mrl3"))
        if(self.use_layers != LAYER_MODE_NONE):
            dbg("using layers %s" % self.use_layers)
        with open(self.filepath, 'rb') as content_file:
            fl = 0
            content = content_file.read()
            if self.reference_data:
                if('data' in bpy.data.texts):
                    dataText = bpy.data.texts['data']
                    dataText.clear()
                else:
                    dataText = bpy.data.texts.new('data')
                dataText.from_string("path:%s" % self.filepath)
            else:
                if self.embed_data:
                    cdata = zlib.compress(content)
                    dbg("len of compressed-data: %d" % len(cdata))
                    data = base64.b64encode(cdata).decode("utf-8")
                    dbg("len of b64-data: %d" % len(data))
                    if('data' in bpy.data.texts):
                        dataText = bpy.data.texts['data']
                        dataText.clear()
                    else:
                        dataText = bpy.data.texts.new('data')
                    dataText.from_string(data)
        self.startImport(fl,content)
        if(self.import_textures):
            area = next(area for area in bpy.context.screen.areas if area.type == 'VIEW_3D')
            space = next(space for space in area.spaces if space.type == 'VIEW_3D')
            space.viewport_shade = "TEXTURED"

        return {'FINISHED'}        
    def startImport(self,fl,content):
        if not "shadeless" in bpy.data.materials:
            shadeless = bpy.data.materials.new("Shadeless")
        else:
            shadeless = bpy.data.materials["Shadeless"]
        shadeless.use_shadeless = True
        shadeless.use_face_texture = True

        self.fl = fl
        Seek(fl,0)
            
        self.readHeader()
        if self.do_read_bones:
            self.readBones()
        self.readMeshParts()
        self.readVertexes()
        
        fi = 0
        pi = 0
        rpi = -1
        lodlayers = {}
        clod = 1
        if(self.use_layers == LAYER_MODE_LOD):
            for m in self.parts:
                if not m.LOD in lodlayers:
                    lodlayers[m.LOD] = clod
                    clod += 1
        dbg("self.parts: %d" % len(self.parts))
        for m in self.parts:
            if ((self.only_import_lod < 0)and(self.only_import_lod_1)) and (m.LOD != 1):
                dbg("Skipped mesh %d because of lod level: %d, expected: 1" % (pi,m.LOD))
                pi += 1
                continue
            if (self.only_import_lod > -1) and (m.LOD != self.only_import_lod):
                dbg("Skipped mesh %d because of lod level: %d , expected: %d" % (pi,m.LOD,self.only_import_lod))
                pi += 1
                continue
            if m.meshdata != None:
                rpi += 1
                dbg("Import mesh %d" % pi)
                bm = bmesh.new()
                my_id = bm.verts.layers.int.new('id')
                bm.verts.ensure_lookup_table()
                mesh = bpy.data.meshes.new("mesh")  # add a new mesh
                s = m.getName()
                obj = bpy.data.objects.new(s, mesh)  # add a new object using the mesh
                dbg("%s %d     %d" % (s,m.VertexCount,len(m.meshdata.vertarray)))
                verts  = []
                verts2 = []
                faces = []
                face_vertex_index = {}
                bmfaces = []
                vi = 0
                for v in m.meshdata.vertarray:
                    #dbg(v)
                    verts2.append(v)
                    bmv = bm.verts.new(v)
                    bmv[my_id] = vi
                    bmv.index = vi
                    verts.append(bmv)
                    vi += 1

                
                if(self.import_textures):
                    tex = bm.faces.layers.tex.new("main_uv_texture")
                    uv = bm.loops.layers.uv.new("main_uv_layer")

                fi = 0
                for f in m.meshdata.facearray:
                    addFace=True
                    for x in f:
                        if x >= len(verts):
                            addFace = False
                            #dbg("%d not in verts [%d]" % (x,len(verts)))
                    if addFace:
                        #if fi<30:
                        vts  = [verts[x] for x in f]
                        vts2 = [verts2[x] for x in f]
                        uvs  = [m.meshdata.uvs[x] for x in f]
                        #dbg(vts)
                        #dbg(vts2)
                        #dbg(f)
                        faces.append(vts)
                        fi+=1
                        try:
                            face = bm.faces.new(vts)
                            vindices = [x for x in f]
                            if(self.import_textures):
                                face[tex].image = bpy.data.images[0]
                                vi = 0
                                for loopi in range(0,len(face.loops)):
                                    loop = face.loops[loopi]
                                    loop[uv].uv = uvs[vi]
                                    vi += 1
                            bmfaces.append(face)
                            face_vertex_index[face] = vindices
                        except:
                            pass
                        #pass
                    else:
                        raise Exception("Problem with face:%s [vert len:%d,pos:%08x]" % (f,len(verts),pos[fl]))

                scene = bpy.context.scene
                scene.objects.link(obj)  # put the object into the scene (link)
                if(self.use_layers == LAYER_MODE_PARTS):
                    for i in range(19):
                        obj.layers[1+i] = (i == (rpi % 19)) # we only have 20 layers available ... sadly
                if(self.use_layers == LAYER_MODE_LOD):
                    for i in range(19):
                        obj.layers[1+i] = (1+i == (lodlayers[m.LOD])) # we only have 20 layers available ... sadly
                    
                scene.objects.active = obj  # set as the active object in the scene
                obj.select = True  # select object

                # make the bmesh the object's mesh
                bm.to_mesh(mesh)
                
                
                if len(verts)>0:
                    boneIds = []
                    for v in verts:
                        v2 = verts2[v[my_id]]
                        if (len(m.meshdata.bones)>0) and len(m.meshdata.bones[v[my_id]])>0:
                            wi = 0
                            for bId in m.meshdata.bones[v[my_id]]:
                                if bId not in boneIds:
                                    boneIds.append(bId)
                                    vg = obj.vertex_groups.new(FMT_BONE % bId)
                                else:
                                    vg = obj.vertex_groups[FMT_BONE % bId]
                                #dbg("add %d to vg: Bone%d" % (v.index,bId))
                                vg.add([v.index],m.meshdata.weights[v[my_id]][wi],"ADD")
                                wi += 1

                mesh.materials.append(shadeless)
                mesh["LOD"] = m.LOD

                bm.free()  # always do this when finished
            else:
                dbg("Skipped mesh %d because of empty data" % pi)

            pi += 1

        if self.do_read_bones:
            self.createBones()
        
# Only needed if you want to add into a dynamic menu
def menu_func_import(self, context):
    self.layout.operator(ImportMOD3.bl_idname, text="MHW MOD (.mod3)")
def menu_func_export(self, context):
    self.layout.operator(ExportMOD3.bl_idname, text="MHW MOD (.mod3)")


