# src/remove_nodes.py
import csv
import os
import networkx as nx

def load_graph(filename):
    G = nx.Graph()
    with open(filename, 'r') as f:
        for line in f:
            u, v, w = map(int, line.strip().split(','))
            G.add_edge(u, v, weight=w)
    return G

def save_graph(G, filename):
    os.makedirs("data", exist_ok=True)
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        for u, v, data in G.edges(data=True):
            writer.writerow([u, v, data['weight']])
    print(f"Nouveau graphe : {G.number_of_nodes()} sommets, {G.number_of_edges()} arêtes")
    print(f"Sauvegardé dans : {filename}")

if __name__ == "__main__":
    if not os.path.exists("data/contacts_original.csv"):
        print("Erreur : contacts_original.csv manquant. Lancez generate_graph.py")
        exit()

    G = load_graph("data/contacts_original.csv")

    # Top 5 degré
    degrees = dict(G.degree())
    top5_deg = [n for n, _ in sorted(degrees.items(), key=lambda x: x[1], reverse=True)[:5]]

    # Top 5 proximité
    sum_dist = {}
    for node in G.nodes():
        try:
            dist = nx.shortest_path_length(G, source=node, weight='weight')
            sum_dist[node] = sum(dist.values())
        except:
            sum_dist[node] = float('inf')
    top5_close = [n for n, _ in sorted(sum_dist.items(), key=lambda x: x[1])[:5]]

    # 10 nœuds uniques
    to_remove = list(set(top5_deg + top5_close))
    print(f"Suppression de {len(to_remove)} nœuds : {sorted(to_remove)}")

    G.remove_nodes_from(to_remove)
    save_graph(G, "data/contacts_reduced.csv")