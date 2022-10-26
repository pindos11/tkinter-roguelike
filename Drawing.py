import tkinter
from PIL import Image
from PIL import ImageTk

class Canvas_ui_element:
    def __init__(self,elem_type,pos,content):
        self.type = elem_type
        self.px = pos[0]
        self.py = pos[1]
        self.data = content

class Canvas_ui_object:
    def __init__(self,canv,draw,pos,size,ui_type):
        self.canv = canv
        self.elements = []
        self.tkobjs = []
        self.draw = draw
        self.px = pos[0]
        self.py = pos[1]
        self.sx = size[0]
        self.sy = size[1]
        self.img = []
        self.utype = ui_type

    def add_element(self,elem):
        self.elements.append(elem)
        return

    def erase(self):
        self.elements = []
        for i in self.tkobjs:
            self.canv.delete(i)
        self.tkobjs = []
        self.img = []

    def display(self):
        #self.canv.delete('all')
        iimg = Image.open('images/gui/ui_object.png')
        iimg = iimg.resize((self.sx,self.sy))
        self.img.append(ImageTk.PhotoImage(iimg))
        #print(self.px)
        self.tkobjs.append(self.canv.create_image((self.px,self.py),image=self.img[-1],anchor='nw'))
        #print(self.tkobjs[0])
        for i in self.elements:
            if i.type == 'text':
                self.disp_text(i,self.px,self.py)
            if i.type == 'frame':
                self.disp_frame(i,self.px,self.py)
        
        for i in self.tkobjs:
            self.canv.tag_raise(i,'all')

    def disp_text(self,elem,x,y):
        px = x+elem.px
        py = y+elem.py
        self.tkobjs.append(self.canv.create_text((px,py),text=elem.data[0],anchor='nw',font=('Helevtica',elem.data[1])))
        return

    def disp_frame(self,elem,x,y):
        iimg = Image.open(elem.data[0])
        iimg = iimg.resize((elem.data[1],elem.data[2]))
        self.img.append(ImageTk.PhotoImage(iimg))
        px = x+elem.px
        py = y+elem.py
        self.tkobjs.append(self.canv.create_image((px,py),image=self.img[-1],anchor='nw'))

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
        self.ui_drawn = 0
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
		
    def draw_char_ui(self,plr):
        gui_width = int(self.win_len/5)
        gui_height = int(gui_width*0.75)
        elem_hgt = int(gui_height/10)
        if self.ui_drawn==0:
            elems = []
            self.ui = Canvas_ui_object(self.canv,self,(10,10),(gui_width,gui_height),'info')
            elems.append(Canvas_ui_element('text',(gui_width/4,elem_hgt*(len(elems)+1)),['Health: '+str(round(plr.health,1))+'/'+str(plr.maxhealth),14]))
            #self.ui.add_element(elem1)
            elems.append(Canvas_ui_element('text',(gui_width/4,elem_hgt*(len(elems)+1)),['Strength: '+str(plr.strength),14]))
            elems.append(Canvas_ui_element('text',(gui_width/4,elem_hgt*(len(elems)+1)),['Dexterity: '+str(plr.dexterity),14]))
            elems.append(Canvas_ui_element('text',(gui_width/4,elem_hgt*(len(elems)+1)),['Endurance: '+str(plr.endurance),14]))
            elems.append(Canvas_ui_element('text',(gui_width/4,elem_hgt*(len(elems)+1)),['Exp '+str(plr.exp)+'/'+str(plr.nexp),14]))
            elems.append(Canvas_ui_element('text',(gui_width/4,elem_hgt*(len(elems)+1)),['Level: '+str(plr.level),14]))
            elems.append(Canvas_ui_element('text',(gui_width/4,elem_hgt*(len(elems)+1)),['Damage: '+str(plr.damage),14]))
            elems.append(Canvas_ui_element('text',(gui_width/4,elem_hgt*(len(elems)+1)),['Armor: '+str(plr.armor),14]))
            for i in elems:
                self.ui.add_element(i)
            
            self.ui.display()
            self.ui_drawn = 1
        else:
            if self.ui.utype != 'lvlup':
                self.ui.erase()
                self.ui_drawn = 0

    def draw_lvlup_ui(self,framepos):
        if self.ui_drawn==1:
            self.ui.erase()
        self.lvlup_framepos = framepos
        self.ui_drawn = 1
        gui_width = int(self.win_len/4)
        gui_height = int(gui_width*0.75)
        elem_hgt = int(gui_height/5)
        self.ui = Canvas_ui_object(self.canv,self,(self.win_len/7,self.win_hgt/7),(gui_width,gui_height),'lvlup')
        elems = []
        elems.append(Canvas_ui_element('text',(gui_width/10,elem_hgt*(len(elems)+1)),['Strength: +2 dmg +1% crit mul',14]))
        elems.append(Canvas_ui_element('text',(gui_width/10,elem_hgt*(len(elems)+1)),['Dexterity +1% dodge chance +1% crit chance',14]))
        elems.append(Canvas_ui_element('text',(gui_width/10,elem_hgt*(len(elems)+1)),['Endurance +3 hp +0.5 armor',14]))
        elems.append(Canvas_ui_element('text',(gui_width/10,elem_hgt*(len(elems)+1.3)),['Press F to accept',14]))
        elems.append(Canvas_ui_element('frame',(gui_width/20,elem_hgt*(self.lvlup_framepos+0.6)),['images/gui/lvl_frame.png',int(gui_width*0.9),elem_hgt]))
        for i in elems:
            self.ui.add_element(i)  
        self.ui.display()

    def clear_lvlup_ui(self):
        self.ui.erase()
        self.ui_drawn = 0

    def draw_picking_ui(self,texts,framepos):
        if self.ui_drawn==1:
            self.ui.erase()
        self.pick_framepos = framepos
        self.ui_drawn = 1
        gui_width = int(self.win_len/3)
        gui_height = int(gui_width)
        elem_hgt = int(gui_height/16)
        self.ui = Canvas_ui_object(self.canv,self,(self.win_len/7,self.win_hgt/7),(gui_width,gui_height),'pick_item')
        elems = []
        for i in texts[0]:
            elems.append(Canvas_ui_element('text',(gui_width/10,elem_hgt*(len(elems)+1)),[i,14]))
        for i in texts[1]:
            elems.append(Canvas_ui_element('text',(gui_width/10,elem_hgt*(len(elems)+2)),[i,14]))
        elems.append(Canvas_ui_element('frame',(gui_width/20,elem_hgt*(self.pick_framepos*(int(len(elems)/2)+1))),['images/gui/lvl_frame.png',int(gui_width*0.9),elem_hgt*(int(len(elems)/2)+1)]))
        elems.append(Canvas_ui_element('text',(gui_width/10,elem_hgt*(len(elems)+1.3)),['Press F to accept',14]))
        for i in elems:
            self.ui.add_element(i)
        self.ui.display()
        
    
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
