from classes import *
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

# UI implementation
def fullfillTable(blocks):
	tab = Table(blocks)
	for y in range(0, 6):
		for x in range(0, 6):
			if(not tab.get_quad(x, y)):
				tab.pieces.append(Peca(len(blocks)+1, x, y, 1, 0, 1))
	return tab
def getSolution(t):
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
	solution_tree = []
	solution_tree.append(solved_tab)
	actual_tab = solved_tab
	for x in range(len(tree)-1, -1, -1):
		print(x)
		actual_tab = getParentTab(tree[x], actual_tab)
		solution_tree.append(actual_tab)
		actual_tab.printTabHuman()
	solution_tree.reverse()
	return solution_tree


	
    