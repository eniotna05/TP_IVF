
from affectation_list import *
from condition_list import *
from result_fonctions import *





class Node:

    def __init__(self, id, condition, affectations, true_children, false_children):

        self.condition = condition
        self.true = None
        self.false = None
        self.affectations = affectations
        self.id = id

class ConditionNode(Node):

    def __init__(self, id, condition):

        self.condition = condition
        self.true = None
        self.false = None
        self.affectations = skip
        self.id = id


class AffectationNode(Node):

    def __init__(self, id, affectations):
        self.condition = alwaystrue
        self.true = None
        self.false = None
        self.affectations = affectations
        self.id = id


class EndNode(Node):

    def __init__(self, id, result_function):
        self.condition = alwaystrue
        self.true = None
        self.false = None
        self.affectations = None
        self.id = id
        self.result = result_function


class ControlGraph:

    def __init__(self, list_of_node, relationships ,number_of_variables):
        self.list_of_node = list_of_node
        self.rootnode = list_of_node[0]
        self.relationships = relationships
        self.number_of_variables = number_of_variables

        for relation in relationships:
            node = self.fetch_node(relation[0])
            if relation[2] == True:
                node.true = self.fetch_node(relation[1])
            else:
                node.false = self.fetch_node(relation[1])

    def fetch_node(self, id):
        for node in self.list_of_node:
            if node.id == id:
                return node


    def go_through_node(self, node,  variable_list):

        if node.condition(variable_list) == True:
            next_node = node.true
        else:
            next_node = node.false
        variable_list = node.affectations(variable_list)
        return (next_node, variable_list)


    def function_test(self,input):

        if len(input) != self.number_of_variables:
            raise AssertionError("Number of variables provided is not correct")

        variable_list = input
        next_node = self.rootnode




        while not isinstance(next_node, EndNode):
            print("node number = " + str(next_node.id) )
            print("variables = " + str(variable_list) + "\n")

            next_node, variable_list = self.go_through_node(next_node, variable_list)

        print("node number = " + str(next_node.id) )
        print("variables = " + str(variable_list) + "\n")
        print("Result of function below")
        next_node.result(variable_list)
        return variable_list











