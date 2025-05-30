from src.utils.Mapping import Mapping

"""
Para verificar e mudar, terminar de fazer as interconexões, e nao esquecer de verificar se para cada no, nao a vizinhos iguais entre as interconexões, por exemplo pegar um vizinho mesh que seja o mesmo diagonal, verificação para ignorar se for igual

Verificar tambem o que pode ser geral e o que pode ser modulado para tornar o codigo melhor.
"""

class Interconnection:
    def __init__(self, cgra_dim,interconnection:str, mapping:Mapping, II) -> None:
        self.bits = Interconnection.get_bits(interconnection)
        self.cgra_dim = cgra_dim
        self.mapping = mapping
        self.II = II
        self.neighbor_dict = self.get_interconnections()

    """
        bits:
        1000,1 bit = mesh
        0100,2 bit = diagonal
        0010,3 bit = one-hop
        0001,4 bit = toroidal
    """
    def get_interconnections(self):
        neighbor_dict = {}

        for node in self.mapping.placement.keys():
            neighbors = set()

            if self.bits[0] == 1:
                neighbors.update(self.mesh(node))
            if self.bits[1] == 1:
                neighbors.update(self.diagonal(node))
            if self.bits[2] == 1:
                neighbors.update(self.one_hop(node))
            if self.bits[3] == 1:
                neighbors.update(self.toroidal(node))

            neighbors.discard(self.mapping.placement.get(node, None))
            neighbor_dict[node] = list(neighbors) 

        return neighbor_dict

    def get_neighbors(self, node, directions, toroidal=False):

        if node not in self.mapping.placement:
            return set()

        rows, cols = self.cgra_dim
        r, c, t = self.mapping.placement[node]
        next_t = (t + 1) % self.II

        neighbors = set()

        if toroidal:
            # Toroidal horizontal (coluna)
            if c == 0:
                neighbors.add((r, cols - 1, next_t)) 
            elif c == cols - 1:
                neighbors.add((r, 0, next_t))

            # Toroidal vertical (linha)
            if r == 0:
                neighbors.add((rows - 1, c, next_t))  
            elif r == rows - 1:
                neighbors.add((0, c, next_t))         

        else:
            for x, y in directions:
                next_row, next_col = r + x, c + y

                if 0 <= next_row < rows and 0 <= next_col < cols:
                    neighbors.add((next_row, next_col, next_t))

        neighbors.add((r, c, next_t))

        return neighbors

    def mesh(self,node):

        directions = [
            (-1, 0),   # cima
            (1, 0),    # baixo
            (0, -1),   # esquerda
            (0, 1)     # direita
        ]

        return self.get_neighbors(node, directions)

    def diagonal(self, node):

        directions = [
            (-1, -1),   # diagonal: cima esquerda
            (-1, 1),    # diagonal: cima direita
            (1, -1),   # diagonal: baixo esquerda
            (1, 1)     # diagonal: baixo direita
        ]

        return self.get_neighbors(node, directions)
    
    def one_hop(self, node):

        directions = [
            (-2, 0),   # cima 
            (2, 0),    # baixo 
            (0, -2),   # esquerda 
            (0, 2)     # direita 
        ]
        return self.get_neighbors(node,directions)
        
    def toroidal(self, node):

                return self.get_neighbors(node,directions=[],toroidal=True)
    
    @staticmethod
    def get_bits(interconnection):
        interconnection = interconnection.ljust(4,'0')
        bits = [int(x) for x in interconnection]
        return bits
