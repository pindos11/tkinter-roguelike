from FieldPos import *
from NPC import *
import random

class Field:
    def __init__(self,sizex,sizey,plr,ztype):
        self.vil=plr
        self.ztype = ztype
        self.sizex = sizex
        self.sizey = sizey
        self.monsters = []
        self.npcs = []
        self.vilposes=[]
        #creating and filling storage for field points
        self.storage=[]
        self.walkable=['1','2','4','5','6','7','9','10','2_1','13']
        for i in range(0,sizex):
            tmp=[]
            self.storage.append(tmp)
            for j in range(0,sizey):
                self.storage[i].append(FieldPos(i,j,'1'))
        random.seed()
        if(self.vil==1):
            self.make_vil()
        if(self.vil==2 and self.ztype==1):
            self.make_smallvil()
        self.make_zone(ztype)
        self.clear_paths(ztype)
        self.set_player_start()
        #self.print_task('player')

    def make_smallvil(self):
        qpos = random.randint(1,2)
        if(qpos==1):
            nwpos=(1,2)
        elif(qpos==2):
            nwpos=(7,2)
        for i in range(0,2):
            for j in range(0,2):
                self.storage[i+nwpos[0]][j+nwpos[1]].set_terrain('1')
                self.vilposes.append((i+nwpos[0],j+nwpos[1]))
        self.storage[nwpos[0]+1][nwpos[1]].set_terrain('3_h_w')
        self.storage[nwpos[0]][nwpos[1]].set_terrain('3_h_s')
        npc = NPC((nwpos[0],nwpos[1]+1),str(random.randint(2,3)))
        self.add_npc(npc)
                
            
    def make_vil(self):
        sx=self.sizex
        sy=self.sizey
        nwpos=(2,2)
        for i in range(0,6):
            for j in range(0,6):
                self.storage[i+nwpos[0]][j+nwpos[1]].set_terrain('1')
                self.vilposes.append((i+nwpos[0],j+nwpos[1]))
        for i in range(3,5):
            for j in range(0,2):
                if(i==3):
                    if(j==0):
                        self.storage[i+nwpos[0]][j+nwpos[1]].set_terrain('3_h_1')
                    elif(j==1):
                        self.storage[i+nwpos[0]][j+nwpos[1]].set_terrain('3_h_4')
                if(i==4):
                    if(j==0):
                        self.storage[i+nwpos[0]][j+nwpos[1]].set_terrain('3_h_2')
                    elif(j==1):
                        self.storage[i+nwpos[0]][j+nwpos[1]].set_terrain('3_h_3')
        self.storage[6][4].set_terrain('3_h_w')
        self.storage[7][2].set_terrain('3_h_b')
        self.storage[7][3].set_terrain('3_h_b2')
        self.storage[3][6].set_terrain('3_h_t')
        npc = NPC((2,6),'1')
        self.add_npc(npc)
        
    def add_monster(self,monster):
        self.monsters.append(monster)
    def kill_monster(self,monster):
        self.monsters.pop(self.monsters.index(monster))
    def ret_monsters(self):
        return(self.monsters)
    
    def add_npc(self,npc):
        self.npcs.append(npc)
    
    def clear_paths(self,ztype):
        if(ztype==1):
            water=['3','3_1','3_2','3_3','3_4','3_5','3_6','3_7','3_8']
            road='2'
            bridge='2_1'
        elif(ztype==3):
            water=['8','8_1','8_2','8_3','8_4','8_5','8_6','8_7','8_8']
            road='7'
            bridge='10'
        elif(ztype==2):
            water=['5_1','5_2','5_3','5_4','5_5','5_6','5_7','5_8']
            road='5'
            bridge='5'
        elif(ztype==4):
            water=['11']
            road='13'
            bridge='13'
        for i in range(0,self.sizex):
            if(((i,4) not in self.vilposes)):
                if(self.storage[i][4].get_terrain() in water):
                    self.storage[i][4].set_terrain(bridge)
                else:
                    self.storage[i][4].set_terrain(road)
            if(ztype==4):
                self.storage[i][5].set_terrain('12')
        for j in range(0,self.sizey):
            if(((4,j) not in self.vilposes)):
                if(self.storage[4][j].get_terrain() in water and ztype==3):
                    self.storage[4][j].set_terrain(bridge)
                else:
                    self.storage[4][j].set_terrain(road)        
    def set_player_start(self):
        if(self.vil==1):
            self.pposx=4
            self.pposy=4
            return
        while(1):
            random.seed()
            self.pposx = random.randint(0,self.sizex-1)
            self.pposy = random.randint(0,self.sizey-1)
            if(self.storage[self.pposx][self.pposy].get_terrain() in self.walkable):
                break
        self.storage[self.pposx][self.pposy].set_player()
    
    def make_zone(self,zone):
        vil = self.vil
        if(vil==2):
            vil = 0
        random.seed()
        if(zone==1):
            lakes=random.randint(4+vil*3,6+vil*3)
            for k in range(0,lakes):
                sizex=random.randint(3+vil*3,4+vil*3)
                sizey=random.randint(3+vil*3,4+vil*3)
                nwpos=(random.randint(0,self.sizex-sizex),random.randint(0,self.sizey-sizey))
                for i in range(0,sizex):
                    for j in range(0,sizey):
                        if((i+nwpos[0],j+nwpos[1]) not in self.vilposes):
                            self.storage[i+nwpos[0]][j+nwpos[1]].set_terrain('3')
        
            sizex=self.sizex
            sizey=self.sizey
            if(self.vil==0):
                for i in range(0,sizex):
                    for j in range(0,sizey):
                        if(i==0):
                            self.storage[i][j].set_terrain('1')
                        if(i==sizex-1):
                            self.storage[i][j].set_terrain('1')
                        if(j==0):
                            self.storage[i][j].set_terrain('1')
                        if(j==sizey-1):
                            self.storage[i][j].set_terrain('1')
            for i in range(0,sizex):
                for j in range(0,sizey):
                    if(self.storage[i][j].get_terrain()!='3'):
                        continue
                    left=self.storage[i-1][j].get_terrain()
                    top=self.storage[i][j-1].get_terrain()
                    try:
                        right=self.storage[i+1][j].get_terrain()
                    except:
                        right=left
                    try:
                        down=self.storage[i][j+1].get_terrain()
                    except:
                        down=top
                    if(left=='1' and top=='1'):
                        self.storage[i][j].set_terrain('3_2')
                    elif(right=='1' and top=='1'):
                        self.storage[i][j].set_terrain('3_4')
                    elif(left=='1' and down=='1'):
                        self.storage[i][j].set_terrain('3_8')
                    elif(right=='1' and down=='1'):
                        self.storage[i][j].set_terrain('3_6')
                    elif(left=='1'):
                        self.storage[i][j].set_terrain('3_1')
                    elif(top=='1'):
                        self.storage[i][j].set_terrain('3_3')
                    elif(right=='1'):
                        self.storage[i][j].set_terrain('3_5')
                    elif(down=='1' or '3_h' in down):
                        self.storage[i][j].set_terrain('3_7')
                        
        if(zone==2):
            for i in range(0,self.sizex):
                for j in range(0,self.sizey):
                    self.storage[i][j].set_terrain('5')
                    if(i==0 and j==0):
                        self.storage[i][j].set_terrain('5_2')
                    elif(i==0 and j==self.sizey-1):
                        self.storage[i][j].set_terrain('5_8')
                    elif(i==self.sizex-1 and j==0):
                        self.storage[i][j].set_terrain('5_4')
                    elif(i==self.sizex-1 and j==self.sizey-1):
                        self.storage[i][j].set_terrain('5_6')
                    elif(i==0):
                        self.storage[i][j].set_terrain('5_1')
                    elif(j==0):
                        self.storage[i][j].set_terrain('5_3')
                    elif(i==self.sizex-1):
                        self.storage[i][j].set_terrain('5_5')
                    elif(j==self.sizey-1):
                        self.storage[i][j].set_terrain('5_7')
            obsts=random.randint(3,7)
            for i in range(0,obsts):
                px=random.randint(1,self.sizex-2)
                py=random.randint(1,self.sizey-2)
                obst=random.randint(9,10)
                self.storage[px][py].set_terrain('5_'+str(obst))
        if(zone==3):
            for i in range(0,self.sizex):
                for j in range(0,self.sizey):
                    self.storage[i][j].set_terrain('9')
            lakes=random.randint(4,6)
            for k in range(0,lakes):
                sizex=random.randint(3,4)
                sizey=random.randint(3,4)
                nwpos=(random.randint(0,self.sizex-1-sizex),random.randint(0,self.sizey-1-sizey))
                for i in range(0,sizex):
                    for j in range(0,sizey):
                        self.storage[i+nwpos[0]][j+nwpos[1]].set_terrain('8')
        
            sizex=self.sizex
            sizey=self.sizey
            for i in range(0,sizex):
                for j in range(0,sizey):
                    if(i==0):
                        self.storage[i][j].set_terrain('9')
                    if(i==sizex-1):
                        self.storage[i][j].set_terrain('9')
                    if(j==0):
                        self.storage[i][j].set_terrain('9')
                    if(j==sizey-1):
                        self.storage[i][j].set_terrain('9')
            for i in range(0,sizex):
                for j in range(0,sizey):
                    if(self.storage[i][j].get_terrain()!='8'):
                        continue
                    left=self.storage[i-1][j].get_terrain()
                    top=self.storage[i][j-1].get_terrain()
                    right=self.storage[i+1][j].get_terrain()
                    down=self.storage[i][j+1].get_terrain()
                    if(left=='9' and top=='9'):
                        self.storage[i][j].set_terrain('8_2')
                    elif(right=='9' and top=='9'):
                        self.storage[i][j].set_terrain('8_4')
                    elif(left=='9' and down=='9'):
                        self.storage[i][j].set_terrain('8_8')
                    elif(right=='9' and down=='9'):
                        self.storage[i][j].set_terrain('8_6')
                    elif(left=='9'):
                        self.storage[i][j].set_terrain('8_1')
                    elif(top=='9'):
                        self.storage[i][j].set_terrain('8_3')
                    elif(right=='9'):
                        self.storage[i][j].set_terrain('8_5')
                    elif(down=='9'):
                        self.storage[i][j].set_terrain('8_7')
        if(zone==4):
            sizex=self.sizex
            sizey=self.sizey
            for i in range(0,sizex):
                for j in range(0,sizey):
                    self.storage[i][j].set_terrain('11')
    def print_task(self,task):
        if(task=="player"):
            self.storage[self.pposx][self.pposy].output_str('pos')
        if(task=="out"):
            print("No such point on field")
    def move_player(self,newx,newy):       
        self.storage[self.pposx][self.pposy].unset_player()
        if(newx<self.sizex and newy<self.sizey):
            self.pposx = newx
            self.pposy = newy
            self.storage[self.pposx][self.pposy].set_player()
        else:
            self.print_task("out")
    def cur_cond(self):
        return self.storage
    def size(self):
        return self.sizex,self.sizey
    def terrains(self):
        terrains=[]
        for i in range(0,self.sizex):
            for j in range(0,self.sizey):
                if(self.storage[i][j].get_terrain() not in terrains):
                    terrains.append(self.storage[i][j].get_terrain())
        return terrains
