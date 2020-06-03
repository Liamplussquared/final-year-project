"""
Contains methods used to map a word to a visualisable object. Depends on pyphonetics, nltk, pronouncing & operator

Use wordInfo(word) to get information about what the different approaches return, as well as a dictionary containing
potential mappings.

e.g. wordInfo(puppy) leads to the output:

synonyms:  ['puppy', 'puppy']
shortest synonym:  puppy
words within:  ['pup', 'pupp', 'puppy', 'upp', 'uppy', 'ppy']
best compound:  pup
rhymes with:  []
sounds like:  ['apple', 'baby', 'bag', 'ball', 'band', 'basin', 'basket', 'bath', 'bed', 'bee', 'bell', 'berry', 'bird', 'blade', 'board', 'boat', 'bone', 'book', 'boot', 'bottle', 'box', 'boy', 'brake', 'bucket', 'bulb', 'button', 'cake', 'cheese', 'cup', 'face', 'house', 'line', 'lip', 'map', 'nose', 'parcel', 'pen', 'pencil', 'pig', 'pin', 'pipe', 'plane', 'plate', 'plough', 'pocket', 'pot', 'potato', 'prison', 'pump', 'sheep', 'ship', 'spade', 'table', 'whip', 'wire']
related to:  [('cat', 0.5), ('dog', 0.5), ('bird', 0.375), ('fish', 0.375), ('horse', 0.375), ('rat', 0.375), ('sponge', 0.375), ('bag', 0.25), ('basket', 0.25), ('blade', 0.25), ('bone', 0.25), ('book', 0.25), ('boy', 0.25), ('cake', 0.25), ('clock', 0.25), ('cow', 0.25), ('ear', 0.25), ('face', 0.25), ('girl', 0.25), ('head', 0.25), ('heart', 0.25), ('leg', 0.25), ('monkey', 0.25), ('pig', 0.25), ('screw', 0.25), ('snake', 0.25), ('spoon', 0.25), ('angle', 0.125), ('apple', 0.125), ('arm', 0.125), ('ball', 0.125), ('bed', 0.125), ('bell', 0.125), ('boot', 0.125), ('bottle', 0.125), ('box', 0.125), ('brain', 0.125), ('brick', 0.125), ('brush', 0.125), ('bucket', 0.125), ('button', 0.125), ('cheese', 0.125), ('chest', 0.125), ('chin', 0.125), ('cloud', 0.125), ('cup', 0.125), ('curtain', 0.125), ('drop', 0.125), ('egg', 0.125), ('eye', 0.125), ('flag', 0.125), ('floor', 0.125), ('fly', 0.125), ('foot', 0.125), ('fork', 0.125), ('fowl', 0.125), ('frame', 0.125), ('garden', 0.125), ('glove', 0.125), ('goat', 0.125), ('hat', 0.125), ('hook', 0.125), ('horn', 0.125), ('house', 0.125), ('jewel', 0.125), ('kettle', 0.125), ('key', 0.125), ('knife', 0.125), ('knot', 0.125), ('line', 0.125), ('map', 0.125), ('mouth', 0.125), ('muscle', 0.125), ('nail', 0.125), ('neck', 0.125), ('nerve', 0.125), ('nose', 0.125), ('nut', 0.125), ('oven', 0.125), ('pen', 0.125), ('picture', 0.125), ('pipe', 0.125), ('plate', 0.125), ('pocket', 0.125), ('pot', 0.125), ('pump', 0.125), ('rod', 0.125), ('root', 0.125), ('sheep', 0.125), ('skin', 0.125), ('spring', 0.125), ('square', 0.125), ('stamp', 0.125), ('stick', 0.125), ('stomach', 0.125), ('street', 0.125), ('table', 0.125), ('tail', 0.125), ('tongue', 0.125), ('train', 0.125), ('wheel', 0.125), ('whip', 0.125), ('wing', 0.125), ('wire', 0.125), ('worm', 0.125)]
potential words:  [('cat', 0.5), ('dog', 0.5), ('bird', 0.375), ('fish', 0.375), ('horse', 0.375), ('rat', 0.375), ('sponge', 0.375), ('bag', 0.25), ('basket', 0.25), ('blade', 0.25), ('bone', 0.25), ('book', 0.25), ('boy', 0.25), ('cake', 0.25), ('clock', 0.25), ('cow', 0.25), ('ear', 0.25), ('face', 0.25), ('girl', 0.25), ('head', 0.25), ('heart', 0.25), ('leg', 0.25), ('monkey', 0.25), ('pig', 0.25), ('screw', 0.25), ('snake', 0.25), ('spoon', 0.25), ('baby', 0.25), ('band', 0.25), ('basin', 0.25), ('bath', 0.25), ('bee', 0.25), ('berry', 0.25), ('board', 0.25), ('boat', 0.25), ('brake', 0.25), ('bulb', 0.25), ('lip', 0.25), ('parcel', 0.25), ('pencil', 0.25), ('pin', 0.25), ('plane', 0.25), ('plough', 0.25), ('potato', 0.25), ('prison', 0.25), ('ship', 0.25), ('spade', 0.25), ('angle', 0.125), ('apple', 0.125), ('arm', 0.125), ('ball', 0.125), ('bed', 0.125), ('bell', 0.125), ('boot', 0.125), ('bottle', 0.125), ('box', 0.125), ('brain', 0.125), ('brick', 0.125), ('brush', 0.125), ('bucket', 0.125), ('button', 0.125), ('cheese', 0.125), ('chest', 0.125), ('chin', 0.125), ('cloud', 0.125), ('cup', 0.125), ('curtain', 0.125), ('drop', 0.125), ('egg', 0.125), ('eye', 0.125), ('flag', 0.125), ('floor', 0.125), ('fly', 0.125), ('foot', 0.125), ('fork', 0.125), ('fowl', 0.125), ('frame', 0.125), ('garden', 0.125), ('glove', 0.125), ('goat', 0.125), ('hat', 0.125), ('hook', 0.125), ('horn', 0.125), ('house', 0.125), ('jewel', 0.125), ('kettle', 0.125), ('key', 0.125), ('knife', 0.125), ('knot', 0.125), ('line', 0.125), ('map', 0.125), ('mouth', 0.125), ('muscle', 0.125), ('nail', 0.125), ('neck', 0.125), ('nerve', 0.125), ('nose', 0.125), ('nut', 0.125), ('oven', 0.125), ('pen', 0.125), ('picture', 0.125), ('pipe', 0.125), ('plate', 0.125), ('pocket', 0.125), ('pot', 0.125), ('pump', 0.125), ('rod', 0.125), ('root', 0.125), ('sheep', 0.125), ('skin', 0.125), ('spring', 0.125), ('square', 0.125), ('stamp', 0.125), ('stick', 0.125), ('stomach', 0.125), ('street', 0.125), ('table', 0.125), ('tail', 0.125), ('tongue', 0.125), ('train', 0.125), ('wheel', 0.125), ('whip', 0.125), ('wing', 0.125), ('wire', 0.125), ('worm', 0.125)]

"""

from nltk.corpus import wordnet as wn  # synsets and such
from nltk.corpus import wordnet_ic
from pyphonetics import RefinedSoundex, Soundex  # phonetic similarity
from storyFunctions import createCNDict, levels
import pronouncing  # for rhyming
import operator # used for sorting dictionary of mappings


CNDict = createCNDict('CN_actual.csv')
wn_lemmas = set(wn.all_lemma_names())  # all words in WordNet
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
# Weightings to each type of mapping
cLevel = 0.5  # weighting to subset of word
sLevel = 1  # weighting to synonyms
rhLevel = 0.75  # weighting to rhyme
reLevel = 0.5  # weighting to relation


# Reads in a word and returns possible mappings based on each approach.
def wordInfo(word):
    if word in wn_lemmas and len(synonym(word)) > 0:
        print("synonyms: ", synonym(word))
        print("shortest synonym: ", min(synonym(word), key=len))
    print("words within: ", compound(word))
    print("best compound: ", bestCompound(compound(word)))
    print("rhymes with: ", rhyme(word))
    print("sounds like: ", soundsLike(word))
    if word in CNDict:
        print("related to: ", sorted(relations(word).items(), key=operator.itemgetter(1), reverse=True))
    print("potential words: ", mapWord(word))


# Returns all synonyms of a word.
def synonym(word):
    synonyms = []
    for syn in wn.synsets(word):
        parts = syn.name().split(".")
        synonyms.append(parts[0])
    return synonyms


# Returns all words contained in another word.
def compound(word):  # go through all substrings, see if any is a real word
    compounds = []
    if not len(word) <= 3:
        for i in range(0, len(word)):
            for j in range(i + 2, len(word)):  # +3 because I don't want to use one or two letter words...
                temp = word[i:j + 1]
                if word in wn_lemmas:
                    compounds.append(temp)
    return compounds


# Returns word within larger word that has the most synonyms
def bestCompound(words):
    num = 0
    best = ""
    for word in words:
        if len(synonym(word)) > num:
            best = word
            num = len(synonym(word))
    return best


# Checks if word rhymes with any visualisable object.
def rhyme(word):
    rhyming = []
    potential = pronouncing.rhymes(word)
    for v in vWords:
        if v in potential:
            rhyming.append(v)
    #print(rhyming)
    return rhyming


# Checks for phonetic similarity. Returns words that fall under threshold of similarity.
def soundsLike(word):
    similar = []
    rs = RefinedSoundex()
    for v in vWords:  # entire word
        if rs.distance(v, word) <= 3 and v not in similar:  # rs.distance returns integers...
            similar.append(v)
    return similar


# Uses functions defined in "storyFunctions" to return a visualisable object that a word has a certain number of
# relations to.
def relations(word):  # check if word is related to any vWords
    # level is an int, determines how many words must be in common for words to be considered "related"
    if word not in CNDict:
        return
    rels = {}
    for v in vWords:
        numCommon = len(levels(v, word)[1])
        if numCommon >= 4:
            rels[v] = 1*reLevel
        elif numCommon == 3:
            rels[v] = 0.75*reLevel
        elif numCommon == 2:
            rels[v] = 0.5*reLevel
        elif numCommon == 1:
            rels[v] = 0.25*reLevel
    return rels


# Performs actual mapping of a word to visualisable objects.
# Returns a weighted dictionary, the higher the weight the "better" the mapping.
# Weights determined by weightings assigned earlier.
def mapWord(word):
    viable = {}
    compounds = compound(word)
    for c in compounds:  # add compound words
        if c in vWords:
            viable[c] = cLevel

    synonyms = synonym(word)
    for s in synonyms:  # add synonyms
        if s in vWords:
            viable[s] = sLevel

    rhymes = rhyme(word)
    for r in rhymes:  # add words that rhyme
        if r in vWords:
            viable[r] = rhLevel

    # now to get results from CN function
    if word in CNDict:
        CNwords = relations(word)
        for k, v in CNwords.items():  # for key,value
            if k in viable:  # word already in dictionary
                if viable[k] < v:  # if value less than new value
                    viable[k] = v  # then update value
            else:
                viable[k] = v

    # RefinedSoundex stuff
    similarSounds = soundsLike(word)
    for s in similarSounds:
        if s in vWords and s not in viable:
            viable[s] = 0.25

    return sorted(viable.items(), key=operator.itemgetter(1), reverse=True)


wordInfo("puppy")