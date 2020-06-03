"""
Contains methods that use infrastructure developed to actually generate stories.
Different stories are defined. A "nameStory" selects surnames from one of the lists below, performs mappings to
visualisable objects, sorts the mappings and generates the stories.

"userStory" generates a story based on user input, "connectedStory" generates a story based on "well-connected" input,
i.e. a list that can be sorted so that each word pair is directly connected. "randomStory" generates a story based on
randomly selected visualisable objects.

The actual story generator algorithms are contained in "simpleStory.py". The only difference between cnStory and
shorter story is in how sentences are presented.
"""
import csv, random
from mapToVisualisableObjects import *
from simpleStory import *

rugbyTeam = ["Will Addison", "Bundee Aki", "Billy Burns", "Ross Byrne", "Will Connors", "Andrew Conway",
             "John Cooney", "Max Deegan", "Ultan Dilane", "Caelan Doris", "Keith Earls", "Chris Farrell",
             "Tadhg Furlong", "Cian Healy", "Dave Heffernan", "Iain Henderson", "Robbie Henshaw", "Rob Herring",
             "David Kearney", "Ronan Kelleher", "Dave Kilcoyne", "Jordan Larmour", "Stuart McCloskey", "Jack McGrath",
             "Conor Murray", "Jack O' Donoghue", "Peter O' Mahony", "Tom O' Toole", "Andrew Porter", "Garry Ringrose",
             "James Ryan", "Johnny Sexton", "CJ Stander", "Jacon Stockdale", "Devin Toner", "Josh van der Flier"]
nobelWinners = ['Riccardo Giacconi', 'Ernst Ruska', 'Pyotr Leonidovich Kapitsa', 'Dennis Gabor', 'Hans Albrecht Bethe',
                'Donald Arthur Glaser', 'Sir Edward Victor Appleton', 'Wolfgang Pauli', 'Carl David Anderson',
                'Victor Franz Hess', 'James Chadwick', 'Sir Chandrasekhara Venkata Raman',
                'Prince Louis-Victor Pierre Raymond de Broglie', 'Karl Manne Georg Siegbahn', 'Robert Andrews Millikan',
                'Max von Laue', 'Wilhelm Wien', 'Johannes Diderik van der Waals', 'Gabriel Lippmann',
                'Philipp Eduard Anton von Lenard', 'Yasser Arafat', 'Joseph Rotblat', 'Carlos Filipe Ximenes Belo',
                'Kim Dae-jung', 'Shirin Ebadi', 'Wangari Muta Maathai', 'Muhammad Yunus', 'Martti Ahtisaari',
                'Liu Xiaobo', 'Ellen Johnson Sirleaf', 'Kailash Satyarthi', 'Juan Manuel Santos', 'Aung San Suu Kyi']
fictionalCharacters = ["Randall Flagg", "Roland Deschain", "Oy", "Eddie Dean", "Jake Chambers",
                      "Father Callahan", "Cutherbert Allgood", "Susannah Dean", "Steve Deschain",
                      "Alain Johns", "Jamie De Curry", "Susan Delgado", "Sheemie Ruiz", "Thomas Whitman"]


# randomly sample |number| elements from one of the lists of surnames
def getSurnames(category, number):
    return random.sample(category, number)


# map each name to a visualisable word using methodsd developed in "mapToVisualisableObjects"
def mapSurnames(surnames):
    alreadyPicked = []
    for name in surnames:
        options = []
        parts = name.split(" ")
        for part in parts:
            # print(part, mapWord(part))
            options = ([x for x in mapWord(part)])
        # (name, ":", options)

        if len(options) > 0:
            for opt in options:
                if opt[0] not in alreadyPicked:
                    alreadyPicked.append(opt[0])
                    print(name, ":", opt[0])
                    break
        else:
            # no mapping found, select a word that starts with the same letter!
            for word in vWords:
                if word[0].lower() == name[0].lower() and word not in alreadyPicked:
                    alreadyPicked.append(word)
                    print(name, ": no mapping found, chose", word)
                    break
    return alreadyPicked


# generate a story using methods in "simpleStory"
# type can be "n" to use Nobel Prize winners, "r" to use the Irish rugby team and "f" to use fictional character names.
def nameStory(type):
    if type == "n":
        # sn = getSurnames(nobelWinners, 10)
        sn = ['Karl Manne Georg Siegbahn', 'Aung San Suu Kyi', 'Prince Louis-Victor Pierre Raymond de Broglie', 'Ernst Ruska', 'Gabriel Lippmann', 'Wolfgang Pauli', 'Kim Dae-jung', 'Donald Arthur Glaser', 'Yasser Arafat', 'Hans Albrecht Bethe']
    elif type == "r":
        sn = getSurnames(rugbyTeam, 10)
    elif type == "f":
        sn = getSurnames(fictionalCharacters, 10)
    else:
        print("invalid type")
        return
    print("Names are:" , sn)
    mps = mapSurnames(sn)
    print("\nMappings are: ", mps)
    orderedMps = orderWords(mps)
    print("Sorted to be:", orderedMps, "\n")
    cnStory(orderedMps)
    shorterStory(orderedMps)


# asks user to input |numEle| words that are sent to generateStory()
def userStory(numEle):
    userInput = getInput(numEle)
    generateStory(userInput)


# selects 10 random words from the list of visualisable objects and sends them to generateStory()
def randomStory(numEle):
    ranInput = randomInput(numEle)
    generateStory(ranInput)


# gets input from wellConnectedInput, which begins with a randomly selected word and then fills the list with a chain of
# directly connected concepts, then sends list to generateStory()
def connectedStory(numEle):
    goodInput = wellConnectedInput(numEle)
    print("Input before being shuffled:", goodInput)
    random.shuffle(goodInput)
    generateStory(goodInput)


# print input, sort the input and then call story generator with ordered input
def generateStory(words):
    print("Input is: ", words)
    ordered = orderWords(words)
    print("Sorted input is: ", ordered)
    # cnStory(ordered)
    shorterStory(ordered)


# randomStory(10)  # story is generated from a list of ten randomly selected visualisable objects
# userStory(10)  # story is generated from a list of 10 user inputted nouns (nouns must be in ConceptNet)
# connectedStory(10)  # generates a story from input that contains a lot of direct connections
# nameStory("r")  # generates a story from a list of surnames. The surnames are mapped to visualisable objects


