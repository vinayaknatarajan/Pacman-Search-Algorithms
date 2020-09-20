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


#NetID: vn686

from pacman import Directions
from game import Agent
from heuristics import *
from collections import deque
import random

# Example datastructure format: alist = [[(a,b,10),(a,b,11),(a,b,12),(a,b,13),(a,b,14)] , [(a,b,20),(a,b,21),(a,b,22),(a,b,23),(a,b,24)], [(a,b,30),(a,b,31),(a,b,32),(a,b,33),(a,b,34)]]
i = 0
successorArray = deque([])
dfsArray = []
aStarArray = []


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

class OneStepLookAheadAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # get all legal actions for pacman
        legal = state.getLegalPacmanActions()
        # get all the successor state for these actions
        successors = [(state.generatePacmanSuccessor(action), action) for action in legal]
        # evaluate the successor states using scoreEvaluation heuristic
        scored = [(admissibleHeuristic(state), action) for state, action in successors]
        # get best choice
        bestScore = min(scored)[0]
        # get all actions that lead to the highest score
        bestActions = [pair[1] for pair in scored if pair[0] == bestScore]
        # return random action from the list of the best actions
        return random.choice(bestActions)

class BFSAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
       return;


    # GetAction Function: Called with every frame
    def getAction(self, state):
        # TODO: write BFS Algorithm instead of returning Directions.STOP
        visited = []
        leafNodes=[]
        state1 = (state, "start")
        successorArray.append([state1])

        while successorArray:
            # Getting the Node that was pushed into the queue first
            AllNodes = successorArray.popleft()

            currentState = AllNodes[-1][0]

            if currentState.isWin():
                return AllNodes[1][1]
            if currentState.isLose():
                continue
            if currentState not in visited:
                visited.append(currentState)
                legal = currentState.getLegalPacmanActions()
                for l in legal:
                    succesor=(currentState.generatePacmanSuccessor(l), l)
                    if succesor[0] is None:
                        #Adding leaf nodes
                        leafNodes.append(AllNodes)
                        break
                    else:
                        AllNodesAdd = AllNodes[:]
                        AllNodesAdd.append(succesor)
                        #Adding nodes to queue to be expanded
                        successorArray.append(AllNodesAdd)

        min=admissibleHeuristic(leafNodes[0][-1][0])
        minAction=leafNodes[0][1][1]
        #calculating heuristics for leaf nodes
        for leaf in leafNodes:
            adhr=admissibleHeuristic(leaf[-1][0])
            if adhr<min:
                min=adhr
                minAction=leaf[1][1]
        return minAction


class DFSAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # TODO: write DFS Algorithm instead of returning Directions.STOP
        leafNodes = []
        state1 = (state, "start")
        dfsArray.append([state1])

        while dfsArray:
            # Getting the node that was pushed last
            AllNodes = dfsArray.pop()
            currentState = AllNodes[-1][0]

            if currentState.isWin():
                return AllNodes[1][1]
            if currentState.isLose():
                continue

            legal = currentState.getLegalPacmanActions()
            for l in legal:
                succesor = (currentState.generatePacmanSuccessor(l), l)
                if succesor[0] is None:
                    # Adding leaf nodes
                    leafNodes.append(AllNodes)
                    break
                else:
                    # Adding nodes to stack
                    AllNodesAdd = AllNodes[:]
                    AllNodesAdd.append(succesor)
                    dfsArray.append(AllNodesAdd)

        min = admissibleHeuristic(leafNodes[0][-1][0]) + len(leafNodes[0]) - 1
        minAction = leafNodes[0][1][1]
        for leaf in leafNodes:
            adhr = admissibleHeuristic(leaf[-1][0]) + len(leaf) - 1
            if adhr < min:
                min = adhr
                minAction = leaf[1][1]
        return minAction

class AStarAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # TODO: write A* Algorithm instead of returning Directions.STOP
        visited = []
        leafNodes = []
        state1 = (state, "start", admissibleHeuristic(state))
        aStarArray.append([state1])

        while aStarArray:
            # Sorting All nodes based on f(n)(total cost) value in descending order
            aStarArray.sort(key = lambda x: x[-1][-1], reverse = True)
            AllNodes = aStarArray.pop()
            currentState = AllNodes[-1][0]

            if currentState.isWin():
                return AllNodes[1][1]
            if currentState.isLose():
                continue
            #if currentState not in visited:
            visited.append(currentState)
            legal = currentState.getLegalPacmanActions()
            for l in legal:
                succesor = (currentState.generatePacmanSuccessor(l), l)
                if succesor[0] is None:
                    leafNodes.append(AllNodes)
                    break
                else:
                    succesor = succesor + (admissibleHeuristic(currentState) + len(AllNodes),)
                    AllNodesAdd = AllNodes[:]
                    AllNodesAdd.append(succesor)
                    aStarArray.append(AllNodesAdd)
        #calculating total cost from leaf nodes
        min = admissibleHeuristic(leafNodes[0][-1][0]) + len(leafNodes[0]) - 1
        minAction = leafNodes[0][1][1]
        for leaf in leafNodes:
            adhr = admissibleHeuristic(leaf[-1][0]) + len(leaf) - 1
            if adhr < min:
                min = adhr
                minAction = leaf[1][1]
        return minAction
