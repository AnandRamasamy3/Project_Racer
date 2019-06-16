import pygame,sys,time,random,math,sqlite3
from pygame.locals import *

#input
pygame.init()
conn=sqlite3.connect('score.db')
name=[];score=[]
cursor=conn.execute("SELECT * from high;")
for row in cursor:
	 name.append(row[0])
	 score.append(row[1])
cur=conn.cursor()
try:highscore=max(score)
except:highscore=2000;print ("exception")
fps=30
ft=pygame.time.Clock()
disp=pygame.display.set_mode((500,650),0,0)
pygame.display.set_caption("Racer")
car=pygame.image.load('cc.jpg')
bg=pygame.image.load('bg.png')
lifeimg=pygame.image.load('life.jpg')
tar=[];ty=[5]
tar.append(pygame.image.load('t1.jpg'))
tar.append(pygame.image.load('t2.jpg'))
tar.append(pygame.image.load('t3.jpg'))
tar.append(pygame.image.load('t4.jpg'))
tr1=pygame.image.load('tr1l.jpg')
tr2=pygame.image.load('tr1r.jpg')
tr3=pygame.image.load('tr2l.jpg')
tr4=pygame.image.load('tr2r.jpg')
myfont=pygame.font.SysFont('Segoe Print',26,bold=True,italic=False)
scorefont=pygame.font.SysFont('Segoe Print',20,bold=True,italic=False)
timefont=pygame.font.SysFont('Segoe Print',100,bold=True,italic=False)
black=(0,0,0);grey=(128,128,128,128);green=(0,128,0)
white=(255,255,255);blue=(0,0,128)
x=160;y=500;key="n";pos=1;a1=75;b1=480;tim=4
t1=-60;t2=-600;t3=-1100;t4=-1800
ty=[-200,-1000,-600,-1500]
crashed=False;speed=5;lev=1;life=3

def home(key):
	while key=="n":
		disp.blit(bg,(0,0))
		back="nb"
		for event in pygame.event.get():
			if event.type==QUIT:
				pygame.quit()
				sys.exit()
			if event.type==KEYDOWN:
				if event.key==pygame.K_p:
					key="y"
				if event.key==pygame.K_h:
					help(back)
				if event.key==pygame.K_q:
					pygame.quit()
					sys.exit()
		textsurface1=timefont.render("Racer...",False,(white))
		textplay=myfont.render("play",False,(white))
		texthelp=myfont.render("help",False,(white))
		pygame.draw.rect(disp,(0,0,0,255),(300,500,150,150))
		pygame.draw.rect(disp,(0,0,0,255),(50,500,150,150))
		disp.blit(textsurface1,(100,150))
		disp.blit(textplay,(350,525))
		disp.blit(texthelp,(100,525))
		mouse_pos=pygame.mouse.get_pos()
		click=pygame.mouse.get_pressed()
		if click[0]==1 and 300<=mouse_pos[0]<=450 and 500<=mouse_pos[1]<=600:
			key="y"
		if click[0]==1 and 50<=mouse_pos[0]<=200 and 500<=mouse_pos[1]<=600:
			help(back)
		pygame.display.update() 
		ft.tick(fps)
	return key
def help(back):
	while back=="nb":
		disp.blit(bg,(0,0))
		for event in pygame.event.get():
			if event.type==QUIT:
				pygame.quit()
				sys.exit()
			if event.type==KEYDOWN:
				if event.key==pygame.K_b:
					back="b"
				if event.key==pygame.K_q:
					pygame.quit()
					sys.exit()
		textl=myfont.render("left = moves left",False,(white))
		textr=myfont.render("right = moves right",False,(white))
		textu=myfont.render("up = speed up",False,(white))
		textd=myfont.render("down = speed down",False,(white))
		texts=myfont.render("space = pause/ play",False,(white))
		textrs=myfont.render("r = restart",False,(white))
		textq=myfont.render("q = quit",False,(white))
		textb=myfont.render("b = back",False,(white))
		disp.blit(textl,(100,150))
		disp.blit(textr,(100,200))
		disp.blit(textu,(100,250))
		disp.blit(textd,(100,300))
		disp.blit(texts,(100,350))
		disp.blit(textrs,(100,400))
		disp.blit(textq,(100,450))
		disp.blit(textb,(100,528))
		pygame.display.update() 
		ft.tick(fps)
	return back
def move_right(x):
	x+=100
	return x
def move_left(x):
	x-=100
	return x
def check(x):
    if x<60 :x=60
    if x>360:x=360
    return x
def draw_track():
	pygame.draw.line(disp,black,(50,0),(50,650),18)
	pygame.draw.line(disp,black,(150,0),(150,650),3)
	pygame.draw.line(disp,black,(250,0),(250,650),3)
	pygame.draw.line(disp,black,(350,0),(350,650),3)
	pygame.draw.line(disp,black,(450,0),(450,650),22)
def move_track1(b,speed):
	disp.blit(tr1,(0,b))
	t=(speed/5)
	b+=(t+3)
	return b
def move_track2(b,speed):
	disp.blit(tr2,(445,b))
	t=(speed/5)
	b+=(t+3)
	return b
def move_track3(b,speed):
	disp.blit(tr3,(0,b))
	t=(speed/5)
	b+=(t+3)
	return b
def move_track4(b,speed):
	disp.blit(tr4,(445,b))
	t=(speed/5)
	b+=(t+3)
	return b
def timer(tim):
	if tim>0:tem=str(tim)
	else:tem="GO"
	textsurface3=timefont.render(tem,True,(white))
	disp.blit(textsurface3,(200,200))
	return tim
def start(a1,b1):
	b11=b1+20
	pygame.draw.line(disp,white,(a1,b1),(a1,b11),3)
	for i in range(1,15):
		a1+=25
		if a1!=150 and a1!=250 and a1!=350:
			pygame.draw.line(disp,white,(a1,b1),(a1,b11),3)
	return 1
def target(tar,tx,ty,speed):
	ty+=speed
	disp.blit(tar,(tx,ty))
	return ty
def sort_with_score(dl):
	#print("\n\n\n",dl)
	l=[]
	for i in dl:
		l.append([i,dl[i]])
	for i in range(len(l)):
		for j in range(i,len(l)):
			if l[i][1]<l[j][1]:
				temp=l[i]
				l[i]=l[j]
				l[j]=temp
	dl={}
	#print(l)
	for i in l:
		#print(i[0],i[1])
		dl.update({i[0]:i[1]})
	return dl
def check_score(pname,pscore):
	scores1=[];names1=[]
	fin_score={}
	cur.execute("INSERT into high values(?,?);",(pname,pscore))
	cursor=conn.execute("SELECT * from high;")
	for row in cursor:
		names1.append(row[0])
		scores1.append(row[1])
	for i in range(len(scores1)):
		#print("\n\n",names1[i],scores1[i])
		fin_score.update({names1[i]:scores1[i]})
	#print(fin_score)
	fin_score=sort_with_score(fin_score)
	#print(fin_score)
	conn.commit()
	return fin_score
def score_card(level,score,life,highscore):
	if score<=5:score=1
	pygame.draw.rect(disp,blue,(5,5,200,60))
	textsurface10=scorefont.render((str(score)),True,(white))
	if highscore>=score:high=highscore
	else:high=score
	texthigh=scorefont.render((str(high)),True,(white))
	textscore=scorefont.render("score:",True,(white))
	texthscore=scorefont.render("high:",True,(white))
	disp.blit(textscore,(5,5))
	disp.blit(textsurface10,(65,5))
	disp.blit(texthscore,(5,30))
	disp.blit(texthigh,(65,30))
	pygame.draw.rect(disp,blue,(295,5,200,60))
	textsurface11=scorefont.render(str(level),True,(white))
	textlevel=scorefont.render("level:",True,(white))
	disp.blit(textlevel,(320,35))
	disp.blit(textsurface11,(380,35))
	if life>=3:disp.blit(lifeimg,(380,10))
	if life>=2:disp.blit(lifeimg,(350,10))
	if life>=1:disp.blit(lifeimg,(320,10))
def level(lev,speed):
	speed+=5
	textsurface8=timefont.render("level",True,(white))
	textsurface9=timefont.render(str(lev),True,(white))
	disp.blit(textsurface8,(150,200))
	disp.blit(textsurface9,(200,300))
	pygame.display.update()
	return speed
def out(x,ty):
	res=True
	if x==60 and 400<ty[0]<550:res=False;ty[0]+=300
	if x==160 and 400<ty[1]<550:res=False;ty[1]+=300
	if x==260 and 400<ty[2]<550:res=False;ty[2]+=300
	if x==360 and 400<ty[3]<550:res=False;ty[3]+=300
	return res
def crash(name,score):
	black=(0,0,0);grey=(128,128,128,128);green=(0,128,0)
	white=(255,255,255);blue=(0,0,128);key="n"
	fin_score=check_score(name,score)
	#print("\n\n\n",fin_score)
	while True:
		disp.blit(bg,(0,0))
		textsurface7=myfont.render("click p to restart",False,(white))
		disp.blit(textsurface7,(100,550))
		textsurfacetop=myfont.render("top scores are:-",False,(white))
		disp.blit(textsurfacetop,(50,100))
		sy=200
		if len(fin_score)<=5:
			length=len(fin_score)
		else:
			length=5
		#print(fin_score)
		fin_score=sort_with_score(fin_score)
		#print(fin_score)
		for i in range(0,length):
			lk=list(fin_score.keys())
			lv=list(fin_score.values())
			textsurfacename=myfont.render(str(lk[i]),False,(white))
			textsurfacerank=myfont.render(str(i+1),False,(white))
			textsurfacescore=myfont.render(str(lv[i]),False,(white))
			if lv[i]==score:
				textsurfaceyour=myfont.render(">>",False,(white))
				disp.blit(textsurfaceyour,(50,sy))
			disp.blit(textsurfacename,(100,sy))
			disp.blit(textsurfacescore,(200,sy))
			disp.blit(textsurfacerank,(350,sy))
			sy+=50
		for event in pygame.event.get():
			if event.type==QUIT:
				pygame.quit()
				sys.exit()
			if event.type==KEYDOWN:
				if event.key==pygame.K_p:
					key="y"
				if event.key==K_q:
					pygame.quit()
					sys.exit()
		if key=="y":
			black=(0,0,0);grey=(128,128,128,128);green=(0,128,0)
			white=(255,255,255);blue=(0,0,128)
			x=160;y=500;key="n";pos=1;a1=75;b1=480;tim=4
			t1=-60;t2=-600;t3=-1100;t4=-1800
			ty=[-200,-1000,-600,-1500]
			crashed=False;speed=5;lev=1;life=3
			highscore=lv[0]
			pname=get_name(x,y,pos,a1,b1,tim,t1,t2,t3,t4,ty,crashed,speed,lev,life,highscore)
			play(x,y,pos,a1,b1,tim,t1,t2,t3,t4,ty,crashed,speed,lev,life,highscore,pname)
		pygame.display.update()
		ft.tick(fps)
def restart(highscore):
	black=(0,0,0);grey=(128,128,128,128);green=(0,128,0)
	white=(255,255,255);blue=(0,0,128)
	x=160;y=500;key="n";pos=1;a1=75;b1=480;tim=4
	t1=-60;t2=-600;t3=-1100;t4=-1800
	ty=[-200,-1000,-600,-1500]
	crashed=False;speed=5;lev=1;life=3
	pname=get_name(x,y,pos,a1,b1,tim,t1,t2,t3,t4,ty,crashed,speed,lev,life,highscore)
	play(x,y,pos,a1,b1,tim,t1,t2,t3,t4,ty,crashed,speed,lev,life,highscore,pname)
def play(x,y,pos,a1,b1,tim,t1,t2,t3,t4,ty,crashed,speed,lev,life,highscore,name):
	while crashed==False:
		disp.fill((128,128,128))
		key="n"
		res=True
		draw_track()
		#running_sound.play()
		pos+=1
		tim-=1;t=0
		if pos<100:
			if tim<-1:b1+=3
			t=start(a1,b1)
		if tim>-2:
			tim=timer(tim)
			if tim!=-2:time.sleep(1)
		pygame.draw.rect(disp,green,(0,0,50,650))
		pygame.draw.rect(disp,green,(450,0,50,650))
		if t4>750:
			t1=-60;t2=-600;t3=-1100;t4=-1800
		if pos>50:
			t1=move_track1(t1,speed)
			t2=move_track2(t2,speed)
			t3=move_track3(t3,speed)
			t4=move_track4(t4,speed)
		for event in pygame.event.get():
			if event.type==QUIT:
				pygame.quit()
				sys.exit()
			if event.type==KEYDOWN:
				if event.key==pygame.K_RIGHT:
					if pos>=65:x=move_right(x)
				if event.key==pygame.K_LEFT:
					if pos>=65:x=move_left(x)
				if event.key==pygame.K_UP:
					speed+=5
				if event.key==pygame.K_DOWN:
					speed-=5
					lv=(speed/5)-1
					if lv<lev:speed+=5
				if event.key==pygame.K_SPACE:
					i=3
					while i>2:
						for event in pygame.event.get():
							if event.type==QUIT:
								pygame.quit()
								sys.exit()
							if event.type==KEYDOWN:
								if event.key==pygame.K_SPACE:
									i=1
				if event.key==K_b:
					key=home(key)
				if event.key==K_r:
					restart(highscore)
				if event.key==K_q:
					pygame.quit()
					sys.exit()
		x=check(x)
		disp.blit(car,(x,y))
		if pos>100:
			if max(ty)>2000:
				ty=[-200,-1000,-600,-1500]
				random.shuffle(ty)
			ty[0]=target(tar[0],75,ty[0],speed)
			ty[1]=target(tar[1],175,ty[1],speed)
			ty[2]=target(tar[2],275,ty[2],speed)
			ty[3]=target(tar[3],375,ty[3],speed)
		res=out(x,ty)
		if res==False:life-=1
		if life==0:
			crashed=True
			crash(name,pos)
		score_card(lev,pos,life,highscore)
		if pos%1000==0:
			lev+=1
			speed=level(lev,speed)
			time.sleep(0.5)
		pygame.display.update()
		ft.tick(fps)
def get_name(x,y,pos,a1,b1,tim,t1,t2,t3,t4,ty,crashed,speed,lev,life,highscore):
	get=True
	name=""
	textsurface_get=myfont.render("enter your name to continue...",False,white)
	while get:
		disp.blit(bg,(0,0))
		textsurface_name=myfont.render(name,False,white)
		disp.blit(textsurface_get,(20,200))
		disp.blit(textsurface_name,(20,250))
		for event in pygame.event.get():
			if event.type==QUIT:
				pygame.quit()
				sys.exit()
			if event.type==KEYDOWN:
				if event.key==pygame.K_a and len(name)<6:name+="a"
				if event.key==pygame.K_b and len(name)<6:name+="b"
				if event.key==pygame.K_c and len(name)<6:name+="c"
				if event.key==pygame.K_d and len(name)<6:name+="d"
				if event.key==pygame.K_e and len(name)<6:name+="e"
				if event.key==pygame.K_f and len(name)<6:name+="f"
				if event.key==pygame.K_g and len(name)<6:name+="g"
				if event.key==pygame.K_h and len(name)<6:name+="h"
				if event.key==pygame.K_i and len(name)<6:name+="i"
				if event.key==pygame.K_j and len(name)<6:name+="j"
				if event.key==pygame.K_k and len(name)<6:name+="k"
				if event.key==pygame.K_l and len(name)<6:name+="l"
				if event.key==pygame.K_m and len(name)<6:name+="m"
				if event.key==pygame.K_n and len(name)<6:name+="n"
				if event.key==pygame.K_o and len(name)<6:name+="o"
				if event.key==pygame.K_p and len(name)<6:name+="p"
				if event.key==pygame.K_q and len(name)<6:name+="q"
				if event.key==pygame.K_r and len(name)<6:name+="r"
				if event.key==pygame.K_s and len(name)<6:name+="s"
				if event.key==pygame.K_t and len(name)<6:name+="t"
				if event.key==pygame.K_u and len(name)<6:name+="u"
				if event.key==pygame.K_v and len(name)<6:name+="v"
				if event.key==pygame.K_w and len(name)<6:name+="w"
				if event.key==pygame.K_x and len(name)<6:name+="x"
				if event.key==pygame.K_y and len(name)<6:name+="y"
				if event.key==pygame.K_z and len(name)<6:name+="z"
				if event.key==pygame.K_0 and len(name)<6:name+="0"
				if event.key==pygame.K_1 and len(name)<6:name+="1"
				if event.key==pygame.K_2 and len(name)<6:name+="2"
				if event.key==pygame.K_3 and len(name)<6:name+="3"
				if event.key==pygame.K_4 and len(name)<6:name+="4"
				if event.key==pygame.K_5 and len(name)<6:name+="5"
				if event.key==pygame.K_6 and len(name)<6:name+="6"
				if event.key==pygame.K_7 and len(name)<6:name+="7"
				if event.key==pygame.K_8 and len(name)<6:name+="8"
				if event.key==pygame.K_9 and len(name)<6:name+="9"
				if event.key==pygame.K_F10:
					pygame.quit()
					sys.exit()
				if event.key==pygame.K_RETURN:
					if len(name)>0:
						get=False
				if event.key==pygame.K_BACKSPACE:
					temp_list=list(name)
					if len(temp_list)>0:
						temp_list.pop()
						name=""
						for character in temp_list:
							name+=character
		pygame.display.update()
		ft.tick(fps)
	play(x,y,pos,a1,b1,tim,t1,t2,t3,t4,ty,crashed,speed,lev,life,highscore,name)
key=home(key)
if key=="y":get_name(x,y,pos,a1,b1,tim,t1,t2,t3,t4,ty,crashed,speed,lev,life,highscore)
