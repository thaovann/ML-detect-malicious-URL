import matplotlib.pyplot as plt
import networkx as nx

G = nx.Graph()
G.add_nodes_from(
    [
        (0, {"color": "blue", "size": 250}),
        (1, {"color": "red", "size": 100}),
        (2, {"color": "purple", "size": 20}),
        (3, {"color": "green", "size": 70}),
    ]
)

G.add_edges_from(
    [
        (0,1),
        (0,2),
        (2,1),
        (2,3),
    ]
)
for node in G.nodes(data=True):
    print(node)

node_colors = nx.get_node_attributes(G, "color").values()
colors = list(node_colors)
node_sizes = nx.get_node_attributes(G, "size").values()
sizes = list(node_sizes)

nx.draw(G, with_labels=True, node_color=colors, node_size=sizes)
plt.waitforbuttonpress()
