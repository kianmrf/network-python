def reverseList( list ):
    # head & tail pointers
    left = 0
    right = len(list)-1
    while left < right :
        tmp = list[left]
        list[left] = list[right]
        list[right] = tmp
        left += 1
        right -= 1
    return list


l1 = ["a", "b", "c", "d"]
l2 = [1,2,3,4,5,6,7,8,9]

print("Reversed List is: ", reverseList(l1))
print("Reversed List is: ", reverseList(l2))
