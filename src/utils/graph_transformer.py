from collections import defaultdict
from src.utils.Mapping import Mapping

class Graph_Transformer:
    """
    Classe para manipulação de grafos no contexto de CGRA e DFG.
    """

    """
    Reflete o placement em relação a um eixo.

    Input:
        dfg_mapping (dict): Mapeamento de nós no CGRA.
        cgra_dim (tuple): Dimensões do CGRA.
        axis (str): 'horizontal' ou 'vertical'.

    Output:
        dict: Novo mapeamento após o deslocamento.
    """
    @staticmethod
    def flip(dfg_mapping, cgra_dim, axis):
        rows, cols = cgra_dim

        if axis not in ["horizontal", "vertical"]:
            raise ValueError("Eixo deve ser 'horizontal' ou 'vertical'.")

        flip_mapping = {}
        for node, (r, c, z) in dfg_mapping.items():
            if axis == "horizontal":
                flip_mapping[node] = (rows - 1 - r, c, z)
            elif axis == "vertical":
                flip_mapping[node] = (r, cols - 1 - c, z)
        
        return flip_mapping


    """
    Desloca os nós do mapeamento por shift_x (horizontal) e shift_y (vertical).

    Input:
        dfg_mapping (dict): Mapeamento de nós no CGRA.
        cgra_dim (tuple): Dimensões do CGRA.
        shift_x (int): Deslocamento no eixo x (columns).
        shift_y (int): Deslocamento no eixo y (rows).

    Output:
        dict: Novo mapeamento deslocado.
    """
    @staticmethod
    def shift(dfg_mapping, cgra_dim, shift_x, shift_y):
      
        rows, cols = cgra_dim
        shifted_mapping = {}

        for node, (r, c, z) in dfg_mapping.items():
            new_r = (r + shift_y) % rows
            new_c = (c + shift_x) % cols
            shifted_mapping[node] = (new_r, new_c, z)
        
        return shifted_mapping

    """
    Rotaciona o placement pelos ângulos 90, 180 ou 270 graus.

    Input:
        dfg_mapping (dict): Mapeamento de nós no CGRA.
        cgra_dim (tuple): Dimensões do CGRA.
        degrees (int): Ângulo de rotação (90, 180 ou 270).

    Output:
        dict: Novo mapeamento rotacionado.
    """
    @staticmethod
    def rotate(dfg_mapping, cgra_dim, degrees):
        
        rows, cols = cgra_dim

        if degrees not in [90, 180, 270]:
            raise ValueError("ERRO. Apenas 90, 180 e 270 graus são suportados")

        rotated_mapping = {}
        for node, (r, c,z) in dfg_mapping.items():
            if degrees == 90:
                rotated_mapping[node] = (c, rows - 1 - r, z)
            elif degrees == 180:
                rotated_mapping[node] = (rows - 1 - r, cols - 1 - c, z)
            elif degrees == 270:
                rotated_mapping[node] = (cols - 1 - c, r, z)

        return rotated_mapping

    """
    Inverte as arestas do DFG.

    Input:
        mapping (Mapping): Objeto contendo o grafo DFG.

    Output:
        Mapping: O mapeamento com arestas invertidas.
    """
    @staticmethod
    def invert(mapping: Mapping):
        
        inverted_edges = defaultdict(set)
        for source, targets in mapping.dfg_edges.items():
            for target in targets:
                inverted_edges[target].add(source)
        mapping.dfg_edges = inverted_edges
        return mapping

    """
    Remove nós do grafo DFG.

    Input:
        mapping (Mapping): O mapeamento contendo o DFG.
        node_type (str): Tipo do nó a ser removido ('leaf' ou 'root').
        allow_disconnected (bool): Parametro que permite ou não desconexão no grafo, garante conectividade se False ou permite desconexo se True.

    Output:
        Mapping: O mapeamento atualizado.
    """
    @staticmethod
    def prune(mapping: Mapping, node_type, allow_disconnected):
      
        if node_type == "leaf":
            leaves = [node for node in mapping.dfg_edges if not mapping.dfg_edges[node]]
            for leaf in leaves:
                if not allow_disconnected:
                    temp_edges = mapping.dfg_edges.copy()
                    temp_edges.pop(leaf)
                    if not Graph_Transformer.is_connected(temp_edges, len(mapping.dfg_vertices)):
                        continue
                for src in list(mapping.dfg_edges.keys()):
                    if leaf in mapping.dfg_edges[src]:
                        mapping.dfg_edges[src].remove(leaf)
                del mapping.dfg_edges[leaf]

        elif node_type == "root":
            roots = [node for node in mapping.dfg_edges if all(node not in targets for targets in mapping.dfg_edges.values())]
            for root in roots:
                if not allow_disconnected:
                    temp_edges = mapping.dfg_edges.copy()
                    temp_edges.pop(root)
                    if not Graph_Transformer.is_connected(temp_edges, len(mapping.dfg_vertices)):
                        continue
                del mapping.dfg_edges[root]

        return mapping
    
    """
    Verifica se o grafo DFG está conectado.

    Inputs:
        dfg_edges (dict): Arestas do grafo DFG.
        total_nodes (int): Número total de nós no DFG.

    Output:
        bool: True se o grafo for conectado, False caso contrário.
    """
    @staticmethod
    def is_connected(dfg_edges, total_nodes):
        if not dfg_edges:
            return False

        visited = set()
        all_nodes = set(dfg_edges.keys()).union(*dfg_edges.values())

        if not all_nodes:
            return False

        start_node = next(iter(all_nodes))

        def dfs(node):
            if node not in visited:
                visited.add(node)
                for neighbor in dfg_edges.get(node, []):
                    dfs(neighbor)

        dfs(start_node)

        return visited == all_nodes
