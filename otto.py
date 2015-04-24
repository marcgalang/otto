#imports
#=====================================================================
import WConio, os, sys, time
from pprint import pprint
import traceback #allows for feedback on errors

#inits
#=====================================================================

WConio.clrscr()
size=[5,5]
arrows=[['left','right','up','down'],[-1,1,0,0],[0,0,-1,1]]
k=None
comment = ""
os.system('cls')
player = 1
score=[2,2]

#just here as development tools
#=====================================================================
def printAscii():	# just used to create an ascii table for my reference
	for x in range(32):
		for y in range(8):
			print "{0}={1}".format(8*x+y,chr(8*x+y)),
		print
		
def printUnicode():	# just used to create an ascii table for my reference
	for x in range(16):
		for y in range(8):
			print "{0}={1}".format(8*x+y,unichr(8*x+y)),
		print
		
#functions
#=====================================================================
def clearLines():
	WConio.gotoxy(0,24)
	WConio.clreol()
	WConio.clreol()
	WConio.gotoxy(0,24)

def printBoard(array):
	for h in range(len(array[0])):
		for w in range(len(array)):
			WConio.gotoxy(w*2+1,h*2+1)
			print array[w][h]
			
def printGrid(array):	
	WConio.gotoxy(0,0)
	y=len(array[0])-1
	x=len(array)-1
	print chr(218)+(chr(196)+chr(194))*x+chr(196)+chr(191)
	for i in range(y):
		WConio.gotoxy(0,i*2+2)
		print chr(195)+(chr(196)+chr(197))*x+chr(196)+chr(180)
	WConio.gotoxy(0,y*2+2)
	print chr(192)+(chr(196)+chr(193))*x+chr(196)+chr(217)	
	for i in range(y+1):
		for j in range (x+2):
			WConio.gotoxy(j*2,i*2+1)
			print chr(179)
		
def makeArray(size):
	WConio.clrscr()
	gameArray=None	
	gameArray=[[chr(250) for y in range(size[1])] for x in range(size[0])]
	printGrid(gameArray)
	printBoard(gameArray)
	return gameArray

def printCursor(gameArray,cursor):
	WConio.gotoxy(cursor[0]*2,cursor[1]*2)
	print chr(201)+chr(205)+chr(187)
	WConio.gotoxy(cursor[0]*2,cursor[1]*2+1)
	print chr(186)+gameArray[cursor[0]][cursor[1]]+chr(186)
	WConio.gotoxy(cursor[0]*2,cursor[1]*2+2)
	print chr(200)+chr(205)+chr(188)
	
def printCursor2(gameArray,cursor):
	WConio.gotoxy(cursor[0]*2,cursor[1]*2)
	print chr(201)+chr(205)+chr(187)
	WConio.gotoxy(cursor[0]*2,cursor[1]*2+1)
	print chr(186)+gameArray[cursor[0]][cursor[1]]+chr(186)
	WConio.gotoxy(cursor[0]*2,cursor[1]*2+2)
	print chr(200)+chr(205)+chr(188)	

def selectToken (gameArray,arrows,player):
	clearLines()
	cursor = [int(len(gameArray)/2),int(len(gameArray[0])/2)]
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
			WConio.gotoxy(cursor[0]*2+1,cursor[1]*2+1) 
			printGrid(gameArray) #'erase' cursor icon
			d=arrows[0].index(k)		
			cursor[0]=(cursor[0]+arrows[1][d])%len(gameArray)
			cursor[1]=(cursor[1]+arrows[2][d])%len(gameArray[0])
		printCursor(gameArray,cursor)

		if k == " ":# when 'spacebar' entered
			if ord(gameArray[cursor[0]][cursor[1]])<>player:
				WConio.gotoxy(0,24)
				print "Player {0}, you can only select a space that is already yours.".format(player)
			else:	
				clearLines()
				WConio.gotoxy(0,24)
				print "{0:^79}".format("Token selected.")
				print " "*79
				gameArray = selectDestination(gameArray,cursor,player,arrows)
			break		
	
def selectDestination(gameArray,cursor,player,arrows):
	k=None
	oldCursor = cursor[:]
	while k<>"q":
		k = WConio.getkey()
		if k in arrows[0]:
			#WConio.gotoxy(cursor[0]*2+1,cursor[1]*2+1) 
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
					WConio.gotoxy(0,24)
					print "Player {0}, you can only move to empty spaces".format(player)
				else:
					finalizeMove(gameArray,oldCursor,cursor,player)
					break
	return gameArray		

def finalizeMove(gameArray,oldCursor,cursor,player):
	clearLines()

	print "{0:^79}".format("Token cloned.")
	gameArray[cursor[0]][cursor[1]]=chr(player)
	if abs(cursor[0]-oldCursor[0])==2 or abs(cursor[1]-oldCursor[1])==2:
		gameArray[oldCursor[0]][oldCursor[1]]=chr(250)
		WConio.gotoxy(0,24)
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
	WConio.gotoxy(0,24)
	return gameArray
	
def printScore(gameArray,score):
	score=[0,0]
	for x in range(len(gameArray)):	
		for y in range(len(gameArray[0])):	
			if gameArray[x][y]==chr(1):
				score[0]+=1
			elif gameArray[x][y]==chr(2):
				score[1]+=1	
	WConio.gotoxy(60,0)
	print"You vs. CPU"
	WConio.gotoxy(60,1)
	print"===     ==="
	WConio.gotoxy(60,2)
	print"{0:^3}     {1:^3}".format(score[0],score[1])
	
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
	WConio.gotoxy(45,11)
	oldCursor=move[3][:]
	WConio.gotoxy(45,12)
	cursor=[move[1],move[2]]
	for i in range(5):
		time.sleep(.25)
		printGrid(gameArray)
		time.sleep(.25)
		printCursor(gameArray,oldCursor)
	for i in range(5):
		time.sleep(.25)
		printGrid(gameArray)
		printCursor(gameArray,oldCursor)
		time.sleep(.25)
		printCursor2(gameArray,cursor)	
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
								WConio.gotoxy(60,5)
								WConio.gotoxy(60,6)
						except:
							pass
	return None


# main, of sorts
#=====================================================================
	
#select board size
makeArray(size)
WConio.gotoxy(0,24)
print "{0:^79}".format("Hit the spacebar to accept this board.")	
while k<>" ":		
	k = WConio.getkey()
	if k in arrows[0]:
		d=arrows[0].index(k)
		size[0]=(size[0]+arrows[1][d]*2)
		size[1]=(size[1]+arrows[2][d]*2)
		if size[0]>15:
			size[0]=15
			comment = "That's as wide as you can go."
		elif size[0]<5:
			size[0]=5
			comment = "That's as narrow as you can go."
		elif size[1]>11:
			size[1]=11
			comment = "That's as tall as you can go."
		elif size[1]<5:
			size[1]=5
			comment = "That's as short as you can go."
		else:
			comment = ""
	gameArray=makeArray(size)
	WConio.gotoxy(0,24)
	print "{0:^79}".format(size,comment,"\nHit the spacebar to accept this board.")
clearLines()

#init pieces
gameArray[0][0]=chr(1)
gameArray[0][len(gameArray[0])-1]=chr(2)
gameArray[len(gameArray)-1][0]=chr(2)

	
gameArray[len(gameArray)-1][len(gameArray[0])-1]=chr(1)
printBoard(gameArray)

#main game loop
while score[0]+score[1]<len(gameArray)*len(gameArray[0]) and score[0]<>0 and score[1]<>0:
	if player == 1:
		selectToken(gameArray,arrows,player)
	if player == 2:
		compTurn(gameArray,player)
	player=player%2+1	
	score = printScore(gameArray,score)

	
print ""
