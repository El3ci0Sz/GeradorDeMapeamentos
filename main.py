import matplotlib.pyplot as plt
import os
from src.utils.Mapping import Mapping
import copy
from src.utils.Graph_Visualizer import Graph_Visualizer
from src.utils.graph_transformer import Graph_Transformer
from src.utils.mapping_generator import Mapping_generator
from src.cgra.cgra import CGRA

# dfg_tam = 10  
# II = 1 
# alpha = 0.2  
# alpha2 = 0.1  
# cgra_dim = (4, 4)  

# cgra = CGRA(cgra_dim, "Teste")
# mapping_generator = Mapping_generator(dfg_tam, II, alpha, alpha2, cgra)

# mapping = mapping_generator.mapp()

cgra_dim = (3, 3)
cgra = CGRA(cgra_dim, "TEST")
mapping = Mapping(8)
mapping.dfg_edges = {
    0: {1, 2},
    1: {3},
    2: {4},
    3: {5},
    4: {6},
    5: {7},
    6: set(),
    7: set()
}
mapping.dfg_vertices = {0, 1, 2, 3, 4, 5, 6, 7}
mapping.placement = {
    0: (0, 0, 0),
    1: (1, 0, 0),
    2: (1, 1, 0),
    3: (0, 1, 0)
}

print(mapping.placement)

Graph_Visualizer.export_to_dot(mapping, "original.dot")
Graph_Visualizer.generate_image_from_dot("original.dot")
Graph_Visualizer.plot_cgra(mapping, cgra.cgra_dim, output_file="original_placement.png")
export_mapping = copy.deepcopy(mapping)


# Teste de Flip
flipped_mapping = Graph_Transformer.flip(mapping.placement, cgra.cgra_dim, 'horizontal')
export_mapping.placement = flipped_mapping
Graph_Visualizer.plot_cgra(export_mapping, cgra.cgra_dim, output_file="flip_horizontal.png")

# Teste de Shift
shifted_mapping = Graph_Transformer.shift(mapping.placement, cgra.cgra_dim, 1, 1)
export_mapping.placement = shifted_mapping
Graph_Visualizer.plot_cgra(export_mapping, cgra.cgra_dim, output_file="shift.png")

# Teste de Rotação
rotated_mapping = Graph_Transformer.rotate(mapping.placement, cgra.cgra_dim, 270)
export_mapping.placement = rotated_mapping
Graph_Visualizer.plot_cgra(export_mapping, cgra.cgra_dim, output_file="rotate_270.png")

#Teste de Inversão de Arestas
temp_mapping = copy.deepcopy(mapping)   
temp_mapping= Graph_Transformer.invert(temp_mapping)

Graph_Visualizer.export_to_dot(temp_mapping, "inverted.dot")
Graph_Visualizer.generate_image_from_dot("inverted.dot")

# Teste de Remoção de Nós Folha
pruned_mapping = copy.deepcopy(mapping)
pruned_mapping = Graph_Transformer.prune(pruned_mapping, "leaf" , False)
Graph_Visualizer.export_to_dot(pruned_mapping, "pruned.dot")
Graph_Visualizer.generate_image_from_dot("pruned.dot")
