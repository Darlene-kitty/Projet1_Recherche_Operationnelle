# src/analyze_graph.py
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

# === CONFIGURATION ===
CSV_FILE = "contacts.csv"  # Fichier d'entrée
RESULTS_DIR = Path("src/results")  # Dossier pour les images
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


# === FONCTIONS ===
def load_graph_from_csv(csv_path):
    """Charge le graphe à partir du fichier CSV."""
    if not Path(csv_path).exists():
        raise FileNotFoundError(f"Fichier {csv_path} introuvable. Exécute generate_graphe.py d'abord.")

    G = nx.Graph()
    df = pd.read_csv(csv_path)

    # Vérification des colonnes
    expected_cols = ['sommet_i', 'sommet_j', 'jours_moyen']
    if not all(col in df.columns for col in expected_cols):
        raise ValueError(f"Le fichier CSV doit contenir les colonnes : {expected_cols}")

    # Ajout des arêtes avec poids
    for _, row in df.iterrows():
        i, j, weight = int(row['sommet_i']), int(row['sommet_j']), int(row['jours_moyen'])
        G.add_edge(i, j, weight=weight)

    print(f"Graphe chargé : {G.number_of_nodes()} sommets, {G.number_of_edges()} arêtes")
    return G


def analyze_degrees(G):
    """Analyse la distribution des degrés."""
    degrees = [d for n, d in G.degree()]
    avg_degree = sum(degrees) / len(degrees)
    max_degree = max(degrees)
    min_degree = min(degrees)

    print(f"\nAnalyse des degrés :")
    print(f"  → Degré moyen : {avg_degree:.2f}")
    print(f"  → Degré max : {max_degree} (nœud {degrees.index(max_degree)})")
    print(f"  → Degré min : {min_degree}")

    return degrees, avg_degree


def plot_degree_distribution(degrees):
    """Génère et sauvegarde l'histogramme des degrés."""
    plt.figure(figsize=(10, 6))
    plt.hist(degrees, bins=30, color='skyblue', edgecolor='black', alpha=0.7)
    plt.title("Distribution des degrés du réseau de contacts", fontsize=14, pad=20)
    plt.xlabel("Degré")
    plt.ylabel("Nombre de nœuds")
    plt.grid(True, alpha=0.3)

    output_path = RESULTS_DIR / "degree_distribution.png"
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Histogramme sauvegardé : {output_path}")


def analyze_closeness_centrality(G, top_n=5):
    """Calcule la centralité de proximité et retourne les top nœuds."""
    print("\nCalcul de la centralité de proximité (peut prendre du temps)...")
    closeness = nx.closeness_centrality(G)

    avg_closeness = sum(closeness.values()) / len(closeness)
    sorted_nodes = sorted(closeness.items(), key=lambda x: x[1], reverse=True)
    top_nodes = sorted_nodes[:top_n]

    print(f"  → Proximité moyenne : {avg_closeness:.4f}")
    print(f"  → Top {top_n} nœuds par proximité :")
    for node, score in top_nodes:
        print(f"     • Nœud {node} : {score:.4f}")

    return closeness, avg_closeness, top_nodes


def top_degree_nodes(G, top_n=5):
    """Retourne les nœuds avec le plus haut degré."""
    degree_dict = dict(G.degree())
    sorted_by_degree = sorted(degree_dict.items(), key=lambda x: x[1], reverse=True)
    top_nodes = sorted_by_degree[:top_n]

    print(f"\nTop {top_n} nœuds par degré :")
    for node, deg in top_nodes:
        print(f"  • Nœud {node} : degré {deg}")

    return top_nodes


# === MAIN ===
def main():
    print("=== ANALYSE DU GRAPHE DE CONTACTS ===\n")

    try:
        # 1. Chargement
        G = load_graph_from_csv(CSV_FILE)

        # 2. Degrés
        degrees, avg_degree = analyze_degrees(G)
        plot_degree_distribution(degrees)

        # 3. Top nœuds par degré
        top_degree_nodes(G, top_n=5)

        # 4. Proximité
        closeness, avg_closeness, top_closeness = analyze_closeness_centrality(G, top_n=5)

        # 5. Résumé final
        print("\n" + "=" * 50)
        print("RÉSUMÉ DE L'ANALYSE")
        print("=" * 50)
        print(f"• Nombre de clients : {G.number_of_nodes()}")
        print(f"• Nombre de relations : {G.number_of_edges()}")
        print(f"• Degré moyen : {avg_degree:.2f}")
        print(f"• Proximité moyenne : {avg_closeness:.4f}")
        print(f"• Fichier image généré : src/results/degree_distribution.png")
        print("=" * 50)

    except Exception as e:
        print(f"Erreur : {e}")


if __name__ == "__main__":
    main()