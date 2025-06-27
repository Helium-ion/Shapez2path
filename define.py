from __future__ import annotations
from enum import Enum

class Op(Enum):
    cut="Cut"
    pin="Pin"
    stack="Stack"
    rotate="Rotate"
    crystallize="Crystallize"
    swap="Swap"
    paint="Paint"

class Level(Enum):
    baseShape="BaseShape"
    stackableLayer="StackableLayer"
    stackablePart="StackablePart"
    crystallize="Crystallize"
    standerdSwapCorner="StanderdSwapCorner"
    standerdStable="StanderdStable"

class Shape:
    def __init__(self):pass
    def __str__(self):pass
    def __repr__(self):return str(self)
    def __int__(self):
        k2c = {"-": 0, "P": 1, "C": 2, "R": 2, "S": 2, "W": 2, "c": 3}
        quad_num=4
        code = 0
        for i, layer in enumerate(str(self).split(":")):
            for j in range(quad_num):
                code |= k2c[layer[j * 2]] << ((i * quad_num + j) * 2)
        return code

class Shape(Shape):
    framecode="Cu"
    class Block(Shape):
        def __init__(self,code:str="--",quad:int=1):
            self.quad=quad
            self.code=code

        def __str__(self):
            return (self.quad-1)*"--"+self.code+"--"*(4-self.quad)

        def __eq__(self,other):
            return self.code==other.code

    class Layer(Shape):
        def __init__(self,*codes:str):
            self.layer=[Shape.Block(codes[i] if i<len(codes) else "--",i+1) for i in range(4)]

        def __str__(self):
            return "".join([i.code for i in self.layer])

        def __getitem__(self,key):
            return self.layer[key]

        def __setitem__(self,key,value):
            self.layer[key]=value

    class Layers(Shape):
        def __init__(self,*layers:str):
            self.layers=[Shape.Layer(*[i[j:j+2] for j in range(0,len(i),2)]) for i in layers]

        def __str__(self):
            return ":".join([str(i) for i in self.layers])

        def __getitem__(self,key):
            return self.layers[key]

        def __setitem__(self,key,value):
            self.layers[key]=value

    class Corner(Shape):
        def __init__(self,quad:int,*codes:str):
            self.quad=quad
            self.codes=list(codes)
            self.frame=Shape.framecode

        def __str__(self):
            return (self.quad-1)*self.frame+(self.frame*(4-self.quad)+":"+(self.quad-1)*self.frame).join(self.codes)+self.frame*(4-self.quad)

        def __len__(self):
            return len(self.codes)

        def __getitem__(self,key):
            if key<len(self):
                return self.codes[key]
            else:
                return "--"

        def __setitem__(self,key,value):
            self.codes[key]=value

    class HalfCorner(Shape):
        def __init__(self,quad:int=None,framequad:int=None,*codes):
            self.quad=quad
            self.codes=list(codes)
            self.framequad=framequad
            self.frame=Shape.framecode

        def __str__(self):
            s=""
            for i in self.codes:
                for j in range(1,5):
                    if j==self.quad:
                        s+=i
                    elif j==self.framequad:
                        s+=self.frame
                    else:
                        s+="--"
                s+=":"
            return s

    class Half(Shape):
        def __init__(self):
            pass

        def __str__(self):
            pass

    class Whole(Shape):
        def __init__(self,shape:str=""):
            self.shape=[Shape.Corner(i,*[j[i*2-2:i*2] for j in shape.split(":")]) for i in range(1,5)]

        def __str__(self):
            pass

        def __getitem__(self,key):
            return self.shape[key]

        def __setitem__(self,key,value):
            self.shape[key]=value

class Operate:
    def __init__(self,_id:str=None):
        self.id=_id

class Operate(Operate):
    class Rotate(Operate):
        def __init__(self,angle:int=0,pre:Path=None):
            super().__init__(Op.rotate)
            self.angle=angle
            self.pre=pre

    class Stack(Operate):
        def __init__(self,lower:Path=None,upper:Path=None):
            super().__init__(Op.stack)
            self.lower=lower
            self.upper=upper

    class Cut(Operate):
        def __init__(self,pre:Path=None,half:list=None):
            super().__init__(Op.cut)
            self.pre=pre
            self.half=half

    class Pin(Operate):
        def __init__(self,pre:Path=None):
            super().__init__(Op.pin)
            self.pre=pre

    class Crystallize(Operate):
        def __init__(self,pre:Path=None,color:str="-"):
            super().__init__(Op.crystallize)
            self.pre=pre
            self.color=color

    class Swap(Operate):
        def __init__(self,first:Path=None,half1:list=None,second:Path=None,half2:list=None):
            super().__init__(Op.swap)
            self.first=first
            self.half1=half1
            self.second=second
            self.half2=half2

    class Paint(Operate):
        def __init__(self,pre:Path=None,color:str="-"):
            super().__init__(Op.paint)
            self.pre=pre
            self.color=color

class Path:
    def __init__(self,shape:Shape|str=None,superior:Operate=None,level:str=Level.baseShape):
        self.shape=shape
        self.superior=superior
        self.level=level

    @staticmethod
    def count(n:int=0):
        while True:
            yield (n:=n+1)

    @staticmethod
    def new(n:int=0):
        counter=Path.count(n)
        def _new(*args,**kwargs):
            path=Path(*args,**kwargs)
            path.count=next(counter)
            return path
        return _new
paths=Path.new

baseShapes=[Shape.Block("--"),Shape.Block("P-")]+[Shape.Block(i+j) for i in "CRSW" for j in "urgbcymw"]

if __name__=="__main__":
    print([i.code for i in baseShapes])
    a=Shape.Whole("--------")
    a[0][0]="Cr"
    print([i.__dict__ for i in a.shape])
    print(Shape.Corner(1,"cr","Cg"))
    print()
    print(Shape.Layers("CuCr----","--CbCy--"))
