from Field import *
from Item import *
from MainGame import *
from Monster import *
from NPC import *
from Player import *
from quest import*
from Drawing import*

import math
import tkinter
class MainGame:
    def __init__(self):
        self.started = 0
        self.qposes = []
        self.curquests = []
        self.state='move'
        self.curf=Field(10,10,1,1)
        self.world={(0,0):self.curf}
        self.curfpos=(0,0)
        self.Drawing = Drawing(self.curf)
        self.bind_moves()
        self.player = Player(self.Drawing.mainwindow)
        self.Drawing.draw_gui(self.player,self.curfpos,self.world,self.qposes)
        self.Drawing.draw_npcs(self.curf.npcs)
        self.Drawing.mainwindow.mainloop()

    def create_mobs(self,field):
        random.seed()
        num=random.randint(2,4)
        zone = field.ztype
        if(zone==4):
            return
        mobs=[]
        if(zone==1):
            mobs.append('goblin')
            mobs.append('rat')
        elif(zone==3):
            mobs.append('drago')
            mobs.append('knight_f')
        elif(zone==2):
            mobs.append('skele_war')
            mobs.append('cobra')
        ctr=0
        fld=field.cur_cond()
        while(ctr<num):
            mposx=random.randint(0,9)
            mposy=random.randint(0,9)
            mob_type=mobs[random.randint(0,len(mobs)-1)]
            if(fld[mposx][mposy].get_terrain() in field.walkable):
                field.add_monster(Monster(self.player,mob_type,(mposx,mposy)))
                ctr+=1

    
                    
    

    def make_field(self,side):
        try:
            curpos=(self.curfpos[0]+side[0],self.curfpos[1]+side[1])
            fld=self.world[curpos]
            
        except:
            
            curpos=(self.curfpos[0]+side[0],self.curfpos[1]+side[1])
            random.seed()
            vil = random.randint(0,4)
            ztype=random.randint(1,4)
            if(vil):
                vil=0
            else:
                vil = 2
            fld=Field(10,10,vil,ztype)
            if(vil==0 or ztype!=1):
                self.create_mobs(fld)
        if(side==(0,1)):
            newpy=0
            newpx=self.curf.pposx
        elif(side==(0,-1)):
            newpy=fld.sizey-1
            newpx=self.curf.pposx
        elif(side==(1,0)):
            newpy=self.curf.pposy
            newpx=0
        elif(side==(-1,0)):
            newpy=self.curf.pposy
            newpx=fld.sizex-1
        else:
            newpx=self.curf.pposx
            newpy=self.curf.pposy
        self.world.update([(curpos,fld)])
        if(fld.cur_cond()[newpx][newpy].get_terrain() in fld.walkable):
            fld.move_player(newpx,newpy)
            
            self.curf=fld
            self.curfpos=curpos
            self.Drawing.draw_field(self.curf)
            self.Drawing.draw_gui(self.player,self.curfpos,self.world,self.qposes)
            self.Drawing.draw_monsters(self.curf.ret_monsters())
            self.Drawing.draw_npcs(self.curf.npcs)
            self.Drawing.edit_msg('')
            if(side!=(0,0)):
                self.Drawing.edit_msg("Entering in: "+str(curpos))

    
    def get_dist(self,x2,x1,y2,y1):
        return(math.sqrt((x2-x1)*(x2-x1)+(y2-y1)*(y2-y1)))
    #   2
    #1 mob 3
    #   4
    #keep this in mind
    def move_mobs(self):
        mobs=self.curf.ret_monsters()
        pposx = float(self.curf.pposx)
        pposy = float(self.curf.pposy)
        for i in mobs:          
            pdist=self.get_dist(pposx,i.posx,pposy,i.posy)
            if(pdist<3 and pdist>1):
                poses = i.get_where_to_go((0,self.curf.sizex),(0,self.curf.sizey),(pposx,pposy),mobs)
                pos = poses[0]
                if self.curf.cur_cond()[pos[0]][pos[1]].get_terrain() in self.curf.walkable:
                    i.move(pos[0],pos[1])
                else:
                    pos = poses[1]
                    if self.curf.cur_cond()[pos[0]][pos[1]].get_terrain() in self.curf.walkable:
                        i.move(pos[0],pos[1])
            if(pdist==1):
                plr = self.player
                dodge = random.randint(0,99)+plr.dodge_chance
                if(dodge>=100):
                    continue
                fin_damage=i.nat_damage+i.ap*plr.armor
                crit_bonus = i.crit_addmul*0.01*i.nat_damage
                crit = random.randint(0,99)+i.crit_chance
                if(crit>=100):
                    fin_damage+=crit_bonus
                fin_damage-=plr.armor
                if(fin_damage<0):
                    fin_damage=0
                plr.health-=fin_damage
                plr.health=round(plr.health,2)
                if(plr.health<=0):
                    self.finish_game()
                self.make_field((0,0))
                self.Drawing.edit_msg('Received '+str(fin_damage)+' damage')
        self.Drawing.draw_monsters(self.curf.ret_monsters())

    def attack_mob(self,pos):
        random.seed()
        tmob = []
        mobs=self.curf.ret_monsters()
        for i in mobs:
            if(pos[0]==i.posx and pos[1]==i.posy):
                tmob.append(i)
                break
        tmobi = tmob[0]
        plr = self.player
        dodge = random.randint(0,99)+tmobi.dodge_chance
        if(dodge>=100):
            self.Drawing.edit_msg('You missed')
            return
        fin_damage=plr.damage
        crit_bonus = plr.crit_addmul*0.01*plr.damage
        crit = random.randint(0,99)+plr.crit_chance
        if(crit>=100):
            fin_damage+=crit_bonus
            self.Drawing.edit_msg('Critical! Plus '+str(plr.crit_addmul)+'% damage')
        fin_damage-=tmobi.nat_armor
        if(fin_damage<0):
            fin_damage=0
        tmobi.health-=fin_damage
        self.Drawing.edit_msg('Dealt '+str(fin_damage)+' damage')
        if(tmobi.health<=0):
            rewexp=tmobi.rewardexp
            drop=0
            random.seed(random.randint(0,1000))
            if(random.randint(0,14)==14):
                drop=1
            if(drop==1):
                dtype=random.randint(1,3)
                if(dtype==1):
                    dropped=Item('wpn',plr.level)
                elif(dtype==2):
                    dropped=Item('arm',plr.level)
                elif(dtype==3):
                    dropped=Item('utl',plr.level)
                self.curf.cur_cond()[tmobi.posx][tmobi.posy].place_loot(dropped)
            self.upd_quest(tmobi.model)
            self.Drawing.edit_msg((tmobi.model+' is slain').capitalize())
            self.curf.kill_monster(tmobi)
            self.unbind_moves()
            text = self.player.add_exp(rewexp)
            self.bind_moves()
            self.make_field((0,0))
            self.Drawing.edit_msg(text)

    def upd_quest(self,mob):
        for i in self.curquests:
            if(i.mob_targ in mob):
                if(i.completed==0):
                    i.killed+=1
                if(i.killed==i.amount):
                    i.completed=1

            
    def interact_npc(self,pos):
        npcs=self.curf.npcs
        tnpc = []
        for i in npcs:
            if(pos[0]==i.posx and pos[1]==i.posy):
                tnpc.append(i)
                break
        tnpci=tnpc[0]
        if(tnpci.quest.qtype==1 and tnpci.quest.completed==0):
            self.qst = tnpci.quest
            self.qwindow = tkinter.Toplevel()
            self.qwindow.geometry('170x200+30+30')
            self.qlabel = tkinter.Label(self.qwindow,text=tnpci.quest.qtext, wrap=150)
            self.qlabel.place(x=10,y=10)
            self.acceptbtn = tkinter.Button(self.qwindow,text='Accept',command=self.take_quest)
            self.acceptbtn.place(x=10,y=170)
            self.denybtn = tkinter.Button(self.qwindow,text='Deny',command=self.deny_quest)
            self.denybtn.place(x=100,y=170)
            self.qwindow.mainloop()

        
        elif(tnpci.quest.completed==1):
            self.qwindow = tkinter.Toplevel()
            self.qwindow.geometry('170x200+30+30')
            self.qlabel = tkinter.Label(self.qwindow,text="Thank you a lot! Take this as a reward", wrap=150)
            self.qlabel.place(x=10,y=10)
            self.denybtn = tkinter.Button(self.qwindow,text='OK',command=self.deny_quest)
            self.denybtn.place(x=100,y=170)
            tnpci.quest.completed = 2
            plr = self.player
            pposx = self.curf.pposx
            pposy = self.curf.pposy
            self.qposes.remove(self.curfpos)
            self.qwindow.mainloop()
            dtype=random.randint(1,3)
            if(dtype==1):
                dropped=Item('wpn',plr.level+2)
            elif(dtype==2):
                dropped=Item('arm',plr.level+2)
            elif(dtype==3):
                dropped=Item('utl',plr.level+2)
            self.curf.cur_cond()[pposx][pposy].place_loot(dropped)
            self.make_field((0,0))
            self.Drawing.edit_msg('')

        elif(tnpci.quest.completed==2):
            self.qwindow = tkinter.Toplevel()
            self.qwindow.geometry('170x200+30+30')
            self.qlabel = tkinter.Label(self.qwindow,text="I have nothing to tell you", wrap=150)
            self.qlabel.place(x=10,y=10)
            self.denybtn = tkinter.Button(self.qwindow,text='OK',command=self.deny_quest)
            self.denybtn.place(x=100,y=170)
            
            
    def take_quest(self):
        if(self.qst not in self.curquests):
            self.curquests.append(self.qst)
            self.qposes.append(self.curfpos)
        #print(len(self.curquests))
        self.make_field((0,0))
        self.Drawing.edit_msg('')
        self.qwindow.quit()
        self.qwindow.destroy()

    def deny_quest(self):
        self.qwindow.quit()
        self.qwindow.destroy()

    def hitext(self):
        text = '''
OLOLO.'''
        return text

    
    def move(self,event):
        if(self.state!='move'):
            self.player_act(event)
        if(self.started==0):
            self.started=1
            self.hiwindow = tkinter.Toplevel()
            self.hilabel = tkinter.Label(self.hiwindow,text=self.hitext())
            self.hilabel.place(x=10,y=10)
            self.hiwindow.geometry('500x300+10+10')
            self.hiwindow.mainloop()
        pposx = self.curf.pposx
        pposy = self.curf.pposy
        mobs = self.curf.ret_monsters()
        npcs = self.curf.npcs
        npcposes = []
        mposes = []
        #(pposx,pposy-1) in mposes
        for i in mobs:
            mposes.append((i.posx,i.posy))
        for i in npcs:
            npcposes.append((i.posx,i.posy))
        if(event.char=='w'):
            if(pposy-1<0):
                self.make_field((0,-1))
                return
            if(self.curf.cur_cond()[pposx][pposy-1].get_terrain() in self.curf.walkable):
                if((pposx,pposy-1) in mposes):
                    self.attack_mob((pposx,pposy-1))
                    self.move_mobs()
                    return
                if((pposx,pposy-1) in npcposes):
                    self.interact_npc((pposx,pposy-1))
                    return
                self.curf.move_player(pposx,pposy-1)
                
                self.Drawing.draw_player(self.curf)
                self.bind_moves()
        if(event.char=='s'):
            if(pposy+1>self.curf.sizey-1):
                self.make_field((0,1))
                return
            if(self.curf.cur_cond()[pposx][pposy+1].get_terrain() in self.curf.walkable):
                if((pposx,pposy+1) in mposes):
                    self.attack_mob((pposx,pposy+1))
                    self.move_mobs()
                    return
                if((pposx,pposy+1) in npcposes):
                    self.interact_npc((pposx,pposy+1))
                    return
                self.curf.move_player(pposx,pposy+1)
                pposx = self.curf.pposx
                pposy = self.curf.pposy
                self.Drawing.draw_player(self.curf)
        if(event.char=='a'):
            if(pposx-1<0):
                self.make_field((-1,0))
                return
            if(self.curf.cur_cond()[pposx-1][pposy].get_terrain() in self.curf.walkable):
                if((pposx-1,pposy) in mposes):
                    self.attack_mob((pposx-1,pposy))
                    self.move_mobs()
                    return
                if((pposx-1,pposy) in npcposes):
                    self.interact_npc((pposx-1,pposy))
                    return
                self.curf.move_player(pposx-1,pposy)
                pposx = self.curf.pposx
                pposy = self.curf.pposy
                self.Drawing.draw_player(self.curf)
        if(event.char=='d'):
            if(pposx+1>self.curf.sizex-1):
                self.make_field((1,0))
                return
            if(self.curf.cur_cond()[pposx+1][pposy].get_terrain() in self.curf.walkable):
                if((pposx+1,pposy) in mposes):
                    self.attack_mob((pposx+1,pposy))
                    self.move_mobs()
                    return
                if((pposx+1,pposy) in npcposes):
                    self.interact_npc((pposx+1,pposy))
                    return
                self.curf.move_player(pposx+1,pposy)
                pposx = self.curf.pposx
                pposy = self.curf.pposy
                self.Drawing.draw_player(self.curf)
        if(event.char=='3'):
            itms=self.player.inventory
            has_bottle=0
            bottle = 0
            for i in itms:
                if(i.itype=='utl'):
                    has_bottle=1
                    bottle=itms.index(i)
                    break
            if(has_bottle==1):
                if(self.player.inventory[bottle].charges>0):
                    self.player.heal(self.player.inventory[bottle].in_regen+self.player.inventory[bottle].add_regen)
                    self.player.inventory[bottle].charges-=1
                    self.make_field((0,0))
                else:
                    return
            else:
                return
        if(event.char=='x'):
            pposx = self.curf.pposx
            pposy = self.curf.pposy
            plr=self.player
            if(pposx<9 and pposy<9):
                wells = []
                wells.append((pposx-1,pposy))
                wells.append((pposx+1,pposy))
                wells.append((pposx,pposy-1))
                wells.append((pposx,pposy+1))
                for w in wells:
                    if(self.curf.cur_cond()[w[0]][w[1]].get_terrain()=='3_h_w'):
                        plr.inventory[2].charges=plr.inventory[2].max_charges
                        self.make_field((0,0))
                        self.Drawing.edit_msg('')
                        break
        if(event.char=='c'):
            pposx = self.curf.pposx
            pposy = self.curf.pposy
            plr=self.player
            if(self.curf.cur_cond()[pposx][pposy].hasloot==1):
                n_item=self.curf.cur_cond()[pposx][pposy].loot
                nitype=n_item.itype
                for i in plr.inventory:
                    if(i.itype==nitype):
                        o_item=i
                        break
                self.pick_thingw=tkinter.Toplevel(self.Drawing.mainwindow)
                self.pick_thingw.title("Picking item")
                self.pick_thingw.geometry('550x200+100+100')
                o_name=o_item.name
                n_name=n_item.name
                if(o_item.itype=='wpn'):
                    o_text=o_name+'\nDamage: '+str(o_item.in_damage)+'+'+str(o_item.add_damage)
                    o_text+='\nStrength: '+str(o_item.in_strength)+'+'+str(o_item.add_strength)
                    o_text+='\nDexterity: '+str(o_item.in_dexterity)+'+'+str(o_item.add_dexterity)
                    n_text=n_name+'\nDamage: '+str(n_item.in_damage)+'+'+str(n_item.add_damage)
                    n_text+='\nStrength: '+str(n_item.in_strength)+'+'+str(n_item.add_strength)
                    n_text+='\nDexterity: '+str(n_item.in_dexterity)+'+'+str(n_item.add_dexterity)

                if(o_item.itype=='arm'):
                    o_text=o_name+'\nArmor: '+str(o_item.in_armor)+'+'+str(o_item.add_armor)
                    o_text+='\nHealth: '+str(o_item.in_health)+'+'+str(o_item.add_health)
                    o_text+='\nDexterity: '+str(o_item.in_dexterity)+'+'+str(o_item.add_dexterity)
                    o_text+='\nEndurance: '+str(o_item.in_endurance)+'+'+str(o_item.add_endurance)
                    n_text=n_name+'\nArmor: '+str(n_item.in_armor)+'+'+str(n_item.add_armor)
                    n_text+='\nHealth: '+str(n_item.in_health)+'+'+str(n_item.add_health)
                    n_text+='\nDexterity: '+str(n_item.in_dexterity)+'+'+str(n_item.add_dexterity)
                    n_text+='\nEndurance: '+str(n_item.in_endurance)+'+'+str(n_item.add_endurance)

                if(o_item.itype=='utl'):
                    o_text=o_name+'\nRegen: '+str(o_item.in_regen)+'+'+str(o_item.add_regen)
                    o_text+='\nMax charges: '+str(o_item.max_charges)
                    o_text+='\nPassive properties:\n'
                    o_text+='\nDexterity: '+str(o_item.add_dexterity)
                    o_text+='\nEndurance: '+str(o_item.add_endurance)
                    n_text=n_name+'\nRegen: '+str(n_item.in_regen)+'+'+str(n_item.add_regen)
                    n_text+='\nMax charges: '+str(n_item.max_charges)
                    n_text+='\nPassive properties:\n'
                    n_text+='\nDexterity: '+str(n_item.add_dexterity)
                    n_text+='\nEndurance: '+str(n_item.add_endurance)
                self.o_text=o_text
                self.n_text=n_text
                self.o_item=o_item
                self.n_item=n_item
                self.o_label=tkinter.Label(self.pick_thingw,text=o_text)
                self.n_label=tkinter.Label(self.pick_thingw,text=n_text)
                self.o_label.place(x=10,y=30)
                self.n_label.place(x=280,y=30)
                self.choice=tkinter.IntVar()
                self.o_rb = tkinter.Radiobutton(self.pick_thingw,variable=self.choice,value=0,text='Keep yours')
                self.n_rb = tkinter.Radiobutton(self.pick_thingw,variable=self.choice,value=1,text='Take this')
                self.o_rb.place(x=10,y=5)
                self.n_rb.place(x=280,y=5)

                self.y_btn = tkinter.Button(self.pick_thingw,text='Accept',command=self.pick_item)        
                self.y_btn.place(x=30,y=170)
                self.pick_thingw.mainloop()
            else:
                if(pposx<9 and pposy<9):
                    wells = []
                    wells.append((pposx-1,pposy))
                    wells.append((pposx+1,pposy))
                    wells.append((pposx,pposy-1))
                    wells.append((pposx,pposy+1))
                    for w in wells:
                        if(self.curf.cur_cond()[w[0]][w[1]].get_terrain()=='3_h_w'):
                            plr.inventory[2].charges=plr.inventory[2].max_charges
                            self.make_field((0,0))
                            self.Drawing.edit_msg('')
                            break
        self.move_mobs()

    
    def pick_item(self):
        if(self.choice.get()==0):
            self.pick_thingw.quit()
            self.pick_thingw.destroy()
        else:
            to_drop=self.player.give_item(self.n_item)
            pposx = self.curf.pposx
            pposy = self.curf.pposy
            self.curf.cur_cond()[pposx][pposy].place_loot(to_drop)
            self.make_field((0,0))
            self.Drawing.edit_msg('')
            self.pick_thingw.quit()
            self.pick_thingw.destroy()
                
    def add_exp(self,event):
        text=self.player.add_exp(5)
        self.make_field((0,0))
        self.Drawing.edit_msg(text)
    def bind_moves(self):
        self.Drawing.mainwindow.bind('w',self.move)
        self.Drawing.mainwindow.bind('s',self.move)
        self.Drawing.mainwindow.bind('a',self.move)
        self.Drawing.mainwindow.bind('d',self.move)
        self.Drawing.mainwindow.bind('3',self.move)
        self.Drawing.mainwindow.bind('x',self.move)
        self.Drawing.mainwindow.bind('c',self.move)

    def unbind_moves(self):
        self.Drawing.mainwindow.unbind('w')
        self.Drawing.mainwindow.unbind('s')
        self.Drawing.mainwindow.unbind('a')
        self.Drawing.mainwindow.unbind('d')
        self.Drawing.mainwindow.unbind('3')
        self.Drawing.mainwindow.unbind('x')
        self.Drawing.mainwindow.unbind('c')
        #self.Drawing.mainwindow.bind('h',self.add_exp)
    def finish_game(self):
        self.Drawing.canv.delete('all')
        you_dead=tkinter.Label(self.Drawing.mainwindow,text='You dead')
        you_dead.place(x=200,y=200)
        self.Drawing.mainwindow.unbind('w')
        self.Drawing.mainwindow.unbind('s')
        self.Drawing.mainwindow.unbind('a')
        self.Drawing.mainwindow.unbind('d')
        raise
