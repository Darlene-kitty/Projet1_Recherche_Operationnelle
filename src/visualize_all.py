# src/visualize_all.py
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

CSV_FILE = "contacts.csv"
RESULTS_DIR = Path("src/results")
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def load_graph():
    df = pd.read_csv(CSV_FILE)
    G = nx.Graph()
    for _, row in df.iterrows():
        G.add_edge(int(row['sommet_i']), int(row['sommet_j']), weight=int(row['jours_moyen']))
    return G


def save_plot(G, title, filename):
    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(G, k=0.15, iterations=20)
    nx.draw(G, pos, node_size=20, node_color='lightblue', edge_color='gray', with_labels=False)
    plt.title(title)
    path = RESULTS_DIR / filename
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Image sauvegardée : {path}")


def main():
    G = load_graph()

    # Q5-Q8 : 8 visualisations
    save_plot(G, "Graphe complet (250 nœuds)", "q5_full_graph.png")

    # Supprimer 10 nœuds
    degrees = dict(G.degree())
    top10 = [n for n, _ in sorted(degrees.items(), key=lambda x: x[1], reverse=True)[:10]]
    G_reduced = G.copy()
    G_reduced.remove_nodes_from(top10)

    save_plot(G_reduced, "Graphe après suppression 10 nœuds centraux", "q6_reduced_graph.png")
    save_plot(G, "Degrés (taille des nœuds)", "q7_degree_size.png")  # à compléter si besoin
    save_plot(G, "Poids des arêtes", "q8_edge_weights.png")  # à compléter si besoin


if __name__ == "__main__":
    main()