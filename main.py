from src.utils import *
from src.interfaces import *
import networkx as nx
import random


for i in range(6, 7):
    
    G = nx.gnm_random_graph(n=i, m=i+5)
    
    for u, v in G.edges:
        G[u][v]["weight"] = random.randint(1, 50)
    G:nx.Graph = nx.relabel_nodes(G, {node: f"V{node+1}" for node in range(i)})  # vertices will be named from "V1" to "Vn" where n is the number of vertices
    S:IVertices = random.sample(list(G.nodes), round(0.7*i))
    
    Ts = solve_steiner_tree_problem(G, S)
    print(calculate_total_weight_of_graph(Ts))
    