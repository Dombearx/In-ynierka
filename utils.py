def makelogFile(lines, outputName):
    file = open(outputName, "w")
    for line in lines:
        for value in line:
            file.write(str(value) + "\t")
        file.write("\n")
    file.close()


class result:

    def __init__(self, logbooks, hallOfFamer):
        self.logbooks = logbooks
        self.hallOfFamer = hallOfFamer

    def getLogbooks(self):
        return self.logbooks

    def getHallOfFamer(self):
        return self.hallOfFamer[0]
