from define import Path,paths,Shape,Operate,Level,baseShapes
from copy import deepcopy

path=paths()

def paintPath(code:str,quad:int):#不生成上色路径，仅占位
    return Shape.Block(code,quad)

def stackableLayerPath(layer:str|Shape.Layer)->Path:#不含晶体的层
    match layer:
        case str():
            p=None
            for i,b in enumerate([layer[i:i+2] for i in range(0,len(layer),2)],1):
                if b!="--":
                    if p:
                        p=path(Shape.Layer(layer[:i*2-2]),Operate.Stack(p,paintPath(b,i)),Level.stackableLayer)
                    else:
                        p=path(paintPath(b,i))
            return p
        case _:
            return stackableLayerPath(str(layer))

def cutPath(quad:int,shape:Path)->Path:#暂时占位，考虑完全使用交换代替切割+堆叠
    match shape.shape:
        case Shape.Layer():
            pass
        case _:
            pass

def rotatePath(angle:int,shape:Path)->Path:#暂时占位
    match shape.shape:
        case Shape.Corner():
            pass

def crystallizePath(color:str,shape:Path)->Path:
    match shape.shape:
        case Shape.Corner():
            newShape=deepcopy(shape)
            for i in range(len(newShape)):
                if newShape[i] in "P--":
                    newShape[i]="c"+color
            return path(newShape,Operate.Crystallize(shape,color),Level.crystallize)
        case _:
            pass

def standerdCornerPath(*corner:str)->Path:#不含空象限的单角
    stackablePath=None
    highestCrystalLayer=len(corner)
    for i in corner[::-1]:
        if i[0]=="c":
            break
        else:
            highestCrystalLayer-=1

def standerdSwapCornerPath(corners:[Path,Path,Path,Path])->Path:#标准支撑的单角交换为整个图形
    shape,shape1,shape2="","",""
    for i in range(max(len(corners[0],corners[1],corners[2],corners[3]))):
        for j in range(4):
            shape+=corners[j].shape[i]
        shape+=":"
    #TODO shape1,shape2
    path1=path(shape1[:-1],Operate.Swap(corners[0],[1,4],corners[1],[2,3]),Level.standerdSwapCorner)
    path2=path(shape2[:-1],Operate.Swap(corners[2],[4,1],corners[3],[3,2]),Level.standerdSwapCorner)
    return path(shape[:-1],Operate.Swap(path1,[1,2],path2,[3,4]),Level.standerdSwapCorner)

def standerdStablePath(shape:str)->Path:#不含空象限的图形
    match shape:
        case str():
            layers=shape.split(":")
            stackableLayers=[]
            highestCrystalLayer=len(layers)
            for i in layers[::-1]:
                if "c" in i[::2]:
                    break
                else:
                    highestCrystalLayer-=1
                    stackableLayers.append(i)
            stackPath=None
            for i,l in enumerate(stackableLayers,1):
                if stackPath:
                    stackPath=path(Shape.Layers(*stackableLayers[:i]),Operate.Stack(stackPath,stackableLayerPath(l)),Level.stackablePart)
                else:
                    stackPath=stackableLayerPath(l)
            if highestCrystalLayer:
                corners=[[],[],[],[]]
                for i in range(highestCrystalLayer):
                    for j in range(4):
                        corners[j].append(layers[i][j*2:j*2+2])
                cps=[]
                for i in corners:
                    cps.append(standerdCornerPath(*i))
                p=path(shape,Operate.Stack(standerdSwapCornerPath(cps),stackPath),Level.standerdStable)
            else:
                p=stackPath
            return p
        case _:
            return standerdStablePath(str(shape))

if __name__=="__main__":
    from beeprint import pp
    pp(standerdStablePath("crCgCbCy:CuCwCcCm"),max_depth=200)
    del pp
