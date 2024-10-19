# import networkx as nx
# G = nx.Graph()
# G.add_edge("A","B", weight=4)
# G.add_edge("A","C", weight=2)
# G.add_edge("B","D", weight=12)
# #G.add_edge("A","E", weight=3)
# G.add_edge("C","E", weight=5)
# shortest_path_a_e = nx.shortest_path(G, "A", "E", weight="weight")
# print(f"shortest path from A to E is {shortest_path_a_e}")
# nx.draw(G, with_labels = True)

import networkx as nx
DG = nx.DiGraph()
DG.add_edges_from([(1,2),(2,3),(3,4),(4,5),(5,2),(4,6)])
print(f"the out edges of node 4 are {DG.out_edges(4)}")
print(f"the in degree of node 2 are {DG.in_degree(2)}")
print(f"the successor of node 4 are {list(DG.successors(4))}")
print(f"the predecessors of node 2 are {list(DG.predecessors(2))}")
nx.draw(DG, with_labels=True)