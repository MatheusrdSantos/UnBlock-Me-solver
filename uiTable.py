from tkinter import *
from solver import * 
from PIL import ImageTk
from table_builder import *
import time
import sys
import os

root = Tk()

# declare global variables
global_elementsBlocks = []
global_table_positions = []
global_actual_table_index = IntVar()
global_solution_tree = []
global_blocks = []


leftFrame = Frame(root, bg='#ABABAB')
leftFrame.pack(side=LEFT, fill=BOTH, expand=True)
rightFrame = Frame(root)
rightFrame.pack(side=RIGHT, expand=True, fill=BOTH)


tableFrame = Frame(leftFrame)

# build your table here

for y in range(0, 6):
    for x in range(0, 6):
        global_table_positions.append(Label(tableFrame, text='('+str(x)+', '+str(y)+')', bg="gray", borderwidth=1, relief="solid"))
        global_table_positions[-1].grid(row=y, column=x, sticky=(N, S, E, W))
    tableFrame.columnconfigure(y, weight=1)
tableFrame.rowconfigure(1, weight=1)
tableFrame.pack(expand=True, fill=X)


tableNavigatorFrame = Frame(leftFrame)

# build table navigator here

button_previous = Button(tableNavigatorFrame, text="Previous", fg="red")
button_previous.grid()
navigatorLabel = Label(tableNavigatorFrame, text="0/0", bg="gray")
navigatorLabel.grid(row=0, column=1)
button_next = Button(tableNavigatorFrame, text="Next", fg="green")
button_next.grid(row=0, column=2)

tableNavigatorFrame.columnconfigure(0, weight=1)
tableNavigatorFrame.columnconfigure(1, weight=1)
tableNavigatorFrame.columnconfigure(2, weight=1)
tableNavigatorFrame.rowconfigure(0, weight=1)

tableNavigatorFrame.pack(expand=True, fill=X)


tableSolverFrame = Frame(leftFrame)

# build solve button here

button_solve = Button(tableSolverFrame, text="SOLVE ME", fg="green")
button_solve.pack(fill=X)

tableSolverFrame.pack(expand=True, fill=X)

imagesFrame = Frame(rightFrame)   

images_label = Label(imagesFrame, text="List of table images: ")
images_label.pack()

imagesFrame.pack()

blocksControllerFrame = Frame(rightFrame)

# add and remove blocks here

label_x = Label(blocksControllerFrame, text="x: ")
label_x.grid(row=1, column=0)
entry_x = Entry(blocksControllerFrame)
entry_x.grid(row=1, column=1)
label_y = Label(blocksControllerFrame, text="y: ")
label_y.grid(row=1, column=2)
entry_y = Entry(blocksControllerFrame)
entry_y.grid(row=1, column=3)

label_size = Label(blocksControllerFrame, text="size: ")
label_size.grid(row=2, column=0)
entry_size = Entry(blocksControllerFrame)
entry_size.grid(row=2, column=1)

h = IntVar()
h.set(0)
Label(blocksControllerFrame, text="Is Horizontal?").grid(row=2, column=2)
Radiobutton(blocksControllerFrame, text="yes", variable=h, value=1).grid(row = 2, column=3)
Radiobutton(blocksControllerFrame, text="no", variable=h, value=0).grid(row = 2, column=4)

#radio buttons
kinds = [("Block", 1),("Prisioner", 2)]

v = IntVar()
v.set(0)
cont = 0
for text, mode in kinds:
    b = Radiobutton(blocksControllerFrame, text=text,
                    variable=v, value=mode)
    b.grid(row = cont+3)
    cont+=1

button_addBlock = Button(blocksControllerFrame, text="add Block")
button_addBlock.grid(columnspan=4)

blocksControllerFrame.pack(expand=True, fill=X)


blockListFrame = Frame(rightFrame)

# list all blocks here

blockListFrame.columnconfigure(0, weight=1)
blockListFrame.columnconfigure(1, weight=1)
blockListFrame.columnconfigure(2, weight=1)
blockListFrame.columnconfigure(3, weight=1)
blockListFrame.columnconfigure(4, weight=1)
blockListFrame.columnconfigure(5, weight=1)
blockListFrame.columnconfigure(6, weight=1)
blockListFrame.rowconfigure(0, weight=1)


blockListFrame.pack(expand=True, fill=X)

# UI implementation
def fullfillTable(blocks):
	tab = Table(blocks)
	for y in range(0, 6):
		for x in range(0, 6):
			if(not tab.get_quad(x, y)):
				tab.pieces.append(Peca(len(blocks)+1, x, y, 1, 0, 1))
	return tab

def resetTable():
    for y in range(0, 6):
        for x in range(0, 6):
            global_table_positions[(6*y)+x].configure(text='('+str(x)+', '+str(y)+')', bg="#674519", borderwidth=1, relief="solid")
def updateTableForSolution(block):
    block_index = (6*block.y)+block.x
    if block.kind==1:
        color = "orange"
    else:
        color = "red"
    global_table_positions[block_index].configure(text=block.id, bg=color, borderwidth=2, relief="solid")
    if(block.isHorizontal):
        for x in range(block_index+1, block_index+block.length):
            global_table_positions[x].configure(text=block.id, bg=color, borderwidth=2, relief="solid")
    else:
        for x in range(block_index, block_index+block.length*6, 6):
            global_table_positions[x].configure(text=block.id, bg=color, borderwidth=2, relief="solid")

def displayTableFromIndex():
    resetTable()
    for block in global_solution_tree[global_actual_table_index.get()].pieces:
        if(block.kind):
            updateTableForSolution(block)
            navigatorLabel.configure(bg="gray", text=str(global_actual_table_index.get())+" / "+ str(len(global_solution_tree)-1))
def displayNextTable():
    global_actual_table_index.set(global_actual_table_index.get()+1)
    displayTableFromIndex()

def displayNextTableDelay():
    global_actual_table_index.set(global_actual_table_index.get()+1)
    displayTableFromIndex()
    if(global_actual_table_index.get()<len(global_solution_tree)-1):
        root.after(1500, displayNextTableDelay)

def displayPreviousTable():
    global_actual_table_index.set(global_actual_table_index.get()-1)
    displayTableFromIndex()

def removeBlock(params):
    print (params[0], params[1])
    x = params[0]
    y = params[1]
    elements = params[2]
    current_block = None
    for block in global_blocks:
        if block.x == x and block.y == y:
            current_block = block
            global_blocks.remove(block)
            break
    block_index = (6*y)+x
    global_table_positions[block_index].configure(text='('+str(block_index-int(block_index/6)*6)+', '+str(int(block_index/6))+')', bg="gray", borderwidth=1, relief="solid")
    if(current_block.isHorizontal):
        for x in range(block_index+1, block_index+current_block.length):
            global_table_positions[x].configure(text='('+str(x-int(x/6)*6)+', '+str(int(x/6))+')', bg="gray", borderwidth=1, relief="solid")
    else:
        for x in range(block_index, block_index+current_block.length*6, 6):
            global_table_positions[x].configure(text='('+str(x-int(x/6)*6)+', '+str(int(x/6))+')', bg="gray", borderwidth=1, relief="solid")
    for element in elements:
        element.destroy()
def removeAllBlocks():
    for block in global_blocks:
        current_block = block
        global_blocks.remove(block)

def updateTable():
    last_block = global_blocks[-1]
    block_index = (6*last_block.y)+last_block.x
    if last_block.kind==1:
        color = "orange"
    else:
        color = "red"
    global_table_positions[block_index].configure(text=last_block.id, bg=color, borderwidth=2, relief="solid")
    if(last_block.isHorizontal):
        for x in range(block_index+1, block_index+last_block.length):
            global_table_positions[x].configure(text=last_block.id, bg=color, borderwidth=2, relief="solid")
    else:
        for x in range(block_index, block_index+last_block.length*6, 6):
            global_table_positions[x].configure(text=last_block.id, bg=color, borderwidth=2, relief="solid")

def updateBlockList():
    new_blockName = Label(blockListFrame, text="Block_"+str(global_blocks[-1].id))
    new_blockName.grid(row=len(global_blocks), sticky=(N, S, E, W))
    new_block_x = Label(blockListFrame, text=str(global_blocks[-1].x))
    new_block_x.grid(row=len(global_blocks), column = 1, sticky=(N, S, E, W))
    new_block_y = Label(blockListFrame, text=str(global_blocks[-1].y))
    new_block_y.grid(row=len(global_blocks), column = 2, sticky=(N, S, E, W))
    new_block_size = Label(blockListFrame, text=str(global_blocks[-1].length))
    new_block_size.grid(row=len(global_blocks), column = 3, sticky=(N, S, E, W))
    new_block_kind = Label(blockListFrame, text=str(global_blocks[-1].kind))
    new_block_kind.grid(row=len(global_blocks), column = 4,sticky=(N, S, E, W))
    elements = [new_blockName, new_block_x, new_block_y, new_block_size, new_block_kind]
    button_remove = Button(blockListFrame, text="del", bg="red")
    elements = [new_blockName, new_block_x, new_block_y, new_block_size, new_block_kind, button_remove]
    button_remove.configure(command=lambda params = [global_blocks[-1].x, global_blocks[-1].y, elements]: removeBlock(params))
    button_remove.grid(row=len(global_blocks), column = 5, sticky=(N, S, E, W))
    global_elementsBlocks.append(elements) 
    updateTable()

def addBlock():
    block_x_value = int(entry_x.get())
    block_y_value = int(entry_y.get())
    block_size_value = int(entry_size.get())
    block_isHorizontal_value = h.get()
    block_kind_value = v.get()
    global_blocks.append(Peca(len(global_blocks), block_x_value, block_y_value, block_isHorizontal_value, block_kind_value, block_size_value))
    print(len(global_blocks))
    updateBlockList()

def addBlockFromImage(block):
    global_blocks.append(block)
    print(len(global_blocks))
    updateBlockList()

def solve():
    full_blocks = []
    full_blocks+=global_blocks
    tab = fullfillTable(full_blocks)
    full_blocks = tab.pieces
    tab.printTabHuman()
    solution = getSolution(tab)
    for tree_tab in solution:
        global_solution_tree.append(tree_tab)
    navigatorLabel.configure(bg="gray", text=str(global_actual_table_index.get())+" / "+ str(len(global_solution_tree)))
    displayNextTableDelay()

def showTable(image):
    resetTable()
    global_blocks.clear()
    global_actual_table_index.set(0)
    global_solution_tree.clear()
    for line in global_elementsBlocks:
        for element in line:
            element.destroy()
    removeAllBlocks()
    pre_table = openImage(image)
    table = blocksInfoToTable(pre_table)
    for block in table.pieces:
        if(block.kind==0):
            continue
        addBlockFromImage(block)
    table.printTabHuman()

source = "tables/"
images = os.listdir(source)
imagesButton = []

for image in images:
    listTabButton = Button(imagesFrame, text=image)
    listTabButton.configure(command=lambda params = source+image: showTable(params))
    listTabButton.pack()
    imagesButton.append(listTabButton) 

button_addBlock.configure(command=addBlock)
button_solve.configure(command=solve)
button_next.configure(command=displayNextTable)
button_previous.configure(command=displayPreviousTable)

def run():
    root.geometry("1440x810")
    root.mainloop()
