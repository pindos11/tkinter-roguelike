from Item import *
import tkinter
class Player:
    def __init__(self):
        self.strength=0
        self.dexterity=0
        self.endurance=0
        
        self.add_strength=0
        self.add_dexterity=0
        self.add_endurance=0
        self.health=0
        self.add_health=0
        self.add_damage=0
        self.add_armor=0
        self.inventory=[]
        self.inventory.append(Item('wpn',1))
        self.inventory.append(Item('arm',1))
        self.inventory.append(Item('utl',1))
        self.chartype='player'
        self.level=1
        self.exp=0
        self.nexp=10
        self.preset_chars()
        self.upd_stats()
        self.health=self.maxhealth
        self.move_dir = "(0000)"
        self.leveluped = 0

    def set_master(self,master):
        self.master = master
    
    def give_item(self,item):
        if(item.itype=='wpn'):
            to_ret=self.inventory[0]
            self.inventory[0]=item
        if(item.itype=='arm'):
            to_ret=self.inventory[1]
            self.inventory[1]=item
        if(item.itype=='utl'):
            to_ret=self.inventory[2]
            self.inventory[2]=item
        self.upd_stats()
        return to_ret
        

    def heal(self,addhp):
        self.health+=addhp
        if(self.health>self.maxhealth):
            self.health=self.maxhealth
    
    def add_exp(self,amount):
        self.exp+=amount
        self.exp = round(self.exp,2)
        if(self.exp>=self.nexp):
            self.leveluped = 1
            nx=self.nexp
            self.nexp+=self.level+5
            self.level+=1
            self.exp-=nx
            self.exp = round(self.exp,2)
            return('Welcome to level '+str(self.level)+'!')
        return('Gained '+str(amount)+' exp')

    def lvlup_new(self,choice):
        if(choice==0):
            self.nat_strength+=1
        elif(choice==1):
            self.nat_dexterity+=1
        elif(choice==2):
            self.nat_endurance+=1
        self.upd_stats()
        self.health+=self.level*2
        if(self.health>=self.maxhealth):
            self.health=self.maxhealth
        self.leveluped = 0
        
    def preset_chars(self):
        random.seed()
        self.nat_strength = random.randint(1+self.level,4+self.level)
        self.nat_dexterity = random.randint(1+self.level,4+self.level)
        self.nat_endurance = random.randint(2+self.level,3+self.level)


    def apply_items(self):
        self.add_strength=0
        self.add_dexterity=0
        self.add_endurance=0
        self.add_health=0
        self.maxhealth=0
        self.add_damage=0
        self.add_armor=0
        self.mh=0
        if(self.health==self.maxhealth):
            self.mh=1    
        for i in self.inventory:
            if(i.itype=='wpn'):
                self.add_strength+=int(i.in_strength+i.add_strength)
                self.add_dexterity+=int(i.in_dexterity+i.add_dexterity)
                self.add_damage+=int(i.in_damage+i.add_damage)
            if(i.itype=='arm'):
                self.add_endurance+=int(i.in_endurance+i.add_endurance)
                self.add_dexterity+=int(i.in_dexterity+i.add_dexterity)
                self.add_armor+=int(i.in_armor+i.add_armor)
                self.add_health+=int(i.in_health+i.add_health)
            if(i.itype=='utl'):
                self.add_endurance+=int(i.add_endurance)
                self.add_dexterity+=int(i.add_dexterity)
                
        
    def upd_stats(self):
        self.apply_items()
        self.strength=self.nat_strength+self.add_strength
        self.dexterity=self.nat_dexterity+self.add_dexterity
        self.endurance=self.nat_endurance+self.add_endurance
        #str
        self.nat_damage = float(self.strength*2)
        self.crit_addmul = float(self.strength*2)
        #dex
        self.dodge_chance = self.dexterity
        self.crit_chance = float(self.dexterity)/2
        #end
        self.maxhealth = float(self.endurance*3)+self.add_health
        self.nat_armor = self.endurance/2

        self.damage=self.nat_damage+self.add_damage
        self.armor=self.nat_armor+self.add_armor
        if(self.health>self.maxhealth):
            self.health=self.maxhealth
        if(self.mh==1):
            self.health=self.maxhealth

    def set_move_dir(self,movement):
        self.move_dir = movement
