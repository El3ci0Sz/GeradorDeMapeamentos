import unittest
from collections import defaultdict
from src.utils.Mapping import Mapping
from src.utils.graph_transformer import Graph_Transformer
from src.cgra.cgra import CGRA
import copy

class TestGraphTransformer(unittest.TestCase):
    
    def setUp(self):
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
        flipped = Graph_Transformer.flip(self.mapping.placement, self.cgra_dim, 'horizontal')
        expected = {
            0: (2, 0, 0), 1: (1, 0, 0), 2: (0, 0, 0),
            3: (2, 1, 0), 4: (1, 1, 0), 5: (0, 1, 0),
            6: (2, 2, 0), 7: (1, 2, 0)
        }
        self.assertEqual(flipped, expected)

    def test_flip_vertical(self):
        flipped = Graph_Transformer.flip(self.mapping.placement, self.cgra_dim, 'vertical')
        expected = {
            0: (0, 2, 0), 1: (1, 2, 0), 2: (2, 2, 0),
            3: (0, 1, 0), 4: (1, 1, 0), 5: (2, 1, 0),
            6: (0, 0, 0), 7: (1, 0, 0)
        }
        self.assertEqual(flipped, expected)

    def test_invert(self):
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

    def test_prune_root_not_allow_disconnected(self):
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

    def test_prune_root_not_allow_disconnected(self):
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
        rotated = Graph_Transformer.rotate(self.mapping.placement, self.cgra_dim, 90)
        expected = {
            0: (0, 2, 0), 1: (0, 1, 0), 2: (0, 0, 0),
            3: (1, 2, 0), 4: (1, 1, 0), 5: (1, 0, 0),
            6: (2, 2, 0), 7: (2, 1, 0)
        }
        self.assertEqual(rotated, expected)

    def test_rotate_180(self):
        rotated = Graph_Transformer.rotate(self.mapping.placement, self.cgra_dim, 180)
        expected = {
            0: (2, 2, 0), 1: (1, 2, 0), 2: (0, 2, 0),
            3: (2, 1, 0), 4: (1, 1, 0), 5: (0, 1, 0),
            6: (2, 0, 0), 7: (1, 0, 0)
        }
        self.assertEqual(rotated, expected)

    def test_rotate_270(self):
        rotated = Graph_Transformer.rotate(self.mapping.placement, self.cgra_dim, 270)
        expected = {
            0: (2, 0, 0), 1: (2, 1, 0), 2: (2, 2, 0),
            3: (1, 0, 0), 4: (1, 1, 0), 5: (1, 2, 0),
            6: (0, 0, 0), 7: (0, 1, 0)
        }
        self.assertEqual(rotated, expected)

    def test_shift_0_1(self):
        shifted = Graph_Transformer.shift(self.mapping.placement, self.cgra_dim, 0, 1)
        expected = {
            0: (0, 0, 0),
            1: (1, 0, 0),
            2: (2, 0, 0),
            3: (0, 1, 0),
            4: (1, 1, 0),
            5: (2, 1, 0),
            6: (0, 2, 0),
            7: (2, 2, 0)
        }
        self.assertEqual(shifted, expected)

    def test_shift_1_0(self):
        shifted = Graph_Transformer.shift(self.mapping.placement, self.cgra_dim, 1, 0)
        expected = {
            0: (0, 0, 0),
            1: (1, 0, 0),
            2: (2, 0, 0),
            3: (0, 1, 0),
            4: (1, 1, 0),
            5: (2, 2, 0),
            6: (0, 2, 0),
            7: (1, 2, 0)
        }
        self.assertEqual(shifted, expected)

    def test_shift_1_1(self):
        shifted = Graph_Transformer.shift(self.mapping.placement, self.cgra_dim, 1, 1)
        expected = {
            0: (0, 0, 0),
            1: (1, 0, 0),
            2: (2, 0, 0),
            3: (0, 1, 0),
            4: (2, 2, 0),
            5: (2, 1, 0),
            6: (0, 2, 0),
            7: (1, 2, 0)
        }
        self.assertEqual(shifted, expected)

if __name__ == "__main__":
    unittest.main()
