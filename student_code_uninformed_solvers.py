
from solver import *
from Lib import queue

class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes her
        
        if self.currentState.state == self.victoryCondition: return True
        self.visited[self.currentState] = True
        nextMoves = self.gm.getMovables()
        if nextMoves == False:
            self.gm.reverseMove(self.currentState.requiredMovable)
            self.currentState = self.currentState.parent
            return False
        for move in nextMoves:
            self.gm.makeMove(move)
            childState = GameState(self.gm.getGameState(),0,move)
            if childState in self.visited: 
                self.gm.reverseMove(move)
                continue # can just continue, cause we should never revisit a child node
            childState.parent = self.currentState
            self.currentState = childState
            return False
        



class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)
        self.visitQueue = queue.Queue()
        #Assemble a list of the children of the root
        nextMoves = self.gm.getMovables()
        for move in nextMoves:
            self.gm.makeMove(move)
            childState = GameState(self.gm.getGameState(), self.currentState.depth + 1, move)
            if childState.state == self.victoryCondition: return True
            if childState in self.visited: 
                self.gm.reverseMove(move)
                continue # can just continue, cause we should never revisit a child node
            self.visited[childState] = True
            childState.parent = self.currentState
            self.visitQueue.put(childState)
            self.gm.reverseMove(move)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        
        #keep a FIFO queue
        #Until at desired nodes / at root, back up the tree
        #If reach root, construct a chain of moves from node to root
        #descend from parent to new node
        #At node, generate children, check if each is victory / already visited
        #If not, then add child to queue

        #Get to the next node to visit
        stateToVisit = self.visitQueue.get()
        movesFromTarget = []
        targetBacktrackNode = stateToVisit
        while self.currentState.depth != 0 and self.currentState != targetBacktrackNode:
            self.gm.reverseMove(self.currentState.requiredMovable)
            self.currentState = self.currentState.parent
            movesFromTarget.append(targetBacktrackNode.requiredMovable)
            targetBacktrackNode = targetBacktrackNode.parent

        if self.currentState == targetBacktrackNode:
            while movesFromTarget != []:
                self.gm.makeMove(movesFromTarget.pop())
            self.currentState = stateToVisit

        if self.currentState.depth == 0 or self.currentState != stateToVisit:
            while self.currentState != targetBacktrackNode:
                movesFromTarget.append(targetBacktrackNode.requiredMovable)
                targetBacktrackNode = targetBacktrackNode.parent
            while movesFromTarget != []:
                self.gm.makeMove(movesFromTarget.pop())
            self.currentState = stateToVisit
        
        #At this point, we should be at the desired state
        #Check if children are winners / already visited
        #if not, add them to the queue
        nextMoves = self.gm.getMovables()
        for move in nextMoves:
            self.gm.makeMove(move)
            childState = GameState(self.gm.getGameState(), self.currentState.depth + 1, move)
            if childState.state == self.victoryCondition: return True
            if childState in self.visited: 
                self.gm.reverseMove(move)
                continue # can just continue, cause we should never revisit a child node
            self.visited[childState] = True
            childState.parent = self.currentState
            self.visitQueue.put(childState)
            self.gm.reverseMove(move)