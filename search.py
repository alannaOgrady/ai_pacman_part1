# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
import heapq

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()

class Node:
    """docstring for ClassName"""
    def __init__(self, state, actions):
        self.state = state
        self.actions = actions
        

def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]




#altered the update function to allow us to update the actions taken to node (if cost was smaller)
def update_with_actions(frontier, node, priority):
    # If item already in priority queue with higher priority, update its priority and rebuild the heap.
    # If item already in priority queue with equal or lower priority, do nothing.
    # If item not in priority queue, do the same thing as self.push.
    for index, (p, c, i) in enumerate(frontier.heap):
        if i.state == node.state:
            if p <= priority:
                break
            del frontier.heap[index]
            frontier.heap.append((priority, c, node))
            heapq.heapify(frontier.heap)
            break
    else:
        frontier.push(node, priority)

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    #initialise LIFO queue and visited array
    frontier = util.Stack()
    visistedArray = []
    frontier.push(Node(problem.getStartState(), []))
    visistedArray.append(problem.getStartState())
    sucessor_list = []

    #while still nodes to search
    while not frontier.isEmpty():
        #get new state
        #get action taken
        #directions to goal will be actions which have not been popped off the stack
        node = frontier.pop()
        state = node.state
        actions_taken = node.actions
        visistedArray.append(state)
        if problem.isGoalState(state):
            return actions_taken
        
        #get successors which has not been visited and add to stack
        sucessor_list = problem.getSuccessors(state)
        for element in sucessor_list:

            next_sucessor = element[0]
            next_action = element[1]
            if next_sucessor not in visistedArray:
                #otehrwise add successor to frontier to continue search
                frontier.push(Node(next_sucessor, actions_taken + [next_action]))


    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    #initialise LIFO queue and visited array
    frontier = util.Queue()
    visistedArray = []
    frontier.push(Node(problem.getStartState(), []))
    visistedArray.append(problem.getStartState())
    sucessor_list = []
    

    #while still nodes to search
    while not frontier.isEmpty():
        #get new state
        #get action taken
        #directions to goal will be actions which have not been popped off the stack
        node = frontier.pop()
        state = node.state
        actions_taken = node.actions
        #print state
        
        if problem.isGoalState(state):
            return actions_taken
        
        #get successors which has not been visited and add to stack
        sucessor_list = problem.getSuccessors(state)
        for element in sucessor_list:
            next_sucessor = element[0]
            next_action = element[1]
            if next_sucessor not in visistedArray:
                #otherwise add successor to frontier to continue search
                frontier.push(Node(next_sucessor, actions_taken + [next_action]))
                visistedArray.append(next_sucessor)
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""

    frontier = util.PriorityQueue()
    visistedArray = []
    frontier.push(Node(problem.getStartState(), []), 0)
    visistedArray.append(problem.getStartState())
    sucessor_list = []
    

    #while still nodes to search
    while not frontier.isEmpty():
        #get new state
        #get action taken
        #directions to goal will be actions which have not been popped off the stack
        node = frontier.pop()
        state = node.state
        actions_taken = node.actions
        
        if problem.isGoalState(state):
                    return actions_taken
        #marking as visited after popping from queue as there may be multiple ways to get to particular node and we want to find smallest
        if state not in visistedArray:
            visistedArray.append(state)
        #get successors which has not been visited and add to stack
        sucessor_list = problem.getSuccessors(state)
        for element in sucessor_list:
            next_sucessor = element[0]
            next_action = element[1]
            #check cost
            cost = problem.getCostOfActions(actions_taken + [next_action])
            #print next_sucessor, cost
            if next_sucessor not in visistedArray:
                #add to queue or update path if smaller
                update_with_actions(frontier, Node(next_sucessor, actions_taken + [next_action]), cost)

    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    frontier = util.PriorityQueue()
    visistedArray = []
    #add node of start state and no actions and combination of heurisitc and actual path cost (right now just heuristic) to priority queue
    frontier.push(Node(problem.getStartState(), []), heuristic(problem.getStartState(), problem))
    visistedArray.append(problem.getStartState())
    sucessor_list = []
    

    #while still nodes to search
    while not frontier.isEmpty():
        #get new state
        #get action taken
        #directions to goal will be actions which have not been popped off the stack
        node = frontier.pop()
        state = node.state
        actions_taken = node.actions
        
        if problem.isGoalState(state):
                    return actions_taken
        #marking as visited after popping from queue as there may be multiple ways to get to particular node and we want to find smallest
        if state not in visistedArray:
            visistedArray.append(state)
        #get successors which has not been visited and add to stack
        sucessor_list = problem.getSuccessors(state)
        for element in sucessor_list:
            next_sucessor = element[0]
            next_action = element[1]
            #check cost
            cost = problem.getCostOfActions(actions_taken + [next_action])
            combo = cost + heuristic(next_sucessor, problem)
            #print next_sucessor, cost
            if next_sucessor not in visistedArray:
                #add to queue or update path if smaller
                update_with_actions(frontier, Node(next_sucessor, actions_taken + [next_action]), combo)

    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
