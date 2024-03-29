import random
import math
class Monster:
    def __init__(self,player,mtype,pos):
        #player
        #97 - 122
        random.seed()
        self.posx=pos[0]
        self.posy=pos[1]
        if(mtype=='skele_war'):
            random.seed()
            self.model=mtype+str(random.randint(1,2))
        else:
            self.model=mtype
        self.level = player.level+random.randint(-1,2)
        if(self.level<1):
            self.level=1
        self.ap = 0
        self.rewardexp=(self.level+random.randint(0,4))*2
        self.preset_chars()
        self.upd_stats()
        self.apply_type()
        self.fix_mob()
        self.maxhealth=self.health
    def fix_mob(self):
        if(self.dodge_chance>15):
            self.dodge_chance=15    
    
    def apply_type(self):
        if(self.model=='skele_war1'):
            self.rewardexp = round(self.rewardexp*0.6,2)
            self.nat_armor = self.nat_armor/2
            self.health = self.health*0.75
            self.dodge_chance=self.dodge_chance*1.3
            self.nat_damage = self.nat_damage*0.9
            self.ap = 0.15
        elif(self.model=='skele_war2'):
            self.rewardexp = round(self.rewardexp*0.65,2)
            self.nat_armor = self.nat_armor*0.85
            self.health = self.health*0.70
            self.dodge_chance=self.dodge_chance*0.3
            self.nat_damage = self.nat_damage*0.8
            self.ap = 0.1
        elif(self.model=='cobra'):
            self.rewardexp = round(self.rewardexp*0.7,2)
            self.nat_armor = self.nat_armor*0.3
            self.health = self.health*0.6
            self.dodge_chance=self.dodge_chance*2.6
            self.ap = 0.35
        elif(self.model=='rat'):
            self.rewardexp = round(self.rewardexp*0.45,2)
            self.nat_armor = self.nat_armor/3
            self.health = self.health*0.5
            self.dodge_chance=self.dodge_chance*0.3
            self.nat_damage = self.nat_damage*0.3
            self.ap = 0.1
        elif(self.model=='knight_f'):
            self.rewardexp = round(self.rewardexp*1.1,2)
            self.nat_armor = self.nat_armor*1.5
            self.health = self.health*1.1
            self.dodge_chance=1
            self.nat_damage = self.nat_damage*1.3
            self.ap = 0.25
        elif(self.model=='drago'):
            self.rewardexp = round(self.rewardexp*1.4,2)
            self.nat_armor = self.nat_armor*0.9
            self.health = self.health*1.1
            self.nat_damage = self.nat_damage*1.6
            self.ap = 0.35
            
        
    def preset_chars(self):
        random.seed()
        mul=2
        self.strength = random.randint(1+self.level*mul,4+self.level*mul)
        self.dexterity = random.randint(1+self.level*mul,4+self.level*mul)
        self.endurance = random.randint(0+self.level*mul,1+self.level*mul)

    def move(self,newx,newy):
        self.posx=newx
        self.posy=newy

    def get_where_to_go(self,x_rest,y_rest,plr_pos,mobs):
        result = []
        result.append((self.posx+1,self.posy))
        result.append((self.posx-1,self.posy))
        result.append((self.posx,self.posy+1))
        result.append((self.posx,self.posy-1))
        possible_results = []
        filtered_results = []
        mobs_near = []
        ok_pos1 = 0
        ok_pos2 = 0
        go_pos = [self.posx,self.posy]
        go_pos2 = [self.posx,self.posy]
        for i in result:
            if i[0]<x_rest[0] or i[1]<y_rest[0] or i[0]>=x_rest[1] or i[1]>=y_rest[1]:
                continue
            filtered_results.append(i)

        for i in mobs:
            for j in filtered_results:
                if i.posx == j[0] and i.posy == j[1]:
                    mobs_near.append(j)
                    

        for i in filtered_results:
            ok = 1
            for j in mobs_near:
                if j[0]==i[0] and j[1]==i[1]:
                    ok = 0
                    
            if ok==1:
                possible_results.append(i)
        
        go_px = self.posx - plr_pos[0]
        go_py = self.posy - plr_pos[1]
        if go_px == 0:
            if go_py<0:
                go_pos[1] = go_pos[1]+1
            elif go_py>0:
                go_pos[1] = go_pos[1]-1
        if go_py == 0:
            if go_px<0:
                go_pos[0] = go_pos[0]+1
            elif go_px>0:
                go_pos[0] = go_pos[0]-1
        if go_py != 0 and go_px !=0:
            ang = math.atan2(go_px,go_py)
            ang += math.pi
            if ang<math.pi/2:
                go_pos[0]+=1
                go_pos2[1]+=1
            if ang>math.pi/2 and ang<math.pi:
                go_pos[1]-=1
                go_pos2[0]+=1
            if ang>math.pi and ang<math.pi*3/2:
                go_pos[0]-=1
                go_pos2[1]-=1
            if ang>math.pi*3/2:
                go_pos[1]+=1
                go_pos2[0]-=1

        myresult = []
        
        for i in possible_results:
            if i[0] == go_pos[0] and i[1] == go_pos[1]:
                ok_pos1 = 1
        for i in possible_results:
            if i[0] == go_pos2[0] and i[1] == go_pos2[1]:
                ok_pos2 = 1
        if ok_pos1 == 1:
            myresult.append(go_pos)
        else:
            myresult.append([self.posx,self.posy])

        if ok_pos2 == 1:
            myresult.append(go_pos2)
        else:
            myresult.append([self.posx,self.posy])
        return myresult #go_pos
        
    def upd_stats(self):
        #str
        self.nat_damage = float(self.strength/2)
        self.crit_addmul = float(self.strength*1)
        #dex
        self.dodge_chance = self.dexterity
        self.crit_chance = float(self.dexterity)/3
        #end
        self.health = float(self.endurance*2)
        self.nat_armor = float(self.endurance/4)
