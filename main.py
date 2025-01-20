from src.cgra.cgra import CGRA
from src.utils.Mapping import Mapping
from src.utils.mapping_generator import Mapping_generator
from src.utils.Graph_Visualizer import Graph_Visualizer

def functional_test():
    cgra_dim = (4, 4)
    arch_name = "TestArchitecture"
    cgra = CGRA(cgra_dim, arch_name)
    dfg_tam = 16
    II = 3
    alpha = 0.6
    alpha2 = 0.3

    mapping_generator = Mapping_generator(dfg_tam, II, alpha, alpha2, cgra)

    print("=== Teste: map_dfg_to_cgra ===")
    mapping = mapping_generator.mapp()
    print("\n\nResultados do Mapeamento:")
    print("- Placement (Posições dos Nós no CGRA):")
    for node, position in mapping.placement.items():
        print(f"  Nó {node}: {position}")
    
    print("\n- DFG Edges (Conexões no DFG):")
    for node, neighbors in mapping.dfg_edges.items():
        print(f"  Nó {node}: {neighbors}")

    print("\n- Routing (Roteamento das Arestas):")
    for route, path in mapping.routing.items(): 
        print(f"  Roteamento: {route} | Caminho : {path}")

    
    Graph_Visualizer.export_to_dot(mapping, "example_graph.dot")
    Graph_Visualizer.generate_image_from_dot("example_graph.dot", "example_graph.png")
    Graph_Visualizer.plot_cgra(mapping, cgra_dim, routing=False, output_file="placement_only.png")
    Graph_Visualizer.plot_cgra(mapping, cgra_dim, routing=True, output_file="placement_and_routing.png")

   


if __name__ == "__main__":
    functional_test()
