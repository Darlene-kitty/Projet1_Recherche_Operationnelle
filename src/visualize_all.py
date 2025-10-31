# src/visualize_all.py
import networkx as nx
import matplotlib.pyplot as plt
import os
import csv

def load_graph(filename):
    G = nx.Graph()
    with open(filename, 'r') as f:
        for line in f:
            u, v, w = map(int, line.strip().split(','))
            G.add_edge(u, v, weight=w)
    return G

def draw_graph(G, title, filename, highlight_nodes=None, highlight_color='red', path_nodes=None):
    plt.figure(figsize=(14, 10))
    pos = nx.spring_layout(G, k=0.6, iterations=50, seed=42)

    # Couleur par degré
    degrees = dict(G.degree())
    deg_values = [degrees[n] for n in G.nodes()]
    max_deg = max(deg_values) if deg_values else 1
    node_colors = [plt.cm.Reds(deg / max_deg * 0.8 + 0.2) for deg in deg_values]

    # Nœuds normaux
    normal = [n for n in G.nodes() if n not in (highlight_nodes or []) and n not in (path_nodes or [])]
    nx.draw_networkx_nodes(G, pos, nodelist=normal, node_color='lightgray', node_size=300, alpha=0.8)

    # Nœuds mis en avant
    if highlight_nodes:
        nx.draw_networkx_nodes(G, pos, nodelist=highlight_nodes,
                               node_color=highlight_color, node_size=600,
                               node_shape='s', edgecolors='black', linewidths=2)

    # Nœuds atteints (campagne)
    if path_nodes:
        nx.draw_networkx_nodes(G, pos, nodelist=path_nodes,
                               node_color='gold', node_size=500, node_shape='o', edgecolors='orange')

    # Arêtes
    nx.draw_networkx_edges(G, pos, alpha=0.5, width=1)
    nx.draw_networkx_labels(G, pos, {n: n for n in G.nodes()}, font_size=9)

    if G.number_of_edges() < 60:
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=7)

    plt.title(title, fontsize=16, pad=20)
    plt.axis('off')
    os.makedirs("results", exist_ok=True)
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Sauvegardé : {filename}")

def analyze_and_visualize():
    if not os.path.exists("data/contacts_original.csv"):
        print("Erreur : contacts_original.csv manquant. Lancez generate_graph.py")
        return

    G = load_graph("data/contacts_original.csv")

    # --- 1. Graphe initial ---
    draw_graph(G, "Graphe Initial (250 sommets)", "results/01_graph_initial.png")

    # --- 2. Top 5 degrés ---
    degrees = dict(G.degree())
    top5_deg = sorted(degrees.items(), key=lambda x: x[1], reverse=True)[:5]
    top5_nodes = [n for n, _ in top5_deg]
    draw_graph(G, "Q1-Q2 : Top 5 Degrés (carrés rouges)", "results/02_graph_degree_top5.png", top5_nodes, 'red')

    # --- 3. Top 5 proximité ---
    sum_dist = {}
    for node in G.nodes():
        try:
            dist = nx.shortest_path_length(G, source=node, weight='weight')
            sum_dist[node] = sum(dist.values())
        except:
            sum_dist[node] = float('inf')
    top5_close = sorted(sum_dist.items(), key=lambda x: x[1])[:5]
    top5_close_nodes = [n for n, _ in top5_close]
    draw_graph(G, "Q3-Q4 : Top 5 Proximité (carrés bleus)", "results/03_graph_closeness_top5.png", top5_close_nodes, 'blue')

    # --- 4. Campagne 5 jours (max degré) ---
    start_deg = max(degrees, key=degrees.get)
    dist5 = nx.shortest_path_length(G, source=start_deg, weight='weight')
    reached5 = [n for n, d in dist5.items() if d <= 5]
    draw_graph(G, f"Q5 : 5 jours (départ {start_deg}) → {len(reached5)} atteints",
               "results/04_campaign_degree_day5.png", [start_deg], 'red', reached5)

    # --- 5. Campagne 7 jours (min proximité) ---
    start_close = min(sum_dist, key=sum_dist.get)
    dist7 = nx.shortest_path_length(G, source=start_close, weight='weight')
    reached7 = [n for n, d in dist7.items() if d <= 7]
    draw_graph(G, f"Q6 : 7 jours (départ {start_close}) → {len(reached7)} atteints",
               "results/05_campaign_closeness_day7.png", [start_close], 'blue', reached7)

    # --- 6. Graphe réduit ---
    if os.path.exists("data/contacts_reduced.csv"):
        Gr = load_graph("data/contacts_reduced.csv")
        draw_graph(Gr, "Graphe Réduit (après suppression)", "results/06_graph_reduced.png")

        # --- 7. Nouveau : 4 jours (max degré) ---
        deg_r = dict(Gr.degree())
        start_r_deg = max(deg_r, key=deg_r.get)
        dist_r4 = nx.shortest_path_length(Gr, source=start_r_deg, weight='weight')
        reached_r4 = [n for n, d in dist_r4.items() if d <= 4]
        draw_graph(Gr, f"Nouveau : 4 jours (départ {start_r_deg}) → {len(reached_r4)} atteints",
                   "results/07_new_campaign_degree_day4.png", [start_r_deg], 'red', reached_r4)

        # --- 8. Nouveau : 3 jours (min proximité) ---
        sum_dist_r = {}
        for node in Gr.nodes():
            try:
                dist = nx.shortest_path_length(Gr, source=node, weight='weight')
                sum_dist_r[node] = sum(dist.values())
            except:
                sum_dist_r[node] = float('inf')
        start_r_close = min(sum_dist_r, key=sum_dist_r.get)
        dist_r3 = nx.shortest_path_length(Gr, source=start_r_close, weight='weight')
        reached_r3 = [n for n, d in dist_r3.items() if d <= 3]
        draw_graph(Gr, f"Nouveau : 3 jours (départ {start_r_close}) → {len(reached_r3)} atteints",
                   "results/08_new_campaign_closeness_day3.png", [start_r_close], 'blue', reached_r3)
    else:
        print("contacts_reduced.csv manquant → images 6-8 non générées")

    print("\nTOUTES LES VISUALISATIONS SONT PRÊTES DANS results/")

if __name__ == "__main__":
    analyze_and_visualize()