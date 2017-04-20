import math, random, pickle, copy
from math import factorial as f

class Grid:
    def __init__(self,h=5,w=8):
        bdata = []
        ndata = []
        mdata = []
        for l in range(h):
            line1 = []
            line2 = []
            line3 = []
            for c in range(w):
                line1 += [int(f(l+c)/(f(l+c-c)*f(c)))]
                line2 += [0]
                line3 += [0]
            ndata += [line1]
            bdata += [line2]
            mdata += [line3]
        bdata.reverse()
        ndata.reverse()
        self.h, self.w = h, w
        self.bdata = bdata
        self.ndata = ndata
        self.score = None
    def load_preset(self,n):
        if n==0: self.bdata, self.score = prst(0)
        elif n==1: self.bdata, self.score = prst(1)
        elif n==2: self.bdata, self.score = prst(2)
        elif n==3: self.bdata, self.score = prst(3)
        elif n==4: self.bdata, self.score = prst(4)
        elif n==5: self.bdata, self.score = prst(5)
        self.h, self.w = len(self.bdata), len(self.bdata[0])
    def load_data(self,file):
        pass
    def subrow(self,y):
        del self.bdata[y]
        del self.ndata[y]
        self.h-=1
        #comment
    def subcol(self,x):
        for r in range(self.h):
            del self.bdata[r][x]
            del self.ndata[r][x]
        self.w-=1
    def randomize(self):
        for line in self.bdata:
            for n in range(len(line)):
                line[n] = int(random.random()*2)
    def compute(self,x):
        print('computation a')
        for n in range(x):
            for l in range(len(self.bdata)):
                line = self.bdata[self.h-l-1]
                sline = list(line)
                bstr = ''.join(str(t) for t in sline)
                print(str(sline)+' '+bstr+' '+str(int(bstr,2)))
            print()
            print(self.trace(0,0) )
            print()
    def cascade(self):
        pass
    def trace(self,x,y):
        path = []
        while x+y<self.h+self.w and y<self.h and x<self.w:
            if self.bdata[y][x]==1:
                self.bdata[y][x]=0
                x+=1
                path += [1]
            else:
                self.bdata[y][x]=1
                y+=1
                path += [0]
        return path
    def printbdata(self):
        print( '       .')
        print( '      /    _'+' _'.join(' ' for a in range(len(self.bdata[0]))))
        for l in range(len(self.bdata)):
            line = self.bdata[self.h-l-1]
            print( '      '+str(self.h-l)+' - '+str(line) )
        print( '      y    '+'  '.join("'" for a in range(len(self.bdata[0]))))
        print( '       \\.x '+'  '.join(str(a+1) for a in range(len(self.bdata[0]))))
    def display(self):
        print(self)
        for line in self.ndata:
            print( line )
        print()
        for line in self.bdata:
            print( line )

def phi(n):
    if n == 0: return 0
    elif n == 1: return 1
    else: return phi(n-1)+phi(n-2)

def mode1():
    print()
    print()
    print('        mode: random')
    print("           type 'menu' to return to title")
    print('        -----------------------------------------------------------')
    print('        rules:')
    print('          - full lines eleminate rows/columns')
    print('          - points equals path length minus full line length plus 1')
    print('          - points are added each turn')
    print('          - beat the lowest score.')
    scoreData = pickle.load(open('scoreData.p','rb'))
    if len(scoreData)>0:
        print()
        print( '        best scores' )
        for sc in range(len(scoreData)):
            print('          lv'+str(sc)+' - '+str(scoreData[sc])+' - complete'*(scoreData[sc]==phi(sc+1) ))
    print()
    lv = 0
    while lv<len(scoreData):
        if scoreData[lv]>phi(lv+1): break
        lv+=1
    while 1:
        grid = Grid(phi(lv+1),phi(lv+2))
        grid.randomize()
        print('        -----------------------------------------------------------')
        print('        level: '+str(lv)+' score: '+str(grid.score))
        if lv<len(scoreData):
            hiscore = scoreData[lv]
        else:
            hiscore = None
        score = 0
        lvrun = 1
        while lvrun:
            grid.printbdata()
            valid = 0
            while valid==0:
                print("        |")
                x = input("        '-- x > ")
                if x=='menu':
                    break
                print("        |")
                y = input("        '-- y ^ ")
                if y=='menu':
                    break
                try:
                    x,y = int(x)-1,int(y)-1
                except:
                    print("        .- invalid entry -'")
                if type(x)==type(y)==int: valid = 1
            if x=='menu' or y=='menu': break
            path = grid.trace(x,y)
            pathstr = ''.join(str(l) for l in path)
            if '0'*grid.h in pathstr:
                grid.subcol(x+pathstr.index('0'*grid.h))
                scoreadd = len(pathstr)-grid.h+1
            elif '1'*grid.w in pathstr:
                grid.subrow(y+pathstr.index('1'*grid.w))
                scoreadd = len(pathstr)-grid.w+1
            else:
                scoreadd = len(pathstr)+1
            score += scoreadd
            print("        '")
            print("        '-> path: "+str(path)+' = '+str(scoreadd))
            hs=''
            if len(grid.bdata)==1:
                if len(grid.bdata[0])==0: grid.bdata = []
            if len(grid.bdata)==0:
                if hiscore==None:
                    scoreData += [score]
                    hs='new '
                elif hiscore>score:
                    scoreData[lv]=score
                    hs='new '
                lvrun=0
                lv+=1
            else:
                print("        score: "+str(score))
        if x=='menu' or y=='menu': break
        print( '        level '+str(lv-1)+' passed with '+hs+'score: '+str(score))
        print()
        print()
    pickle.dump(scoreData,open('scoreData.p','wb'))

def mode2():
    print()
    print()
    print('        mode: preset')
    print("           type 'menu' to return to title")
    print('        -----------------------------------------------------------')
    print('        rules:')
    print('          - full lines eleminate rows/columns')
    print('          - points equal to path length minus full line length plus 1')
    print('          - points are subtracted each turn')
    print('          - complete grid using points avaliable')
    scoreData = pickle.load(open('scoreData.p','rb'))
    hiscore = None
    lv = 0
    while 1:
        grid = Grid()
        grid.load_preset(lv)
        score = grid.score
        print("           type 'menu' to return to title")
        print('        -----------------------------------------------------------')
        print('        level: '+str(lv)+' points: '+str(grid.score))
        lvrun = 1
        while lvrun:
            grid.printbdata()
            valid = 0
            while valid==0:
                print("        |")
                x = input("        '-- x > ")
                if x=='menu':
                    break
                print("        |")
                y = input("        '-- y ^ ")
                if y=='menu':
                    break
                try:
                    x,y = int(x)-1,int(y)-1
                except:
                    print("        .- invalid entry -'")
                if type(x)==type(y)==int: valid = 1
            if x=='menu' or y=='menu': break
            path = grid.trace(x,y)
            pathstr = ''.join(str(l) for l in path)
            if '0'*grid.h in pathstr:
                grid.subcol(x+pathstr.index('0'*grid.h))
                scoreadd = len(pathstr)-grid.h+1
            elif '1'*grid.w in pathstr:
                grid.subrow(y+pathstr.index('1'*grid.w))
                scoreadd = len(pathstr)-grid.w+1
            else:
                scoreadd = len(pathstr)+1
            score -= scoreadd
            print("        '")
            print("        '-> path: "+str(path)+' = '+str(scoreadd))
            hs=''
            if score<=0: lvrun = 0
            if len(grid.bdata)>0:
                if len(grid.bdata[0])==0: grid.bdata = []
            if len(grid.bdata)==0: 
                lvrun=0
                lv+=1
            print('        '+hs+"score: "+str(score))
        print()
        print()
        if x=='menu' or y=='menu': break
    pickle.dump(scoreData,open('scoreData.p','wb'))

def prst(n):
    return copy.deepcopy(pslist[2*n]), pslist[2*n+1]

def preset1():
    return [[0,0,0,0,0,0,0],\
            [1,1,1,0,1,0,1],\
            [0,0,0,0,0,0,0],\
            [1,1,1,0,1,1,1],\
            [0,0,1,1,1,1,1]], 9

ps0 = [[[1,1,0,1,1]],2]

ps1 = [[[0,0],\
        [0,1]],2]

ps2 = [[[1,0,0,1,1],\
        [0,1,0,1,0],\
        [1,1,1,0,0]],9]

ps3 = [[[1,0,0],\
        [0,1,0]],9]

ps4 = [[[1,0,0],\
        [0,1,0]],10]

ps5 = [[[1,0,0],\
        [0,1,0]],10]

pslist = ps0+ps1+ps2+ps3+ps4+ps5

while 1:
    print( '                                          ')
    print( '                                           \            ')            
    print( '                      __________.__         \           ')
    print( '                      \______   \  |   ____ _\_  ___  ')
    print( '                       |     ___/  |  / __ \\\  \/  / ')
    print( '                       |    |   |  |_\  ___/ >    <-------------  ')
    print( '                       |____|   |____/\___  >__/\_ \  ')
    print( '                                          \/      \/  ')
    print( '                                              ')
    print( '                                          ')
    print( '        MENU:                  ')
    print( '          1 - start')
    print( '          2 - reset scores')
    print( '          3 - exit')
    chk = 1
    while chk:
        try:
            select = int(input( '        select: '))
            chk = 0
        except: print('            invalid')
        
            
        
    if select==1: mode1()
    #elif select==2: mode2()
    elif select==2: pickle.dump([],open('scoreData.p','wb'))
    elif select==3: break

