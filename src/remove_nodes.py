# src/remove_nodes.py
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import random

CSV_FILE = "contacts.csv"
RESULTS_DIR = Path("src/results")
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

def load_graph():
    df = pd.read_csv(CSV_FILE)
    G = nx.Graph()
    for _, row in df.iterrows():
        G.add_edge(int(row['sommet_i']), int(row['sommet_j']), weight=int(row['jours_moyen']))
    return G

def remove_top_degree_nodes(G, n=10):
    degrees = dict(G.degree())
    top_nodes = sorted(degrees.items(), key=lambda x: x[1], reverse=True)[:n]
    removed = [node for node, _ in top_nodes]
    G_copy = G.copy()
    G_copy.remove_nodes_from(removed)
    return G_copy, removed

def plot_graph(G, title, filename, node_size=20):
    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(G, k=0.15, iterations=20)
    nx.draw(G, pos, node_size=node_size, node_color='lightblue', with_labels=False, alpha=0.7)
    plt.title(title)
    plt.savefig(RESULTS_DIR / filename, dpi=150, bbox_inches='tight')
    plt.close()

def main():
    print("Suppression des 10 nœuds les plus influents...")
    G = load_graph()
    print(f"Graphe original : {G.number_of_nodes()} nœuds, {G.number_of_edges()} arêtes")

    G_reduced, removed = remove_top_degree_nodes(G, n=10)
    print(f"Nœuds supprimés : {removed}")
    print(f"Graphe réduit : {G_reduced.number_of_nodes()} nœuds, {G_reduced.number_of_edges()} arêtes")

    # Visualisation
    plot_graph(G, "Graphe original (250 nœuds)", "original_graph.png")
    plot_graph(G_reduced, "Graphe après suppression (240 nœuds)", "reduced_graph.png", node_size=30)

    print("Images sauvegardées dans src/results/")
    print("Q5-Q8 : Analyse dans le rapport.")

if __name__ == "__main__":
    main()