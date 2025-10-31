# src/generate_graph.py
import networkx as nx
import random
import csv
import os

def generate_random_graph(n_nodes=250, avg_degree=6, max_weight=6):
    """Génère un graphe aléatoire avec poids sur les arêtes."""
    p = avg_degree / n_nodes
    G = nx.gnp_random_graph(n_nodes, p, seed=42)
    for u, v in G.edges():
        G.edges[u, v]['weight'] = random.randint(1, max_weight)
    return G

def save_to_csv(G, filename="data/contacts_original.csv"):
    os.makedirs("data", exist_ok=True)
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        for u, v, data in G.edges(data=True):
            writer.writerow([u, v, data['weight']])
    print(f"Graphe généré : {G.number_of_nodes()} sommets, {G.number_of_edges()} arêtes")
    print(f"Sauvegardé dans : {filename}")

if __name__ == "__main__":
    G = generate_random_graph()
    save_to_csv(G)