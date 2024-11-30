# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        currentPositon = currentGameState.getPacmanPosition()
        walls = currentGameState.getWalls()
        food = currentGameState.getFood()

        ghostDistance = 0
        isGhostThere = False
        penalty = 0

        x, y = currentPositon
        cntWalls = 0
        cntArea = 0
        for i in range(max(0,  -2), min(x + 2, walls.width)):
            for j in range(max(0, -2), min(y + 2, walls.height)):
                cntArea += 1
                if walls[i][j]:
                    cntWalls += 1

        freeSpace = cntArea - cntWalls

        for ghost in newGhostStates:
            ghostPosition = ghost.getPosition()
            ghostDistance = manhattanDistance(newPos, ghostPosition)
            isGhostThere |= ghostPosition == newPos

        furthestDistance = manhattanDistance(currentPositon, (walls.height, walls.width))
        nearestFoodScore = furthestDistance - min([manhattanDistance(newPos, food) for food in newFood.asList()]) if newFood.asList() else 0

        totalScaredTimes = sum(newScaredTimes)

        if currentPositon == newPos:
            penalty = 0.1 * successorGameState.getScore()

        bonusEatGhost = 0
        if totalScaredTimes > 10:
            bonusEatGhost += 10 * (furthestDistance - ghostDistance)
            if isGhostThere:
                bonusEatGhost += 100
            ghostDistance = 0
        elif isGhostThere:
            return -10

        ghostDistance = min(ghostDistance, 10)

        bonusEatFood = 10 if food[newPos[0]][newPos[1]] else 0

        return successorGameState.getScore() + ghostDistance + nearestFoodScore + bonusEatFood + bonusEatGhost - penalty + freeSpace

def scoreEvaluationFunction(currentGameState: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns bestAction list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is bestAction winning state

        gameState.isLose():
        Returns whether or not the game state is bestAction losing state
        """
        "*** YOUR CODE HERE ***"

        def minimaxDecision(agentIndex: int, state: GameState):
            v = -2 ** 31
            bestAction = None
            numOfAgents = state.getNumAgents()

            for action in state.getLegalActions(agentIndex):
                result = minValue(0, (agentIndex + 1) % numOfAgents, state.generateSuccessor(agentIndex, action))
                if v < result:
                    v = result
                    bestAction = action
            return bestAction

        def minValue(depth:int, agentIndex: int, state: GameState) -> int:
            numOfAgents = state.getNumAgents()

            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)

            v = 2**31 - 1
            for action in state.getLegalActions(agentIndex):
                if agentIndex == numOfAgents - 1:
                    v = min(v, maxValue(depth + 1, 0, state.generateSuccessor(agentIndex, action)))
                else:
                    v = min(v, minValue(depth, agentIndex + 1, state.generateSuccessor(agentIndex, action)))
            return v

        def maxValue(depth:int, agentIndex: int, state: GameState) -> int:
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)

            v = -2**31
            for action in state.getLegalActions(agentIndex):
                v = max(v, minValue(depth, agentIndex + 1, state.generateSuccessor(agentIndex, action)))

            return v

        return minimaxDecision(0, gameState)

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def alphaBetaSearch(agentIndex: int, state: GameState):
            v = -2 ** 31
            bestAction = None
            numOfAgents = state.getNumAgents()
            alpha = -2**31
            beta = 2**31 - 1

            for action in state.getLegalActions(agentIndex):
                result = minValue(0, (agentIndex + 1) % numOfAgents, state.generateSuccessor(agentIndex, action), alpha, beta)
                if v < result:
                    v = result
                    bestAction = action
                alpha = max(alpha, v)
            return bestAction

        def minValue(depth:int, agentIndex: int, state: GameState, alpha, beta) -> int:
            numOfAgents = state.getNumAgents()

            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)

            v = 2**31 - 1
            for action in state.getLegalActions(agentIndex):
                if agentIndex == numOfAgents - 1:
                    v = min(v, maxValue(depth + 1, 0, state.generateSuccessor(agentIndex, action), alpha, beta))
                else:
                    v = min(v, minValue(depth, agentIndex + 1, state.generateSuccessor(agentIndex, action), alpha, beta))

                if v < alpha:
                    return v
                beta = min(beta, v)

            return v

        def maxValue(depth:int, agentIndex: int, state: GameState, alpha, beta) -> int:
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)

            v = -2**31
            for action in state.getLegalActions(agentIndex):
                v = max(v, minValue(depth, agentIndex + 1, state.generateSuccessor(agentIndex, action), alpha, beta))

                if v > beta:
                    return v
                alpha = max(alpha, v)
            return v

        return alphaBetaSearch(0, gameState)



class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
