class Move:
	def __init__(self, x, y):
		self.x = x
		self.y = y
class Peca:
	def __init__(self, id, x, y, isHorizontal, kind, length, moved_backward=False, moved_foward=False):
		self.id = id
		self.x = x
		self.y = y
		self.isHorizontal = isHorizontal
		self.kind = kind
		self.length = length
		# move backward means to move left or up
		# move foward means to move right or down
		self.moved_backward = moved_backward
		self.moved_foward = moved_foward
class Tabuleiro:
	def __init__(self, pecas, parent_move = ['-', -1]):
		self.pecas = pecas
		#[id_peca, type_move(up or donw)]
		self.parent_move = parent_move
	def printTab(self):
		print("---------")
		for y in range(0, 6):
			for x in range(0,6):
				if x == 5:
					print(str(self.get_quad_id(x, y))+" | ", end='\n')
				else:
					print(str(self.get_quad_id(x, y))+" |", end=' ')
		print("---------")
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
	def get_quad_id(self, x, y):
		for peca in self.pecas:
			if self.point_belongs(x, y, peca):
				if peca.id>9:
					return peca.id
				else:
					return "0"+str(peca.id)
		return "--"
	def get_quad(self, x, y):
		for peca in self.pecas:
			if self.point_belongs(x, y, peca):
				return peca
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
	def print_pecas(self):
		for peca in pecas:
			print("--------------")
			print("id: " + str(peca.id))
			print("Peça x: " + str(peca.x))
			print("Peça y: " + str(peca.y))
			print("Peça size: " + str(peca.length))
			print("Peça kind: " + str(peca.kind))
			print("horizontal:" + str(peca.isHorizontal))
	def find_prisioner(self):
		for peca in self.pecas:
			if peca.kind == 2:
				return peca
	def is_Solved(self):
		prisioner = self.find_prisioner()
		if prisioner.x==4:
			return True
		for x in range(prisioner.x+prisioner.length, 6):
			if self.get_quad(x, 2).kind==1:
				return False
		return True
	def peca_can_move(self, peca):
		if peca.isHorizontal:
			#print("isH")
			if peca.x>0 and self.get_quad(peca.x-1, peca.y).kind==0 and not peca.moved_backward and (self.parent_move[0]!= peca.id or self.parent_move[1]!=1):
				#print("left")
				# move left
				return 1
			elif(peca.x+peca.length-1<5 and self.get_quad(peca.x+peca.length, peca.y).kind==0 and not peca.moved_foward) and (self.parent_move[0]!= peca.id or self.parent_move[1]!=2):
				#print("right")
				# move right
				return 2
		else:
			#print("isntH")
			#print("peca.moved_backward: "+ str(peca.moved_backward))
			#print("peca.moved_foward: "+ str(peca.moved_foward))

			if peca.y>0 and self.get_quad(peca.x, peca.y-1).kind==0 and not peca.moved_backward and (self.parent_move[0]!= peca.id or self.parent_move[1]!=3):
				#print("up")
				# move up
				return 3
			elif peca.y+peca.length-1<5 and self.get_quad(peca.x, peca.y+peca.length).kind==0 and not peca.moved_foward and (self.parent_move[0]!= peca.id or self.parent_move[1]!=4):
				#print("donw")
				# move donw
				return 4
		#print(str(peca.id)+" cant move")
		return False
	def update_peca_by_id(self, id, x, y):
		for peca in self.pecas:
			if peca.id == id:
				peca.x = x
				peca.y = y
				break
	def get_peca_by_id(self, id):
		for peca in self.pecas:
			if peca.id == id:
				return peca
	def create_new_pecas(self, pecas):
		pecas_new = []
		for peca in pecas:
			pecas_new.append(Peca(peca.id, peca.x, peca.y, peca.isHorizontal, peca.kind, peca.length, peca.moved_backward, peca.moved_foward))			
		return pecas_new
	def get_new_state(self):
		has_peca_to_move = False
		new_pecas = self.create_new_pecas(self.pecas)
		#print(new_pecas)
		#print(self.pecas)
		
		for peca in self.pecas:
			if peca.kind!=0:
				can_move = self.peca_can_move(peca)
				if can_move == 1:
					new_table = Tabuleiro(new_pecas, [peca.id, 1])
					# move empyt space
					new_table.update_peca_by_id(new_table.get_quad(peca.x-1, peca.y).id, peca.x+peca.length-1, peca.y)
					# move left
					new_table.update_peca_by_id(peca.id, peca.x-1, peca.y)
					# informa o estado anteriror da peça
					self.get_peca_by_id(peca.id).moved_backward = True
					has_peca_to_move = True
					break
				elif can_move == 2:
					new_table = Tabuleiro(new_pecas, [peca.id, 2])
					# move empyt space
					new_table.update_peca_by_id(new_table.get_quad(peca.x+peca.length, peca.y).id, peca.x, peca.y)
					# move right
					new_table.update_peca_by_id(peca.id, peca.x+1, peca.y)
					# informa o estado anterior da peça
					self.get_peca_by_id(peca.id).moved_foward = True
					has_peca_to_move = True
					break
				elif can_move == 3:
					new_table = Tabuleiro(new_pecas, [peca.id, 3])
					# move empyt space
					new_table.update_peca_by_id(new_table.get_quad(peca.x, peca.y-1).id, peca.x, peca.y+peca.length-1)
					# move up
					new_table.update_peca_by_id(peca.id, peca.x, peca.y-1)
					# informa o estado anterior da peça
					self.get_peca_by_id(peca.id).moved_backward = True
					has_peca_to_move = True
					break
				elif can_move == 4:
					new_table = Tabuleiro(new_pecas, [peca.id, 4])
					# move empyt space
					new_table.update_peca_by_id(new_table.get_quad(peca.x, peca.y+peca.length).id, peca.x, peca.y)
					# move down
					new_table.update_peca_by_id(peca.id, peca.x, peca.y+1)
					# informa o estado anterior da peça
					self.get_peca_by_id(peca.id).moved_foward = True
					has_peca_to_move = True
					break
		if not has_peca_to_move:
			return False
		return new_table
	def get_all_stages(self):
		all_stages = []
		while True:
			new_stage = self.get_new_state()
			#input()
			if new_stage==False:
				break
			new_stage.reset_moved()
			new_stage.printTabHuman()
			if new_stage.is_Solved():
				new_stage.printTabHuman()
				return True
			all_stages.append(new_stage)
		return all_stages
	def reset_moved(self):
		for peca in self.pecas:
			peca.moved_foward = False
			peca.moved_backward = False
def tab_are_equal(tab1, tab2):
	for x in range(0, len(tab1.pecas)):
		if tab1.pecas[x].x != tab2.pecas[x].x or tab1.pecas[x].y != tab2.pecas[x].y:
			return False
	return True
						
def tab_visited(tab_array, tab):
	for past_tab in tab_array:
		if tab_are_equal(past_tab, tab):
			return True
	return False

def tab_visited_array(tab_array, tab_array2):
	for past_tab in tab_array:
		for past_tab2 in tab_array2:
			if tab_are_equal(past_tab, past_tab2):
				return True
	return False

		

#letras = ['a', 'b', 'c', 'd', 'e', 'f']	
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
"""
initial_t = []
#lines = []
for x in range(0,6):
	lines = []
	for y in range(0,6):
		lines.append(input())
	initial_t.append(lines)

#print(initial_t)
"""
t = Tabuleiro(pecas)
#t.print_pecas()
#print(t.pecas[5].id)
#print(t.point_belongs(0, 1, t.pecas[5]))
t.printTabHuman()
print("tab inicial is solved: "+str(t.is_Solved()))
cont_natural = 0
cont_2 = 1
cont_node_stage = 0
nodes = []
nodes.append(t.get_all_stages())
found = False
while not found:
	for node in nodes[cont_node_stage]:
		new_nodes_from_depht = []
		new_nodes_from_tab = node.get_all_stages()
		print("cont interno: "+str(cont_2))
		cont_2+=1
		if new_nodes_from_tab is True:
			found == True
			break
		#print("length: "+ str(len(new_nodes_from_tab)))
		new_nodes_from_depht+=new_nodes_from_tab
	cont_2 = 0
	nodes.append(new_nodes_from_depht)
	cont_node_stage+=1
	print("stage: "+ str(cont_node_stage))
	input()
"""
while True:
	new_stage = nodes[cont_node_stage].get_new_state()
	if  new_stage == False:
		#nodes[cont_node_stage-1].printTabHuman()
		cont_node_stage+=1
		print("Node stage finished: " + str(cont_node_stage))
		continue
	#input()
	#print("isSolved: "+ str(new_stage.is_Solved()))
	new_stage.printTabHuman()

	if cont_node_stage==1000:
		new_stage.printTabHuman()
		break

	if new_stage.is_Solved():
		new_stage.printTabHuman()
		break
	cont_2+=1
	if tab_visited(nodes, new_stage):
		print("Achou tab visited")
		continue
	nodes.append(new_stage)
"""
"""
print(t.is_Solved())
print("--- node 1 -------")
t.get_new_state().printTab()
#t.printTab()
print("--- node 2 -------")
t.get_new_state().printTab()
print("--- node 3 -------")
t.get_new_state().printTab()
print("--- node 4 -------")
t.get_new_state().printTab()
print("--- node 5 -------")
t.get_new_state().printTab()
print("--- node 6 -------")
t.get_new_state().printTab()

print("---- original ----")
t.printTab()
"""