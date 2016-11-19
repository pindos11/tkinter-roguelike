import random
class Item:
    def __init__(self,itype,level):
        random.seed()
        self.level = level+random.randint(-1,1)
        if(self.level<=0):
            self.level=1
        self.itype=itype
        if(itype=='wpn'):
            self.generate_wpn()
        if(itype=='arm'):
            self.generate_arm()
        if(itype=='utl'):
            self.generate_utl()
    def generate_wpn(self):
        prefixes = ['Bitter','Convex','Curved','Hard','Hot','Narrow','Strong','Unpleasant','Awful']
        suffixes = ['evil','loyalty','justice','despair','honor','pain','faith','hate','courage']
        mod = random.randint(1,3)
        self.model='wpn'+str(mod)
        if(mod==1):
            self.name='sword'
            self.model=self.name
        elif(mod==2):
            self.name='axe'
            self.model=self.name
        elif(mod==3):
            self.name='mace'
            self.model=self.name
        self.in_damage = self.level + random.randint(0,5)
        self.add_damage = 0
        self.add_strength = 0
        self.add_dexterity = 0
        self.in_dexterity = 0
        self.in_strength = self.level/2 + random.randint(0,2)
        if(self.in_strength<1):
            self.in_strength=1
        if(random.randint(0,1)):
            self.add_damage+=random.randint(int(self.level/3),int(self.level*0.75))
            self.add_strength+= self.level/1.5 + random.randint(0,2)
            self.name=prefixes[random.randint(0,len(prefixes)-1)] +' '+ self.name
        if(random.randint(0,9)>=9):
            self.add_damage+=random.randint(self.level,int(self.level*1.5))
            self.add_strength+= self.level + random.randint(1,5)
            self.add_dexterity+= random.randint(3,4)+self.level/3
            self.name += ' of '+suffixes[random.randint(0,len(suffixes)-1)]
        self.name = self.name.capitalize()
        print(self.name)
    def generate_arm(self):
        prefixes = ['Bitter','Convex','Curved','Hard','Hot','Narrow','Strong','Unpleasant','Awful']
        suffixes = ['evil','loyalty','justice','despair','honor','pain','faith','hate','courage']
        mod = random.randint(1,2)
        if(mod==1):
            self.name='mail'
            self.model=self.name
        elif(mod==2):
            self.name='cuirass'
            self.model=self.name
        self.in_armor = self.level + random.randint(0,2)
        self.add_armor = 0
        self.in_endurance = 1 + random.randint(0,self.level)
        self.add_endurance = 0
        self.in_dexterity = random.randint(0,int(self.level*0.3))*(mod%2)
        self.add_dexterity = 0
        self.in_health = self.level*2 + random.randint(0,int(self.level*1.5))
        self.add_health = 0
        if(random.randint(0,1)):
            self.add_armor+=random.randint(0,int(self.level*1.5))
            self.add_endurance+=random.randint(0,int(self.level*0.5))
            self.name=prefixes[random.randint(0,len(prefixes)-1)] +' '+ self.name
        if(random.randint(0,9)>=9):
            self.add_armor+=random.randint(int(self.level*0.5),int(self.level*1.5))
            self.add_endurance+=random.randint(1,int(self.level*0.5)+1)
            self.add_health+=random.randint(int(self.level*0.5),int(self.level*1.5))
            self.add_dexterity+=random.randint(1,int(self.level*0.5)+1)
            self.name += ' of '+suffixes[random.randint(0,len(suffixes)-1)]
        self.name = self.name.capitalize()
        print(self.name)
    def generate_utl(self):
        self.model='bottle'
        self.name=self.model
        self.model+=str(random.randint(1,4))
        self.in_regen = self.level*2
        self.add_regen=0
        self.add_dexterity = int(self.level/2)
        self.add_endurance = int(self.level/2)
        addc=0
        if(random.randint(0,100)>80):
            addc=1
            self.name='Big '+self.name
        self.max_charges=3+addc
        if(random.randint(0,50)>37):
            self.name+=' of baltika 9'
            self.add_regen=random.randint(0,self.level)
            self.add_endurance+=random.randint(1,int(self.level/3)+2)
        self.name = self.name.capitalize()
        self.charges=self.max_charges
        print(self.name)
        print('\tRegens: '+str(self.in_regen+self.add_regen))
        print('\tAdds: '+str(self.add_dexterity)+'dex '+str(self.add_endurance)+'end')