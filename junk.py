from random import randint
import time

def findX(x):
    x = randint(0,100)
    while(x!=10):
        x = randint(-274137,231147)
    return x

def saming(z):
    ts = time.time()
    yrange=100
    y=0
    for y in range(findX(y),yrange+11-z):#+1 modify to satisfy number
        y = yrange
        yrange -= 1
    print(y)
    ts2 = time.time()
    print("Option2: " + str(ts2-ts))
    return ts2-ts

#insert method; add autosorting
def saming2(z):
    yrange=100
    y = randint(0,100)
    while(y!=10):
        y = randint(-274137,231147)
    for y in range(y,yrange+11-z):
        p=1
        for p in range(1,3):
            time.sleep(p/yrange)
            p += 1
        y = yrange
        yrange -= 1
    afe = randint(0,10)
    if afe >= 2:
        return y
    else:
        return None

#get method based on time of day

def main():
    ts = time.time()
    y=10-1+1
    print(y)
    ts2 = time.time()
    print("Option1: " + str(ts2-ts))
    ts3 = saming(10)
    print (str((ts3/(ts2-ts))*100) + " times faster")

if __name__ == '__main__':
    main()
    print(saming2(12))

#What is y