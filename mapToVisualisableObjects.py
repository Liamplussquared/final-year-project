"""
07-11-19: if a word is big or complicated, it might be useful to represent it as another word (easier to remember)
Could find synonym, rhyming word, or a substring which is also a word
Made synonym and compound for this purpose...

08-11-19
given list of words, return list of visualisable objects

11-11-19
vWords is the list of visualisable objects
rhyme...
mapword...

12-11-19
PQ to store potential words... would allow for weighting of different strategies!
spending more time on rhyming than expected... messing around with pyphonetics has given pretty poor results for words that "rhyme"
pronoucning library... https://pronouncing.readthedocs.io/en/latest/
PQ would be useless while I'm not actually finding anything to map to...

13-11-19
could write another function to check if word is related to any vWords using CN (more relations =? more related)
could use ConceptNet API, but I'd have to make 10*200 = 2000 queries.
"""

from nltk.corpus import wordnet as wn  # synsets and such
from nltk.corpus import wordnet_ic
from pyphonetics import RefinedSoundex, Soundex  # phonetic similarity
from storyFunctions import createCNDict, findCommon
import pronouncing  # for rhyming
import operator


CNDict = createCNDict('CN_actual.csv')
vWords = ["angle", "ant", "apple", "arch", "arm", "army", "baby", "bag", "ball", "band", "basin", "basket", "bath",
          "bed", "bee", "bell", "berry", "bird", "blade", "board", "boat",
          "bone", "book", "boot", "bottle", "box", "boy", "brain", "brake", "branch", "brick", "bridge", "brush",
          "bucket", "bulb", "button", "cake", "camera", "card", "cart",
          "carriage", "cat", "chain", "cheese", "chest", "chin", "church", "circle", "clock", "cloud", "coat", "collar",
          "comb", "cord", "cow", "cup", "curtain", "cushion", "dog",
          "door", "drain", "drawer", "dress", "drop", "ear", "egg", "engine", "eye", "face", "farm", "feather",
          "finger", "fish", "flag", "floor", "fly", "foot", "fork", "fowl",
          "frame", "garden", "girl", "glove", "goat", "gun", "hair", "hammer", "hand", "hat", "head", "heart", "hook",
          "horn", "horse", "hospital", "house", "island", "jewel",
          "kettle", "key", "knee", "knife", "knot", "leaf", "leg", "library", "line", "lip", "lock", "map", "match",
          "monkey", "moon", "mouth", "muscle", "nail", "neck", "needle",
          "nerve", "net", "nose", "nut", "office", "orange", "oven", "parcel", "pen", "pencil", "picture", "pig", "pin",
          "pipe", "plane", "plate", "plough", "pocket", "pot",
          "potato", "prison", "pump", "rail", "rat", "receipt", "ring", "rod", "roof", "root", "sail", "school",
          "scissors", "screw", "seed", "sheep", "shelf", "ship",
          "shoe", "skin", "snake", "sock", "spade", "sponge", "spoon", "spring", "square", "stamp", "star", "station",
          "stem", "stick", "stocking", "stomach", "store",
          "street", "sun", "table", "tail", "thread", "throat", "thumb", "ticket", "toe", "tongue", "tooth", "town",
          "train", "tray", "tree", "trousers", "umbrella", "wall",
          "watch", "wheel", "whip", "whistle", "window", "wing", "wire", "worm"]
cLevel = 0.5  # weighting to subset of word
sLevel = 1  # weighting to synonyms
rhLevel = 0.75  # weighting to rhyme
reLevel = 0.5  # weighting to relation

def wordInfo(word):
    print("synonyms: ", synonym(word))
    print("shortest synonym: ", min(synonym(word), key=len))
    print("words within: ", compound(word))
    print("best compound: ", bestCompound(compound(word)))
    print("rhymes with: ", rhyme(word))
    print("related to: ", sorted(relations(word).items(), key=operator.itemgetter(1), reverse=True))
    print("potential words: ", mapWord(word))


def synonym(word):
    synonyms = []
    for syn in wn.synsets(word):
        parts = syn.name().split(".")
        synonyms.append(parts[0])
    return synonyms


def compound(word):  # go through all substrings, see if any is a real word
    compounds = []
    if not len(word) <= 3:
        for i in range(0, len(word)):
            for j in range(i + 2, len(word)):  # +3 because I don't want to use one or two letter words...
                temp = word[i:j + 1]
                if wn.synsets(temp):
                    compounds.append(temp)
    return compounds


def bestCompound(words):  # return word with most synonyms
    num = 0
    best = ""
    for word in words:
        if len(synonym(word)) > num:
            best = word
            num = len(synonym(word))
    return best


def mapWord(word):
    viable = {}
    compounds = compound(word)
    for c in compounds:  # add compound words
        if c in vWords and c not in viable:
            viable[c] = cLevel
    synonyms = synonym(word)
    for s in synonyms:  # add synonyms
        if s in vWords and s not in viable:
            viable[s] = sLevel
    rhymes = rhyme(word)
    for r in rhymes:  # add words that rhyme
        if r in vWords and r not in viable:
            viable[r] = rhLevel
    # now to get results from CN function
    CNwords = relations(word)
    for k, v in CNwords.items():  # for key,value
        if k in viable:  # word already in dictionary
            if viable[k] < v:  # if value less than new value
                viable[k] = v  # then update value
        else:
            viable[k] = v

    return sorted(viable.items(), key=operator.itemgetter(1), reverse=True)


def rhyme(word):
    rhyming = []
    potential = pronouncing.rhymes(word)
    for v in vWords:
        if v in potential:
            rhyming.append(v)
    #print(rhyming)
    return rhyming


def soundsLike(word):
    similar = []
    rs = RefinedSoundex()
    for v in vWords:  # entire word
        if rs.distance(v,word) < 3 and v not in similar:  # rs.distance returns integers...
            similar.append(v)
    return similar


def relations(word):  # check if word is related to any vWords
    # level is an int, determines how many words must be in common for words to be considered "related"
    rels = {}
    for v in vWords:
        numCommon = len(findCommon(v, word)["unrestricted"])
        if numCommon >= 4:
            rels[v] = 1*reLevel
        elif numCommon == 3:
            rels[v] = 0.75*reLevel
        elif numCommon == 2:
            rels[v] = 0.5*reLevel
        elif numCommon == 1:
            rels[v] = 0.25*reLevel
    return rels


print("enter word")
word = input()
while not wn.synsets(word):
    print("word not in wordnet")
    word = input()
wordInfo(word)


