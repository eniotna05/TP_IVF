from control_flow_graph.affectation_list import *
from control_flow_graph.control_graph import *
from control_flow_graph.result_fonctions import *
from control_flow_graph.condition_list import *


list_of_node = [ConditionNode(1, Comparaison(0,1)),
                AffectationNode(2,Skip()),
                AffectationNode(3, Somme(0,[1])),
                EndNode(4, Imprimer(0))]
relations = [(1,2, True) , (1,3, False), (2,4, True), (3,4 , True)]
CFGmin = ControlGraph(list_of_node, relations, 2, 2)

Dataset1 = [[1,4], [4,5], [7,9]]
Dataset2 = [[1,3], [7,5], [7,9]]
Dataset3 = [[4,2], [7,5], [7,9]]

CFGmin.cover_analysis_affectation(Dataset1, False)
CFGmin.cover_analysis_affectation(Dataset2, False)
CFGmin.cover_analysis_decision(Dataset1, False)
CFGmin.cover_analysis_decision(Dataset2, False)
CFGmin.cover_analysis_decision(Dataset3, False)

CFGmin.cover_analysis_k_path(2, Dataset1, False)









