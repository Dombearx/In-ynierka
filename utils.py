def makelogFile(lines, outputName):
    file = open(outputName, "w")
    for line in lines:
        for value in line:
            file.write(str(value) + "\t")
        file.write("\n")
    file.close()
