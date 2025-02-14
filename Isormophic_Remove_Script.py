import os
import networkx as nx
from networkx.algorithms.isomorphism import GraphMatcher

def load_graph_from_dot(file_path):
    """
        Carrega um grafo a partir de um arquivo .dot .

        file_path: Caminho para o arquivo.dot.
    """
    try:
        return nx.drawing.nx_pydot.read_dot(file_path)
    except Exception as e:
        print(f"Erro ao carregar {file_path}: {e}")
        return None

def remove_isomorphic_graphs(folder_path):
    """
        Remove grafos isomorfos dentro de uma pasta.
    
        folder_path: Caminho para a pasta, que se quer remover grafos isomorfos.
    """
    graph_files = [f for f in os.listdir(folder_path) if f.endswith(".dot")]
    graphs = []
    graphs_to_remove = set()

    for file in graph_files:
        file_path = os.path.join(folder_path, file)
        graph = load_graph_from_dot(file_path)
        if graph is None:
            continue
        
        is_isomorphic = False
        for existing_graph in graphs:
            if GraphMatcher(existing_graph, graph).is_isomorphic():
                is_isomorphic = True
                graphs_to_remove.add(file_path)
                break
        
        if not is_isomorphic:
            graphs.append(graph)
    
    for file in graphs_to_remove:
        os.remove(file)
        print(f"Removido: {file}")

    print("Processo concluído. Grafos isomorfos removidos.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Uso: python remover_isomorfos.py <caminho_para_pasta>")
    else:
        remove_isomorphic_graphs(sys.argv[1])