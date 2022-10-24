import tkinter
from PIL import Image
from PIL import ImageTk
class Drawing:
    def __init__(self,curf,plr):
        self.mainwindow=tkinter.Tk()
        self.mainwindow.geometry('1280x720+0+0')
        #self.mainwindow.attributes("-fullscreen", True)
        self.canv = tkinter.Canvas(self.mainwindow)
        self.canv.pack(fill='both', expand=True)
        self.win_hgt = self.mainwindow.winfo_screenheight()
        self.win_len = self.mainwindow.winfo_screenwidth()
        self.mobs_c=[]
        self.npcs_c=[]
        self.mobhp_c = []
        self.msg_log=[]
        self.pic_size = self.win_hgt/curf.sizey
        self.pic_size = int(self.pic_size)
        self.draw_field(curf,plr)
        
	
    def get_mwin(self):
        return(self.mainwindow)
		
    def draw_npcs(self,npcs):
        for i in self.npcs_c:
            self.canv.delete(i)
        self.npcs_c=[]
        self.npcimgs=[]
        for i in npcs:
            self.npcimgs.append(tkinter.PhotoImage(file='images/chars/npc/'+i.ntype+'.gif'))
            self.npcs_c.append(self.canv.create_image((i.posx*60,i.posy*60),image=self.npcimgs[len(self.npcimgs)-1],anchor='nw'))
    
    def draw_monsters(self,mobs):
        for i in self.mobs_c:
            self.canv.delete(i)
        for i in self.mobhp_c:
            self.canv.delete(i)
        self.mobs_c = []
        self.mobhp_c = []
        self.mgimgs=[]
        for i in mobs:
            mob_dir = i.mov_pos
            iimg = Image.open('images/chars/mobs/'+i.model+'/mob_'+mob_dir+'.png')
            iimg.resize((self.pic_size,self.pic_size), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(iimg)        
            self.mgimgs.append(img)
            self.mobs_c.append(self.canv.create_image(((i.posx)*self.pic_size,(i.posy-0.5)*self.pic_size),image=self.mgimgs[len(self.mgimgs)-1],anchor='nw'))
            self.mobhp_c.append(self.canv.create_rectangle(i.posx*self.pic_size,(i.posy-0.5)*self.pic_size,i.posx*self.pic_size+(self.pic_size*0.8),(i.posy-0.5)*self.pic_size+self.pic_size/30,fill='white',outline='red'))
            self.mobhp_c.append(self.canv.create_rectangle(i.posx*self.pic_size,(i.posy-0.5)*self.pic_size,i.posx*self.pic_size+(self.pic_size*0.8)*(i.health/i.maxhealth),(i.posy-0.5)*self.pic_size+self.pic_size/30,fill='red',outline='red'))
            
    def draw_gui(self,plr,curfpos,wrd,qposes):
        return
        self.canv.create_text((610,2),text="Moves log",anchor='nw')
        self.msgboximg=tkinter.PhotoImage(file='images/gui/msg.png')
        self.msgboxic=self.canv.create_image((600,20),image=self.msgboximg,anchor='nw')
        #all text in img after img
        self.msgbox=[]
        for i in range(0,6):
            self.msgbox.append(self.canv.create_text((610,30+i*14),text='',anchor='nw'))
        self.wpnimgc = 1000
        self.armimgc = 1000
        self.utlimgc = 1000
        self.canv.create_text((610,132),text="Status",anchor='nw')
        self.statusboximg=tkinter.PhotoImage(file='images/gui/stats.png')
        self.statusboxic=self.canv.create_image((600,150),image=self.statusboximg,anchor='nw')
        self.canv.create_rectangle(610,160,700,175,fill='white',outline='red')
        self.canv.create_rectangle(610,160,610+90*(plr.health/plr.maxhealth),175,fill='red',outline='red')
        self.canv.create_text((610,160),text='Health: '+str(round(plr.health,1))+'/'+str(plr.maxhealth),anchor='nw')
        self.canv.create_text((610,200),text='Strength: '+str(plr.strength),anchor='nw')
        self.canv.create_text((610,215),text='Dexterity: '+str(plr.dexterity),anchor='nw')
        self.canv.create_text((610,230),text='Endurance: '+str(plr.endurance),anchor='nw')
        self.canv.create_text((710,160),text='Exp '+str(plr.exp)+'/'+str(plr.nexp),anchor='nw')
        self.canv.create_text((610,185),text='Level: '+str(plr.level),anchor='nw')
        self.canv.create_text((710,185),text='Damage: '+str(plr.damage),anchor='nw')
        self.canv.create_text((710,200),text='Armor: '+str(plr.armor),anchor='nw')
        self.canv.create_text((700,215),text='You are in '+str(curfpos),anchor='nw')
        
        self.invboximg = tkinter.PhotoImage(file='images/gui/stats.png')
        self.inventimg = tkinter.PhotoImage(file='images/gui/inv_box.png')
        self.invboxc=self.canv.create_image((600,280),image=self.invboximg,anchor='nw')
        self.invbox1=self.canv.create_image((608,322),image=self.inventimg,anchor='nw')
        self.invbox2=self.canv.create_image((670,322),image=self.inventimg,anchor='nw')
        self.invbox3=self.canv.create_image((732,322),image=self.inventimg,anchor='nw')
        self.q_logt = self.canv.create_text((605,390),text='Minimap (quest NPC - blue):',anchor='nw')
        #if(len(self.qposes)>0):
         #   qposc = []
          #  for i in self.qposes:
           #     qposc.append(self.canv.create_text((610,420+self.qposes.index(i)*15),text=str(i),anchor='nw'))
                
        self.draw_minimap(wrd,curfpos,qposes)
        #items
        self.invtext=self.canv.create_text((620,300),text='Inventory',anchor='nw')
        if(len(plr.inventory)>0):
            for i in plr.inventory:
                if(i.itype=='wpn'):
                    self.wpnimg=tkinter.PhotoImage(file='images/items/'+i.model+'.gif')
                    if(self.wpnimgc!=1000):
                        self.canv.itemconfig(self.wpnimgc,image=self.wpnimg)
                    else:
                        self.wpnimgc=self.canv.create_image((623,337),image=self.wpnimg,anchor='nw')
                if(i.itype=='arm'):
                    self.armimg=tkinter.PhotoImage(file='images/items/'+i.model+'.gif')
                    if(self.armimgc!=1000):
                        self.canv.itemconfig(self.armimgc,image=self.armimg)
                    else:
                        self.armimgc=self.canv.create_image((685,337),image=self.armimg,anchor='nw')
                if(i.itype=='utl'):
                    self.utlimg=tkinter.PhotoImage(file='images/items/'+i.model+'.gif')
                    if(self.utlimgc!=1000):
                        self.canv.itemconfig(self.utlimgc,image=self.utlimg)
                    else:
                        self.utlimgc=self.canv.create_image((747,337),image=self.utlimg,anchor='nw')
                    self.chargec=self.canv.create_text((747,337),text=i.charges,anchor='nw')


    def draw_minimap(self,wrd,curfpos,qposes):
        return
        mpos = (700,500)
        mmsize=8
        offset = (curfpos[0]*mmsize,curfpos[1]*mmsize)
        cpos = curfpos
        mpos = (mpos[0]-offset[0],mpos[1]-offset[1])
        for pos,fld in wrd.items():
            if(pos[0]>10+cpos[0] or pos[0]<-10+curfpos[0] or pos[1]>10+cpos[1] or pos[1]<-10+curfpos[1]):
                continue
            color = 'white'
            if(fld.ztype==1):
                color='green'
            elif(fld.ztype==2):
                color='yellow'
            elif(fld.ztype==3):
                color='red'
            elif(fld.ztype==4):
                color='black'
            if(pos in qposes):
                color = 'blue2'
            if(pos==curfpos):
                color = 'white'
            self.canv.create_rectangle((mpos[0]+pos[0]*mmsize,mpos[1]+pos[1]*mmsize,mpos[0]+pos[0]*mmsize+mmsize,mpos[1]+pos[1]*mmsize+mmsize),fill=color)
    
    def draw_field(self,curf,plr):
        self.canv.delete('all')
        self.terrain = []
        self.lootimgs=[]
        self.texlist={}
        zoom = 1
        tlist=curf.terrains()
        
        for i in tlist:
            if('3_h' in i):
                iimg = Image.open('images/buildings/'+str(i)+'.gif')
                iimg.resize((self.pic_size,self.pic_size), Image.ANTIALIAS)
                img = ImageTk.PhotoImage(iimg)
                self.texlist.update([(i,img)])
            else:
                iimg = Image.open('images/60x60terrain/'+str(i)+'.gif')
                iimg.resize((self.pic_size,self.pic_size), Image.ANTIALIAS)
                img = ImageTk.PhotoImage(iimg)
                self.texlist.update([(i,img)])
        for i in range(0,curf.sizex):
            tmp = []
            self.terrain.append(tmp)
            for j in range(0,curf.sizey):
                ttype=curf.cur_cond()[i][j].get_terrain()
                if('3_h' in ttype):
                    self.terrain[i].append(self.canv.create_image((i*self.pic_size,j*self.pic_size),image=self.texlist['1'],anchor='nw'))
                    self.terrain[i].append(self.canv.create_image((i*self.pic_size,j*self.pic_size),image=self.texlist[ttype],anchor='nw'))
                else:    
                    self.terrain[i].append(self.canv.create_image((i*self.pic_size,j*self.pic_size),image=self.texlist[ttype],anchor='nw'))
                if(curf.cur_cond()[i][j].hasloot==1):
                    loot = curf.cur_cond()[i][j].loot
                    self.lootimgs.append(tkinter.PhotoImage(file='images/items/'+loot.model+'.gif'))
                    self.canv.create_image((i*self.pic_size,j*self.pic_size),image=self.lootimgs[len(self.lootimgs)-1],anchor='nw')
        self.draw_player(curf,plr)
    
    def draw_player(self,curf,plr):
        img_name = 'images/chars/player/plr_'
        img_name += plr.move_dir
        img_name += ".png"
        iimg = Image.open(img_name)
        iimg.resize((self.pic_size,self.pic_size), Image.ANTIALIAS)
        self.psprite = ImageTk.PhotoImage(iimg)        
        pposx = curf.pposx
        pposy = curf.pposy
        self.plabel=self.canv.create_image(((pposx)*self.pic_size,(pposy-0.5)*self.pic_size),image=self.psprite,tags='player',anchor='nw')
		
    def edit_msg(self,text):
        return
        if(text!=''):
            self.msg_log.append(text)
        if(len(self.msg_log)>6):
            self.msg_log=self.msg_log[len(self.msg_log)-6:len(self.msg_log)]
        for i in range(0,6):
            if(len(self.msg_log)==0):
                break
            try:
                outtext=self.msg_log[i]
            except:
                break
            color='black'
            if('Received' in outtext):
                color='red'
            elif('Dealt' in outtext):
                color='green'
            elif('Entering' in outtext):
                color='blue'
            self.canv.itemconfig(self.msgbox[i],text=outtext,fill=color)
