from cgra import CGRA
import random

class Graph_Transformer:

    """
    Classe que contém metodos, para manipulação de grafos.
    """

    """
        Inverte as posições dos nós do mapeamento em relação ao eixo especificado.
        inputs:
            mapping (dict): Contem a posição dos nos mapeados {nó: (linha, coluna)}.
            cgra_dim (tupla): Dimensões do CGRA.
            axis (str): 'horizontal' ou 'vertical'.
        output:
            dict: Novo mapeamento após o flip.
    """

    @staticmethod
    def flip(dfg_mapping, cgra_dim, axis="horizontal"):
        rows, columns = cgra_dim

        if axis not in ["horizontal", "vertical"]:
            raise ValueError("O eixo deve ser 'horizontal' ou 'vertical'.")

        flip_mapping = {}
        for node, (r, c) in dfg_mapping.items():
            if axis == "horizontal":
                flip_mapping[node] = (rows - 1 - r, c)
            elif axis == "vertical":
                flip_mapping[node] = (r, columns - 1 - c)
        
        return flip_mapping
    
    """
        Desloca os nós do mapeamento por shift_x (horizontal) e shift_y (vertical).
        inputs:
            mapping (dict): Dicionário de mapeamento {nó: (linha, coluna)}.
            cgra_dim (tupla): Dimensões do CGRA.
            shift_x (int): Deslocamento no eixo x (columns).
            shift_y (int): Deslocamento no eixo y (rows).
        output:
            dict: Novo mapeamento após o deslocamento.
    """

    def shift(dfg_mapping, cgra_dim, shift_x, shift_y):
        
        rows, columns = cgra_dim
        shifted_mapping = {}

        for node, (r, c) in dfg_mapping.items():
            new_r = (r + shift_y) % rows
            new_c = (c + shift_x) % columns
            if new_r < 0: new_r += rows
            if new_c < 0: new_c += columns
            shifted_mapping[node] = (new_r, new_c)
        
        return shifted_mapping


    """
        Rotaciona o mapeamento pelos ângulos 90, 180 ou 270 graus.
        inputs:
            mapping (dict): Dicionário de mapeamento {nó: (linha, coluna)}.
            cgra_dim (tupla): Dimensões do CGRA.
            degrees (int): Ângulo de rotação (90, 180, 270).
        output:
            dict: Novo mapeamento após a rotação.
    """

    @staticmethod
    def rotate(dfg_mapping, cgra_dim, degrees):
        rows, columns = cgra_dim

        if degrees not in [90, 180, 270]:
            raise ValueError("ERRO. Apenas 90, 180 e 270 graus são suportados.")

        rotate_mapping = {}
        for node, (r, c) in dfg_mapping.items():
            if degrees == 90:
                rotate_mapping[node] = (c, rows - 1 - r)
            elif degrees == 180:
                rotate_mapping[node] = (rows - 1 - r, columns - 1 - c)
            elif degrees == 270:
                rotate_mapping[node] = (columns - 1 - c, r)

            rotate_mapping[node] = (
                rotate_mapping[node][0] % rows,
                rotate_mapping[node][1] % columns,
            )

        return rotate_mapping
    
    """
        Troca as coordenadas (x, y) para (y, x) de cada nó no mapeamento.
        inputs:
            mapping (dict): Dicionário de mapeamento {nó: (linha, coluna)}.
        outputs:
            inverted_mapping (dict): Novo dicionário com as coordenadas trocadas.
    """

    @staticmethod
    def invert(dfg_mapping):
        
        inverted_mapping = {node: (pos[1], pos[0]) for node, pos in dfg_mapping.items()}
        return inverted_mapping
    
    """
        Remove posições do mapeamento, subistituindo a posição por -1.
        inputs:
            mapping (dict): Dicionário de mapeamento {nó: (linha, coluna)}.
            allow_disconnected (bool): ?.
        output:
            dict: Mapeamento após a remoção das posições.
    """
    
    @staticmethod
    def prune(mapping, allow_disconnected):
        
        prune_mapping = {}
        prune_mapping = {node: -1 for node in mapping.keys()}

        return prune_mapping
    
    """
        Remove mapeamentos isomórficos em uma lista de mapeamentos.

        inputs:
            mappings_list (list[dict]): Lista de dicionários de mapeamento {nó: (linha, coluna)}.
        
        outputs:
            unique_mappings (list[dict]): Lista de mapeamentos únicos (não-isomórficos).
    """
    
    @staticmethod
    def remove_isomorphic_mappings(mappings_list):
      
        unique_set = set()
        unique_mappings = []

        for mapping in mappings_list:

            comparation_tuple = tuple(sorted(mapping.items()))

            if comparation_tuple not in unique_set:
                unique_set.add(comparation_tuple)
                unique_mappings.append(mapping)

        return unique_mappings
