import random
from collections import deque, defaultdict
from src.cgra.cgra import CGRA
from src.utils.Mapping import Mapping

class Mapping_generator:
    """
    Classe responsável por gerar e verificar mapeamentos aleatórios deum DFG para um CGRA.
    """

    """
    input:
    dfg_tam (int)-> tamanho do dfg
    II (int)-> Initiation Interval
    alpha, alpha2 (float)-> Limiar de conexões
    CGRA (CGRA)-> Arquitetura CGRA
    """
    def __init__(self, dfg_tam, II, alpha, alpha2, cgra: CGRA):

        self.dfg_tam = dfg_tam
        self.II = II
        self.alpha = alpha
        self.alpha2 = alpha2
        self.CGRA = cgra
    """
    Verifica se o grafo DFG está totalmente conectado.

    Input:
        mapping (Mapping): Contem os dados do mapeamento.

    Returns:
        bool: True se o grafo for conectado, False caso contrário.
    """
    def is_connected(self, mapping: Mapping):
       
        if not mapping.dfg_edges:
            return False

        visited = set()

        def dfs(node):
            if node not in visited:
                visited.add(node)
                for neighbor in mapping.dfg_edges[node]:
                    dfs(neighbor)

        start_node = next(iter(mapping.dfg_edges))
        dfs(start_node)

        return len(visited) == self.dfg_tam
    
    """
    Realiza um placement aleatório dos nós no CGRA.

    Input:
        mapping (Mapping): Contem os dados do mapeamento.

    Ouput:
        Atualiza o valor do placement no Mapping.
    """
    def Placement(self, mapping: Mapping):

        rows, cols = self.CGRA.cgra_dim
        max = rows * cols * self.II

        if max < self.dfg_tam:
            raise ValueError("Capacidade insuficiente!!")

        available_positions = [
            (row, col, cycle)
            for row in range(rows)
            for col in range(cols)
            for cycle in range(self.II)
        ]
        random.shuffle(available_positions)

        for node in range(self.dfg_tam):
            if not available_positions:
                raise ValueError(f"Capacidade insuficiente!!")
            mapping.placement[node] = available_positions.pop()

    """
    Realiza o roteamentodas conexões no CGRA, com um numero maximo de tentativas pré-estabelecidas, esta sem limite para testes por enqunato.

    Input:
        mapping (Mapping): Contem os dados do mapeamento.
        alpha (float): Probabilidade de criar novas conexões.
        alpha2 (float): Probabilidade de remover conexões existentes.

    Ouput:
        Atualiza o valor do Routing em Mapping, e retorna as arestas do DFG.
    """
    def Routing(self, mapping: Mapping, alpha, alpha2):
        max_attempts = 10

        rows, cols = self.CGRA.cgra_dim

        for attempt in range(max_attempts):
            mapping.dfg_edges = defaultdict(list)
            mapping.routing = []

            queue = deque([random.randint(0, self.dfg_tam - 1)])
            visited = set(queue)

            position_to_node = {pos: node for node, pos in mapping.placement.items()}

            while queue:
                current_node = queue.popleft()
                current_cycle = mapping.placement[current_node][2]
                neighbors = self.get_neighbors_mesh(current_node, (rows, cols), current_cycle)

                for neighbor_pos in neighbors:
                    if neighbor_pos not in position_to_node:
                        continue

                    neighbor_node = position_to_node[neighbor_pos]

                    if neighbor_node == current_node:
                        continue

                    if neighbor_node not in visited:
                        mapping.dfg_edges[current_node].append(neighbor_node)
                        mapping.routing.append((current_node, neighbor_node))
                        queue.append(neighbor_node)
                        visited.add(neighbor_node)

                    else:
                        if random.random() < alpha:
                            mapping.dfg_edges[current_node].append(neighbor_node)
                            mapping.routing.append((current_node, neighbor_node))

                            if random.random() < alpha2 and mapping.dfg_edges[neighbor_node]:
                                target_to_remove = random.choice(list(mapping.dfg_edges[neighbor_node]))
                                mapping.routing.remove((neighbor_node, target_to_remove))

            if self.is_connected(mapping):
                return mapping.dfg_edges


    """
    Realiza o mapeamento completo (placement + routing) de um DFG no CGRA.

    Returns:
        Mapping: O mapeamento gerado.
    """
    def mapp(self):

        while True:
            mapping = Mapping(self.dfg_tam)
            self.Placement(mapping)
            self.Routing(mapping, self.alpha, self.alpha2)
            if self.is_connected(mapping):
                return mapping
            
    """
    Calcula os vizinhos de um nó, no ciclo atual e também no próximo ciclo.

    Input:
        node (int): Indice do no.
        cgra_dim (tuple): Dimensões do CGRA (linhas, colunas).
        cycle (int): Ciclo atual do nó.

    Returns:
        list[tuple]: Lista dos vizinhos no formato (row, col, cycle).
    """
    def get_neighbors_mesh(self, node, cgra_dim, cycle):
       

        rows, cols = cgra_dim
        r_node = node // cols
        c_node = node % cols

        neighbors = []

        if r_node > 0:
            neighbors.append((r_node - 1, c_node, cycle))
        if r_node < rows - 1:
            neighbors.append((r_node + 1, c_node, cycle))
        if c_node > 0:
            neighbors.append((r_node, c_node - 1, cycle))
        if c_node < cols - 1:
            neighbors.append((r_node, c_node + 1, cycle))

        if self.II > 0:
            cycle_prox = (cycle + 1) % self.II
            if r_node > 0:
                neighbors.append((r_node - 1, c_node, cycle_prox))
            if r_node < rows - 1:
                neighbors.append((r_node + 1, c_node, cycle_prox))
            if c_node > 0:
                neighbors.append((r_node, c_node - 1, cycle_prox))
            if c_node < cols - 1:
                neighbors.append((r_node, c_node + 1, cycle_prox))

        return neighbors
