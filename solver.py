from classes import *
def getSolution(t):
	tree = [[t]]
	solved = False
	cont = 0
	while not solved:
		cont+=1
		print("Moves: "+str(cont))
		actual_depth = tree[-1]
		childs = []
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
		if(not solved):
			childs = removeRepeatedTabs(childs)
			tree.append(childs)

	print("---- SOLVED! ----")
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