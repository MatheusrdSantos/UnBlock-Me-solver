from classes import *
from utils import *
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