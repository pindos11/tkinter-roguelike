import random
class quest:
    def __init__(self,qtype):
        self.qtype=qtype
        self.completed = 0
        if(qtype==1):
            self.mobs = ['skele','drago','knight','cobra','rat','goblin']
            self.mob_targ = self.mobs[random.randint(0,len(self.mobs)-1)]
            self.amount = random.randint(1,5)
            self.qtext = 'Please, hero, kill '+str(self.amount)+' '+self.mob_targ
            self.qtext += 's to keep our village safe!'
            self.killed = 0