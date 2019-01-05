from classes import *
#from utils import *
def findBlock(pre_table, x , y):
    for index, block in enumerate(pre_table, start=0):
        if(block['x']==x and block['y']==y):
            return index
def blocksInfoToTable(pre_table):
    blocks = []
    cont = 0
    for y in range(0, 6):
        for x in range(0, 6):
            index = findBlock(pre_table, x, y)
            block = pre_table[index]
            if(block['visited']):
                continue
            if(block['kind']==0):
                blocks.append(Block(cont, block['x'], block['y'], True, 0, 1))
            elif(block['kind']==2):
                blocks.append(Block(cont, block['x'], block['y'], True, 2, 2))
                index = findBlock(pre_table, x+1, y)
                pre_table[index]['visited'] = True
            elif(block['isHorizontal']):
                c_x = x
                while(True):
                    c_x+=1
                    index = findBlock(pre_table, c_x, y)
                    next_block = pre_table[index]
                    pre_table[index]['visited'] = True
                    if(next_block['isFinal']):
                        break
                blocks.append(Block(cont, block['x'], block['y'], True, block['kind'], c_x-block['x']+1))
            else:
                c_y = y
                while(True):
                    c_y+=1
                    index = findBlock(pre_table, x, c_y)
                    next_block = pre_table[index]
                    pre_table[index]['visited'] = True
                    if(next_block['has_bottom']):
                        break
                blocks.append(Block(cont, block['x'], block['y'], False, block['kind'], c_y-block['y']+1))
            block['visited'] = True
            cont+=1
    return Table(blocks)