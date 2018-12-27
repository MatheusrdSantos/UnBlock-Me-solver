def tabs_are_equal(tab1, tab2):
	for x in range(0, len(tab1.pieces)):
		if(tab1.pieces[x].kind == 0 and tab2.pieces[x].kind == 0):
			continue
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
	print("n_tabs: "+str(len(tabs)))
	for count, tab in enumerate(tabs, start=0):
		tabs = removeEqualTabs(tab, tabs, count)
	print("left_tabls: "+str(len(tabs)))
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




	
    