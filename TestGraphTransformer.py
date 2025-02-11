import unittest
from collections import defaultdict
from src.utils.Mapping import Mapping
from src.utils.graph_transformer import Graph_Transformer
from src.cgra.cgra import CGRA
import copy

class TestGraphTransformer(unittest.TestCase):

    """
    Classe que contém testes unitarios para a classe graph_transformer.
    """
    
    def setUp(self):
        """
        Configuração das variaveis:

            cgra_dim (tuple): dimensão do cgra.
            mapping (Mapping): objeto da classe mapping, que armazena dados de mapemanto.
            
            - Define os vértices e arestas do grafo.
            - Define o posicionamento dos nós no CGRA.
        """
        self.cgra_dim = (3, 3)
        self.mapping = Mapping(8)
        self.mapping.dfg_edges = {
            0: {1, 2},
            1: {3},
            2: {4},
            3: {5},
            4: {6},
            5: {7},
            6: set(),
            7: set()
        }
        self.mapping.dfg_vertices = {0, 1, 2, 3, 4, 5, 6, 7}
        self.mapping.placement = {
            0: (0, 0, 0),
            1: (1, 0, 0),
            2: (2, 0, 0),
            3: (0, 1, 0),
            4: (1, 1, 0),
            5: (2, 1, 0),
            6: (0, 2, 0),
            7: (1, 2, 0)
        }

    def test_flip_horizontal(self):
        """
        Testa a função de espelhamento horizontal do grafo.
        """
        flipped = Graph_Transformer.flip(self.mapping.placement, self.cgra_dim, 'horizontal')
        expected = {
            0: (2, 0, 0), 1: (1, 0, 0), 2: (0, 0, 0),
            3: (2, 1, 0), 4: (1, 1, 0), 5: (0, 1, 0),
            6: (2, 2, 0), 7: (1, 2, 0)
        }
        self.assertEqual(flipped, expected)
    
    def test_flip_vertical(self):
        """
        Testa a função de espelhamento vertical do grafo.
        """
        flipped = Graph_Transformer.flip(self.mapping.placement, self.cgra_dim, 'vertical')
        expected = {
            0: (0, 2, 0), 1: (1, 2, 0), 2: (2, 2, 0),
            3: (0, 1, 0), 4: (1, 1, 0), 5: (2, 1, 0),
            6: (0, 0, 0), 7: (1, 0, 0)
        }
        self.assertEqual(flipped, expected)

    def test_invert(self):
        """
        Testa a inversão das arestas do grafo.
        """
        inverted = Graph_Transformer.invert(self.mapping)
        expected = {
            0: set(),
            1: {0},
            2: {0},
            3: {1},
            4: {2},
            5: {3},
            6: {4},
            7: {5}
        }
        self.assertEqual(inverted.dfg_edges, expected)

    def test_prune_leaf_allow_disconnected(self):
        """
        Testa a poda de nós folha, permitindo grafos desconectados.
        """
        pruned = Graph_Transformer.prune(self.mapping, 'leaf', True)
        expected = {
            0: {1, 2},
            1: {3},
            2: {4},
            3: {5},
            4: set(),
            5: set()
        }
        self.assertEqual(pruned.dfg_edges, expected)

    def test_prune_leaf_not_allow_disconnected(self):
        """
        Testa a poda de nós folha, sem permitir grafos desconectados.
        """
        pruned = Graph_Transformer.prune(self.mapping, 'leaf', False)
        expected = {
            0: {1, 2},
            1: {3},
            2: {4},
            3: {5},
            4: set(),
            5: set()
        }
        self.assertEqual(pruned.dfg_edges, expected)

    def test_prune_root_not_allow_disconnected_1(self):
        """
        Testa a poda de nó raiz, sem permitir grafos desconectados.

        Caso: A poda deixaria o grafo desconectado, então deve-se retornar o grafo sem alteração.
        """
        pruned = Graph_Transformer.prune(self.mapping, 'root', False)
        expected = {
            0: {1, 2},
            1: {3},
            2: {4},
            3: {5},
            4: {6},
            5: {7},
            6: set(),
            7: set()
        }
        self.assertEqual(pruned.dfg_edges, expected)

    def test_prune_root_not_allow_disconnected_2(self):
        """
        Testa a poda de nó raiz, sem permitir grafos desconectados.

        pruned_mapping_test: Nova configuração das arestas do grafo, para teste onde a poda de um nó raiz não gera um grafo desconectado.
        """
        pruned_mapping_test = copy.deepcopy(self.mapping)
        pruned_mapping_test.dfg_edges = {
            0: {1},
            1: {2},
            2: {3,4},
            3: {5},
            4: {6},
            5: {7},
            6: set(),
            7: set()
        }
        pruned = Graph_Transformer.prune(pruned_mapping_test, 'root', False)
        expected = {
            1: {2},
            2: {3,4},
            3: {5},
            4: {6},
            5: {7},
            6: set(),
            7: set()
        }
        self.assertEqual(pruned.dfg_edges, expected)

    def test_prune_root_allow_disconnected(self):
        """
        Testa a poda de nó raiz, sem permitindo grafos desconectados.
        """
        pruned = Graph_Transformer.prune(self.mapping, 'root', True)
        expected = {
            1: {3},
            2: {4},
            3: {5},
            4: {6},
            5: {7},
            6: set(),
            7: set()
        }
        self.assertEqual(pruned.dfg_edges, expected)
    
    def test_rotate_90(self):
        """
        Testa a rotação do grafo em 90 graus no sentido horário.
        """
        rotated = Graph_Transformer.rotate(self.mapping.placement, self.cgra_dim, 90)
        expected = {
            0: (0, 2, 0), 1: (0, 1, 0), 2: (0, 0, 0),
            3: (1, 2, 0), 4: (1, 1, 0), 5: (1, 0, 0),
            6: (2, 2, 0), 7: (2, 1, 0)
        }
        self.assertEqual(rotated, expected)

    def test_rotate_180(self):
        """
        Testa a rotação do grafo em 180 graus no sentido horário.
        """
        rotated = Graph_Transformer.rotate(self.mapping.placement, self.cgra_dim, 180)
        expected = {
            0: (2, 2, 0), 1: (1, 2, 0), 2: (0, 2, 0),
            3: (2, 1, 0), 4: (1, 1, 0), 5: (0, 1, 0),
            6: (2, 0, 0), 7: (1, 0, 0)
        }
        self.assertEqual(rotated, expected)

    def test_rotate_270(self):
        """
        Testa a rotação do grafo em 270 graus no sentido horário.
        """
        rotated = Graph_Transformer.rotate(self.mapping.placement, self.cgra_dim, 270)
        expected = {
            0: (2, 0, 0), 1: (2, 1, 0), 2: (2, 2, 0),
            3: (1, 0, 0), 4: (1, 1, 0), 5: (1, 2, 0),
            6: (0, 0, 0), 7: (0, 1, 0)
        }
        self.assertEqual(rotated, expected)

    """
    Configuração das variaveis para teste do shift

    test_placement: Nova configuração de placement usada, há apenas 4 nós, em 4 posições de 9 do CGRA (3x3).
    """
    def test_shift_0_1(self):
        """
        Testa o deslocamento do grafo em (0,1)-> uma posição para a direita.
        """
        test_placement = {
            0: (0, 0, 0),
            1: (1, 0, 0),
            2: (2, 0, 0),
            3: (0, 1, 0)
        }
        shifted = Graph_Transformer.shift(test_placement, self.cgra_dim, 0, 1)
        expected = {
            0: (0, 1, 0),
            1: (1, 1, 0),
            2: (2, 1, 0),
            3: (0, 2, 0)
        }
        self.assertEqual(shifted, expected)

    def test_shift_1_0(self):
        """
        Testa o deslocamento do grafo em (1,0)-> uma posição para baixo.
        """
        test_placement = {
            0: (0, 0, 0),
            1: (1, 0, 0),
            2: (2, 0, 0),
            3: (0, 1, 0)
        }
        shifted = Graph_Transformer.shift(test_placement, self.cgra_dim, 1, 0)
        expected = {
            0: (0, 0, 0),
            1: (1, 0, 0),
            2: (2, 0, 0),
            3: (0, 1, 0)
        }
        self.assertEqual(shifted , expected)

    def test_shift_1_1(self):
        """
        Testa o deslocamento do grafo em (1,1)-> uma posição para a direita e uma para baixo.
        """
        test_placement = {
            0: (0, 0, 0),
            1: (1, 0, 0),
            2: (1, 1, 0),
            3: (0, 1, 0)
        }
        shifted = Graph_Transformer.shift(test_placement, self.cgra_dim, 1, 1)
        expected = {
            0: (1, 1, 0),
            1: (2, 1, 0),
            2: (2, 2, 0),
            3: (1, 2, 0)
        }
        self.assertEqual(shifted, expected)

    def test_shift_0_1_not_possible(self):
        """
        Testa o deslocamento do grafo em (0,1)-> uma posição para a direita.

        Caso: Nesse caso há 8 nós, em um CGRA (3x3), não é possivel o deslocamento, se espera que o valor do placement retornado
        esteja sem alteração.

        expected: Mesma configuração que o placement original.
        """
        shifted = Graph_Transformer.shift(self.mapping.placement, self.cgra_dim, 0, 1)
        expected = {
            0: (0, 0, 0),
            1: (1, 0, 0),
            2: (2, 0, 0),
            3: (0, 1, 0),
            4: (1, 1, 0),
            5: (2, 1, 0),
            6: (0, 2, 0),
            7: (1, 2, 0)
        }
        self.assertEqual(shifted, expected)

if __name__ == "__main__":
    unittest.main()
