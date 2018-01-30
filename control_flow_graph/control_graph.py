from copy import deepcopy

from control_flow_graph.affectation_list import *
from control_flow_graph.condition_list import *
from control_flow_graph.result_fonctions import *

class Node:

    def __init__(self, id, condition, affectations, true_children, false_children):

        self.condition = condition
        self.true = None
        self.false = None
        self.affectations = affectations
        self.id = id

class ConditionNode(Node):

    def __init__(self, id, condition, while_loop = True):

        self.condition = condition
        self.true = None
        self.false = None
        self.affectations = Skip()
        self.id = id
        self.while_loop = while_loop


class AffectationNode(Node):

    def __init__(self, id, affectations):
        self.condition = AlwaysTrue()
        self.true = None
        self.false = None
        self.affectations = affectations
        self.id = id


class EndNode(Node):

    def __init__(self, id, result_function):
        self.condition = AlwaysTrue()
        self.true = None
        self.false = None
        self.affectations = Skip()
        self.id = id
        self.result = result_function

class ControlGraph:

    def __init__(self, list_of_node, relationships , number_of_input_var, number_of_total_var):
        self.list_of_node = list_of_node
        self.rootnode = list_of_node[0]
        self.relationships = relationships
        self.number_of_input_var = number_of_input_var
        self.number_of_total_var = number_of_total_var

        self.to_cover = None
        self.path_size = None

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

        if node.condition.test(variable_list) is True:
            next_node = node.true
        else:
            next_node = node.false
        variable_list = node.affectations.run(variable_list)
        return next_node, variable_list

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
                    self.to_cover[current_node] = True

            #All decisions criteria
            if criteria == "decision":
                if not isinstance(current_node.condition, AlwaysTrue):
                    self.to_cover[current_node].append(current_node.condition.test(variable_list))
                    #On ajoute le resultat du chemin emprunté par la condition (True ou False)

            current_node, variable_list = self.go_through_node(current_node, variable_list)

        if explicit is True:
            print("node number = " + str(current_node.id) )
            print("variables = " + str(variable_list) + "\n")
            print("Result of function below")
            current_node.result.run(variable_list)

        return variable_list

    def cover_analysis_affectation(self, data_set, explicit=True):

        self.to_cover = {}

        for node in self.list_of_node:
            if not isinstance(node.affectations, Skip):
                self.to_cover[node] = False

        for input in data_set:
            self.function_run(list(input), "affectation", explicit)

        cover_percentage, non_covered = self.cover_count()
        print("# of elements to cover: " + str(len(self.to_cover)))
        print("Cover percentage :" + str(cover_percentage))
        print("Non covered :" + str(non_covered))


    def cover_analysis_decision(self, data_set, explicit=True):

        self.to_cover = {}

        for node in self.list_of_node:
            if not isinstance(node.condition, AlwaysTrue):
                self.to_cover[node] = []

        for input in data_set:
            self.function_run(list(input), "decision", explicit)

        for cle, valeur in self.to_cover.items():
            if True in valeur and False in valeur:
            #Pour chaque noeud de condition le critere est couvert
            #  si les chemin True et False ont tout deux été emprunté
                self.to_cover[cle] = True
            else:
                self.to_cover[cle] = False

        cover_percentage, non_covered = self.cover_count()

        print("# of elements to cover: " + str(len(self.to_cover)))
        print("Cover percentage : " + str(cover_percentage))
        print("Non covered : " + str(non_covered))

    def cover_analysis_k_path(self, k,  data_set, explicit=True):

        self.path_size = k
        self.to_cover = {}

        for node in self.list_of_node:
            if not isinstance(node.condition, AlwaysTrue):
                self.to_cover[node] = []

        for input in data_set:
            self.function_run(list(input), "decision", explicit)

        for cle, valeur in self.to_cover.items():
            if True in valeur and False in valeur:
            #Pour chaque noeud de condition le critere est couvert
            #  si les chemin True et False ont tout deux été emprunté
                self.to_cover[cle] = True
            else:
                self.to_cover[cle] = False

        cover_percentage, non_covered = self.cover_count()

        print("# of elements to cover: " + str(len(self.to_cover)))
        print("Cover percentage : " + str(cover_percentage))
        print("Non covered : " + str(non_covered))

    def cover_count(self):

        covered_count = 0
        non_covered = []
        for key, value in self.to_cover.items():
            if value is True:
                covered_count += 1
            else:
                non_covered.append(key.id)

        if len(self.to_cover) == 0:
            cover_percentage = "NA No items to cover"
        else:
            cover_percentage = covered_count / len(self.to_cover)
        return cover_percentage, non_covered



















