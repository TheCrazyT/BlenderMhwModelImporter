from ..dbg import dbg
from ..common.fileOperations import *
from ..common.constants import *
def proxima(value1,value2=0,epsilon=0.0001):
    return (value1 <= (value2+epsilon)) and (value1 >= (value2-epsilon))

def calcBonesAndWeightsArr(cnt,weights,bones):
    weightArrResult = []
    boneArrResult = []
    cwt = []
    cbn = []
    #for b in range(0,cnt):
    #    if (weights[b]>0) and not proxima(weights[b]):
    #        try:
    #            fitem = cbn.index(bones[b])
    #        except:
    #            fitem = -1
    #        if fitem > -1:
    #            cwt[fitem] += weights[b]
    #        else:
    #            cbn.append(bones[b])
    #            cwt.append(weights[b])
    #return (cwt,cbn)
    return (weights,bones)

def calcBonesAndWeights(cnt,weightVal,weightVal2,bns):
    global WEIGHT_MULTIPLIER
    wt = []
    w1 = (weightVal & BIT_LENGTH_10)*WEIGHT_MULTIPLIER
    w2 = ((weightVal>>10) & BIT_LENGTH_10)*WEIGHT_MULTIPLIER
    w3 = ((weightVal>>20) & BIT_LENGTH_10)*WEIGHT_MULTIPLIER
    w4 = 1.0 - w1 - w2 - w3
    wt.append(w1)
    wt.append(w2)
    wt.append(w3)
    wt.append(w4)
    
    if cnt > 4:
        wt.append((weightVal2[0]) * WEIGHT_MULTIPLIER2)
        wt.append((weightVal2[1]) * WEIGHT_MULTIPLIER2)
        wt.append((weightVal2[2]) * WEIGHT_MULTIPLIER2)
        wt.append((weightVal2[3]) * WEIGHT_MULTIPLIER2)
        wt.append(1 - wt[0] - wt[1] - wt[2] - wt[3] - wt[4] - wt[5]- wt[6])
        if wt[7] < 0:
            wt[7] = 0
    else:
        wt.append(1 - wt[0] - wt[1] - wt[2])

    
    return calcBonesAndWeightsArr(cnt,wt,bns)
def basicAppendEmptyVertices(cls,fl,VertexRegionEnd,oldVertexCount,addVertexCount):
    dbg("basicAppendEmptyVertices %08x %d %d" % (VertexRegionEnd,oldVertexCount,addVertexCount))
    if(addVertexCount > 0):
        InsertEmptyBytes(fl,VertexRegionEnd,cls.getStructSize()*addVertexCount)
    elif(addVertexCount < 0):
        subVertexCount = 0-addVertexCount
        DeleteBytes(fl,VertexRegionEnd-subVertexCount*cls.getStructSize(),cls.getStructSize()*subVertexCount)


class MODVertexBuffer818904dc:
    def __init__(self,headerref,vertexcount):
        dbg("MODVertexBuffer818904dc %d" % vertexcount)
        self.vertarray   = []
        self.uvs         = []
        self.weights     = []
        self.bones       = []
        self.normalarray = []
        self.headerref   = headerref
        self.vertexcount = vertexcount
        for i in range(0,vertexcount):
            if headerref.bendian:
                self.vertarray.append([ReadBEFloat(headerref.fl),ReadBEFloat(headerref.fl),ReadBEFloat(headerref.fl)])
            else:
                self.vertarray.append([ReadFloat(headerref.fl),ReadFloat(headerref.fl),ReadFloat(headerref.fl)])
            self.normalarray.append((Read8s(headerref.fl),Read8s(headerref.fl),Read8s(headerref.fl)))
            ReadByte(headerref.fl)
            ReadLong(headerref.fl)
            self.uvs.append((ReadHalfFloat(headerref.fl),1-ReadHalfFloat(headerref.fl)))
            ReadLong(headerref.fl)
    @staticmethod
    def getStructSize():
        return 4+4+4+1+1+1+1+4+2+2+4
    @staticmethod
    def getUVOFFAfterNormals():
        return 1+4
    @staticmethod
    def getWeightsOFFAfterUVOFF():
        return -1
    @staticmethod
    def getBonesOFFAfterWeightsOFF():
        return -1
    @classmethod
    def appendEmptyVertices(cls,fl,VertexRegionEnd,oldVertexCount,addVertexCount):
        basicAppendEmptyVertices(cls,fl,VertexRegionEnd,oldVertexCount,addVertexCount)

class MODVertexBufferf06033f:
    def __init__(self,headerref,vertexcount):
        dbg("MODVertexBufferf06033f %d" % vertexcount)
        self.vertarray   = []
        self.uvs         = []
        self.weights     = []
        self.bones       = []
        self.normalarray = []
        self.headerref   = headerref
        self.vertexcount = vertexcount
        for i in range(0,vertexcount):
            if headerref.bendian:
                self.vertarray.append([ReadBEFloat(headerref.fl),ReadBEFloat(headerref.fl),ReadBEFloat(headerref.fl)])
            else:
                self.vertarray.append([ReadFloat(headerref.fl),ReadFloat(headerref.fl),ReadFloat(headerref.fl)])
            self.normalarray.append((Read8s(headerref.fl),Read8s(headerref.fl),Read8s(headerref.fl)))
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
    def getUVOFFAfterNormals():
        return 1+4
    @staticmethod
    def getWeightsOFFAfterUVOFF():
        return 0
    @staticmethod
    def getBonesOFFAfterWeightsOFF():
        return 0
    @staticmethod
    def getBoneMode():
        return WEIGHTS3_BONES4
    @classmethod
    def appendEmptyVertices(cls,fl,VertexRegionEnd,oldVertexCount,addVertexCount):
        basicAppendEmptyVertices(cls,fl,VertexRegionEnd,oldVertexCount,addVertexCount)
       
class MODVertexBuffer81f58067:
    def __init__(self,headerref,vertexcount):
        dbg("MODVertexBuffer81f58067 %d" % vertexcount)
        self.vertarray   = []
        self.uvs         = []
        self.weights     = []
        self.bones       = []
        self.normalarray = []
        self.headerref   = headerref
        self.vertexcount = vertexcount
        for i in range(0,vertexcount):
            if headerref.bendian:
                self.vertarray.append([ReadBEFloat(headerref.fl),ReadBEFloat(headerref.fl),ReadBEFloat(headerref.fl)])
            else:
                self.vertarray.append([ReadFloat(headerref.fl),ReadFloat(headerref.fl),ReadFloat(headerref.fl)])
            self.normalarray.append((Read8s(headerref.fl),Read8s(headerref.fl),Read8s(headerref.fl)))
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
    def getUVOFFAfterNormals():
        return 1+4
    @staticmethod
    def getWeightsOFFAfterUVOFF():
        return 0
    @staticmethod
    def getBonesOFFAfterWeightsOFF():
        return 0
    @staticmethod
    def getBoneMode():
        return WEIGHTS7_BONES8
    @classmethod
    def appendEmptyVertices(cls,fl,VertexRegionEnd,oldVertexCount,addVertexCount):
        basicAppendEmptyVertices(cls,fl,VertexRegionEnd,oldVertexCount,addVertexCount)
      
class MODVertexBufferf471fe45:
    def __init__(self,headerref,vertexcount):
        dbg("MODVertexBufferf471fe45 %d" % vertexcount)
        self.vertarray   = []
        self.uvs         = []
        self.uvs2        = []
        self.weights     = []
        self.bones       = []
        self.normalarray = []
        self.headerref   = headerref
        self.vertexcount = vertexcount
        for i in range(0,vertexcount):
            if headerref.bendian:
                self.vertarray.append([ReadBEFloat(headerref.fl),ReadBEFloat(headerref.fl),ReadBEFloat(headerref.fl)])
            else:
                self.vertarray.append([ReadFloat(headerref.fl),ReadFloat(headerref.fl),ReadFloat(headerref.fl)])
            self.normalarray.append((Read8s(headerref.fl),Read8s(headerref.fl),Read8s(headerref.fl)))
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
        return 4+4+4+1+1+1+1+4+2+2+2+2+4+1+1+1+1
    @staticmethod
    def getUVOFFAfterNormals():
        return 1+4
    @staticmethod
    def getWeightsOFFAfterUVOFF():
        return 0
    @staticmethod
    def getBonesOFFAfterWeightsOFF():
        return 0
    @staticmethod
    def getBoneMode():
        return WEIGHTS3_BONES4
    @classmethod
    def appendEmptyVertices(cls,fl,VertexRegionEnd,oldVertexCount,addVertexCount):
        basicAppendEmptyVertices(cls,fl,VertexRegionEnd,oldVertexCount,addVertexCount)

class MODVertexBuffer3c730760:
    def __init__(self,headerref,vertexcount):
        dbg("MODVertexBuffer3c730760 %d" % vertexcount)
        self.vertarray   = []
        self.uvs         = []
        self.weights     = []
        self.bones       = []
        self.normalarray = []
        self.headerref   = headerref
        self.vertexcount = vertexcount
        for i in range(0,vertexcount):
            if headerref.bendian:
                self.vertarray.append([ReadBEFloat(headerref.fl),ReadBEFloat(headerref.fl),ReadBEFloat(headerref.fl)])
            else:
                self.vertarray.append([ReadFloat(headerref.fl),ReadFloat(headerref.fl),ReadFloat(headerref.fl)])
            self.normalarray.append((Read8s(headerref.fl),Read8s(headerref.fl),Read8s(headerref.fl)))
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
    def getUVOFFAfterNormals():
        return 1+4
    @staticmethod
    def getWeightsOFFAfterUVOFF():
        return 0
    @staticmethod
    def getBonesOFFAfterWeightsOFF():
        return 0      
    @staticmethod
    def getBoneMode():
        return WEIGHTS3_BONES4
    @classmethod
    def appendEmptyVertices(cls,fl,VertexRegionEnd,oldVertexCount,addVertexCount):
        basicAppendEmptyVertices(cls,fl,VertexRegionEnd,oldVertexCount,addVertexCount)

class MODVertexBufferb2fc0083:
    def __init__(self,headerref,vertexcount):
        dbg("MODVertexBufferb2fc0083 %d" % vertexcount)
        raise Exception("ToDo")
        self.vertarray   = []
        self.uvs         = []
        self.weights     = []
        self.bones       = []
        self.normalarray = []
        self.headerref   = headerref
        self.vertexcount = vertexcount
        for i in range(0,vertexcount):
            if headerref.bendian:
                self.vertarray.append([ReadBEFloat(headerref.fl),ReadBEFloat(headerref.fl),ReadBEFloat(headerref.fl)])
            else:
                self.vertarray.append([ReadFloat(headerref.fl),ReadFloat(headerref.fl),ReadFloat(headerref.fl)])
            self.normalarray.append((Read8s(headerref.fl),Read8s(headerref.fl),Read8s(headerref.fl)))
            ReadByte(headerref.fl)
            ReadLong(headerref.fl)
            self.uvs.append((ReadHalfFloat(headerref.fl),1-ReadHalfFloat(headerref.fl)))
            ReadLong(headerref.fl)
    @staticmethod
    def getStructSize():
        return 4+4+4+1+1+1+1+4+2+2+4
    @staticmethod
    def getUVOFFAfterNormals():
        return 1+4
    @staticmethod
    def getWeightsOFFAfterUVOFF():
        return -1
    @staticmethod
    def getBonesOFFAfterWeightsOFF():
        return -1
    @staticmethod
    def getBoneMode():
        return WEIGHTS0_BONES0
    @classmethod
    def appendEmptyVertices(cls,fl,VertexRegionEnd,oldVertexCount,addVertexCount):
        basicAppendEmptyVertices(cls,fl,VertexRegionEnd,oldVertexCount,addVertexCount)
       
class MODVertexBuffer366995a7:
    def __init__(self,headerref,vertexcount):
        dbg("MODVertexBuffer366995a7 %d" % vertexcount)
        self.vertarray   = []
        self.uvs         = []
        self.weights     = []
        self.bones       = []
        self.normalarray = []
        self.headerref   = headerref
        self.vertexcount = vertexcount
        for i in range(0,vertexcount):
            if headerref.bendian:
                self.vertarray.append([ReadBEFloat(headerref.fl),ReadBEFloat(headerref.fl),ReadBEFloat(headerref.fl)])
            else:
                self.vertarray.append([ReadFloat(headerref.fl),ReadFloat(headerref.fl),ReadFloat(headerref.fl)])
            self.normalarray.append((Read8s(headerref.fl),Read8s(headerref.fl),Read8s(headerref.fl)))
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
    def getUVOFFAfterNormals():
        return 1+4
    @staticmethod
    def getWeightsOFFAfterUVOFF():
        return 0
    @staticmethod
    def getBonesOFFAfterWeightsOFF():
        return 0
    @staticmethod
    def getBoneMode():
        return WEIGHTS7_BONES8
    @classmethod
    def appendEmptyVertices(cls,fl,VertexRegionEnd,oldVertexCount,addVertexCount):
        basicAppendEmptyVertices(cls,fl,VertexRegionEnd,oldVertexCount,addVertexCount)
        
class MODVertexBufferc9690ab8:
    def __init__(self,headerref,vertexcount):
        dbg("MODVertexBufferc9690ab8 %d" % vertexcount)
        raise Exception("ToDo")
        self.vertarray   = []
        self.uvs         = []
        self.weights     = []
        self.bones       = []
        self.normalarray = []
        self.headerref   = headerref
        self.vertexcount = vertexcount
        for i in range(0,vertexcount):
            if headerref.bendian:
                self.vertarray.append([ReadBEFloat(headerref.fl),ReadBEFloat(headerref.fl),ReadBEFloat(headerref.fl)])
            else:
                self.vertarray.append([ReadFloat(headerref.fl),ReadFloat(headerref.fl),ReadFloat(headerref.fl)])
            self.normalarray.append((Read8s(headerref.fl),Read8s(headerref.fl),Read8s(headerref.fl)))
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
    def getUVOFFAfterNormals():
        return 1+4
    @staticmethod
    def getWeightsOFFAfterUVOFF():
        return -1
    @staticmethod
    def getBonesOFFAfterWeightsOFF():
        return -1
    @staticmethod
    def getBoneMode():
        return WEIGHTS7_BONES8
    @classmethod
    def appendEmptyVertices(cls,fl,VertexRegionEnd,oldVertexCount,addVertexCount):
        basicAppendEmptyVertices(cls,fl,VertexRegionEnd,oldVertexCount,addVertexCount)
        
class MODVertexBuffer5e7f202d:
    def __init__(self,headerref,vertexcount):
        dbg("MODVertexBuffer5e7f202d %d" % vertexcount)
        raise Exception("ToDo")
        self.vertarray   = []
        self.uvs         = []
        self.weights     = []
        self.bones       = []
        self.normalarray = []
        self.headerref   = headerref
        self.vertexcount = vertexcount
        for i in range(0,vertexcount):
            if headerref.bendian:
                self.vertarray.append([ReadBEFloat(headerref.fl),ReadBEFloat(headerref.fl),ReadBEFloat(headerref.fl)])
            else:
                self.vertarray.append([ReadFloat(headerref.fl),ReadFloat(headerref.fl),ReadFloat(headerref.fl)])
            self.normalarray.append((Read8s(headerref.fl),Read8s(headerref.fl),Read8s(headerref.fl)))
            ReadByte(headerref.fl)
            ReadLong(headerref.fl)
            self.uvs.append((ReadHalfFloat(headerref.fl),1-ReadHalfFloat(headerref.fl)))
            ReadLong(headerref.fl)
    @staticmethod
    def getStructSize():
        return 4+4+4+1+1+1+1+4+2+2+4
    @staticmethod
    def getUVOFFAfterNormals():
        return 1+4
    @staticmethod
    def getWeightsOFFAfterUVOFF():
        return -1
    @staticmethod
    def getBonesOFFAfterWeightsOFF():
        return -1
    @staticmethod
    def getBoneMode():
        return WEIGHTS0_BONES0
    @classmethod
    def appendEmptyVertices(cls,fl,VertexRegionEnd,oldVertexCount,addVertexCount):
        basicAppendEmptyVertices(cls,fl,VertexRegionEnd,oldVertexCount,addVertexCount)
       
class MODVertexBufferd829702c:
    def __init__(self,headerref,vertexcount):
        dbg("MODVertexBufferd829702c %d" % vertexcount)
        self.vertarray   = []
        self.uvs         = []
        self.weights     = []
        self.bones       = []
        self.normalarray = []
        self.headerref   = headerref
        self.vertexcount = vertexcount
        for i in range(0,vertexcount):
            if headerref.bendian:
                self.vertarray.append([ReadBEFloat(headerref.fl),ReadBEFloat(headerref.fl),ReadBEFloat(headerref.fl)])
            else:
                self.vertarray.append([ReadFloat(headerref.fl),ReadFloat(headerref.fl),ReadFloat(headerref.fl)])
            self.normalarray.append((Read8s(headerref.fl),Read8s(headerref.fl),Read8s(headerref.fl)))
            ReadByte(headerref.fl)
            ReadLong(headerref.fl)
            self.uvs.append((ReadHalfFloat(headerref.fl),1-ReadHalfFloat(headerref.fl)))
    @staticmethod
    def getStructSize():
        return 4+4+4+1+1+1+1+4+2+2
    @staticmethod
    def getUVOFFAfterNormals():
        return 1+4
    @staticmethod
    def getWeightsOFFAfterUVOFF():
        return -1
    @staticmethod
    def getBonesOFFAfterWeightsOFF():
        return -1
    @staticmethod
    def getBoneMode():
        return WEIGHTS0_BONES0  
    @classmethod
    def appendEmptyVertices(cls,fl,VertexRegionEnd,oldVertexCount,addVertexCount):
        basicAppendEmptyVertices(cls,fl,VertexRegionEnd,oldVertexCount,addVertexCount)
        
class MODVertexBufferb8e69244:
    def __init__(self,headerref,vertexcount):
        dbg("MODVertexBufferd829702c %d" % vertexcount)
        self.vertarray   = []
        self.uvs         = []
        self.weights     = []
        self.bones       = []
        self.normalarray = []
        self.headerref   = headerref
        self.vertexcount = vertexcount
        for i in range(0,vertexcount):
            if headerref.bendian:
                self.vertarray.append([ReadBEFloat(headerref.fl),ReadBEFloat(headerref.fl),ReadBEFloat(headerref.fl)])
            else:
                self.vertarray.append([ReadFloat(headerref.fl),ReadFloat(headerref.fl),ReadFloat(headerref.fl)])
            self.normalarray.append((Read8s(headerref.fl),Read8s(headerref.fl),Read8s(headerref.fl)))
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
    def getUVOFFAfterNormals():
        return 1+4
    @staticmethod
    def getWeightsOFFAfterUVOFF():
        return 0
    @staticmethod
    def getBonesOFFAfterWeightsOFF():
        return 0
    @staticmethod
    def getBoneMode():
        return WEIGHTS7_BONES8
    @classmethod
    def appendEmptyVertices(cls,fl,VertexRegionEnd,oldVertexCount,addVertexCount):
        basicAppendEmptyVertices(cls,fl,VertexRegionEnd,oldVertexCount,addVertexCount)

MODVertexBuffera5104ca0 = MODVertexBuffer5e7f202d
MODVertexBufferf637401c = MODVertexBufferf06033f
MODVertexBuffera756f2f9 = MODVertexBufferd829702c