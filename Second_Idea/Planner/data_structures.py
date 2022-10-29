from Robot.joint_state import JointState
import numpy as np

class Node:
    def __init__(self, joint_values):
        self.joint_values = joint_values #list of JointStates --> for robot with 3dof: need [JointState(angle1), JointState(angle2), JointState(angle3)]

    def vectorized_values(self):
        return np.array([self.joint_values[i].value for i in range(len(self.joint_values))])

    def equal_to(self, node):
        return np.array_equal(node.vectorized_values, self.vectorized_values)

class Edge:
    def __init__(self, node1, node2):
        self.node1 = node1
        self.node2 = node2
        self.weight = np.linalg.norm(node1.vectorized_values() - node2.vectorized_values())

    def vectorized_values(self):
        return np.array([self.node1.vectorized_values, self.node2.vectorized_values])

    def equal_to(self, edge):
        return np.array_equal(edge.vectorized_values, self.vectorized_values)

class Graph:
    def __init__(self, bidirected = True):
        self.nodes = []
        self.edges = []
        self.bidirected = bidirected

    def add_node(self, node):
        self.nodes.append(node)

    def add_edge(self, node1, node2):
        self.edges.append(node1, node2)

    def query_node_in_graph(self, node):
        for node_i in self.nodes:
            if node_i.is_equal(node):
                return True
        return False

    def query_edge_in_graph(self, edge):
        for edge_i in self.edges:
            if self.bidirected:
                if edge_i.is_equal(edge) or edge_i.is_equal(np.flip(edge)):
                    return True
            else:
                if edge_i.is_equal(edge):
                    return True
        return False



class TreeNode(Node):
    def __init__(self, joint_value, predecessor = None):
        super().__init__(joint_value)
        self.predecessor = predecessor
        self.successors = []
    
    def add_successor(self, successor):
        self.successors.append(successor)

    def add_predecessor(self, predecessor):
        self.predecessor.append(predecessor)

class Tree(Graph):
    def __init__(self):
        super().__init__()


    