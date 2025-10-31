# src/propagation.py
import networkx as nx
from analyze_graph import load_graph_from_csv


def campaign_reach(G, start_node, days):
    """
    Chaque arête = 1 jour
    Retourne le nombre de sommets atteints en <= days
    """
    distances = nx.shortest_path_length(G, source=start_node, weight='weight')
    reached = sum(1 for d in distances.values() if d <= days)
    return reached


if __name__ == "__main__":
    G = load_graph_from_csv()

    # Q5: Démarrer du sommet de plus haut degré, 5 jours
    degrees = dict(G.degree())
    start_deg = max(degrees, key=degrees.get)
    reach5 = campaign_reach(G, start_deg, 5)
    print(f"Q5: {reach5} sommets atteints en 5 jours (départ degré max)")

    # Q6: Démarrer du sommet de proximité la plus basse (somme max), 7 jours
    sum_dist = {n: sum(nx.shortest_path_length(G, n, weight='weight').values()) for n in G.nodes()}
    start_close = max(sum_dist, key=sum_dist.get)
    reach7 = campaign_reach(G, start_close, 7)
    print(f"Q6: {reach7} sommets atteints en 7 jours (départ proximité min)")