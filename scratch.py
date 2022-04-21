import time

import debugpy

# 5678 is the default attach port in the VS Code debug configurations. Unless a host and port are specified, host defaults to 127.0.0.1
debugpy.listen(5678)
print("Waiting for debugger attach")
debugpy.wait_for_client()

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

debugpy.breakpoint()
print('break on this line')


for x in range(20):

    start = time.time()
    mylist = [i for i in range(iterations)]
    end = time.time()
    compreList.append(end-start)

print(sum(loopList) / len(loopList))
print(sum(compreList) / len(compreList))
