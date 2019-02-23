from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### student code goes here
        result = []
        for i in range(1,4):
            onBindings = self.kb.kb_ask(parse_input('fact: (on ?disk peg' + str(i) + ')'))
            disksOnPeg = []
            if onBindings == False: 
                result.append(())
                continue
            for bind in onBindings:
                disksOnPeg.append(int(bind.bindings[0].constant.element[-1:]))
            disksOnPeg.sort()
            result.append(tuple(disksOnPeg))
        return tuple(result)



    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        pred = movable_statement.predicate
        sl = movable_statement.terms
        self.kb.kb_retract(Fact(Statement(["on", sl[0],sl[1]])))
        self.kb.kb_retract(Fact(Statement(["topof", sl[0], sl[1]])))
        potentialNewTop = self.kb.kb_ask(parse_input('fact: (ontopof ' + sl[0].term.element + " ?disk)"))
        #Determine if inital peg is now empty or has a new top
        if potentialNewTop != False:
            potentialNewTop = potentialNewTop[0].bindings[0].constant.element
            self.kb.kb_retract(Fact(Statement(["ontopof",sl[0],potentialNewTop])))
            self.kb.kb_assert(Fact(Statement(["topof", potentialNewTop, sl[1]])))
        else: 
            self.kb.kb_assert(Fact(Statement(["empty",sl[1]])))
        #Determine if the target peg is empty or already has disks
        if self.kb.kb_ask(parse_input('fact: (empty ' + sl[2].term.element + ')')) == False:
            oldTop = self.kb.kb_ask(parse_input('fact: (topof ?disk ' + sl[2].term.element + ')'))
            oldTop = oldTop[0].bindings[0].constant.element
            self.kb.kb_retract(Fact(Statement(["topof", oldTop, sl[2]])))
            self.kb.kb_assert(Fact(Statement(["ontopof", sl[0], oldTop])))
        else: 
            self.kb.kb_retract(Fact(Statement(["empty",sl[2]])))
        
        self.kb.kb_assert(Fact(Statement(["on",sl[0],sl[2]])))
        self.kb.kb_assert(Fact(Statement(["topof",sl[0],sl[2]])))
        




    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### Student code goes here
        result = []
        for i in range(1,4):
            tilesInRow = []
            for j in range(1,4):
                #breakpoint()
                tile = self.kb.kb_ask(parse_input('fact: (at ?tile pos' + str(j) + ' pos' + str(i) + ')'))
                tile = tile[0].bindings[0].constant.element
                if (tile == 'empty'):
                    tilesInRow.append(-1)
                else:
                    tilesInRow.append(int(tile[-1:]))
            result.append(tuple(tilesInRow))

        return tuple(result)
                


    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        pred = movable_statement.predicate
        sl = movable_statement.terms
        self.kb.kb_retract(Fact(Statement(["at",sl[0],sl[1],sl[2]])))
        self.kb.kb_retract(Fact(Statement(["at","empty",sl[3],sl[4]])))
        self.kb.kb_assert(Fact(Statement(["at",sl[0],sl[3],sl[4]])))
        self.kb.kb_assert(Fact(Statement(["at","empty",sl[1],sl[2]])))


    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
