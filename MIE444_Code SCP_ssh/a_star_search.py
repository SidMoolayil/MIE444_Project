import queue
import numpy as np
from search_problems import Node, get_maze_problem
from matplotlib import pyplot as plt


def a_star_search(problem):
    """
    :param problem: an instance of the maze, start, and goal to solve
    :return: path: a list of states (ints) describing the path from problem.init_state to problem.goal_state[0]
             num_nodes_expanded: number of nodes expanded by your search
             max_frontier_size: maximum frontier size during search (max branches along path)
    """
    # initialization
    max_frontier_size = 0
    num_nodes_expanded = 0
    path = []

    # setting up starting node
    state = problem.init_state
    action = problem.get_actions(state)
    parent = None
    node = Node(parent, state, action, 0)

    # check if starting node is goal node
    if problem.goal_test(node.state):
        path += [node.state]
        return path, num_nodes_expanded, max_frontier_size

    # initialization of search variables
    frontier = queue.PriorityQueue()
    frontier.put(((node.path_cost + problem.heuristic(node.state)), node))
    explored = set()

    while True:
        # if frontier is empty, no path exists, esentially looping until frontier empty or goal found
        if frontier.empty():
            return [], num_nodes_expanded, max_frontier_size

        # pop new node from frontier by priority (cost to get to node + cost from node to goal)
        node = frontier.get()[1]
        # record that the node has been visited
        explored.add(node.state)

        # check all possible children of the node
        for action in problem.get_actions(node.state):
            child = problem.get_child_node(node, action)

            # check if current child is goal node
            if problem.goal_test(child.state):
                path = problem.trace_path(child)
                return path, num_nodes_expanded, max_frontier_size

            # if child is new (not visited yet), add to frontier and record as visited
            if not(child.state in explored):
                num_nodes_expanded += 1
                frontier.put((child.path_cost + problem.heuristic(child.state), child))
                explored.add(child.state)

                # update max frontier size if needed
                if frontier.qsize() > max_frontier_size:
                    max_frontier_size = frontier.qsize()

def maze_solver(init, goal):
    # Create an instance of maze
    problem = get_maze_problem(init_state=init, goal_state=goal)
    # Solve it
    if problem != -1:
        path, num_nodes_expanded, max_frontier_size = a_star_search(problem)
        # Check the result
        #correct = problem.check_solution(path)
        #print("Solution is correct: {:}".format(correct))
        # Plot the result
        #problem.plot_solution(path)
    return path

def maze_solver_disp(init, goal):
    # Create an instance of maze
    problem = get_maze_problem(init_state=init, goal_state=goal)
    # Solve it
    if problem != -1:
        path, num_nodes_expanded, max_frontier_size = a_star_search(problem)
        # Check the result
        #correct = problem.check_solution(path)
        #print("Solution is correct: {:}".format(correct))
        # Plot the result
        plt.close('fig')
        problem.plot_solution(path)
    return path

if __name__ == '__main__':
    # Create an instance of maze
    problem = get_maze_problem(init_state = 29)
    # Solve it
    if problem != -1:
        path, num_nodes_expanded, max_frontier_size = a_star_search(problem)
        # Check the result
        correct = problem.check_solution(path)
        print("Solution is correct: {:}".format(correct))
        # Plot the result
        problem.plot_solution(path)
