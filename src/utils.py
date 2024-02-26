import networkx as nx
import matplotlib.pyplot as plt
from src.interfaces import *


def calculate_total_weight_of_graph(G: nx.Graph) -> float:
    '''
    This function calculates the total weight of a given graph.
    '''
    return sum([G.get_edge_data(u, v)["weight"] for u, v in G.edges])


def plot_graph(G: nx.Graph, title: str) -> None:
    '''
    This function plots a graph using networkx and matplotlib libraries.
    '''
    plt.title(title)
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color="lightblue", edge_color="gray", node_size=500, font_size=15, font_weight="bold")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, "weight"))
    plt.show()


def complete_subgraph_from_graph_with_shortest_paths(G: nx.Graph, vertices: IVertices) -> nx.Graph:
    '''
    This function creates a complete subgraph from a given graph. The subgraph will contain all vertices from the vertices list
    and these vertices will be connected directly, but the edges will have weights equal to the shortest path weights
    between the vertices in the original graph.
    '''
    subgraph = nx.Graph()
    
    for vertex in vertices:
        subgraph.add_node(vertex)
    
    for source in vertices:
        for target in vertices:
            if source != target:
                shortest_path = nx.shortest_path(G, source=source, target=target, weight="weight")
                weight = sum([G.get_edge_data(u=shortest_path[i], v=shortest_path[i+1])["weight"] for i in range(len(shortest_path)-1)])
                subgraph.add_edge(source, target, weight=weight)
    
    return subgraph


def build_subgraph_from_graph_with_minimum_spanning_tree(G: nx.Graph, minimum_spanning_tree: nx.Graph) -> nx.Graph:
    '''
    This function builds a subgraph from a given graph using a minimum spanning tree. The subgraph will contain all vertices of the
    minimum spanning tree. For each edge in the minimum spanning tree, we should find the shortest path between these two vertices
    from the original graph. Then all additional vertices found in the shortest paths should be added to the subgraph to connect the
    vertices of the minimum spanning tree.
    '''
    subgraph = nx.Graph()
    
    for edge in minimum_spanning_tree.edges:
        source, target = edge
        shortest_path = nx.shortest_path(G, source=source, target=target, weight="weight")
        for i in range(len(shortest_path)-1):
            subgraph.add_edge(shortest_path[i], shortest_path[i+1], weight=G.get_edge_data(u=shortest_path[i], v=shortest_path[i+1])["weight"])
            
    return subgraph


def remove_nodes_leaves_from_minimum_spanning_tree(minimum_spanning_tree: nx.Graph, allowed_leaves: IVertices) -> nx.Graph:
    '''
    This function takes as input a minimum spanning tree and a list of allowed leaves (Steiner vertices).
    It removes from the minimum spanning tree all leaves that are not in the allowed leaves list.
    The process repeats until all leaves in the resulting tree are in the allowed leaves list.
    '''    
    while True:
        leaves = [node for node in minimum_spanning_tree.nodes if minimum_spanning_tree.degree(node) == 1]
        leaves_to_remove = [leaf for leaf in leaves if leaf not in allowed_leaves]

        if not leaves_to_remove: break
        
        minimum_spanning_tree.remove_nodes_from(leaves_to_remove)
    
    return minimum_spanning_tree


def solve_steiner_tree_problem(G: nx.Graph, S: IVertices, plot_charts: bool = False) -> nx.Graph:
    '''
    This function solves the Steiner Tree Problem for a given graph and a list of Steiner vertices.
    '''
    G1 = complete_subgraph_from_graph_with_shortest_paths(G, S)
    T1:nx.Graph = nx.minimum_spanning_tree(G1)
    
    Gs:nx.Graph = build_subgraph_from_graph_with_minimum_spanning_tree(G, T1)
    Ts:nx.Graph = nx.minimum_spanning_tree(Gs)
    
    Th:nx.Graph = remove_nodes_leaves_from_minimum_spanning_tree(Ts, S)

    if plot_charts:
        plot_graph(G, f"Original Graph G containing {len(G.nodes)} vertices and {len(G.edges)} edges")
        plot_graph(G1, f"Complete Subgraph G1 containing {len(G1.nodes)} vertices and {len(G1.edges)} edges (Shortest Paths)")
        plot_graph(T1, "Minimum Spanning Tree T1 of the Complete Subgraph")
        plot_graph(Gs, "Subgraph Gs containing the Minimum Spanning Tree Edges and Shortest Paths")
        plot_graph(Ts, "Minimum Spanning Tree Ts of the Subgraph Gs")
        plot_graph(Th, "Final Steiner Tree Th")
    
    return Th
