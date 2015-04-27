#imports
#=====================================================================
import WConio, os, sys, time, msvcrt
from random import randint
import math


#inits
#=====================================================================
k= None
gameOn=1
WConio.clrscr()
arrows=[['left','right','up','down'],[-1,1,0,0],[0,0,-1,1]]
os.system('cls')
player = 1
		
#functions
#=====================================================================
def clearLines():
	for i in range (21,24):
		WConio.gotoxy(0,i)
		WConio.clreol()
	
def printBoard(array):
	for h in range(len(array[0])):
		for w in range(len(array)):
			WConio.gotoxy(w*2+1+40-len(array),h*2+1)
			print array[w][h]
			
def printGrid(array):	
	WConio.gotoxy(40-len(array),0)
	y=len(array[0])-1
	x=len(array)-1
	print chr(218)+(chr(196)+chr(194))*x+chr(196)+chr(191)
	for i in range(y):
		WConio.gotoxy(40-len(array),i*2+2)
		print chr(195)+(chr(196)+chr(197))*x+chr(196)+chr(180)
	WConio.gotoxy(40-len(array),y*2+2)
	print chr(192)+(chr(196)+chr(193))*x+chr(196)+chr(217)	
	for i in range(y+1):
		for j in range (x+2):
			WConio.gotoxy(j*2+40-len(array),i*2+1)
			print chr(179)
		
def makeArray(size):
	WConio.clrscr()
	gameArray=None	
	gameArray=[[chr(250) for y in range(size[1])] for x in range(size[0])]
	printGrid(gameArray)
	printBoard(gameArray)
	return gameArray

def printCursor(gameArray,cursor):
	WConio.gotoxy(cursor[0]*2+40-len(gameArray),cursor[1]*2)
	print chr(201)+chr(205)+chr(187)
	WConio.gotoxy(cursor[0]*2+40-len(gameArray),cursor[1]*2+1)
	print chr(186)+gameArray[cursor[0]][cursor[1]]+chr(186)
	WConio.gotoxy(cursor[0]*2+40-len(gameArray),cursor[1]*2+2)
	print chr(200)+chr(205)+chr(188)
	
def printCursor2(gameArray,cursor):
	WConio.gotoxy(cursor[0]*2+40-len(gameArray),cursor[1]*2)
	print chr(201)+chr(205)+chr(187)
	WConio.gotoxy(cursor[0]*2+40-len(gameArray),cursor[1]*2+1)
	print chr(186)+gameArray[cursor[0]][cursor[1]]+chr(186)
	WConio.gotoxy(cursor[0]*2+40-len(gameArray),cursor[1]*2+2)
	print chr(200)+chr(205)+chr(188)	

def selectToken (gameArray,arrows,player):
	WConio.gotoxy(0,23)
	print "{0:^79}".format("Select one of your tokens to initiate a move.")
	k=None
	player=1
	while k<>"q":
		printCursor(gameArray,cursor)
		if k =="u":
			printUnicode()
		if k =="a":
			printAscii()
			
		k = WConio.getkey()
		if k in arrows[0]:
			WConio.gotoxy(cursor[0]*2+1+40-len(gameArray),cursor[1]*2+1) 
			printGrid(gameArray) #'erase' cursor icon
			d=arrows[0].index(k)		
			cursor[0]=(cursor[0]+arrows[1][d])%len(gameArray)
			cursor[1]=(cursor[1]+arrows[2][d])%len(gameArray[0])
		printCursor(gameArray,cursor)

		if k == " ":# when 'spacebar' entered
			if ord(gameArray[cursor[0]][cursor[1]])<>player:
				WConio.gotoxy(0,21)
				print "{0:^79}".format("Player {0}, you can only select a space that is already yours.".format(player))
			else:	
				clearLines()
				WConio.gotoxy(0,21)
				print "{0:^79}".format("Token selected.")
				#print " "*79
				gameArray = selectDestination(gameArray,cursor,player,arrows)
				break		
	
def selectDestination(gameArray,cursor,player,arrows):
	k=None
	oldCursor = cursor[:]
	while k<>"q":
		k = WConio.getkey()
		if k in arrows[0]:
			#WConio.gotoxy(cursor[0]*2+1+40-len(gameArray),cursor[1]*2+1) 
			printGrid(gameArray) #'erase' cursor icon
			d=arrows[0].index(k)		
			cursor[0]=(cursor[0]+arrows[1][d])
			if cursor[0]<0 or cursor[0]>len(gameArray) or abs(cursor[0]-oldCursor[0])>2:
				cursor[0]=(cursor[0]-arrows[1][d])
			cursor[1]=(cursor[1]+arrows[2][d])
			if cursor[1]<0 or cursor[1]>len(gameArray[0]) or abs(cursor[1]-oldCursor[1])>2:
				cursor[1]=(cursor[1]-arrows[2][d])
		printCursor(gameArray,oldCursor)
		printCursor2(gameArray,cursor)

		if k == " ":# when 'spacebar' entered
				if ord(gameArray[cursor[0]][cursor[1]])<>250:
					WConio.gotoxy(0,21)
					print "{0:^79}".format("Player {0}, you can only move to empty spaces".format(player))
				else:
					finalizeMove(gameArray,oldCursor,cursor,player)
					break
	return gameArray		

def finalizeMove(gameArray,oldCursor,cursor,player):
	WConio.gotoxy(0,21)
	if cursor==None:
		return gameArray
	print "{0:^79}".format("Token cloned.")
	gameArray[cursor[0]][cursor[1]]=chr(player)
	if abs(cursor[0]-oldCursor[0])==2 or abs(cursor[1]-oldCursor[1])==2:
		gameArray[oldCursor[0]][oldCursor[1]]=chr(250)
		WConio.gotoxy(0,21)
		print "{0:^79}".format("Token moved.")
	time.sleep(0)
	c=0
	for i in range (cursor[0]-1,cursor[0]+2):
		for j in range (cursor[1]-1,cursor[1]+2):
			try:
				if gameArray[i][j]==chr(player%2+1) and i>=0 and i<=len(gameArray) and j>=0 and j<= len(gameArray[0]):
					gameArray[i][j]=chr(player)
					c+=1
			except:
				pass
	print "{0:^79}".format("Assimilated {0} of the opponent's tokens.".format(c))	
	printGrid(gameArray)
	printBoard(gameArray)
	WConio.gotoxy(40-len(gameArray),21)
	return gameArray
	
def printScore(gameArray,score):
	score=[0,0]
	for x in range(len(gameArray)):	
		for y in range(len(gameArray[0])):	
			if gameArray[x][y]==chr(1):
				score[0]+=1
			elif gameArray[x][y]==chr(2):
				score[1]+=1	
	WConio.gotoxy(5,0)
	print"You"
	WConio.gotoxy(5,1)
	print"==="
	WConio.gotoxy(5,2)
	print "{:^3}".format(score[0])
	WConio.gotoxy(72,0)
	print"CPU"
	WConio.gotoxy(72,1)
	print"==="
	WConio.gotoxy(72,2)
	print "{:^3}".format(score[1])
	
	#check for wion by skunk
	if score[0]*score[1]==0:
		clearLines()
		if score[0]==0:
			print "{0:^79}".format("You have lost all of your tokens on the board.")
			print "{0:^79}".format("Therefore the COMPUTER is the winner!") 
		else:
			print "{0:^79}".format("The computer has lost all of its tokens on the board.")
			print "{0:^79}".format("Therefore YOU are the winner!") 	
	
	#check for win by filled board
	if score[0]+score[1]==len(gameArray)*len(gameArray[0]):
		clearLines()
		if score[0]>score[1]:
			print "{0:^79}".format("You have dominated the board and have acquired the most tokens.")
			print "{0:^79}".format("Therefore YOU are the winner!") 
		else:
			print "{0:^79}".format("You have been dominated and have acquired the least tokens.")
			print "{0:^79}".format("Therefore the COMPUTER is the winner!") 	
	
	return score
	
def compTurn(gameArray,player):
	compMoves=[] 							#list of how many acquisitions per each open spot
	for x in range(len(gameArray)):			#create compMoves
		for y in range(len(gameArray[0])):
			if gameArray[x][y]==chr(250):
				c=0
				for i in range (x-1,x+2):
					for j in range (y-1,y+2):
						if i>=0 and j>=0 and i<=len(gameArray) and j<=len(gameArray[0]):
							try:
								if gameArray[i][j]==chr(1):
									c+=1
							except:
								pass
				compMoves.append([c,x,y])
	move=compPicksMove(gameArray,sorted(compMoves, reverse=True)) #
	try:
		oldCursor=move[3][:]
		cursor=[move[1],move[2]]
		pauselength=0
		for i in range(5):
			time.sleep(pauselength)
			printGrid(gameArray)
			time.sleep(pauselength)
			printCursor(gameArray,oldCursor)
		for i in range(5):
			time.sleep(pauselength)
			printGrid(gameArray)
			printCursor(gameArray,oldCursor)
			time.sleep(pauselength)
			printCursor2(gameArray,cursor)
	except:
		oldCursor=None
		cursor=None	
	finalizeMove(gameArray,oldCursor,cursor,player)				

def compPicksMove(gameArray,moves):	#picks a move with the greatest # of acquisitions
	maybeJump=[]	
	for move in moves:
		for i in range (move[1]-1,move[1]+2):
			for j in range (move[2]-1,move[2]+2):
				if i>=0 and j>=0 and i<=len(gameArray) and j<=len(gameArray[0]):
					try:
						if gameArray[i][j]==chr(2):
							move.append([i,j])
							try:
								if maybeJump[0]>move[0]+1:
									return maybeJump
								else:
									return move
							except:
								return move
								
							return move
					except:
						pass
		try:
			move[3]
		except:	
			for i in range (move[1]-2,move[1]+3):
				for j in range (move[2]-2,move[2]+3):
					if i>=0 and j>=0 and i<=len(gameArray) and j<=len(gameArray[0]):
						try:
							if gameArray[i][j]==chr(2):
								maybeJump=move[:]
								maybeJump.append([i,j])
						except:
							pass
	return None
	
def selectBoard(arrows):
	WConio.clrscr()
	k=None
	comment = None
	size=[5,5]
	gameArray=makeArray(size)
	WConio.gotoxy(0,21)
	print "{0:^79}".format("Hit the spacebar to accept this board.")	
	while k<>" ":		
		k = WConio.getkey()
		if k in arrows[0]:
			d=arrows[0].index(k)
			size[0]=(size[0]+arrows[1][d]*2)
			size[1]=(size[1]+arrows[2][d]*2)
			if size[0]>21:
				size[0]=21
				comment = "That's as wide as you can go."
			elif size[0]<5:
				size[0]=5
				comment = "That's as narrow as you can go."
			elif size[1]>9:
				size[1]=9
				comment = "That's as tall as you can go."
			elif size[1]<5:
				size[1]=5
				comment = "That's as short as you can go."
			else:
				comment = ""
		gameArray=makeArray(size)
		WConio.gotoxy(0,21)
		print "{0:^79}".format("{} {}".format(size,comment))
		if size[0]*size[1]>50:
			print "{0:^79}".format("This size board will get some random tokens thrown on.")	
		print "{0:^79}".format(" Hit the spacebar to accept this board.")
	#init pieces
	gameArray[0][0]=chr(1)
	gameArray[0][len(gameArray[0])-1]=chr(2)
	gameArray[len(gameArray)-1][0]=chr(2)
	gameArray[len(gameArray)-1][len(gameArray[0])-1]=chr(1)
	if len(gameArray)*len(gameArray[0])>50:
		c=0
		WConio.gotoxy(0,21)
		
		while c< len(gameArray)*len(gameArray[0])-40:
			m=randint(0,len(gameArray)-1)
			n=randint(0,len(gameArray[0])-1)
			p=randint(0,len(gameArray)-1)
			q=randint(0,len(gameArray[0])-1)
			if gameArray[m][n]==chr(250) and gameArray[p][q]==chr(250) and m<>p:
				gameArray[m][n]=chr(1)
				gameArray[p][q]=chr(2)
				c=c+2
	clearLines()
	return (gameArray)

def intro():
	WConio.gotoxy(0,10)
	print "{0:^79}".format("  O     O  ")
	print "{0:^79}".format("  O     O  ")
	print "{0:^79}".format(" OOOOO OOOOO")
	print "{0:^79}".format("  O     O  ")
	print "{0:^79}".format("  O     O  ")
	print "{0:^79}".format("  O     O  ")
	print "{0:^79}".format("  O     O ")
	print "\n"*4
	print "{0:^79}".format("hit spacebar to continue")
	k=None
	speed = 20 #higher is slower
	inc=10
	r=12

	while 1:
		i=0
		while i<math.pi:
			ang=0
			while ang<math.pi/2:
				x=math.cos(ang)*r
				y=math.sin(ang)*r
				scale=math.cos(i)
				oldScale = math.cos(i-2*math.pi/speed)
				for j in range(-1,3,2):
					for k in range(-1,3,2):
						WConio.gotoxy(int(20+x*oldScale*j),int(12+y*k))
						print " "
						WConio.gotoxy(int(20+x*scale*j),int(12+y*k))
						print "O"
						WConio.gotoxy(int(60+x*oldScale*j),int(12+y*k))
						print " "
						WConio.gotoxy(int(60+x*scale*j),int(12+y*k))
						print "O"
				ang+=math.pi/4/inc		
			i+=math.pi/speed	
		if msvcrt.kbhit():
			if msvcrt.getch() ==" ":
				break		
	
intro()	
while gameOn==1:	
	score=[2,2]
	gameArray=selectBoard(arrows)
	cursor = [int(len(gameArray)/2),int(len(gameArray[0])/2)]
	printBoard(gameArray)
	score = printScore(gameArray,score)
	#main game loop
	while score[0]+score[1]<len(gameArray)*len(gameArray[0]) and score[0]<>0 and score[1]<>0:
		if player == 1:
			selectToken(gameArray,arrows,player)
		if player == 2:
			compTurn(gameArray,player)
		player=player%2+1	
		score = printScore(gameArray,score)
	
	print "{0:^79}".format("Play again? y/n")
	while gameOn==1:
		k = WConio.getkey()
		if k.lower()=="y":
			break
		elif k.lower()=="n":
			gameOn=0
		else:
			print "{0:^79}".format("What is that-- Spanish? Yo no lo comprendo. Try again.")
			print "{0:^79}".format("Play again? y/n")
			
	
WConio.clrscr()	
WConio.gotoxy(0,12)
print "{0:^79}".format("Fine. Bye. Whatever.")
print "\n\n\n\n"
time.sleep(2)
