# src/visualize_all.py
# Étudiant 3 : Q5, Q6, Q7, Q8 + 8 images
import networkx as nx
import matplotlib.pyplot as plt
import os


def load_graph(filename):
    G = nx.Graph()
    with open(filename, 'r') as f:
        for line in f:
            u, v, w = map(int, line.strip().split(','))
            G.add_edge(u, v, weight=w)
    return G


def draw_graph(G, title, filename, highlight=None, reached=None):
    plt.figure(figsize=(14, 10))
    pos = nx.spring_layout(G, k=0.6, iterations=50, seed=42)

    nx.draw_networkx_nodes(G, pos, node_color='lightgray', node_size=300)
    if highlight:
        nx.draw_networkx_nodes(G, pos, nodelist=highlight, node_color='red', node_size=600, node_shape='s')
    if reached:
        nx.draw_networkx_nodes(G, pos, nodelist=reached, node_color='gold', node_size=500)

    nx.draw_networkx_edges(G, pos, alpha=0.5)
    nx.draw_networkx_labels(G, pos, font_size=8)

    if G.number_of_edges() < 60:
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=7)

    plt.title(title, fontsize=16)
    plt.axis('off')
    os.makedirs("results", exist_ok=True)
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Image : {filename}")


def campaign(G, start_node, days, title, filename):
    dist = nx.shortest_path_length(G, source=start_node, weight='weight')
    reached = [n for n, d in dist.items() if d <= days]
    print(f"{title} : {len(reached)} sommets atteints")
    draw_graph(G, f"{title} → {len(reached)} atteints", filename, [start_node], reached)


if __name__ == "__main__":
    G = load_graph("data/contacts_original.csv")
    Gr = load_graph("data/contacts_reduced.csv") if os.path.exists("data/contacts_reduced.csv") else None

    # Q5
    start_deg = max(dict(G.degree()), key=dict(G.degree()).get)
    campaign(G, start_deg, 5, "Q5: 5 jours (degré max)", "results/04_campaign_degree_day5.png")

    # Q6
    sum_dist = {n: sum(nx.shortest_path_length(G, n, weight='weight').values()) for n in G.nodes()}
    start_close = min(sum_dist, key=sum_dist.get)
    campaign(G, start_close, 7, "Q6: 7 jours (proximité min)", "results/05_campaign_closeness_day7.png")

    if Gr:
        # Q7
        start_deg_r = max(dict(Gr.degree()), key=dict(Gr.degree()).get)
        campaign(Gr, start_deg_r, 4, "Q7: 4 jours (degré max réduit)", "results/07_new_campaign_degree_day4.png")

        # Q8
        sum_dist_r = {n: sum(nx.shortest_path_length(Gr, n, weight='weight').values()) for n in Gr.nodes()}
        start_close_r = min(sum_dist_r, key=sum_dist_r.get)
        campaign(Gr, start_close_r, 3, "Q8: 3 jours (proximité min réduit)",
                 "results/08_new_campaign_closeness_day3.png")