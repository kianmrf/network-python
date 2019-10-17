from __future__ import division # for compatibility of // between Python 2 and 3
def digits(number, base=10):
    assert number >= 0
    if number == 0:
        return [0]
    l = []
    while number > 0:
        l.append(number % base)
        number = number // base
    return l


def main():
    x = input("enter a number: ")
    print(digits(int(x)))


main()
