number = input("Please Enter an Integer: ")
comp_mode = input("Press 'f' for factorial of n or 's' for sum of 1-n:")

if comp_mode == 'f':
    factorial(number)
elif comp_mode == 's':
    sum(number)
else:
    print("Error! Wrong Format Entered")

def sum(n):
    sum = 0
    for i in range(1,int(n)+1):
        sum = sum + i
    print("The sum from 1 to n is: ",str(sum))

def factorial(number):
    if number == 1:
        return number
    else:
        return number*factorial(number-1)

