# following function determines if a list contains item x
def itemExists( x , list ):
    for item in list:
        if x == item :
            return True
    return False        


l1 = ["a", "b", "c", "d"]
if itemExists("a", l1):
    print("'a' exists in this list : ", l1)
if not itemExists("z", l1):
    print("'z' does NOT exists in this list : ", l1)

