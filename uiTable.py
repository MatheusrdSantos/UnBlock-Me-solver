from tkinter import *
from classes import *

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
for y in range(0, 6):
    for x in range(0, 6):
        table_positions.append(Label(tableFrame, text='('+str(x)+', '+str(y)+')', bg="blue").grid(row=y, column=x, sticky=(N, S, E, W)))
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
button_addBlock = Button(blocksControllerFrame, text="add Block")
button_addBlock.grid(columnspan=4)
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
scrollbar.rowspan = 2
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

root.geometry("1440x810")

root.mainloop()
