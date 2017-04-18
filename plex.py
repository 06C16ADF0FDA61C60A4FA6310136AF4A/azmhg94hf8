import math, random, pickle
from math import factorial as f
    
class Grid:
    def __init__(self,h,w):
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
                #sline.reverse()
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
            #print( x+y,self.h+self.w )
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
        print()
        for l in range(len(self.bdata)):
            line = self.bdata[self.h-l-1]
            print( line )
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

while 1:
    print('----')
    print('---------------------------')
    print('|        ==PLEX==         |')
    print('---------------------------')
    hiscores = pickle.load(open('scores.p','rb'))#[0,0,0,0,0,0,0]
    print('hiscores: '+str(hiscores))
    lv = 0
    while lv<7:
        print('----------------')
        print('level: '+str(lv)+' score: '+str(hiscores[lv]))
        grid = Grid(phi(lv+1),phi(lv+2))
        grid.randomize()
        score = 0
        turns = lv+1
        lvrun = 1
        while lvrun:
            grid.printbdata()
            x,y = input('x,y:').split(',')
            x,y = int(x),int(y)
            
            path = grid.trace(x,y)
            print("path'-> "+str(path))
            score += len(path)
            turns -= 1
            if turns<=0:
                hs=''
                if hiscores[lv]<score:
                    hiscores[lv]=score
                    hs='new '
                lvrun=0
                lv+=1
            
            print(hs+"score: "+str(score))
            print("turns: "+str(turns))
        print()
        print()
    pickle.dump(hiscores,open('scores.p','wb'))
  
            
print( '__________.__                 ' )
print( '\______   \  |   ____ ___  ___' )
print( ' |     ___/  | _/ __ \\  \/  /' )
print( ' |    |   |  |_\  ___/ >    < ' )
print( ' |____|   |____/\___  >__/\_ \'')
print( '                    \/      \/' )

