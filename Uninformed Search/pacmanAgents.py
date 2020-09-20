# pacmanAgents.py
# ---------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from pacman import Directions
from game import Agent
from heuristics import *
import random
import math

class RandomAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # get all legal actions for pacman
        actions = state.getLegalPacmanActions()
        # returns random action from all the valide actions
        return actions[random.randint(0,len(actions)-1)]

class RandomSequenceAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        self.actionList = [];
        for i in range(0,10):
            self.actionList.append(Directions.STOP);
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # get all legal actions for pacman
        possible = state.getAllPossibleActions();
        for i in range(0,len(self.actionList)):
            self.actionList[i] = possible[random.randint(0,len(possible)-1)];
        tempState = state;
        for i in range(0,len(self.actionList)):
            if tempState.isWin() + tempState.isLose() == 0:
                tempState = tempState.generatePacmanSuccessor(self.actionList[i]);
            else:
                break;
        # returns random action from all the valide actions
        return self.actionList[0];

class HillClimberAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        self.actionList = [];
        for i in range(0, 5):
            self.actionList.append(Directions.STOP);
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # TODO: write Hill Climber Algorithm instead of returning Directions.STOP
        possible = state.getAllPossibleActions();
        for i in range(0,len(self.actionList)):
            self.actionList[i] = possible[random.randint(0,len(possible)-1)];
        bestSequenceList = self.actionList[:]
        firstSequence = True
        callLimit = False
        bestSeqScore = -101

        while callLimit is False:
            newSequence = bestSequenceList[:]
            if firstSequence is True:
                firstSequence = False
            else:
                for i in range(0,len(newSequence)):
                    if random.randint(0,1) == 1:
                        newSequence[i] = possible[random.randint(0,len(possible) - 1)]
            tempState = state
            for i in range (0, len(newSequence)):
                if tempState.isWin() or tempState.isLose():
                    break
                else:
                    state1 = tempState
                    tempState = tempState.generatePacmanSuccessor(newSequence[i]);
                    if tempState is None:
                        callLimit = True
                        tempState = state1
                        break
            tempSeqScore = gameEvaluation(state,tempState)
            if tempSeqScore > bestSeqScore:
                bestSeqScore = tempSeqScore
                bestSequenceList = newSequence[:]


        return bestSequenceList[0]






class GeneticAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):

        self.actionList = [];
        for i in range(0, 5):
            self.actionList.append(Directions.STOP);
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # TODO: write Genetic Algorithm instead of returning Directions.STOP
        self.chromosomeList = []
        possible = state.getAllPossibleActions();
        defaultGameScore = -101
        for i in range(0, 8):
            for j in range(0, 5):
                self.actionList[j] = possible[random.randint(0, len(possible) - 1)]
            chromosomescore = []
            chromosomescore.append(self.actionList[:])
            chromosomescore.append(defaultGameScore)
            self.chromosomeList.append(chromosomescore[:])

        callLimit = False

        while callLimit is False:
            for j in range(0, 8):
                tempState = state
                for i in range(0, 5):
                    if tempState.isWin() or tempState.isLose():
                        break
                    else:
                        state1 = tempState
                        tempState = tempState.generatePacmanSuccessor(self.chromosomeList[j][0][i]);
                        if tempState is None:
                            callLimit = True
                            tempState = state1
                            break
                tempSeqScore = gameEvaluation(state, tempState)
                self.chromosomeList[j][1] = tempSeqScore
            self.chromosomeList.sort(key=lambda x: x[:][1], reverse=True)
            bestSequence = self.chromosomeList[0][:]
            newChromosomeList = []
            for k in range(0, 4):
                parent1 = self.chromosomeList[self.selectParentRank()][0][:]
                parent2 = self.chromosomeList[self.selectParentRank()][0][:]
                if random.randint(1,10) < 8:

                    child = []
                    for l in range(0,2):
                        for z in range(0,5):
                            if random.randint(0,1) == 1:
                                child.append(parent1[z])
                            else:
                                child.append(parent2[z])
                        newChromosomeList.append(child)
                else:
                    newChromosomeList.append(parent1)
                    newChromosomeList.append(parent2)

                for y in range (0,len(newChromosomeList)):
                    if random.randint(1,10) == 1:
                        newChromosomeList[y][random.randint(0, 4)] = possible[random.randint(0, len(possible)-1)]

            self.chromosomeList = []
            for a in range(0,len(newChromosomeList)):
                chromosome = []
                chromosome.append(newChromosomeList[a][:])
                chromosome.append(defaultGameScore)
                self.chromosomeList.append(chromosome[:])


        return bestSequence[0][0]

    def selectParentRank(self):
        x = random.randint(1, 36)
        if x < 9:
            return 0
        elif x < 16:
            return 1
        elif x < 22:
            return 2
        elif x < 27:
            return 3
        elif x < 31:
            return 4
        elif x < 34:
            return 5
        elif x < 36:
            return 6
        elif x < 37:
            return 7

#MCTS
class Tree:
    def __init__(self, action, state):
        self.children = []
        self.expandedChildren = 0
        self.action = action
        self.visited = 1
        self.parent = None
        self.currentState = state
        self.score = 0

class MCTSAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # TODO: write MCTS Algorithm instead of returning Directions.STOP

        global callLimit
        callLimit = False
        rootNode = Tree(None,state)
        maxScore = -101
        action = state.getLegalPacmanActions()
        x = random.randint(0,len(action)-1)
        while callLimit is False:
            selectedNode = self.treePolicy(state, rootNode)
            if selectedNode is None:
                break
            if selectedNode != 0:
                try:
                    reward = self.defaultPolicy(state, selectedNode)
                except :
                    print(selectedNode)
            else:
                continue
            self.backup(selectedNode, reward)

        rootNodeChildren = rootNode.children[:]
        finalChildren = []
        for child1 in rootNodeChildren:
            if child1.score > maxScore:
                maxScore = child1.score
                finalChildren = []
                finalChildren.append(child1)
            elif child1.score == maxScore:
                finalChildren.append(child1)
        try:
            a = random.randint(0,len(finalChildren)-1)
        except:
            return action[x]
        child2 = finalChildren[a]
        return child2.action



    def defaultPolicy(self,state , selectedNode):
        currentState = selectedNode.currentState
        for i in range(0,5):
            if currentState.isWin() or currentState.isLose():
                break
            else:
                actions = currentState.getLegalPacmanActions()
                if len(actions) == 0:
                    break
                a = random.randint(0, len(actions)-1)
                state1 = currentState
                currentState = currentState.generatePacmanSuccessor(actions[a])
                if currentState is None:
                    global noneReached
                    currentState = state1
                    noneReached = True
                    break

        rewardScore = gameEvaluation(state,currentState)
        return rewardScore



    def treePolicy(self,state,rootNode):
        node = rootNode
        tempFlag = True
        while tempFlag is True:
            if node.expandedChildren == -1:
                node = self.nodeSelection(node)
            else:
                tempFlag = False

        currentState = node.currentState
        legal = currentState.getLegalPacmanActions()
        usedAction = []
        for children1 in node.children:
            usedAction.append(children1.action)

        for action in legal:
            if action not in usedAction:
                newState = currentState.generatePacmanSuccessor(action)
                if newState is None:
                    self.backup(node, gameEvaluation(state,currentState))
                    return None
                if newState.isWin() or newState.isLose():
                    self.backup(node, gameEvaluation(state,newState))
                    return 0
                childNode = Tree(action,newState)
                childNode.parent = node
                node.children.append(childNode)
                node.expandedChildren = node.expandedChildren + 1
                break
        if len(legal) == len(node.children):
            node.expandedChildren = -1

        return node.children[-1]

    def nodeSelection(self, parentNode):
        bestScore = -101
        selectedChildren = []
        for child in parentNode.children:
            exploit = child.score / child.visited
            explore = math.sqrt((2*math.log(parentNode.visited))/child.visited)
            ucbValue = exploit + (1*explore)
            if ucbValue > bestScore:
                bestScore = ucbValue
                selectedChildren.append(child)
            if ucbValue == bestScore:
                selectedChildren.append(child)

        a = random.randint(0, len(selectedChildren) - 1)
        return selectedChildren[a]


    def backup(self, node, score):
        while node is not None:
            node.visited = node.visited + 1
            node.score = node.score + score
            node = node.parent
        return


