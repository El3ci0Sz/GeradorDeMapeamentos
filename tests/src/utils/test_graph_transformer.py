import unittest
from cgra import CGRA
from graph_transformer import Graph_Transformer

class TestGraphTransformer(unittest.TestCase):

    def setUp(self):
        # Configuração inicial para os testes
        self.dfg_mapping = {
            "A": (0, 0),
            "B": (1, 2),
            "C": (2, 1),
            "D": (3, 3),
        }
        self.cgra_dim = (4, 4)

    def test_flip_horizontal(self):
        result = Graph_Transformer.flip(self.dfg_mapping, self.cgra_dim, axis="horizontal")
        expected = {
            "A": (3, 0),
            "B": (2, 2),
            "C": (1, 1),
            "D": (0, 3),
        }
        self.assertEqual(result, expected)

    def test_flip_vertical(self):
        result = Graph_Transformer.flip(self.dfg_mapping, self.cgra_dim, axis="vertical")
        expected = {
            "A": (0, 3),
            "B": (1, 1),
            "C": (2, 2),
            "D": (3, 0),
        }
        self.assertEqual(result, expected)

    def test_shift(self):
        result = Graph_Transformer.shift(self.dfg_mapping, self.cgra_dim, shift_x=1, shift_y=2)
        expected = {
            "A": (2, 1),
            "B": (3, 3),
            "C": (0, 2),
            "D": (1, 0),
        }
        self.assertEqual(result, expected)

    def test_rotate_90(self):
        result = Graph_Transformer.rotate(self.dfg_mapping, self.cgra_dim, degrees=90)
        expected = {
            "A": (0, 3),
            "B": (2, 2),
            "C": (1, 1),
            "D": (3, 0),
        }
        self.assertEqual(result, expected)

    def test_rotate_180(self):
        result = Graph_Transformer.rotate(self.dfg_mapping, self.cgra_dim, degrees=180)
        expected = {
            "A": (3, 3),
            "B": (2, 1),
            "C": (1, 2),
            "D": (0, 0),
        }
        self.assertEqual(result, expected)

    def test_rotate_270(self):
        result = Graph_Transformer.rotate(self.dfg_mapping, self.cgra_dim, degrees=270)
        expected = {
            "A": (3, 0),
            "B": (1, 1),
            "C": (2, 2),
            "D": (0, 3),
        }
        self.assertEqual(result, expected)

    def test_invert(self):
        result = Graph_Transformer.invert(self.dfg_mapping)
        expected = {
            "A": (0, 0),
            "B": (2, 1),
            "C": (1, 2),
            "D": (3, 3),
        }
        self.assertEqual(result, expected)

    def test_prune(self):
        result = Graph_Transformer.prune(self.dfg_mapping, True)
        expected = {
            "A": -1,
            "B": -1,
            "C": -1,
            "D": -1,
        }
        self.assertEqual(result, expected)

    def test_remove_isomorphic_mappings(self):
        mappings_list = [
            {"A": (0, 0), "B": (1, 1)},
            {"A": (0, 0), "B": (1, 1)},
            {"A": (0, 1), "B": (1, 0)},
        ]
        result = Graph_Transformer.remove_isomorphic_mappings(mappings_list)
        expected = [
            {"A": (0, 0), "B": (1, 1)},
            {"A": (0, 1), "B": (1, 0)},
        ]
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()