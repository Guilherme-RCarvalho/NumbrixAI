
import os

boardSize = 10
myFile = open("myTest", "w")
myFile.write(str(boardSize) + "\n")

lineList = []
for line in range(boardSize):
    myLine = ""
    for col in range(boardSize):
        myLine = myLine + f"{0}\t"
    myLine = myLine[:-1] + "\n"

    lineList.append(myLine)

lineList[-1] = lineList[-1][:-1]


for line in lineList:
    myFile.write(line)


myFile.close()