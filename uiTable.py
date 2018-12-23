from tkinter import *

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
tableLabel = Label(tableFrame, text="table", bg="red")
tableLabel.pack(fill=X)

tableFrame.pack(expand=True, fill=X)


tableNavigatorFrame = Frame(leftFrame)

# build table navigator here
navigatorLabel = Label(tableNavigatorFrame, text="nevigator", bg="gray")
navigatorLabel.pack(fill=X)

tableNavigatorFrame.pack(expand=True, fill=X)


tableSolverFrame = Frame(leftFrame)

# build solve button here
solverLabel = Label(tableSolverFrame, text="solve me!", bg="pink")
solverLabel.pack(fill=X)

tableSolverFrame.pack(expand=True, fill=X)



blocksControllerFrame = Frame(rightFrame)

# add and remove blocks here
blocksControllerLabel = Label(blocksControllerFrame, text="controll blocks!", bg="orange")
blocksControllerLabel.pack(fill=X)

blocksControllerFrame.pack(expand=True, fill=X)


blockListFrame = Frame(rightFrame)

# list all blocks here
blockListLabel = Label(blockListFrame, text="list blocks!", bg="purple")
blockListLabel.pack(fill=X)

blockListFrame.pack(expand=True, fill=X)


root.mainloop()
