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
            self.levelup()
            nx=self.nexp
            self.nexp+=self.level+5
            self.level+=1
            self.exp-=nx
            self.exp = round(self.exp,2)
            self.upd_stats()
            self.health+=self.level*2
            if(self.health>=self.maxhealth):
                self.health=self.maxhealth
            return('Welcome to level '+str(self.level)+'!')
        return('Gained '+str(amount)+' exp')

    def levelup(self):
        self.lvlup=tkinter.Toplevel(self.master)
        self.lvlup.title("Choose charasteristic to upgrade")
        self.lvlup.geometry('300x200+100+100')
        self.charact=tkinter.IntVar()
        stren = tkinter.Radiobutton(self.lvlup,variable=self.charact,text="Strength: +2 dmg +1% crit mul",value=1)
        dex = tkinter.Radiobutton(self.lvlup,variable=self.charact,text="Dexterity +1% dodge chance +1% crit chance",value=2)
        end = tkinter.Radiobutton(self.lvlup,variable=self.charact,text="Endurance +3 hp +0.5 armor",value=3)
        stren.place(x=20,y=20)
        dex.place(x=20,y=45)
        end.place(x=20,y=70)
        acbtn=tkinter.Button(self.lvlup,text='Accept',command=self.add_char)
        acbtn.place(x=20,y=95)
        self.lvlup.mainloop()
        
    def add_char(self):
        to_add=self.charact.get()
        if(to_add==1):
            self.nat_strength+=1
        elif(to_add==2):
            self.nat_dexterity+=1
        elif(to_add==3):
            self.nat_endurance+=1
        else:
            return(0)
        self.lvlup.quit()
        self.lvlup.destroy()
        
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
