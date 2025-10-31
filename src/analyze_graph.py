# src/analyze_graph.py
# Étudiant 2 : Degrés + Proximité + Distributions
import networkx as nx
import matplotlib.pyplot as plt
import os
from collections import Counter


def load_graph(filename):
    G = nx.Graph()
    with open(filename, 'r') as f:
        for line in f:
            u, v, w = map(int, line.strip().split(','))
            G.add_edge(u, v, weight=w)
    return G


def degree_analysis(G):
    degrees = dict(G.degree())
    count = Counter(degrees.values())
    max_k = max(count.keys()) if count else 0
    distribution = [count.get(k, 0) for k in range(max_k + 1)]

    plt.figure(figsize=(10, 6))
    plt.bar(range(len(distribution)), distribution, color='skyblue', edgecolor='black')
    plt.title("Distribution des degrés")
    plt.xlabel("Degré k")
    plt.ylabel("Nombre de sommets")
    plt.grid(True, alpha=0.3)
    os.makedirs("results", exist_ok=True)
    plt.savefig("results/degree_distribution.png", dpi=150, bbox_inches='tight')
    plt.close()

    top5 = sorted(degrees.items(), key=lambda x: x[1], reverse=True)[:5]
    print("Top 5 degrés :", top5)
    return distribution, top5


def closeness_analysis(G):
    sum_dist = {}
    for node in G.nodes():
        try:
            dist = nx.shortest_path_length(G, source=node, weight='weight')
            sum_dist[node] = sum(dist.values())
        except:
            sum_dist[node] = float('inf')

    values = [v for v in sum_dist.values() if v != float('inf')]
    plt.figure(figsize=(10, 6))
    plt.hist(values, bins=30, color='lightcoral', edgecolor='black')
    plt.title("Distribution de la proximité (somme des distances)")
    plt.xlabel("Somme des distances")
    plt.ylabel("Nombre de sommets")
    plt.grid(True, alpha=0.3)
    plt.savefig("results/closeness_distribution.png", dpi=150, bbox_inches='tight')
    plt.close()

    top5 = sorted(sum_dist.items(), key=lambda x: x[1])[:5]
    print("Top 5 proximité :", top5)
    return sum_dist, top5


if __name__ == "__main__":
    G = load_graph("data/contacts_original.csv")
    degree_analysis(G)
    closeness_analysis(G)