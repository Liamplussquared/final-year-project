import csv
import random
from collections import deque

CNdict = {}
assocs = {"AtLocation": "1", "benzoic_acid": "2", "CapableOf": "3", "Causes": "4", "CausesDesire": "5", "cfc": "6",
          "chemical_compound": "7", "chemical_object": "8", "chemistry_lab": "9", "CreatedBy": "10", "DefinedAs": "11",
          "Desires": "12", "dimethylhydrazine": "13", "disaccharide_molecule": "14", "discovered_every_year": "15",
          "Entails": "16", "ether": "17", "exiled_in_saudi_arabia": "18", "FormOf": "19", "HasA": "20",
          "HasContext": "21", "HasFirstSubevent": "22", "HasLastSubevent": "23", "HasPrerequisite": "24",
          "HasProperty": "25", "HasSubevent": "26", "injured_at_work": "27", "InstanceOf": "28", "IsA": "29",
          "LocatedNear": "30", "MadeOf": "31", "MannerOf": "32", "methylenedioxymethamphetamine": "33",
          "MotivatedByGoal": "34", "NotCapableOf": "35", "NotDesires": "36", "NotHasProperty": "37",
          "organic_compound": "38", "organic_molecule": "39", "PartOf": "40", "phosphoinositide": "41",
          "pyridine": "42", "ReceivesAction": "43", "second_messenger": "44", "SymbolOf": "45",
          "tangible_thing": "46", "UsedFor": "47"}
assocs_rev = {v: k for k, v in assocs.items()}
# how to find "good" ways to write relationships?
relationships = {"1": "went", "3": "both", "4" : "were responsible for", "5": "intrigued someone to",
                 "10": "were manufactured by", "11": "were referred to as", "16": "lead to ", "19": "are both types of",
                 "20": "lost their", "21": "are both part of","22": "were instigated by", "23": "were proceeded by",
                 "24": "were hindered by", "25": "were both", "26": "lead to", "28": "were both", "29": "were both",
                 "30": "were found close to", "31": "were known as", "32": "were called", "34": "were inspired by",
                 "35": "could not", "36": "are not", "40": "made up",  "43": "were both", "45": "were symbolised as",
                 "46": "were both touched", "47": "were both used in"}
# verbs = ["shot", ""]


def createCNDict(fname):
    # couldn't open file until I set encoding = "utf8" for some reason
    reader = csv.reader(open(fname, encoding="utf8"))
    global CNdict
    for row in reader:
        # s is key, o is value, v is relation between them
        # how to store v efficiently?
        s, o, v = row
        o = o + assocs[v]
        try:
            CNdict[s].append(o)
            # print(1, end="")
        except KeyError:
            # print(2, end="")
            CNdict[s] = [o]
    return CNdict


def getInput():
    print("Enter 10 line separated words!")
    words = []
    for i in range(10):
        word = input()
        while word not in CNdict:
            print("Word not in corpus! Please enter new word!")
            word = input()
        words.append(word)
    # print(words)
    return words


def findCommon(a, b):
    allCommon = {}
    allCommon["unrestricted"]= set(getWord(x) for x in CNdict[a]) & set(getWord(y) for y in CNdict[b])  # without relations
    allCommon["restricted"] = set(CNdict[a]) & set(CNdict[b])  # with relations
    return allCommon


# get connections between a & b at levels 0-3 (a ~ b, a ~ x ~ b, a ~ x ~ y ~ b, a ~ x ~ y ~ z ~ b)
def levels(a, b):
    relA = [getWord(x) for x in CNdict[a]]
    relB = [getWord(x) for x in CNdict[b]]
    connections = {}

    connections[0] = a in [getWord(x) for x in CNdict[b]] or b in [getWord(x) for x in CNdict[a]]
    connections[1] = sorted(set(relA) & set(relB))

    l2 = [] # level 2
    l3 = []  # level 3

    for x in relA:
        if x in CNdict:
            relX = [getWord(t) for t in CNdict[x]]
            for y in relX:
                if y in CNdict:
                    l2.append([x,y])
                    relY = [getWord(t) for t in CNdict[y]]
                    for z in relY:
                        if z in relB:
                            l3.append([x, y, z])

    connections[2] = l2
    connections[3] = l3

    return connections


# just to get association
def getDigits(word):
    return ''.join([i for i in word if i.isdigit()])


def getWord(word):
    return ''.join([i for i in word if not i.isdigit()])


# sort input in list of words (words next to closest related words)
def orderWords(wordz):
    story = []
    word = wordz[0]
    wordz.remove(word)
    story.append(word)
    currR, bW, bestR = 0, "", 0

    while wordz:  # story structure, pairings
        bW = wordz[0]
        for o in wordz:
            if not word == o:
                currR = getRScore(o, word)
                if currR > bestR:
                    bestR = currR
                    bW = o
        story.append(bW)
        wordz.remove(bW)
        word = bW
        bestR = 0
    return story


def naiveStory(story):  # should probably split up function, bit unwieldly
    # now to make some simple sentences
    print("Once upon a time", end=" ")
    for i in range(0, 9):
        common = findCommon(story[i],story[i+1])
        if len(common["restricted"]) > 0:  # word in common with same relation
            link = list(common["restricted"])[0]  # DEVELOP A BETTER WAY TO PICK, maybe preference for some relations
            relation = relationships[getDigits(link)]  # should probably get more diversity...
            print(story[i], "and", story[i+1], relation, getWord(link), end=".\n")
        elif len(common["unrestricted"]) > 0:
            link = list(common["unrestricted"])[0]
            print(story[i], "and", story[i+1], "were both somehow related to", link, end="\n")
        else:
            print(story[i], "and", story[i+1], "don't seem very related.")


def getRScore(a, b):  # return score for how related words are
    relations, rScore = levels(a, b), 0
    if relations[0]: rScore += 10
    rScore += 0.1 * len(relations[1]) + 0.01 * len(relations[2]) + 0.001 * len(relations[3])
    # print(a, b, rScore)
    return rScore