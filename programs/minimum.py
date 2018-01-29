

from condition_list import *
from affectation_list import *
from control_graph import *
from result_fonctions import *


list_of_node = [ConditionNode(1, min_2_var),AffectationNode(2,skip), AffectationNode(3, second_to_first), EndNode(4, print_first)]

relations = [(1,2, True) , (1,3, False), (2,4, True), (3,4 , True)]


CFG = ControlGraph(list_of_node, relations, 2)

CFG.function_test([1,3])