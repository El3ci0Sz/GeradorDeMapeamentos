import unittest
from collections import deque
from cgra import CGRA
from mapping_generator import Mapping_generator

class TestMapping_generator(unittest.TestCase):

    def setUp(self):
        self.cgra_dim = (3, 3)
        self.cgra = CGRA(self.cgra_dim, "Teste_CGRA")
        self.alpha = 2
        self.graph_edges = [
            (0, 1),
            (1, 2), 
            (2, 3)
        ]
    
    def test_get_neighbors_mesh(self):
        node = (1, 1)
        target_neighbors = [(0, 1),
                            (2, 1),
                            (1, 0),
                            (1, 2)]
        
        actual_neighbors = Mapping_generator.get_neighbors_mesh(node, self.cgra_dim)
        self.assertCountEqual(actual_neighbors, target_neighbors, "Teste de vizinhos da malha está correto")

    def test_calculate_distance(self):
        pe1 = (0, 0)
        pe2 = (2, 2)
        target_distance = 4
        actual_distance = Mapping_generator.calculate_distance(pe1, pe2)
        self.assertEqual(actual_distance, target_distance, "Teste de cálculo de distância Manhattan está correto")

    def test_is_connection_valid(self):
        pe1 = (0, 0)
        pe2 = (1, 1)
        self.assertTrue(Mapping_generator.is_connection_valid(pe1, pe2, self.alpha), "Conexão deve ser válida")
        pe3 = (3, 3)
        self.assertFalse(Mapping_generator.is_connection_valid(pe1, pe3, self.alpha), "Conexão deve ser inválida")

    def test_mapping(self):
        mapped_nodes = Mapping_generator.mapping(self.graph_edges, self.cgra, self.alpha)
        node_count = len(set(n for edge in self.graph_edges for n in edge))
        self.assertEqual(len(mapped_nodes), node_count, "Todos os nós do grafo devem ser mapeados")
        for node, position in mapped_nodes.items():
            self.assertTrue(0 <= position[0] < self.cgra_dim[0], "A posição da linha está dentro do limite do CGRA")
            self.assertTrue(0 <= position[1] < self.cgra_dim[1], "A posição da coluna está dentro do limite do CGRA")



if __name__ == "__main__":
    unittest.main()