from utils import *
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
			return False
		else:
			if (self.canMoveFowards(piece)):
				return self.moveFowards(piece) 
			elif (self.canMoveBackwards(piece)):
				return self.moveBackwards(piece)
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
		while True:
			child = self.getChild()
			if not child:
				break
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