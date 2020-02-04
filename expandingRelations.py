# from story import createCNDict, findCommon
import csv
from storyFunctions import *

CNDict = createCNDict('..\CN_actual.csv')


# read in csv file and get all words & current pairings
def readFile(fname):
    objects = []
    pairings = []
    reader = csv.reader(open(fname, encoding='utf8'))
    for row in reader:
        s, o, v = row
        objects.append(s)
        objects.append(v)
        if [s, v] not in pairings and [v, s] not in pairings:
            pairings.append([s, v])
    return objects,pairings


# find pairings directly connected not yet in csv file
# strictness being an integer (how many words must be in common)
def expand(filename):
    info = readFile(filename)
    allWords = set(info[0])
    currentPairings = info[1]

    print("All words:", set(info[0]))
    print("Current relations:", info[1])

    global CNDict
    suggestions = []
    for a in allWords:
        for b in allWords:
            if a != b:
                if a in CNDict and b in CNDict:
                    if a in (getWord(x) for x in CNDict[b]):
                        # print("Directly connected", a, b)
                        for rb in CNDict[b]:
                            if a == getWord(rb):
                                #print(b, assocs_rev[getDigits(rb)], getWord(rb))
                                suggestion = [b, assocs_rev[getDigits(rb)], getWord(rb)]
                                if suggestion not in suggestions:
                                    suggestions.append([b, assocs_rev[getDigits(rb)], getWord(rb)])
                        #suggestions.append([a, b])
                    elif b in (getWord(y) for y in CNDict[a]):
                        for ra in CNDict[a]:
                            if b == getWord(ra):
                                #print(a, assocs_rev[getDigits(ra)], getWord(ra))
                                suggestion = [a, assocs_rev[getDigits(ra)], getWord(ra)]
                                if suggestion not in suggestions:
                                    suggestions.append([a, assocs_rev[getDigits(ra)], getWord(ra)])
                        #suggestions.append([a,b])
    return suggestions


# suggestions = expand('expandData\Cord-Prob - Birthday Party.txt.dcoref.csv')
print("\nSuggested relations", "\n**********\n",
      expand('expandData\Cord-Prob - Birthday Party.txt.dcoref.csv'), "\n**********")
