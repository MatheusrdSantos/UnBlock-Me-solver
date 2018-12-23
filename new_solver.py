class Move:
	def __init__(self, last_pos = {}, new_pos = {}, piece_id = -1):
		self.last_pos = last_pos
		self.new_pos = new_pos
		self.piece_id = piece_id
class Peca:
	def __init__(self, id, x, y, isHorizontal, kind, length):
		self.id = id
		self.x = x
		self.y = y
		self.isHorizontal = isHorizontal
        # there are three kinds of pieces:
        # 0 -> empty space
        # 1 -> normal piece
        # 2 -> prisioner piece
		self.kind = kind
		self.length = length
class Table:
	def __init__(self, pieces, parent_move = Move(last_pos={'x': -1, 'y':-1}, piece_id=-1, new_pos={'x':-1, 'y':-1}), moves = []):
		self.pieces = pieces
		#[id_piece, type_move(up or donw)]
		self.parent_move = parent_move
        # for each new move create a new child table
		self.moves = moves
	def get_quad(self, x, y):
		for peca in self.pieces:
			if self.point_belongs(x, y, peca):
				return peca
	def get_piece_by_id(self, id):
		for piece in self.pieces:
			if piece.id == id:
				return piece
	def point_belongs(self, x, y, peca):
		#print("x:"+str(x)+" | y:"+ str(y))
		#print("peca.x+length:"+str(peca.x+peca.length))
		if peca.isHorizontal:
			if (y == peca.y) and (x in range(peca.x, peca.x+peca.length)):
				return True
			else:
				return False
		else:
			if (x == peca.x) and (y in range(peca.y, peca.y+peca.length)):
				return True
			else:
				return False
	def printTabHuman(self):
		print("---------")
		for y in range(0, 6):
			for x in range(0,6):
				quad = self.get_quad(x, y) 
				if(quad.kind == 0):
					if x==5:
						print(" "+" |", end='\n')
					else:
						print(" "+" |", end=' ')
				elif(quad.kind == 1):
					if quad.isHorizontal:
						if x == 5:
							print("-"+" |", end='\n')
						else:
							print("-"+" |", end=' ')
					else:
						if x == 5:
							print("I"+" |", end='\n')
						else:
							print("I"+" |", end=' ')
				elif(quad.kind == 2):
					if x == 5:
						print("x"+" |", end='\n')
					else:
						print("x"+" |", end=' ')
		print("---------")
	def movesAreEqual(self, move_1, move_2):
		if(move_1.piece_id == move_2.piece_id):
			if(move_1.last_pos['x'] == move_2.last_pos['x'] and move_1.last_pos['y'] == move_2.last_pos['y']):
				if(move_1.new_pos['x'] == move_2.new_pos['x'] and move_1.new_pos['y'] == move_2.new_pos['y']):
					return True
		return False
	def movesAreInverse(self, move_1, move_2):
		if(move_1.piece_id == move_2.piece_id):
			if(move_1.last_pos['x'] == move_2.new_pos['x'] and move_1.last_pos['y'] == move_2.new_pos['y']):
				if(move_1.new_pos['x'] == move_2.last_pos['x'] and move_1.new_pos['y'] == move_2.last_pos['y']):
					return True
		return False
	def findMove(self, new_move):
		for move in self.moves:
			if(self.movesAreEqual(move, new_move)):
				return  move
		return False
				
	def canMoveFowards(self, piece):
		if(piece.isHorizontal):
			new_move = Move(last_pos={'x':piece.x, 'y':piece.y}, piece_id=piece.id, new_pos={'x':piece.x+1, 'y':piece.y})
			if (self.findMove(new_move)):
				return False
			if(self.movesAreInverse(self.parent_move, new_move)):
				return False
			if(piece.x+piece.length<6 and self.get_quad(piece.x+piece.length, piece.y).kind == 0):
				return True
		else:
			new_move = Move(last_pos={'x':piece.x, 'y':piece.y}, piece_id=piece.id, new_pos={'x':piece.x, 'y':piece.y+1})
			if (self.findMove(new_move)):
				return False
			if(self.movesAreInverse(self.parent_move, new_move)):
				return False
			if(piece.y+piece.length<6 and self.get_quad(piece.x, piece.y+piece.length).kind == 0):
				return True
		return False
	def canMoveBackwards(self, piece):
		if(piece.isHorizontal):
			new_move = Move(last_pos={'x':piece.x, 'y':piece.y}, piece_id=piece.id, new_pos={'x':piece.x-1, 'y':piece.y})
			if (self.findMove(new_move)):
				return False
			if(self.movesAreInverse(self.parent_move, new_move)):
				return False
			if(piece.x!=0 and self.get_quad(piece.x-1, piece.y).kind == 0):
				return True
		else:
			new_move = Move(last_pos={'x':piece.x, 'y':piece.y}, piece_id=piece.id, new_pos={'x':piece.x, 'y':piece.y-1})
			if (self.findMove(new_move)):
				return False
			if(self.movesAreInverse(self.parent_move, new_move)):
				return False
			if(piece.y!=0 and self.get_quad(piece.x, piece.y-1).kind == 0):
				return True
		return False
	def getNewInstance(self):
		new_pieces = []
		for piece in self.pieces:
			new_pieces.append(Peca(piece.id, piece.x, piece.y, piece.isHorizontal, piece.kind, piece.length))
		new_tab = Table(pieces=new_pieces)
		new_tab.moves = []
		return new_tab
	def moveFowards(self, piece):
		if(piece.isHorizontal):
			new_tab = self.getNewInstance()
			new_tab.getFrontPiece(piece).x = piece.x
			new_tab.get_piece_by_id(piece.id).x+=1
			move = Move(piece_id=piece.id, new_pos={'x':piece.x+1, 'y': piece.y}, last_pos={'x':piece.x, 'y':piece.y})
			self.moves.append(move)
			new_tab.parent_move = move
			return new_tab
		else:
			new_tab = self.getNewInstance()
			new_tab.getFrontPiece(piece).y = piece.y
			new_tab.get_piece_by_id(piece.id).y+=1
			move = Move(piece_id=piece.id, new_pos={'x':piece.x, 'y': piece.y+1}, last_pos={'x':piece.x, 'y':piece.y})
			self.moves.append(move)
			new_tab.parent_move = move
			return new_tab
	def getBackPiece(self, piece):
		if (piece.isHorizontal):
			return self.get_quad(piece.x-1, piece.y)
		else:
			return self.get_quad(piece.x, piece.y-1)
	def getFrontPiece(self, piece):
		if (piece.isHorizontal):
			return self.get_quad(piece.x+piece.length, piece.y)
		else:
			return self.get_quad(piece.x, piece.y+piece.length)
	def moveBackwards(self, piece):
		if(piece.isHorizontal):
			new_tab = self.getNewInstance()
			new_tab.getBackPiece(piece).x = piece.x+piece.length-1
			new_tab.get_piece_by_id(piece.id).x-=1
			move = Move(piece_id=piece.id, new_pos={'x':piece.x-1, 'y': piece.y}, last_pos={'x':piece.x, 'y':piece.y})
			self.moves.append(move)
			new_tab.parent_move = move
			return new_tab
		else:
			new_tab = self.getNewInstance()
			new_tab.getBackPiece(piece).y = piece.y+piece.length-1
			new_tab.get_piece_by_id(piece.id).y-=1
			move = Move(piece_id=piece.id, new_pos={'x':piece.x, 'y': piece.y-1}, last_pos={'x':piece.x, 'y':piece.y})
			self.moves.append(move)
			new_tab.parent_move = move
			return new_tab
	def pieceCanMove(self, piece):
		count = 0
		for move in self.moves:
			if(move.piece_id == piece.id):
				count+=1
		if (count==2):
			#print("primeiro")
			return False
		else:
			if (self.canMoveFowards(piece)):
				return self.moveFowards(piece) 
			elif (self.canMoveBackwards(piece)):
				return self.moveBackwards(piece)
		#print("segundo")
		return False

    # the child tab is created based on parent move and the other moves that create the other childs
    # this function returns a child (table)
	def getChild(self):
		for piece in self.pieces:
			if(piece.kind != 0):
				result = self.pieceCanMove(piece)
				if(result):
					return result
		return False
    #this function returns an array with all childs (tables)
	def getAllChilds(self):
		childs = []
		#print('-----parent----')
		#self.printTabHuman()
		#print(self.moves)
		#print('-----parent----')
		while True:
			child = self.getChild()
			if not child:
				break
			#input()
			#child.printTabHuman()
			childs.append(child)
		return childs
	def find_prisioner(self):
		for piece in self.pieces:
			if piece.kind == 2:
				return piece
	def is_solved(self):
		prisioner = self.find_prisioner()
		if prisioner.x==4:
			return True
		for x in range(prisioner.x+prisioner.length, 6):
			if self.get_quad(x, 2).kind==1:
				return False
		return True
def tabs_are_equal(tab1, tab2):
	for x in range(0, len(tab1.pieces)):
		if tab1.pieces[x].x != tab2.pieces[x].x or tab1.pieces[x].y != tab2.pieces[x].y:
			return False
	return True
def hasSolvedTab(tabs):
	for index, tab in enumerate(tabs, start=0):
		if tab.is_solved():
			return [tab, index]
	return False
def removeEqualTabs(tab, tabs, count):
	for index, current_tab in enumerate(tabs, start=0):
		if(index==count):
			continue
		if(tabs_are_equal(current_tab, tab)):
			tabs.pop(index)
	return tabs
		
def removeRepeatedTabs(tabs):
	for count, tab in enumerate(tabs, start=0):
		tabs = removeEqualTabs(tab, tabs, count)
	return tabs

def tabIsInArray(tabs, tab):
	for current_tab in tabs:
		if(tabs_are_equal(current_tab, tab)):
			return True
	return False
def isParent(parent, child):
	#parent.printTabHuman()
	for piece in parent.pieces:
		if(piece.kind == 0):
			continue
		child_peace = child.get_piece_by_id(piece.id)
		#print(str(piece.id) + " - " +str(child.parent_move.piece_id))
		if piece.id == child.parent_move.piece_id:
			#compara as peças com o move invertido
			#print('achou')
			if piece.x != child.parent_move.last_pos['x'] or piece.y != child.parent_move.last_pos['y']:
				return False
		else:
			#print("segundo if (1): " + str(piece.x) + "-"+ str(piece.y))
			#print("segundo if (2): " + str(child_peace.x) + "-"+ str(child_peace.y))
			if piece.x != child_peace.x or piece.y != child_peace.y:
				return False
	return True
def getParentTab(tabs, child):
	for tab in tabs:
		if(isParent(tab , child)):
			return tab
			
cont = 0
pecas = []
while (True):
	print("1 - Inseri  uma nova peça;")
	print("2 - finalizar;")
	command = int(input())
	if command == 2:
		break
	print("Digite as coordenada x, y:")
	x, y = input().split()
	x = int(x)
	y = int(y)
	print("É horizontal?")
	isHorizontal = bool(int(input()))
	print("Qual o tipo? 0 - vazio / 1 - bloco / 2 - prisioneiro")
	kind = int(input())
	print("Qual o tamanho?")
	length = int(input())

	peca = Peca(cont, x, y, isHorizontal, kind, length)
	pecas.append(peca)
	cont+=1

t = Table(pecas)
t.printTabHuman()

tree = [[t]]
solved = False
cont = 0
while not solved:
	cont+=1
	print(cont)
	actual_depth = tree[-1]
	childs = []
	print(len(actual_depth))
	for tab in actual_depth:
		new_childs = tab.getAllChilds()
		solved_tab_result = hasSolvedTab(new_childs)
		if(solved_tab_result):
			solved_tab = solved_tab_result[0]
			solved_tab.printTabHuman()
			solved = True
			solved_tab_index = solved_tab_result[1]
			break
		childs+=new_childs
	#tree.clear()
	if(not solved):
		childs = removeRepeatedTabs(childs)
		tree.append(childs)

print("RESOLVIDO")
print(len(tree))
actual_tab = solved_tab
for x in range(len(tree)-1, -1, -1):
	print(x)
	actual_tab = getParentTab(tree[x], actual_tab)	
	actual_tab.printTabHuman()
#tree[cont][solved_tab_index].printTabHuman()
#for child_table in t.getAllChilds():
	#child_table.printTabHuman()