from src.cgra.cgra import CGRA
from src.utils.Mapping import Mapping
from src.utils.mapping_generator import Mapping_generator
import traceback
import networkx as nx
import matplotlib.pyplot as plt

def functional_test():

    cgra_dim = (4, 4)
    arch_name = "TestArchitecture"
    cgra = CGRA(cgra_dim, arch_name)

    dfg_tam = 10
    II = 2
    alpha = 0.6
    alpha2 = 0.3

    mapping_generator = Mapping_generator(dfg_tam, II, alpha, alpha2, cgra)

    print("=== Teste: map_dfg_to_cgra ===")
    mapping = mapping_generator.mapp()
    print("\n\nArestas")
    print(mapping.dfg_edges)
    print("\n\nResultados do Mapeamento:")
    print("- Placement (Posições dos Nós no CGRA):")
    for node, position in mapping.placement.items():
        print(f"  Nó {node}: {position}")
    
    print("\n- DFG Edges (Conexões no DFG):")
    for node, neighbors in mapping.dfg_edges.items():
        print(f"  Nó {node}: {neighbors}")

    print("\n- Routing (Roteamento das Arestas):")
    for route in mapping.routing:
        print(f"  {route}")

if __name__ == "__main__":
    functional_test()
