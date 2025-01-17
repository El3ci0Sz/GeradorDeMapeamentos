import random
from collections import deque, defaultdict
from src.cgra.cgra import CGRA
from src.utils.Mapping import Mapping

class Mapping_generator:
    """
    Classe responsável por gerar e verificar mapeamentos aleatórios de um DFG para um CGRA.
    """

    def __init__(self, dfg_tam, II, alpha, alpha2, cgra: CGRA):
        """
        Inicializa os parâmetros necessários para o mapeamento.

        Args:
            dfg_tam (int): Número de nós no DFG.
            II (int): Intervalo de inicialização (Initiation Interval) do CGRA.
            alpha (float): Probabilidade de criar conexões adicionais.
            alpha2 (float): Probabilidade de remover conexões existentes.
            cgra (CGRA): Objeto representando a arquitetura do CGRA.
        """
        self.dfg_tam = dfg_tam
        self.II = II
        self.alpha = alpha
        self.alpha2 = alpha2
        self.CGRA = cgra

    def is_connected(self, mapping: Mapping):
        """
        Verifica se o grafo DFG está completamente conectado.

        Args:
            mapping (Mapping): Objeto contendo dados do mapeamento.

        Returns:
            bool: True se o DFG for conectado, False caso contrário.
        """
        if not mapping.dfg_edges:
            return False

        visited = set()

        def dfs(node):
            """
            Realiza busca em profundidade para verificar conectividade.
            """
            if node not in visited:
                visited.add(node)
                for neighbor in mapping.dfg_edges[node]:
                    dfs(neighbor)

        start_node = next(iter(mapping.dfg_edges))
        dfs(start_node)
        return len(visited) == self.dfg_tam

    def Placement(self, mapping: Mapping):
        """
        Realiza o placement aleatório dos nós no CGRA.

        Args:
            mapping (Mapping): Objeto contendo dados do mapeamento.

        Raises:
            ValueError: Se a capacidade do CGRA for insuficiente.
        """
        rows, cols = self.CGRA.cgra_dim
        max_positions = rows * cols * self.II

        if max_positions < self.dfg_tam:
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

    def Routing(self, mapping: Mapping):
        max_attempts = 10
        rows, cols = self.CGRA.cgra_dim

        for attempt in range(max_attempts):
            mapping.dfg_edges = defaultdict(list)
            mapping.routing = []
            mapping.neighbors = defaultdict(list)

            position_to_node = {pos: node for node, pos in mapping.placement.items()}
            visited = set()

            queue = deque([random.randint(0, self.dfg_tam - 1)])
            visited.add(queue[0])

            while queue:
                current_node = queue.popleft()
                current_pos = mapping.placement[current_node]

                neighbors = self.get_neighbors_mesh(mapping, current_node)
                mapping.neighbors[current_node] = neighbors

                if len(visited) > self.dfg_tam * 2:
                    raise RuntimeError("Timeout no roteamento devido a possíveis loops infinitos.")

                for neighbor_pos in neighbors:
                    if neighbor_pos not in position_to_node:
                        continue

                    neighbor_node = position_to_node[neighbor_pos]

                    if neighbor_node == current_node:
                        continue

                    if neighbor_node in mapping.dfg_edges[current_node] or current_node in mapping.dfg_edges[neighbor_node]:
                        continue

                    if neighbor_node not in visited:
                        mapping.dfg_edges[current_node].append(neighbor_node)
                        mapping.routing.append((current_node, neighbor_node))
                        queue.append(neighbor_node)
                        visited.add(neighbor_node)

                    else:
                        if random.random() < self.alpha:
                            mapping.dfg_edges[current_node].append(neighbor_node)
                            mapping.routing.append((current_node, neighbor_node))

                            if random.random() < self.alpha2 and mapping.dfg_edges[neighbor_node]:
                                target_to_remove = random.choice(list(mapping.dfg_edges[neighbor_node]))
                                if (neighbor_node, target_to_remove) in mapping.routing:
                                    mapping.routing.remove((neighbor_node, target_to_remove))

            if self.is_connected(mapping):
                return mapping.dfg_edges

    def mapp(self):
        """
        Realiza o mapeamento completo (placement + routing) do DFG no CGRA.

        Returns:
            Mapping: Objeto contendo o mapeamento gerado.
        """
        while True:
            mapping = Mapping(self.dfg_tam)
            self.Placement(mapping)
            self.Routing(mapping)
            if self.is_connected(mapping):
                return mapping

    def get_neighbors_mesh(self, mapping, node):
        """
        Retorna os vizinhos de um nó no CGRA com base na posição atual.

        Args:
            mapping (Mapping): Objeto contendo o mapeamento atual.
            node (int): Nó atual.
            cgra_dim (tuple): Dimensões do CGRA (linhas, colunas).
            cycle (int): Ciclo atual.

        Returns:
            list: Lista de posições (linha, coluna, ciclo) dos vizinhos.
        """
        rows, cols = self.CGRA.cgra_dim

        if node not in mapping.placement:
            return []

        r_node, c_node, cycle_node = mapping.placement[node]
        neighbors = []

        if r_node > 0:
            neighbors.append((r_node - 1, c_node, cycle_node))
        if r_node < rows - 1:
            neighbors.append((r_node + 1, c_node, cycle_node))
        if c_node > 0:
            neighbors.append((r_node, c_node - 1, cycle_node))
        if c_node < cols - 1:
            neighbors.append((r_node, c_node + 1, cycle_node))

        if self.II > 0:
            next_cycle = (cycle_node + 1) % self.II
            if r_node > 0:
                neighbors.append((r_node - 1, c_node, next_cycle))
            if r_node < rows - 1:
                neighbors.append((r_node + 1, c_node, next_cycle))
            if c_node > 0:
                neighbors.append((r_node, c_node - 1, next_cycle))
            if c_node < cols - 1:
                neighbors.append((r_node, c_node + 1, next_cycle))

        return neighbors
