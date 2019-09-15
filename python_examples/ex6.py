def sum(n):
    sum = 0
    for i in range(1,n+1):
        sum = sum + i
    print("The sum from 1 to n is: ",str(sum))

def fact(n):
    if n == 0:
        return 1
    if n == 1:
        return n
    else:
        return n * fact(n-1)

number = input("Please Enter an Integer: ")
comp_mode = input("Press 'f' for factorial of n or 's' for sum of 1-n: ")

if comp_mode == 'f':
    print("The factorial of n is: ", str(fact(int(number))))
elif comp_mode == 's':
    sum(int(number))
else:
    print("Error! Wrong Format Entered")

