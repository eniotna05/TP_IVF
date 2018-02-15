from control_flow_graph.affectation_list import *
from control_flow_graph.condition_list import *
from control_flow_graph.result_fonctions import *

class Node:

    def __init__(self, id, condition, affectations):

        self.condition = condition
        self.true = None
        self.false = None
        self.affectations = affectations
        self.id = id

    def __str__(self):
        return "Node " + str(self.id)

class ConditionNode(Node):

    def __init__(self, id, condition, while_loop=False):

        super().__init__(id=id, condition=condition, affectations=Skip())

        # used for all affectation criteria
        self.true_covered = False
        self.false_covered = False

        # used  for loop criteria
        self.while_loop = while_loop

    def __str__(self):
        return "Cond Node " + str(self.id)


class AffectationNode(Node):

    def __init__(self, id, affectations):
        super().__init__(id=id, condition=AlwaysTrue(), affectations=affectations)

    def __str__(self):
        return "Aff Node " + str(self.id)


class EndNode(Node):

    def __init__(self, id, result_function):
        super().__init__(id=id, condition=AlwaysTrue(), affectations=Skip())
        self.result = result_function

    def __str__(self):
        return "End Node " + str(self.id)


class ControlGraph:

    def __init__(self, list_of_node, relationships , number_of_input_var, number_of_total_var):
        self.list_of_node = list_of_node
        self.rootnode = list_of_node[0]
        self.relationships = relationships
        self.number_of_input_var = number_of_input_var
        self.number_of_total_var = number_of_total_var

        self.covered = None
        self.non_covered = None

        self.path_size = None

        for relation in relationships:
            node = self.fetch_node(relation[0])
            if relation[2] is True:
                node.true = self.fetch_node(relation[1])
            else:
                node.false = self.fetch_node(relation[1])

    def fetch_node(self, id):
        for node in self.list_of_node:
            if node.id == id:
                return node

    def go_through_node(self, node, vlist):
        if node.condition.test(vlist) is True:
            next_node = node.true
        else:
            next_node = node.false
        vlist = node.affectations.run(vlist)
        return next_node, vlist

    def function_run(self, input, criteria=None, explicit=True):

        if len(input) != self.number_of_input_var:
            raise AssertionError("Number of variables provided is not correct")
        variable_list = input

        var_to_add = self.number_of_total_var - self.number_of_input_var
        for k in range(var_to_add):
            variable_list.append(None)

        current_node = self.rootnode

        while not isinstance(current_node, EndNode):
            if explicit is True:
                print("node number = " + str(current_node.id) )
                print("variables = " + str(variable_list) + "\n")

            #All affectation criteria
            if criteria == "affectation":
                if not isinstance(current_node.affectations, Skip):
                    if current_node in self.non_covered:
                        self.non_covered.remove(current_node)
                        self.covered.append(current_node)

            #All decisions criteria
            if criteria == "decision":
                if not isinstance(current_node.condition, AlwaysTrue):
                    if current_node in self.non_covered:
                        if current_node.condition.test(variable_list) is True:
                            current_node.true_covered = True
                        if current_node.condition.test(variable_list) is False:
                            current_node.false_covered = True
                        if current_node.true_covered is True and current_node.false_covered is True:
                            self.non_covered.remove(current_node)
                            self.covered.append(current_node)

            #K path critteria
            if criteria == "k_path":
                self.function_path.append(current_node.id)

            current_node, variable_list = self.go_through_node(current_node, variable_list)

        # K path critteria (final node)
        if criteria == "k_path":
            self.function_path.append(current_node.id)

        if explicit is True:
            print("node number = " + str(current_node.id) )
            print("variables = " + str(variable_list) + "\n")
            print("Result of function below")
            current_node.result.run(variable_list)

        return variable_list

    def cover_analysis_affectation(self, data_set, explicit=True):

        self.covered = []
        self.non_covered = []

        for node in self.list_of_node:
            if not isinstance(node.affectations, Skip):
                self.non_covered.append(node)

        for input in data_set:
            self.function_run(list(input), "affectation", explicit)

        return self.cover_analysis_result()

    def cover_analysis_decision(self, data_set, explicit=True):

        self.covered = []
        self.non_covered = []

        for node in self.list_of_node:
            if not isinstance(node.condition, AlwaysTrue):
                self.non_covered.append(node)

        for input in data_set:
            self.function_run(list(input), "decision", explicit)

        # condition nodes are reinitialized
        for node in self.list_of_node:
            if not isinstance(node.condition, AlwaysTrue):
                node.true_covered = False
                node.false_covered = False

        return self.cover_analysis_result()

    def cover_analysis_k_path(self, k,  data_set, explicit=True):

        self.covered = []
        self.non_covered = []

        for node in self.list_of_node:
            self.create_paths(k, node, [])

        print(self.non_covered)

        for input in data_set:
            self.function_path = []
            self.function_run(list(input), "k_path", explicit)
            #print(self.function_path)
            for path in self.non_covered:
                #print(path)
                #print(self.sublist(path, self.function_path))
                if self.sublist(path, self.function_path):
                    self.non_covered.remove(path)
                    self.covered.append(path)

        return self.cover_analysis_result()

    def cover_analysis_result(self):

        if len(self.non_covered) + len(self.covered) == 0:
            cover_percentage = "N.A. (No items to cover)"
        else:
            cover_percentage = len(self.covered) / (len(self.non_covered) + len(self.covered)) * 100

        print("# of elements to cover: " + str(len(self.non_covered) + len(self.covered)))
        print("Cover percentage : " + str(cover_percentage) + " %")
        print("Non covered : " + str([str(x) for x in self.non_covered]) + "\n")

        return cover_percentage, self.non_covered

    def create_paths(self, max_size, node, current_path):
        #function that is used to get all possible paths for the k_path cover analysis
        #recursive function that adds all path starting from a node, of a maximum size
        current_path.append(node.id)
        self.non_covered.append(current_path)
        if len(current_path) < max_size:
            if node.true is not None:
                self.create_paths(max_size, node.true, list(current_path))
            if node.false is not None:
                self.create_paths(max_size, node.false, list(current_path))

    def sublist(self, lst1, lst2):
        #Checks if list1 is a sublist of list2
        #Useful for k path cover analysist
        result = False
        curseur = 0
        for element in lst2:
            if result is False:
                if element == lst1[0]:
                    if len(lst1) == 1:
                        return True
                    result = True
                    curseur += 1
            if result is True:
                if element == lst1[curseur]:
                    if curseur == len(lst1) - 1:
                        return True
                    curseur += 1
                else:
                    curseur = 0
                    result = False
        return False






























