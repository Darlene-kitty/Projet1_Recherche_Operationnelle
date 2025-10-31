# src/analyze_graph.py
# Étudiant 2 : Degrés + Proximité + Top 5 + Distributions
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

def analyze_degrees(G):
    degrees = dict(G.degree())
    dist = Counter(degrees.values())
    top5 = sorted(degrees.items(), key=lambda x: x[1], reverse=True)[:5]
    print("Top 5 degrés :", top5)
    return dist, top5

def analyze_proximity(G):
    sum_dist = {}
    for node in G.nodes():
        try:
            dist = nx.shortest_path_length(G, source=node, weight='weight')
            sum_dist[node] = sum(dist.values())
        except:
            sum_dist[node] = float('inf')
    values = [v for v in sum_dist.values() if v != float('inf')]
    top5 = sorted(sum_dist.items(), key=lambda x: x[1])[:5]
    print("Top 5 proximité :", top5)
    return values, top5

def plot_distribution(data, title, filename, xlabel):
    plt.figure(figsize=(10, 6))
    if isinstance(data, dict):
        plt.bar(data.keys(), data.values(), color='skyblue', edgecolor='black')
    else:
        plt.hist(data, bins=30, color='lightcoral', edgecolor='black')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel("Nombre de sommets")
    plt.grid(True, alpha=0.3)
    os.makedirs("results", exist_ok=True)
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Histogramme : {filename}")

if __name__ == "__main__":
    if not os.path.exists("data/contacts_original.csv"):
        print("Erreur : contacts_original.csv manquant.")
        exit()
    G = load_graph("data/contacts_original.csv")
    deg_dist, _ = analyze_degrees(G)
    prox_values, _ = analyze_proximity(G)
    plot_distribution(deg_dist, "Distribution des degrés", "results/degree_distribution.png", "Degré")
    plot_distribution(prox_values, "Distribution de proximité", "results/proximity_distribution.png", "Somme des distances")