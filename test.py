list = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]
for index, item in enumerate(list, start=0):
	print (index)
	if(item%3==0):
		list.remove(list[index+1])