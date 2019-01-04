from PIL import Image
def openImage():
	im = Image.open('tables/tab3.jpeg')
	pix_val = list(im.getdata())
	print(im.size)
	width, height = im.size
	pre_table = []
	for y in range(347, 857+1):
		for x in range(16, 526+1):
			t_x = x-16
			t_y = y-347
			if(t_x%85==0 or t_y%85==0):
				im.putpixel((x, y), (255,0,0))
			if(t_x%85==0 and t_y%85==0 and t_x!=0 and t_y!=0):
				pixel_index = int(x-(85/2))+int(y-(85/2)-1)*width
				actual_pixel = pix_val[pixel_index]
				has_bottom = False
				has_top = False
				is_final = False
				#print(actual_pixel)
				if(actual_pixel[0] in range(180, 256)):
					if(actual_pixel[1]>95):
						for a in range(1, 44):
							border = pix_val[pixel_index+(a*(width))]
							if(border[0]<50 and border[1]<30 and border[2]<30):
								has_bottom = True
								break
						for a in range(1, 44):
							border = pix_val[pixel_index-(a*(width))]
							if(border[0]>200 and border[1]>140 and border[2]>100):
								has_top = True
								break
						for a in range(1, 44):
							border = pix_val[pixel_index+a]
							if(border[0] not in range(180, 256)):
								is_final = True
								break
						if(has_bottom and has_top):
							pre_table.append({'kind':1, 'has_top':True, 'has_bottom':True, 'isHorizontal': True, 'x': int(t_x/85)-1, 'y': int(t_y/85)-1, 'visited': False, 'isFinal':is_final})
							print("horizontal block")
						elif((has_top and not has_bottom) or (has_bottom and not has_top) or (not has_top and not has_bottom)):
							#print(has_top, " ",has_bottom)
							pre_table.append({'kind':1, 'has_top':has_top, 'has_bottom':has_bottom, 'isHorizontal': False, 'x': int(t_x/85)-1, 'y': int(t_y/85)-1, 'visited': False, 'isFinal':is_final})
							print("vertical block")
						else:
							print("deu merda")
					else:
						pre_table.append({'kind':2, 'has_top':True, 'has_bottom':True, 'isHorizontal': True, 'x': int(t_x/85)-1, 'y': int(t_y/85)-1, 'visited': False, 'isFinal':is_final})
						print("prisioner")
				else:
					pre_table.append({'kind':0, 'has_top':False, 'has_bottom':False, 'isHorizontal': True, 'x': int(t_x/85)-1, 'y': int(t_y/85)-1, 'visited': False, 'isFinal':is_final})
					print("empty")
				im.putpixel((int(x-(85/2)), int(y-(85/2))), (255,0,0))
	im.putpixel((10, 10), (255,0,0))
	im.save('tables/modified.jpeg')
	im.show()
	return pre_table
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



	
    