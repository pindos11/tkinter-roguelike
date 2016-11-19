from quest import*

class NPC:
    def __init__(self,pos,ntype):
        self.posx=pos[0]
        self.posy=pos[1]
        self.ntype=ntype
        self.create_quest()
    def create_quest(self):
        self.quest=quest(1)