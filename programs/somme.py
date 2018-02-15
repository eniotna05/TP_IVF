from control_flow_graph.affectation_list import *
from control_flow_graph.control_graph import *
from control_flow_graph.result_fonctions import *
from control_flow_graph.condition_list import *


list_of_node = [AffectationNode(1,Somme(0,[0,1])), EndNode(2, Imprimer(0))]
relations = [(1,2, True)]
CFGsum = ControlGraph(list_of_node, relations, 2, 2)

Dataset1 = [[1,4], [4,5], [7,9]]

CFGsum.cover_analysis_affectation(Dataset1, False)
CFGsum.cover_analysis_decision(Dataset1, False)

CFGsum.cover_analysis_k_path(2, Dataset1, False)

