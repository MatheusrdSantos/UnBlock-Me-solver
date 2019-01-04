from classes import *
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
			print("antes: "+str(len(childs)))
			childs = removeRepeatedTabs(childs)
			print("depois: "+str(len(childs)))
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