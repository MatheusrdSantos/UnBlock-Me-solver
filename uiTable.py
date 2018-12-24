from tkinter import *
from classes import *
from utils import *

root = Tk()
leftFrame = Frame(root, bg="green")
leftFrame.pack(side=LEFT, fill=BOTH, expand=True)
rightFrame = Frame(root)
rightFrame.pack(side=RIGHT, expand=True, fill=BOTH)

#button1 = Button(leftFrame, text="Button 1", fg="red")
#button1.pack()

#button2 = Button(leftFrame, text="Button 2", fg="green")
#button2.pack()

#button3 = Button(rightFrame, text="Button 3", fg="blue")
#button3.pack()

tableFrame = Frame(leftFrame, bg="yellow")

# build your table here
#tableLabel = Label(tableFrame, text="table", bg="red")
#tableLabel.pack(fill=X)
table_positions = []
actual_table_index = IntVar()
solution_tree = []
for y in range(0, 6):
    for x in range(0, 6):
        #table_positions.append(Label(tableFrame, text='('+str(x)+', '+str(y)+')', bg="blue"))
        table_positions.append(Label(tableFrame, text='('+str(x)+', '+str(y)+')', bg="gray", borderwidth=1, relief="solid"))
        table_positions[-1].grid(row=y, column=x, sticky=(N, S, E, W))
    tableFrame.columnconfigure(y, weight=1)
tableFrame.rowconfigure(1, weight=1)
tableFrame.pack(expand=True, fill=X)


tableNavigatorFrame = Frame(leftFrame)

# build table navigator here
#navigatorLabel = Label(tableNavigatorFrame, text="nevigator", bg="gray")
#navigatorLabel.pack(fill=X)
button_previous = Button(tableNavigatorFrame, text="Previous", fg="red")
button_previous.pack(side=LEFT)

button_next = Button(tableNavigatorFrame, text="Next", fg="green")
button_next.pack(side=RIGHT)


tableNavigatorFrame.pack(expand=True, fill=X)


tableSolverFrame = Frame(leftFrame)

# build solve button here
#solverLabel = Label(tableSolverFrame, text="solve me!", bg="pink")
#solverLabel.pack(fill=X)
button_solve = Button(tableSolverFrame, text="SOLVE ME", fg="green")
button_solve.pack(fill=X)

tableSolverFrame.pack(expand=True, fill=X)


blocksControllerFrame = Frame(rightFrame)

# add and remove blocks here
#blocksControllerLabel = Label(blocksControllerFrame, text="controll blocks!", bg="orange")
#blocksControllerLabel.pack(fill=X)

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

#label_isHorizontal = Label(blocksControllerFrame, text="Is Horizontal? ")
#label_isHorizontal.grid(row=2, column=2)
#entry_isHorizontal = Entry(blocksControllerFrame)
#entry_isHorizontal.grid(row=2, column=3)

h = IntVar()
h.set(0)
Label(blocksControllerFrame, text="Is Horizontal?").grid(row=2, column=2)
Radiobutton(blocksControllerFrame, text="yes", variable=h, value=1).grid(row = 2, column=3)
Radiobutton(blocksControllerFrame, text="no", variable=h, value=0).grid(row = 2, column=4)

#radio buttons
kindes = [("Block", 1),("Prisioner", 2)]

v = IntVar()
v.set(0) # initialize
cont = 0
for text, mode in kindes:
    b = Radiobutton(blocksControllerFrame, text=text,
                    variable=v, value=mode)
    b.grid(row = cont+3)
    cont+=1
blocks = []
button_addBlock = Button(blocksControllerFrame, text="add Block")
#button_addBlock.configure(command=addBlock)
button_addBlock.grid(columnspan=4)

blocksControllerFrame.pack(expand=True, fill=X)


blockListFrame = Frame(rightFrame)

# list all blocks here
#blockListLabel = Label(blockListFrame, text="list blocks!", bg="purple")
#blockListLabel.pack(fill=X)
blockName = Label(blockListFrame, text="Block_1")
blockName.grid(row=0, sticky=(N, S, E, W))
block_x = Label(blockListFrame, text="0")
block_x.grid(row=0, column = 1, sticky=(N, S, E, W))
block_y = Label(blockListFrame, text="1")
block_y.grid(row=0, column = 2, sticky=(N, S, E, W))
block_size = Label(blockListFrame, text="3")
block_size.grid(row=0, column = 3, sticky=(N, S, E, W))
block_kind = Label(blockListFrame, text="block")
block_kind.grid(row=0, column = 4,sticky=(N, S, E, W))


button_remove = Button(blockListFrame, text="del", bg="red")
button_remove.grid(row=0, column = 5, sticky=(N, S, E, W))
scrollbar = Scrollbar(blockListFrame)
scrollbar.grid(row=0, column=6)


blockListFrame.columnconfigure(0, weight=1)
blockListFrame.columnconfigure(1, weight=1)
blockListFrame.columnconfigure(2, weight=1)
blockListFrame.columnconfigure(3, weight=1)
blockListFrame.columnconfigure(4, weight=1)
blockListFrame.columnconfigure(5, weight=1)
blockListFrame.columnconfigure(6, weight=1)
blockListFrame.rowconfigure(0, weight=1)


blockListFrame.pack(expand=True, fill=X)
def resetTable():
    for y in range(0, 6):
        for x in range(0, 6):
            table_positions[(6*y)+x].configure(text='('+str(x)+', '+str(y)+')', bg="gray", borderwidth=1, relief="solid")
def updateTableForSolution(block):
    block_index = (6*block.y)+block.x
    if block.kind==1:
        color = "orange"
    else:
        color = "red"
    table_positions[block_index].configure(text=block.id, bg=color, borderwidth=2, relief="solid")
    if(block.isHorizontal):
        for x in range(block_index+1, block_index+block.length):
            table_positions[x].configure(text=block.id, bg=color, borderwidth=2, relief="solid")
    else:
        for x in range(block_index, block_index+block.length*6, 6):
            table_positions[x].configure(text=block.id, bg=color, borderwidth=2, relief="solid")

def displayTableFromIndex():
    resetTable()
    for block in solution_tree[actual_table_index.get()].pieces:
        if(block.kind):
            updateTableForSolution(block)

def displayNextTable():
    actual_table_index.set(actual_table_index.get()+1)
    displayTableFromIndex()

def displayPreviousTable():
    actual_table_index.set(actual_table_index.get()-1)
    displayTableFromIndex()

def removeBlock(x, y, elements):
    current_block = None
    for block in blocks:
        if block.x == x and block.y == y:
            current_block = block
            blocks.remove(block)
            break
    block_index = (6*y)+x
    table_positions[block_index].configure(text=" ", bg="gray", borderwidth=1, relief="solid")
    if(current_block.isHorizontal):
        for x in range(block_index+1, block_index+current_block.length):
            table_positions[x].configure(text=" ", bg="gray", borderwidth=1, relief="solid")
    else:
        for x in range(block_index, block_index+current_block.length*6, 6):
            table_positions[x].configure(text=" ", bg="gray", borderwidth=1, relief="solid")
    for element in elements:
        element.destroy()

def updateTable():
    last_block = blocks[-1]
    block_index = (6*last_block.y)+last_block.x
    if last_block.kind==1:
        color = "orange"
    else:
        color = "red"
    table_positions[block_index].configure(text=last_block.id, bg=color, borderwidth=2, relief="solid")
    if(last_block.isHorizontal):
        for x in range(block_index+1, block_index+last_block.length):
            table_positions[x].configure(text=last_block.id, bg=color, borderwidth=2, relief="solid")
    else:
        for x in range(block_index, block_index+last_block.length*6, 6):
            table_positions[x].configure(text=last_block.id, bg=color, borderwidth=2, relief="solid")

def updateBlockList():
    new_blockName = Label(blockListFrame, text="Block_"+str(blocks[-1].id))
    new_blockName.grid(row=len(blocks), sticky=(N, S, E, W))
    new_block_x = Label(blockListFrame, text=str(blocks[-1].x))
    new_block_x.grid(row=len(blocks), column = 1, sticky=(N, S, E, W))
    new_block_y = Label(blockListFrame, text=str(blocks[-1].y))
    new_block_y.grid(row=len(blocks), column = 2, sticky=(N, S, E, W))
    new_block_size = Label(blockListFrame, text=str(blocks[-1].length))
    new_block_size.grid(row=len(blocks), column = 3, sticky=(N, S, E, W))
    new_block_kind = Label(blockListFrame, text=str(blocks[-1].kind))
    new_block_kind.grid(row=len(blocks), column = 4,sticky=(N, S, E, W))
    elements = [new_blockName, new_block_x, new_block_y, new_block_size, new_block_kind]

    button_remove = Button(blockListFrame, text="del", bg="red")
    elements = [new_blockName, new_block_x, new_block_y, new_block_size, new_block_kind, button_remove]
    button_remove.configure(command=lambda: removeBlock(blocks[-1].x, blocks[-1].y, elements))
    button_remove.grid(row=len(blocks), column = 5, sticky=(N, S, E, W))
    updateTable()

def addBlock():
    block_x_value = int(entry_x.get())
    block_y_value = int(entry_y.get())
    block_size_value = int(entry_size.get())
    block_isHorizontal_value = h.get()
    block_kind_value = v.get()
    blocks.append(Peca(len(blocks), block_x_value, block_y_value, block_isHorizontal_value, block_kind_value, block_size_value))
    print(len(blocks))
    updateBlockList()

def solve():
    full_blocks = []
    full_blocks+=blocks
    tab = fullfillTable(full_blocks)
    full_blocks = tab.pieces
    tab.printTabHuman()
    solution = getSolution(tab)
    for tree_tab in solution:
        solution_tree.append(tree_tab)
    displayTableFromIndex()


button_addBlock.configure(command=addBlock)
button_solve.configure(command=solve)
button_next.configure(command=displayNextTable)
button_previous.configure(command=displayPreviousTable)

root.geometry("1440x810")

root.mainloop()
