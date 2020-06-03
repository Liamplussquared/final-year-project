"""
Contains methods taking advantage of ConceptNet file. Methods deal with reading in input, working with ConceptNet file,
identifying relations between words.

Methods find semantic connections between concepts. From these connections a measure of connectivity is defined, and
a sorting algorithm is defined which uses this metric. Several methods from getting input are defined.
"""


import csv
import random

CNdict = {}  # dictionary that will store data from ConceptNet file
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
          "tangible_thing": "46", "UsedFor": "47"}  # contains encoded relations
assocs_rev = {'1': 'AtLocation', '2': 'benzoic_acid', '3': 'CapableOf', '4': 'Causes', '5': 'CausesDesire', '6': 'cfc',
 '7': 'chemical_compound', '8': 'chemical_object', '9': 'chemistry_lab', '10': 'CreatedBy', '11': 'DefinedAs',
 '12': 'Desires', '13': 'dimethylhydrazine', '14': 'disaccharide_molecule', '15': 'discovered_every_year',
 '16': 'Entails', '17': 'ether', '18': 'exiled_in_saudi_arabia', '19': 'FormOf', '20': 'HasA',
 '21': 'HasContext', '22': 'HasFirstSubevent', '23': 'HasLastSubevent', '24': 'HasPrerequisite',
 '25': 'HasProperty', '26': 'HasSubevent', '27': 'injured_at_work', '28': 'InstanceOf', '29': 'IsA',
 '30': 'LocatedNear', '31': 'MadeOf', '32': 'MannerOf', '33': 'methylenedioxymethamphetamine', '34': 'MotivatedByGoal',
 '35': 'NotCapableOf', '36': 'NotDesires', '37': 'NotHasProperty', '38': 'organic_compound', '39': 'organic_molecule',
 '40': 'PartOf', '41': 'phosphoinositide', '42': 'pyridine', '43': 'ReceivesAction', '44': 'second_messenger',
 '45': 'SymbolOf', '46': 'tangible_thing', '47': 'UsedFor'}  # reverse of above
vWords = ["angle", "ant", "apple", "arch", "arm", "army", "baby", "bag", "ball", "band", "basin", "basket", "bath",
          "bed", "bee", "bell", "berry", "bird", "blade", "board", "boat","bone", "book", "boot", "bottle", "box",
          "boy", "brain", "brake", "branch", "brick", "bridge", "brush","bucket", "bulb", "button", "cake", "camera",
          "card", "cart","carriage", "cat", "chain", "cheese", "chest", "chin", "church", "circle", "clock", "cloud",
          "coat", "collar", "comb", "cord", "cow", "cup", "curtain", "cushion", "dog", "door", "drain", "drawer",
          "dress", "drop", "ear", "egg", "engine", "eye", "face", "farm", "feather", "finger", "fish", "flag", "floor",
          "fly", "foot", "fork", "fowl", "frame", "garden", "girl", "glove", "goat", "gun", "hair", "hammer", "hand",
          "hat", "head", "heart", "hook", "horn", "horse", "hospital", "house", "island", "jewel", "kettle", "key",
          "knee", "knife", "knot", "leaf", "leg", "library", "line", "lip", "lock", "map", "match", "monkey", "moon",
          "mouth", "muscle", "nail", "neck", "needle", "nerve", "net", "nose", "nut", "office", "orange", "oven",
          "parcel", "pen", "pencil", "picture", "pig", "pin", "pipe", "plane", "plate", "plough", "pocket", "pot",
          "potato", "prison", "pump", "rail", "rat", "receipt", "ring", "rod", "roof", "root", "sail", "school",
          "scissors", "screw", "seed", "sheep", "shelf", "ship", "shoe", "skin", "snake", "sock", "spade", "sponge",
          "spoon", "spring", "square", "stamp", "star", "station", "stem", "stick", "stocking", "stomach", "store",
          "street", "sun", "table", "tail", "thread", "throat", "thumb", "ticket", "toe", "tongue", "tooth", "town",
          "train", "tray", "tree", "trousers", "umbrella", "wall", "watch", "wheel", "whip", "whistle", "window",
          "wing", "wire", "worm"]  # list of visualisable objects


# creates a dictionary from the ConceptNet excel file.
# CNdict[key] = value : the key is the first word of a row, the value is a concatenation of the second word and
# an encoding of the relationship between the two words. (assocs details the mapping between numbers and relationships)
def createCNDict(fname):
    # encoding = "utf8" must be set
    reader = csv.reader(open(fname, encoding="utf8"))
    global CNdict
    for row in reader:
        # s is key, o is value, v is relation between them
        s, o, v = row
        o = o + assocs[v]
        try:
            CNdict[s].append(o)
            # print(1, end="")
        except KeyError:
            # print(2, end="")
            CNdict[s] = [o]
    return CNdict


# ask user to enter |size| line separated words. Words are restricted based on what's in the ConceptNet dictionary
def getInput(size):
    print("Enter", size, "line separated words!")
    words = []
    for i in range(size):
        word = input()
        while word not in CNdict:
            print("Word not in corpus! Please enter new word!")
            word = input()
        words.append(word)
    # print(words)
    return words


# selects size number of words randomly from the list of visualisable words, ensuring no repetition
def randomInput(size):
    chosen = []
    for i in range(size):
        vWord = random.choice(vWords)
        while vWord in chosen:
            vWord = random.choice(vWords)
        chosen.append(vWord)
    return chosen


# randomly selects size number of words contained in the ConceptNet dictionary, ensuring no repetition
def randomCNInput(size):
    listW = []
    for i in range(size):
        listW.append(random.choice(list(CNdict.keys())))
    print(listW)
    return listW


# randomly selects a word from the list of visualisable words and then selects (size - 1) number of
# words such that every word's neighbour is directly connected to it
def wellConnectedInput(size):
    chosen = []
    firstWord = random.choice(vWords)
    chosen.append(firstWord)
    for i in range(1, size):
        previousWord = chosen[i-1]
        randomDirectly = getWord(random.choice(CNdict[previousWord]))
        while (randomDirectly not in CNdict) and (randomDirectly not in chosen):
            randomDirectly = getWord(random.choice(CNdict[previousWord]))
        chosen.append(randomDirectly)
    # print(chosen)
    return chosen


"""
# This method returns a list containing information about the connections between two words. Four levels of
# "connectedness" are considered.
# level 0 means directly connected, e.g. cat is directly connected to kitten
# level 1 means indirectly connected with one word in-between,
#    e.g. cat is connected to animal which is connected to kitten
# level 2 means indirectly connected with two words in-between,
#    e.g. cat is connected to mouse which is connected to attic which is connected to kitten
# level 3 means indirectly connected with three words in-between,
#    e.g. cat is connected to petting, connected to animal, connected to kitten
"""


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
                    l2.append([x, y])
                    relY = [getWord(t) for t in CNdict[y]]
                    for z in relY:
                        if z in relB:
                            l3.append([x, y, z])
    connections[2] = l2
    connections[3] = l3

    return connections


#  CNdict[key] = value+digit, the value is the word that key is related to.
#  The digit is the encoding of what the relationship is.
#  This method simply returns the digit(s) (which can be used to find the relationship)
def getDigits(word):
    return ''.join([i for i in word if i.isdigit()])


# similar to getDigits except the word is returned.
def getWord(word):
    return ''.join([i for i in word if not i.isdigit()])


# This method takes in as input a list of  words, with the restriction that every word in contained in the CNdict
# dictionary. The list of words is sorted iteratively by starting at the first element of the list and placing next to
# it the word that is most strongly related to it. The strength of the relation is determined via getRScore. After a
# word is selected, it is removed from the pool of available words for selection.
def orderWords(words):
    story = []
    word = words[0]
    words.remove(word)
    story.append(word)
    currR, bW, bestR = 0, "", 0

    while words:  # story structure, pairings
        bW = words[0]
        for o in words:
            if not word == o:
                currR = getRScore(o, word)
                if currR > bestR:
                    bestR = currR
                    bW = o
        story.append(bW)
        words.remove(bW)
        word = bW
        bestR = 0
    return story


# This method returns an unbounded number that can be used a measure of how related two words are. The score is
# generated as a weighted sum of the number of elements in each level of connectedness (based on the levels function).
# Words that are directly connected are given a higher weighting.
# e.g. getRScore("cat", "kitten") returns 27.8912 and getRScore("cat", "hammer") returns 14.9623.
def getRScore(a, b):
    relations, rScore = levels(a, b), 0
    if relations[0]:
        rScore += 10
    rScore += 0.1 * len(relations[1]) + 0.005 * len(relations[2]) + 0.00005 * len(relations[3])
    return rScore
