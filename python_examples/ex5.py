n = input('Enter a number/integer: ')
sum = 0
for i in range(1,int(n)+1):
    if (i%3 == 0 or i%5 == 0):
        sum = sum + i
    else:
        continue
print("The sum from 1 to n is (only integers which are multiplications of 3 or 5 are considered): ",str(sum))
