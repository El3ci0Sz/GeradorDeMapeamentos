import unittest
import numpy as np
from tests.src.utils.cgra import CGRA

class TestCGRA(unittest.TestCase):

    def test_faz_matriz(self):

        actual_cgra = CGRA((2,2), "Teste_CGRA")
        target_matriz = [[-1,-1],
                         [-1,-1]]
        
        target_edges = [((0, 0), (1, 0)),  
                       ((0, 0), (0, 1)),
                       ((0, 1), (1, 1)), 
                       ((1, 0), (1, 1))] 

        np.testing.assert_array_equal(actual_cgra.matriz, target_matriz, "Teste da matriz esta certo")
        self.assertEqual(actual_cgra.edges , target_edges, "Teste das conexões esta certo")

if __name__ == "__main__":
    unittest.main()