from storyFunctions import *
from simplenlg import *
import random
import statistics

CNDict = createCNDict('CN_actual.csv')
lexicon = Lexicon.getDefaultLexicon()  # using default lexicon
nlg_factory = NLGFactory(lexicon)  # create structure
realiser = Realiser(lexicon)  # realise sentence


# generate a randomStory after ordering the words based on analysis, sort of a SimpleNLG tutorial too
def simpleRandomStory(ws):
    verbs = ["make", "do", "be", "go", "see"]

    # simpleNLG stuff
    for i in range(0, 9):
        subject = ws[i]  # might need to switch subject, object depending on relation
        obj = ws[i+1]
        verb = random.choice(verbs)
        # complement = random.choice(complements)
        # more simpleNLG stuff
        sentence = nlg_factory.createClause()
        sentence.setSubject(subject)
        sentence.setVerb(verb)
        sentence.setObject(obj)
        # complements going after verbs
        # sentence.addComplement(complement)

        # can change tense
        # sentence.setFeature(Feature.TENSE, Tense.FUTURE)

        # can have questions    WHO_OBJECT, YES_NO, HOW_MANY
        # sentence.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.YES_NO)

        # add adjectives via 'modifier', set object as a noun phrase
        # obj = nlg_factory.createNounPhrase(ws[i+1])
        # obj.addModifier(random.choice(modifiers))
        # sentence.setObject(obj)
        #  can do the same with verbs, subject...
        print(realiser.realiseSentence(sentence))


# like simpleRandomStory but with bells and whistles of simpleNLG attached
# settings = [tense f/pr/pa, complement rate, modifier y/n, interrogative rate]
def randomStory(ws, settings):
    verbs = ["make a", "do a", "be a", "go a", "see a", "make the", "do the", "be the", "go to the", "see the"]
    complements = ["very quickly", "very slowly", "discreetly", "loudly"]
    modifiers = ["quickly", "slowly", "abruptly", "beautifully", "delicately", "firmly", "lightly",
                 "cheerfully"]  # adverbs or adjectives

    for i in range(0, 9):
        sentence = nlg_factory.createClause()
        # set tense of sentence, defaults to present
        tense = settings[0]
        compRate = settings[1]
        mRate = settings[2]
        interRate = settings[3]

        if tense == "f":
            sentence.setFeature(Feature.TENSE, Tense.FUTURE)
        elif tense == "pa":
            sentence.setFeature(Feature.TENSE, Tense.PAST)

        # get subject and object, add modifiers
        sub = nlg_factory.createNounPhrase("The " + ws[i])
        obj = nlg_factory.createNounPhrase(ws[i+1])
        if random.random() > mRate:
            obj.addModifier(random.choice(modifiers))
        if random.random() > mRate:
            sub.addModifier(random.choice(modifiers))
        # set subject, verb, object
        sentence.setObject(obj)
        sentence.setSubject(sub)
        sentence.setVerb(random.choice(verbs))

        # add complements at given rate
        if random.random() > compRate:
            sentence.addComplement(random.choice(complements))

        if random.random() > interRate:
            iType = random.random()
            if iType < 0.33:
                sentence.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.WHO_OBJECT)
            elif iType < 0.67:
                sentence.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.YES_NO)
            else:
                sentence.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.HOW_MANY)
        # realise sentence
        print(realiser.realiseSentence(sentence))


# loop through entry in CNdict, see if matches
def retrieveFromCN(entry, word):
    for a in entry:
        if getWord(a) == word:
            return getDigits(a)
    return "nadda" # didn't find anything


def findVerb(A, B):
    verbs = {"1": "was in the", "3": "can", "4": "results in", "5": "wanted", "10": "created", "11": "was a",
             "12": "desired", "16": "will cause", "19": "was a type of", "20": "had", "21": "was contextualised by",
             "22" : "has first subevent", "23" : "has last subevent", "24": "requires", "25": "had the property of",
             "26" : "has subevent", "28": "was a", "29": "was a kind of", "30": "found near", "31": "was made from",
             "32": "was a manner of", "34": "was motivated by", "35": "was not capable of", "36": "didn't want",
             "37": "doesn't have the property of", "40": "was a part of", "43": "was affected by", "45": "symbolised",
             "46": "was a", "47": "was used for"}
    # mapping of verbs to relations (digits)
    nums = findRelation(A, B)
    # print(nums, type(nums))
    if isinstance(nums, str):
        return [verbs[nums]]
    elif isinstance(nums, list):
        if len(nums) == 2:
            return [verbs[nums[0]], nums[1]]
        elif len(nums) == 3:
            return [verbs[nums[0]], verbs[nums[1]], nums[2]]


# sends appropriate relation(s) to findVerb
def findRelation(A, B):
    potentialRels = levels(A, B)
    # Check if the words are directly connected, if they are just return what the relation between them is
    if potentialRels[0]:
        # get relation between two words
        bInA = retrieveFromCN(CNDict[A], B)
        if bInA != "nadda":
            return bInA
        aInB = retrieveFromCN(CNDict[B], A)
        if aInB != "nadda":
            return aInB
        # print(A, CNDict[A], "\n", B, CNDict[B]
    # If the words are indirectly connected, return how each word is related to the in-between word
    # and the word itself.
    elif len(potentialRels[1]) > 0:
        chosenWord = random.choice(potentialRels[1])
        firstSide = retrieveFromCN(CNDict[A], chosenWord)
        secondSide = retrieveFromCN(CNDict[B], chosenWord)
        return [firstSide, secondSide, chosenWord]
    # the words aren't directly connected or indirectly connected. Decided to just use a relation for the first word
    # to construct the sentence.
    else:
        # randomly selects pair of words between A, B and takes first word in pair
        if len(potentialRels[2]) > 0:
            chosen = random.choice(potentialRels[2])[0]
            return [retrieveFromCN(CNDict[A], chosen), chosen]
        # nothing to choose from
        else:
            print("Didn't consider this, will have to fix.")
            return [1, "Eolas"]


# take advantage of functions developed from ConceptNet file to pick a better verb
def cnStory(ws):
    for i in range(9):
        sentence = nlg_factory.createClause()
        A = ws[i]
        B = ws[i+1]
        verbs = findVerb(A, B)
        # e.g : "The tree desires water." "The leaf is in the tree."
        if len(verbs) == 1:
            # need to check which is object, which is subject
            if A in [getWord(x) for x in CNDict[B]]:
                obj = A
                sub = B
            else:
                obj = B
                sub = A
            sentence.setObject(obj)
            sentence.setSubject("the " + sub)
            sentence.setVerb(verbs[0])
            print(realiser.realiseSentence(sentence))
        # e.g : "Are the leaf and the chicken a kind of turn?"
        elif len(verbs) == 2:
            together = nlg_factory.createCoordinatedPhrase(nlg_factory.createNounPhrase("the " + A)
                                                           , nlg_factory.createNounPhrase("the " + B))
            sentence.setObject(verbs[1])
            sentence.setSubject(together)
            sentence.setVerb(verbs[0])
            sentence.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.YES_NO)
            print(realiser.realiseSentence(sentence))
        # e.g : "The bird is in the sea and the water is a part of the sea."
        # verbs = [
        elif len(verbs) == 3:
            # print(A, B, verbs)
            if verbs[0] == verbs[1]:
                # both words have the same relation to the word in between them, can make a shorter sentence
                together = nlg_factory.createCoordinatedPhrase(nlg_factory.createNounPhrase("The " + A)
                                                               , nlg_factory.createNounPhrase("the " + B))
                sentence.setObject(verbs[2])
                sentence.setSubject(together)
                sentence.setVerb(verbs[0])
                print(realiser.realiseSentence(sentence))
            else:
                # don't have same relation to word, so construct two separate clauses and join together
                clause1 = nlg_factory.createClause("The " + A, verbs[0], "the " + verbs[2])
                clause2 = nlg_factory.createClause("the " + B, verbs[1], "the " + verbs[2])
                bothClauses = nlg_factory.createCoordinatedPhrase()
                bothClauses.addCoordinate(clause1)
                bothClauses.addCoordinate(clause2)
                print(realiser.realiseSentence(bothClauses))


rInput = randomInput(10)
print(rInput)
words = orderWords(rInput)
print(words)
cnStory(words)


#simpleRandomStory(words)
#print("\n")
#s = ["pr", 0.9, 0.7, 0.9] # | "pr", 0.9, 0.7, 0.9
#randomStory(words, s)




"""while True:
    rInput = randomInput()
    print(rInput)
    words = orderWords(rInput)
    flag = cnStory(words)
    print("\n", flag, "\n")
    if flag == 0: break """



# 04/02/20 simpleNLG has some cool stuff, features like interrogatives, setting tenses, complements
# 05/02/20 instead of randomly selecting verbs, should pick a verb that suits based on relation between words!

