import time
import random
import fileinput

# The object for each vertex state, holds the states name, connections, color and
# Potential colors the state can be, which is used in the backtracking method
class State:
    # States have color and adajacent states unknown upon initialization
    def __init__(self, name, colors):
        self.name = name
        self.color = ''
        self.colorSet = []
        self.makeColorSet(colors)
        self.adjacent = []
        self.numOfConnections = 0
    
    # Otherwise all states share the same color set
    def makeColorSet(self, givenColors):
        for color in givenColors:
            self.colorSet.append(color)
    
    def addAdjacent(self, toAdd):
        self.adjacent.append(toAdd)

#Will be started from the node with most children
# Tries color in potential, if it doesnt work for children tried a new color
# and tests children again
def backtrack(state):
    global steps
    # Will try colors, return false if none work, resets the potential colors
    # when none work
    steps += 1
    for testColor in colors:
        # The color must be a possible candidate before testing
        state.color = testColor
        colorWorks = True
        # Tests if the testColor works first by checking adjacent
        for adjState in state.adjacent:
            if adjState.color == testColor:
                state.colorSet.remove(testColor)
                colorWorks = False
                break
        # If it is still in the possible colors, start recursive call
        # Only calls on neighbors that dont have any color assigned yet
        if colorWorks:
            for adjState in state.adjacent:
                if adjState.color == '':
                    if not backtrack(adjState):
                        state.colorSet.remove(testColor)
        else:
            continue
        # Will only be true still if it works for children,
        # keeps other possible test colors
        if testColor in state.colorSet:
            return True
        else:
            if len(state.colorSet) == 0:
                state.colorSet = colors
                state.color = ''
                return False
    print("Some error") 
    return False

# Generates a random start state, gives each state a random color
def generateStart(stateStrings, colors):
    for stateString in stateStrings:
        state = allStates.get(stateString)
        randomColor = random.randrange(len(colors))
        state.color = colors[randomColor]

# Print out the states and their corresponding colors
def showResult():
    print("A solution was found in " + str(steps) + " steps")
    print("The colors are:")
    for stateString in allStates:
        state = allStates.get(stateString)
        print(state.name + ": " + state.color)

# Gives a list of all the states that need to be changed
def invalidVertices(stateSet):
    invalidStates = []
    for state in stateSet:
        for adjState in state.adjacent:
            if state.color == adjState.color:
                invalidStates.append(state)
    return invalidStates

# Gives all the states a random color        
def randomizeColors(toRandomize, incorrectStates):
    for state in toRandomize:
        if state in incorrectStates:
            foundColor = False
            for testColor in colors:
                result = True
                for adjStates in state.adjacent:
                    if adjStates.color == testColor:
                        result = False
                if result:
                    state.color = testColor
            if not foundColor:
                randomNumber = random.randrange(len(colors))
                state.color = colors[randomNumber]
# The local search alogrithm, done by taking the random starting colors 
# and changing the incorrect ones to get more correct ones
def localSearch():
    global steps
    currentScore = len(invalidVertices(list(allStates.values())))
    endTime = time.time() + 120
    counter = 0
    while time.time() < endTime:
        steps += 1
        if currentScore == 0:
            break
        trialColors = list(allStates.values()).copy()
        incorrectTrialColors = invalidVertices(trialColors)
        randomizeColors(trialColors, incorrectTrialColors)
        newScore = len(invalidVertices(trialColors))
        if newScore <= currentScore:
            currentScore = newScore
            for trialState in trialColors:
                stateName = trialState.name
                allStates.get(stateName).color = trialState.color
        counter += 1
        if counter > 75:
            generateStart(allStates.keys(), colors)
            currentScore = len(invalidVertices(list(allStates.values())))
    if currentScore == 0:
        showResult()
    else:
        print("Could not find solution in " + str(steps) + " steps")

#loop reads in input lines, starts with one, breaks when it is empty
# The first loop reads in possible colors
collectColors = True
collectStates = True
colors = []
allStates = {}
for line in fileinput.input():
  line = line.rstrip()
  if collectColors:
    if line.strip() == '':
      collectColors = False
      continue
    else:
      colors.append(line)
      continue
  if collectStates:
    if line.strip() == '':
      collectStates = False
      continue
    else:
      allStates[line] = State(line, colors)
      continue
  else:
    space = line.find(" ")
    firstState = line[:space]
    if firstState not in allStates:
      print("There was an error splitting the line")
      sys.exit()
    secondState = line[space + 1:]
    firstStateObject = allStates.get(firstState)
    secondStateObject = allStates.get(secondState)
    firstStateObject.addAdjacent(secondStateObject)
    secondStateObject.addAdjacent(firstStateObject)


print("Map made")

# Finds the state with the most states to begin the backtracking algorithm
highestConnections = 0
highestState = None
noConnections = []
for state in allStates.values():
    state.numOfConnections = len(state.adjacent)
    if state.numOfConnections == 0:
        noConnections.append(state)
    if state.numOfConnections > highestConnections:
        highestConnections = state.numOfConnections
        highestState = state

# The calling of backtracking, keeps track of the number of loops that must be done
print("Start backtrack")
steps = 0
# How I impemented the back tracking would not find states without connections
# must program for them in case
if len(noConnections) > 0:
    for state in noConnections:
        state.color = colors[0]
alreadyTested = []
alreadyTested.append(highestState)
if backtrack(highestState):
    showResult()
# If the most constrained index didnt work, will try calling it on every index
else :
    print("testing other indices index")
    for stateString in allStates:
        state = allStates.get(stateString)
        if state not in alreadyTested:
            if backtrack(state):
                showResult()
                break
            else :
                alreadyTested.append(state)
                print("testing new vertex")
    
# Now will generate a result using the local search method
print("Starting local search")
steps = 0
generateStart(allStates, colors)
localSearch()

    
