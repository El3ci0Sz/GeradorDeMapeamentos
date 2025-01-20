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
        """
        Realiza o roteamento do DFG no CGRA, gerando os caminhos de roteamento.

        Args:
            mapping (Mapping): Objeto contendo dados do mapeamento.
        """
        mapping.dfg_edges = defaultdict(list)
        mapping.routing = {}  # Inicializar como dicionário para salvar caminhos completos.

        position_to_node = {pos: node for node, pos in mapping.placement.items()}
        visited = set()

        queue = deque([random.randint(0, self.dfg_tam - 1)])
        visited.add(queue[0])

        while queue:
            current_node = queue.popleft()

            neighbors = self.get_neighbors_mesh(mapping, current_node)

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
                    queue.append(neighbor_node)
                    visited.add(neighbor_node)

                else:
                    if random.random() < self.alpha:
                        mapping.dfg_edges[current_node].append(neighbor_node)

                        if random.random() < self.alpha2 and mapping.dfg_edges[neighbor_node]:
                            target_to_remove = random.choice(list(mapping.dfg_edges[neighbor_node]))
                            mapping.dfg_edges[neighbor_node].remove(target_to_remove)

        for source, targets in mapping.dfg_edges.items():
            for target in targets:
                if (source, target) not in mapping.routing:
                    path = self.get_routing_path(mapping, source, target)
                    if path:
                        mapping.routing[(source, target)] = path
                    else:
                        raise ValueError(f"Roteamento falhou entre {source} e {target}.")


    def mapp(self, max_attempts=20000):
        """
        Realiza o mapeamento completo (placement + routing) do DFG no CGRA,
        garantindo que o mapeamento seja balanceado.

        Args:
            max_attempts (int): Número máximo de tentativas para encontrar um mapeamento balanceado.

        Returns:
            Mapping: Objeto contendo o mapeamento gerado.

        Raises:
            ValueError: Se o número máximo de tentativas for atingido sem encontrar um mapeamento balanceado.
        """
        for attempt in range(max_attempts):
            mapping = Mapping(self.dfg_tam)
            self.Placement(mapping)
            self.Routing(mapping)
            if self.is_connected(mapping) and not self.has_cycle(mapping.dfg_edges) and self.is_balanced(mapping):
                return mapping

        raise ValueError("Não foi possível encontrar um mapeamento balanceado após {max_attempts} tentativas.")

    def get_neighbors_mesh(self, mapping, node):
        """
        Retorna os vizinhos de um nó no CGRA com base na posição atual,
        considerando a conexão ao mesmo nó no próximo ciclo e aos vizinhos no próximo ciclo.

        Args:
            mapping (Mapping): Objeto contendo o mapeamento atual.
            node (int): Nó atual.

        Returns:
            list: Lista de posições (linha, coluna, ciclo) dos vizinhos.
        """
        rows, cols = self.CGRA.cgra_dim

        if node not in mapping.placement:
            return []

        r_node, c_node, cycle_node = mapping.placement[node]
        neighbors = []

        next_cycle = (cycle_node + 1) % self.II

        neighbors.append((r_node, c_node, next_cycle))

        if r_node > 0:
            neighbors.append((r_node - 1, c_node, next_cycle))
        if r_node < rows - 1:
            neighbors.append((r_node + 1, c_node, next_cycle))
        if c_node > 0:
            neighbors.append((r_node, c_node - 1, next_cycle))
        if c_node < cols - 1:
            neighbors.append((r_node, c_node + 1, next_cycle))

        return neighbors
    
    @staticmethod
    def get_routing_path(mapping, src, dst):
        """
        Retorna o caminho de roteamento de um nó para outro.

        Args:
            mapping (Mapping): Objeto contendo o mapeamento.
            src (int): Nó de origem.
            dst (int): Nó de destino.

        Returns:
            list: Caminho do roteamento (ex: [0, 1, 2]).
        """
        def dfs(current, path):
            if current == dst:
                return path
            for next_node in mapping.dfg_edges.get(current, []):
                if next_node not in path:
                    result = dfs(next_node, path + [next_node])
                    if result:
                        return result
            return None

        path = dfs(src, [src])
        if path:
            return path
        raise ValueError(f"Não foi encontrado um caminho de {src} para {dst}.")

    def has_cycle(self, dfg_edges):
        """
        Detecta se há ciclos em um grafo direcionado.

        Args:
            dfg_edges (dict): Dicionário de adjacência representando o grafo.

        Returns:
            bool: True se houver ciclo, False caso contrário.
        """
        visited = set()
        stack = set()

        def dfs(node, path):
            if node in stack:
                return True, path + [node]
            if node in visited:
                return False, []

            visited.add(node)
            stack.add(node)

            for neighbor in dfg_edges.get(node, []):
                has_cycle, cycle_path = dfs(neighbor, path + [node])
                if has_cycle:
                    return True, cycle_path

            stack.remove(node)
            return False, []

        for node in dfg_edges.keys():
            has_cycle, cycle_path = dfs(node, [])
            if has_cycle:
                return True

        return False
    
    @staticmethod
    def calculate_predecessors_and_levels(dfg_edges):
        
        """
        Calcula os predecessores e os níveis de cada nó no grafo de fluxo de dados (DFG).

        Args:
            dfg_edges (dict): Dicionário onde as chaves são nós e os valores são listas
                              de nós destino representando as arestas do DFG.

        Returns:
            tuple: Um dicionário com os predecessores de cada nó e um dicionário com os
                   níveis de cada nó no DFG.

        Raises:
            ValueError: Se forem detectados ciclos no DFG.
        """

        predecessors = {node: [] for node in dfg_edges}
        levels = {}
        
        for node, edges in dfg_edges.items():
            for dest in edges:
                predecessors[dest].append(node)
        
        aux_predecessors = {node: preds.copy() for node, preds in predecessors.items()}
        
        nodes_without_predecessors = deque(node for node, preds in aux_predecessors.items() if not preds)
        visited = set() 
        current_level = 0
        
        while nodes_without_predecessors:
            next_nodes = deque()
            for node in nodes_without_predecessors:
                if node in visited:
                    continue
                visited.add(node)
                levels[node] = current_level
                
                for dest in dfg_edges.get(node, []):
                    aux_predecessors[dest].remove(node)
                    if not aux_predecessors[dest]:
                        next_nodes.append(dest)
            
            nodes_without_predecessors = next_nodes
            current_level += 1
        

        nodes_in_cycles = set(dfg_edges.keys()) - visited
        if nodes_in_cycles:
            raise ValueError(f"Ciclo detectado nos nós: {nodes_in_cycles}")
        
        return predecessors, levels
    
    def is_balanced(self, mapping:Mapping):
        
        """
        Verifica se os predecessores de cada nó no DFG estão no mesmo nível.

        Args:
            mapping (Mapping): Objeto contendo os vértices e arestas do DFG.

        Returns:
            bool: True se todos os predecessores de cada nó estiverem no mesmo nível, False caso contrário.

        Raises:
            ValueError: Se o DFG apresentar ciclos.
        """

        predecessors, levels = self.calculate_predecessors_and_levels(mapping.dfg_edges)

        for node in mapping.dfg_vertices:
            preds = predecessors[node]
            if preds:
                pred_levels = {levels[pred] for pred in preds}
                if len(pred_levels) > 1:
                    print(f"Nó {node} tem predecessores em diferentes níveis: {pred_levels}")
                    return False
        return True
