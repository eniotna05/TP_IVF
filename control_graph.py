

def skip(variable_list):
    return variable_list


class Node:

    def __init__(self, condition, affectations, true_children, false_children):

        self.condition = condition
        self.true = true_children
        self.false = false_children
        self.affections = affectations

class ConditionNode(Node):

    def __init__(self, condition, true_children, false_children):

        self.condition = condition
        self.true = true_children
        self.false = false_children
        self.affections = skip


class AffectationNode(Node):

    def __init__(self, affectations , true_children):
        self.condition = condition
        self.true = true_children
        self.false = None
        self.affections = affectations


class ControlGraph:

    def __init__(self, rootnode, number_of_variables):
        self.rootnode = rootnode
        self.number_of_variables = number_of_variables

    def go_through_node(self, variable_list):

        if self.condition == True:
            next_node = self.true
        else:
            next_node = self.false
        variable_list = self.affectations(variable_list)
        return (next_node, variable_list)


    def function_test(self,input):

        if len(input) != self.number_of_variables:
            raise AssertionError("Number of variables provided is not correct")

        variable_list = input
        next_node = self.rootnode

        while next_node != None:






