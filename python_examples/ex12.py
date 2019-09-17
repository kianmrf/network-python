def maxOfList( list ):
    maxVal = list[0]
    for item in list:
        if item > maxVal :
            maxVal = item
    return maxVal

a = [1,2,3,4,5,6,7]
b = ['aaa', 'bcd', 'eee', 'fgh']
print("the max is: ", maxOfList(a))
print("the max is: ", maxOfList(b))
