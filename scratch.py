import time
iterations = 1_000_000


loopList = []
compreList = []

for x in range(20):
    start = time.time()
    mylist = []
    for i in range(iterations):
        mylist.append(i)
    end = time.time()
    loopList.append(end-start)

for x in range(20):

    start = time.time()
    mylist = [i for i in range(iterations)]
    end = time.time()
    compreList.append(end-start)

print(sum(loopList) / len(loopList))
print(sum(compreList) / len(compreList))
