class FieldPos:
    def __init__(self,x,y,ttype):
        self.posx = x
        self.posy = y
        self.player = 0
        self.terrain=ttype
        self.hasloot=0
    def place_loot(self,loot):
        self.loot=loot
        self.hasloot=1
    def remove_loot(self):
        self.hasloot=0
    def set_terrain(self,ttype):
        self.terrain=ttype
    def get_terrain(self):
        return self.terrain
    def set_player(self):
        self.player = 1
    def unset_player(self):
        self.player = 0
    def contains(self,what):
        if(what=="player"):
            return self.player
    def output_str(self,task):
        print("##")
        print("Output from FieldPos: ")
        if(task=='pos'):
            print("Pos "+str(self.posx)+","+str(self.posy))
            if(self.player==1):
                print("Contains player")
        print("##")