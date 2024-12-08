from cgra.cgra import CGRA
from utils.mapping_generator import Mapping_generator

def main():
    cgra_dim = (4, 4)
    arch_name = "Teste5"
    cgra = CGRA(cgra_dim, arch_name)

    graph_edges = [
        (0, 1),
        (1, 2),
        (2, 3)
    ]

    alpha = 2

    mapping_generator = Mapping_generator(len(graph_edges), graph_edges, II=1, alpha=alpha, cgra=cgra.__class__, cgra_dim=cgra_dim, arch_name=arch_name)

    mapped_nodes = mapping_generator.mapping(graph_edges, cgra, alpha)
    print(mapped_nodes)


if __name__ == '__main__':
    main()