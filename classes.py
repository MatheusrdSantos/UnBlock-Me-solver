from utils import *
class Move:
	def __init__(self, last_pos = {}, new_pos = {}, block_id = -1):
		self.last_pos = last_pos
		self.new_pos = new_pos
		self.block_id = block_id
class Block:
	def __init__(self, id, x, y, isHorizontal, kind, length):
		self.id = id
		self.x = x
		self.y = y
		self.isHorizontal = isHorizontal
        # there are three kinds of blocks:
        # 0 -> empty space
        # 1 -> normal block
        # 2 -> prisioner block
		self.kind = kind
		self.length = length
class Table:
	def __init__(self, blocks, parent_move = Move(last_pos={'x': -1, 'y':-1}, block_id=-1, new_pos={'x':-1, 'y':-1}), moves = []):
		self.blocks = blocks
		self.parent_move = parent_move
        # for each new move create a new child table
		self.moves = moves
	def get_quad(self, x, y):
		for block in self.blocks:
			if self.point_belongs(x, y, block):
				return block
	def get_block_by_id(self, id):
		for block in self.blocks:
			if block.id == id:
				return block
	def point_belongs(self, x, y, block):
		if block.isHorizontal:
			if (y == block.y) and (x in range(block.x, block.x+block.length)):
				return True
			else:
				return False
		else:
			if (x == block.x) and (y in range(block.y, block.y+block.length)):
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
		if(move_1.block_id == move_2.block_id):
			if(move_1.last_pos['x'] == move_2.last_pos['x'] and move_1.last_pos['y'] == move_2.last_pos['y']):
				if(move_1.new_pos['x'] == move_2.new_pos['x'] and move_1.new_pos['y'] == move_2.new_pos['y']):
					return True
		return False
	def movesAreInverse(self, move_1, move_2):
		if(move_1.block_id == move_2.block_id):
			if(move_1.last_pos['x'] == move_2.new_pos['x'] and move_1.last_pos['y'] == move_2.new_pos['y']):
				if(move_1.new_pos['x'] == move_2.last_pos['x'] and move_1.new_pos['y'] == move_2.last_pos['y']):
					return True
		return False
	def findMove(self, new_move):
		for move in self.moves:
			if(self.movesAreEqual(move, new_move)):
				return  move
		return False
				
	def canMoveFowards(self, block):
		if(block.isHorizontal):
			new_move = Move(last_pos={'x':block.x, 'y':block.y}, block_id=block.id, new_pos={'x':block.x+1, 'y':block.y})
			if (self.findMove(new_move)):
				return False
			if(self.movesAreInverse(self.parent_move, new_move)):
				return False
			if(block.x+block.length<6 and self.get_quad(block.x+block.length, block.y).kind == 0):
				return True
		else:
			new_move = Move(last_pos={'x':block.x, 'y':block.y}, block_id=block.id, new_pos={'x':block.x, 'y':block.y+1})
			if (self.findMove(new_move)):
				return False
			if(self.movesAreInverse(self.parent_move, new_move)):
				return False
			if(block.y+block.length<6 and self.get_quad(block.x, block.y+block.length).kind == 0):
				return True
		return False
	def canMoveBackwards(self, block):
		if(block.isHorizontal):
			new_move = Move(last_pos={'x':block.x, 'y':block.y}, block_id=block.id, new_pos={'x':block.x-1, 'y':block.y})
			if (self.findMove(new_move)):
				return False
			if(self.movesAreInverse(self.parent_move, new_move)):
				return False
			if(block.x!=0 and self.get_quad(block.x-1, block.y).kind == 0):
				return True
		else:
			new_move = Move(last_pos={'x':block.x, 'y':block.y}, block_id=block.id, new_pos={'x':block.x, 'y':block.y-1})
			if (self.findMove(new_move)):
				return False
			if(self.movesAreInverse(self.parent_move, new_move)):
				return False
			if(block.y!=0 and self.get_quad(block.x, block.y-1).kind == 0):
				return True
		return False
	def getNewInstance(self):
		new_blocks = []
		for block in self.blocks:
			new_blocks.append(Block(block.id, block.x, block.y, block.isHorizontal, block.kind, block.length))
		new_tab = Table(blocks=new_blocks)
		new_tab.moves = []
		return new_tab
	def moveFowards(self, block):
		if(block.isHorizontal):
			new_tab = self.getNewInstance()
			new_tab.getFrontPiece(block).x = block.x
			new_tab.get_block_by_id(block.id).x+=1
			move = Move(block_id=block.id, new_pos={'x':block.x+1, 'y': block.y}, last_pos={'x':block.x, 'y':block.y})
			self.moves.append(move)
			new_tab.parent_move = move
			return new_tab
		else:
			new_tab = self.getNewInstance()
			new_tab.getFrontPiece(block).y = block.y
			new_tab.get_block_by_id(block.id).y+=1
			move = Move(block_id=block.id, new_pos={'x':block.x, 'y': block.y+1}, last_pos={'x':block.x, 'y':block.y})
			self.moves.append(move)
			new_tab.parent_move = move
			return new_tab
	def getBackPiece(self, block):
		if (block.isHorizontal):
			return self.get_quad(block.x-1, block.y)
		else:
			return self.get_quad(block.x, block.y-1)
	def getFrontPiece(self, block):
		if (block.isHorizontal):
			return self.get_quad(block.x+block.length, block.y)
		else:
			return self.get_quad(block.x, block.y+block.length)
	def moveBackwards(self, block):
		if(block.isHorizontal):
			new_tab = self.getNewInstance()
			new_tab.getBackPiece(block).x = block.x+block.length-1
			new_tab.get_block_by_id(block.id).x-=1
			move = Move(block_id=block.id, new_pos={'x':block.x-1, 'y': block.y}, last_pos={'x':block.x, 'y':block.y})
			self.moves.append(move)
			new_tab.parent_move = move
			return new_tab
		else:
			new_tab = self.getNewInstance()
			new_tab.getBackPiece(block).y = block.y+block.length-1
			new_tab.get_block_by_id(block.id).y-=1
			move = Move(block_id=block.id, new_pos={'x':block.x, 'y': block.y-1}, last_pos={'x':block.x, 'y':block.y})
			self.moves.append(move)
			new_tab.parent_move = move
			return new_tab
	def blockCanMove(self, block):
		count = 0
		for move in self.moves:
			if(move.block_id == block.id):
				count+=1
		if (count==2):
			return False
		else:
			if (self.canMoveFowards(block)):
				return self.moveFowards(block) 
			elif (self.canMoveBackwards(block)):
				return self.moveBackwards(block)
		return False

    # the child tab is created based on parent move and the other moves that create the other childs
    # this function returns a child (table)
	def getChild(self):
		for block in self.blocks:
			if(block.kind != 0):
				result = self.blockCanMove(block)
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
		for block in self.blocks:
			if block.kind == 2:
				return block
	def is_solved(self):
		prisioner = self.find_prisioner()
		if prisioner.x==4:
			return True
		for x in range(prisioner.x+prisioner.length, 6):
			if self.get_quad(x, 2).kind==1:
				return False
		return True