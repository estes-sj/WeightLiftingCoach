from random import randint
import time

def findX(x):
    x = randint(0,100)
    while(x!=10):
        x = randint(-274137,231147)
    return x

def findY():
    ts = time.time()
    yrange=100
    y=0
    for y in range(findX(y),yrange+1):#+1 modify to satisfy number
        y = yrange
        yrange -= 1
    print(y)
    ts2 = time.time()
    print("Option2: " + str(ts2-ts))

def main():
    ts = time.time()
    y=10-1+1
    print(y)
    ts2 = time.time()
    print("Option1: " + str(ts2-ts))
    findY()

if __name__ == '__main__':
    main()

#What is y