import pandas as pd
import glob
import matplotlib.pyplot as plt
import networkx as nx

# Read all data
all_data = []
file_paths_Adware_Dowgin = glob.glob("Data/Adware/Dowgin*.csv")
file_paths_Adware_Ewind = glob.glob("Data/Adware/Ewind*.csv")

file_paths_Benign = glob.glob("Data/Benign2015/*.csv")
columns_to_skip = ["Protocol", "Timestamp"]

for file in file_paths_Benign:
    data = pd.read_csv(file, usecols=lambda col: col not in columns_to_skip, nrows=3)
    all_data.append(data)

data = pd.concat(all_data, ignore_index=True)
data.columns = (
    data.columns.str.strip()
)  # Remove leading and trailing spaces from column names


# flow-graph
flow_graph = nx.DiGraph()

end_points = data[
    ["Source IP", "Destination IP"]
].values.tolist()  # Không cần dùng đến port
edges = [(src_ip, dst_ip) for src_ip, dst_ip in end_points]

flow_graph.add_edges_from(edges)

for index, row in data.iterrows():
    src_ip = row["Source IP"]
    dst_ip = row["Destination IP"]

# bỏ qua protocol, Timestamp
if not flow_graph.has_edge(src_ip, dst_ip):
    flow_graph.add_edge(
        src_ip,
        dst_ip,
        flow_duration=[],
        total_fwd_packets=[],
    )

for src, dst in flow_graph.edges():
    for attr in flow_graph[src][dst]:
        values = flow_graph[src][dst][attr]
        aggregate_values = {
            "mean": pd.Series(values).mean(),
            "std": pd.Series(values).std(),
            "skewness": pd.Series(values).skew(),
            "kurtosis": pd.Series(values).kurtosis(),
            "median": pd.Series(values).median(),
        }
        flow_graph[src][dst][attr] = aggregate_values

# Draw the graph
plt.figure(figsize=(10, 8))
pos = nx.spring_layout(flow_graph)  # You can change the layout algorithm as needed

# Draw nodes
nx.draw_networkx_nodes(flow_graph, pos, node_size=200, node_color="skyblue")

# Draw edges
nx.draw_networkx_edges(flow_graph, pos, width=1.0, alpha=0.5, edge_color="gray")

# Draw labels (if you want to label the nodes)
nx.draw_networkx_labels(flow_graph, pos, font_size=8, font_color="black")
# Show plot
plt.title("Flow Graph Visualization")

plt.show()
