from control_flow_graph.affectation_list import *
from control_flow_graph.control_graph import *
from control_flow_graph.result_fonctions import *
from control_flow_graph.condition_list import *


list_of_node = [AffectationNode(1, Somme(1,[],1)),
                AffectationNode(2,Somme(2,[],1)),
                ConditionNode(3, Comparaison(0,1)),
                AffectationNode(4, Multiplication(2,[1,2])),
                AffectationNode(5,Somme(1,[1],1)),
                EndNode(6,Imprimer(2))
                ]

relations = [(1,2, True) , (2,3, True), (3,4, False, True), (3,6 , True),(4,5 , True), (5,3,True)]
CFGfac = ControlGraph(list_of_node, relations, 1, 3)

Dataset1 = [[0]]
Dataset2 = [[0], [3], [6]]

CFGfac.cover_analysis_affectation(Dataset1, False)
CFGfac.cover_analysis_affectation(Dataset2, False)
CFGfac.cover_analysis_decision(Dataset1, False)
CFGfac.cover_analysis_decision(Dataset2, False)
#CFGfac.cover_analysis_k_path(2, Dataset2, False)
