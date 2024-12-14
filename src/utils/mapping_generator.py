import random
import numpy as np
from collections import deque
from cgra.cgra import CGRA

class Mapping_generator:
    '''
    Classe:
        Classe principal, onde estão os metodos de mapeamento e os metodos de Manipulação.

    inputs:
    dfg_tam (int)-> tamanho do dfg
    graph_edges (list[list])-> lista de arestas de um grafo
    II (int)-> Initiation Interval
    alpha (int)-> Limiar de conexões
    cgra_dim (tupla)-> Dimensão do cgra 
    arch_name (str)-> Nome da Arquitetura
    '''

    def __init__(self, dfg_tam, graph_edges, II, alpha, cgra : CGRA, cgra_dim, arch_name):
        self.dfg_tam = dfg_tam
        self.graph_edges = graph_edges
        self.II = II
        self.alpha = alpha
        self.CGRA = cgra(cgra_dim, arch_name)

    '''
    Metodo:
        Apartir de um nó, é verificado e armazenado os vizinhos dele.
    inputs:
        node (tupla): Posição de um nó.
        cgra_dim (tuplas): Dimensões do CGRA.
    outputs:
        neighbors (lits): Lista com os vizinhos do nó.
    '''
    @staticmethod
    def get_neighbors_mesh(node, cgra_dim):
            r_node, c_node = node
            linhas, colunas = cgra_dim

            neighbors = []
            if r_node > 0: neighbors.append((r_node - 1, c_node))
            if r_node < linhas - 1: neighbors.append((r_node + 1, c_node)) 
            if c_node > 0: neighbors.append((r_node, c_node - 1))  
            if c_node < colunas - 1: neighbors.append((r_node, c_node + 1))  
            return neighbors

    
    '''
    Quero sua opnião sobre essas 2 funções, Estava pesquisandosobre como o alpha é utilizado em algoritmos e
    codigos, e encontrei essa forma, que fez sentido para mim.
    '''
    @staticmethod
    def calculate_distance(pe1, pe2):
        """
        Calcula a distância Manhattan entre dois PEs.
        """
        return abs(pe1[0] - pe2[0]) + abs(pe1[1] - pe2[1])

    @staticmethod
    def is_connection_valid(pe1, pe2, alpha):
        """
        Verifica se a conexão entre dois PEs é válida com base no limiar alpha.
        """
        return Mapping_generator.calculate_distance(pe1, pe2) <= alpha

    
    '''
    Metodo:
        Realiza o mapeamento dos nós de um grafo no CGRA utilizando BFS (Busca em Largura).
        O mapeamento associa cada nó a uma unidade de processamento do CGRA, considerando
        as conexões válidas com base no limiar alpha.

    inputs:
        graph_edges (list[list]): Lista de arestas do grafo, onde cada aresta conecta dois nós.
        cgra (CGRA): Instância da arquitetura CGRA.
        alpha (int): Limiar de distância para conexões válidas.

    outputs:
        mapped_nodes (dict): Dicionário onde as chaves são os nós do grafo e os valores
        são as posições correspondentes no CGRA.
    '''
    @staticmethod
    def mapping(graph_edges, cgra: CGRA, alpha):
        linhas, colunas = cgra.cgra_dim
        visited = set()
        start = (random.randint(0, linhas - 1), random.randint(0, colunas - 1))
        queue = deque([start])
        mapped_nodes = {}
        node_count = len(set(n for edge in graph_edges for n in edge))

        while queue and len(mapped_nodes) < node_count:
            current = queue.popleft()
            if current in visited:
                continue
            visited.add(current)

            node = len(mapped_nodes)
            mapped_nodes[node] = current

            neighbors = Mapping_generator.get_neighbors_mesh(current, cgra.cgra_dim)
            valid_neighbors = [n for n in neighbors if Mapping_generator.is_connection_valid(current, n, alpha)]
        
            if valid_neighbors:
                queue.extend(valid_neighbors)
                
        return mapped_nodes
    
    
    