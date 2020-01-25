from subprocess import Popen, PIPE
import sys
import errno
import re
import os

dir = "..\\Framsticks50rc14\\frams"


cmd = "C:\\Windows\\System32\\cmd.exe"

dir2 = "E:\\Polibuda\\semestr7\\inzynierka\\Nowyfolder\\In-ynierka\\Framsticks50rc14\\frams"

#args = ["frams", "-Q", "-s", "-icliutils.ini", "\"getsimplest 1\"", "-q"]


# print(args)

dir = "print(123)"


def parseIndividual(text):
    found = re.search('\n(.*)', text.decode("utf-8"))
    print(found.group(1))


def getSimpleIndividual():
    args = "frams -Q -s -icliutils.ini \"getsimplest 1\" -q"
    process = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    print(stdout.decode("utf-8"))
    parseIndividual(stdout)


def mutate(ind):
    args = "frams -Q -s -icliutils.ini rnd mut -q"
    process = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate(bytes(ind, encoding="utf-8"))
    print(stdout.decode("utf-8"))


def evaluate(ind_file):
    args = "frams -Q -s -icliutils.ini \"expdef standard-eval\" \"eval eval-allcriteria.sim ..\\\\..\\\\framsy\\\\" + ind_file + "\" -q"
    process = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    print(stdout.decode("utf-8"))


# getSimpleIndividual()
evaluate("testGen.gen")

'''

for line in process.stdout.read():
    print(line)

process = Popen([], cwd=r'../Framsticks50rc14/frams.exe',
                stdout=PIPE, stderr=PIPE)
stdout, stderr = process.communicate(
    "frams -Q -s -icliutils.ini \"getsimplest 1\" -q")
print(stdout)
print(stderr)

#print >>process.stdin, "cd " + dir2


#print >>process.stdin, args
process.stdin.write(bytes(args, encoding='ascii'))

process.stdin.write(bytes("e: ", encoding='ascii'))


process.stdin.write(bytes("cd " + dir2, encoding='ascii'))
'''
