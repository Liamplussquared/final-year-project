"""
Contains the methods used by the story generator algorithms (SGAs) as well as two SGAs.
cnStory and shorterStory are the actual developed SGAs. They only differ in how sentences are presented.
"""
from storyFunctions import *
from simplenlg import *
import random
import statistics


# Needed for SimpleNLG
lexicon = Lexicon.getDefaultLexicon()  # using default lexicon
nlg_factory = NLGFactory(lexicon)  # create structure
realiser = Realiser(lexicon)  # realise sentence
relationCounter = []  # tracks how many times each relation is used


# generate a randomStory after ordering the words based on analysis, sort of a SimpleNLG tutorial too
def simpleRandomStory(ws):
    verbs = ["make", "do", "be", "go", "see"]

    # simpleNLG stuff
    for i in range(len(ws) - 1):
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


# Checks if word contained within list at CNdict[entry]
# Returns encoded relation if it is.
def retrieveFromCN(entry, word):
    for a in entry:
        if getWord(a) == word:
            return getDigits(a)
    return "nadda" # didn't find anything


# takes as input two concepts A & B and returns a list containing a verb and any additional necessary information
# for directly connected concepts, the method simply returns a verb connecting the concepts
# for indirectly connected concepts, multiple verbs may be returned
# as well as the words indirectly connecting the concepts
def findVerb(A, B):
    verbs = {"1": "is in", "3": "is capable of", "4": "results in", "5": "wants", "10": "creates", "11": "is a",
             "12": "desires", "16": "entails", "18": "is exiled", "19": "is a type of", "20": "has",
             "21": "has context", "22" : "has first subevent", "23" : "has last subevent", "24": "requires",
             "25": "has the property of",  "26" : "has subevent", "28": "is a", "29": "is a kind of",
             "30": "is found near", "31": "is made from", "32": "is a manner of", "34": "is motivated by",
             "35": "is not capable of", "36": "does not want", "37": "does not have the property of",
             "40": "is a part of", "43": "is affected by", "45": "symbolises", "46": "is a", "47": "is used for"}
    # mapping of verbs to relations (digits)
    nums = findRelation(A, B)
    # Concepts are directly connected, returning single verb to generate story
    if isinstance(nums, str):
        return [verbs[nums]]
    # Concepts are indirectly connected
    elif isinstance(nums, list):
        if len(nums) == 2:
            return [verbs[nums[0]], nums[1]]
        # indirectly connected with one shared relation, return appropriate verbs for concepts relations
        elif len(nums) == 3:
            return [verbs[nums[0]], verbs[nums[1]], nums[2]]


# takes in as input two concepts and returns an appropriate relation / number of relations
# based on how the words are related
def findRelation(A, B):
    potentialRels = levels(A, B)
    # if the concepts are directly connected, return the relation between them
    if potentialRels[0]:
        bInA = retrieveFromCN(CNdict[A], B)
        if bInA != "nadda":
            return bInA
        aInB = retrieveFromCN(CNdict[B], A)
        if aInB != "nadda":
            return aInB
        # print(A, CNDict[A], "\n", B, CNDict[B]
    # if the concepts are indirectly connected with one word between them, randomly choose such a
    # word and return each concepts relation to the word
    elif len(potentialRels[1]) > 0:
        chosenWord = random.choice(potentialRels[1])
        firstSide = retrieveFromCN(CNdict[A], chosenWord)
        secondSide = retrieveFromCN(CNdict[B], chosenWord)
        return [firstSide, secondSide, chosenWord]
    # if the concepts are indirectly connected with two words in between them, choose a random word that
    # one of the concepts is related to and return the given concepts relation to it.
    # the concept's relation to the concept is used as the other concept's relation to the word
    elif len(potentialRels[2]) > 0:
        chosen = random.choice(potentialRels[2])[0]
        return [retrieveFromCN(CNdict[A], chosen), chosen]
    # if the concepts have no relation up till now, just return a random relation
    else:
        # print("Didn't consider this, will have to fix.")
        return [str(random.randint(1, 48)), "Eolas"]


# Actual story generator.
# Generates sentences based on word pairs. Sentence structure changes depending on how the words are related.
def cnStory(ws):
    for i in range(len(ws) - 1):
        sentence = nlg_factory.createClause()
        A = ws[i]
        B = ws[i+1]
        verbs = findVerb(A, B)
        # e.g : "The tree desires water." "The leaf is in the tree."
        # Words are directly connected
        if len(verbs) == 1:
            # need to check which is object, which is subject
            if A in [getWord(x) for x in CNdict[B]]:
                obj = A
                sub = B
            else:
                obj = B
                sub = A
            # remove _ from words
            if "_" in obj: obj = obj.replace("_", " ")
            if "_" in sub: sub = sub.replace("_", " ")
            sentence.setObject(obj)
            sentence.setSubject("the " + sub)
            sentence.setVerb(verbs[0])
            print(realiser.realiseSentence(sentence))
        # No direct or indirect connections found.
        # A relation to one word is extended to another.
        # e.g : "The nerve and the cake are in human"
        # In the above example, nerve is related to human but cake isn't.
        elif len(verbs) == 2:
            if "_" in A: A = A.replace("_", " ")
            if "_" in B: B = B.replace("_", " ")
            together = nlg_factory.createCoordinatedPhrase(nlg_factory.createNounPhrase("the " + A)
                                                           , nlg_factory.createNounPhrase("the " + B))
            sentence.setObject(verbs[1].replace("_", " "))
            sentence.setSubject(together)
            sentence.setVerb(verbs[0])
            # sentence.setFeature(Feature.INTERROGATIVE_TYPE, InterrogativeType.YES_NO)
            print(realiser.realiseSentence(sentence))
        # Words are indirectly connected. Two different sentence structures based on whether or not they share the same
        # relation to what indirectly connects them.
        elif len(verbs) == 3:
            # print(A, B, verbs)
            # e.g : "The boy and the girl are in the school"
            if verbs[0] == verbs[1]:
                if "_" in A: A = A.replace("_", " ")
                if "_" in B: B = B.replace("_", " ")
                # both words have the same relation to the word in between them, can make a shorter sentence
                together = nlg_factory.createCoordinatedPhrase(nlg_factory.createNounPhrase("The " + A)
                                                               , nlg_factory.createNounPhrase("the " + B))
                sentence.setObject(verbs[2].replace("_", " "))
                sentence.setSubject(together)
                sentence.setVerb(verbs[0])
                print(realiser.realiseSentence(sentence))
            # e.g : "The bird is in the sea and the water is a part of the sea."
            else:
                # don't have same relation to word, so construct two separate clauses and join together
                if "_" in A: A = A.replace("_", " ")
                if "_" in B: B = B.replace("_", " ")
                clause1 = nlg_factory.createClause("The " + A, verbs[0], "the " + verbs[2])
                clause2 = nlg_factory.createClause("the " + B, verbs[1], "the " + verbs[2])
                bothClauses = nlg_factory.createCoordinatedPhrase()
                bothClauses.addCoordinate(clause1)
                bothClauses.addCoordinate(clause2)
                print(realiser.realiseSentence(bothClauses))


# Almost identical to cnStory except it uses a different presentation for the sentences.
# Sentence structure constrained to be A ... B where A and B are the two words used as a basis for sentence generation.
def shorterStory(ws):
    for i in range(len(ws) - 1):
        sentence = nlg_factory.createClause()
        A, B = ws[i], ws[i+1]
        verbs = findVerb(A, B)
        # Words are directly connected, can make sentences such as "The cat is an animal."
        if len(verbs) == 1:
            if A in [getWord(x) for x in CNdict[B]]:
                obj, sub = A, B
            else:
                obj, sub = B, A
            sentence.setObject("the " + obj.replace("_", " "))
            sentence.setSubject("the " + sub.replace("_", " "))
            sentence.setVerb(verbs[0])
            print(realiser.realiseSentence(sentence))
        # No direct or suitable indirect connections found, a connection is taken from one concept
        # and extended to the other, e.g "The nerve is in the human, the cake isn't".
        elif len(verbs) == 2:
            sentence.setSubject("the " + A.replace("_", " "))
            sentence.setObject(verbs[1].replace("_", " "))
            sentence.setVerb(verbs[0])
            if "is" in verbs[0]:
                print(realiser.realiseSentence(sentence), "As is", B.replace("_", " ")+".")
            else:
                print(realiser.realiseSentence(sentence), "As does", B.replace("_", " ")+".")
        # Both words are connected to the same concept.
        elif len(verbs) == 3:
            # both words have the same relation to shared concept
            if verbs[0] == verbs[1]:
                sentence.setObject(verbs[2].replace("_", " "))
                sentence.setSubject("the " + A.replace("_", " "))
                sentence.setVerb(verbs[0])
                if "is" in verbs[0]:
                    print(realiser.realiseSentence(sentence), "As is", B.replace("_", " ")+".")
                else:
                    print(realiser.realiseSentence(sentence), "As does", B.replace("_", " ")+".")
            else:
                print("The"+A, "is linked to", verbs[2], ", as is", B)



