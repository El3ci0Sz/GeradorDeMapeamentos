import matplotlib.pyplot as plt
import networkx as nx
from src.utils.Mapping import Mapping
import os

class Graph_Visualizer:
    
    # @staticmethod
    # def export_to_dot(mapping: Mapping, filename="graph.dot"):
    #     """
    #     Exporta o grafo gerado para um arquivo DOT.

    #     Args:
    #         mapping (Mapping): Objeto contendo o mapeamento.
    #         filename (str): Nome do arquivo DOT.
    #     """
    #     G = nx.DiGraph()

    #     for node, pos in mapping.placement.items():
    #         if len(pos) == 3 and all(isinstance(coord, (int, float)) for coord in pos):
    #             pos_str = f"{pos[0]},{pos[1]},{pos[2]}"
    #             G.add_node(node, position=pos_str)
    #         else:
    #             print(f"Aviso: Posição inválida para o nó {node}: {pos}")

    #     for (src, dst), path in mapping.routing.items():
    #         G.add_edge(src, dst, path=str(path))

    #     nx.drawing.nx_agraph.write_dot(G, filename)
    
    @staticmethod
    def generate_image_from_dot(dot_file):
        """
        Gera uma imagem do grafo a partir de um arquivo DOT e salva no mesmo diretório.

        Args:
            dot_file (str): Caminho para o arquivo DOT.
        """
        directory = os.path.dirname(dot_file)
        output_file = os.path.join(directory, os.path.splitext(os.path.basename(dot_file))[0] + ".png")

        os.system(f"dot -Tpng {dot_file} -o {output_file}")

    @staticmethod
    def plot_cgra(mapping, cgra_dim, routing=True, output_file="cgra.png"):
        """
        Gera uma representação gráfica do CGRA com subplots para cada ciclo de II.

        Args:
            mapping (Mapping): Objeto contendo o mapeamento.
            cgra_dim (tuple): Dimensões do CGRA (linhas, colunas).
            routing (bool): Se True, desenha as conexões de roteamento.
            output_file (str): Nome do arquivo para salvar a imagem.
        """
        rows, cols = cgra_dim
        II = max(pos[2] for pos in mapping.placement.values()) + 1
        fig, axes = plt.subplots(nrows=1, ncols=II, figsize=(5 * II, 5))

        if II == 1:
            axes = [axes]

        for cycle in range(II):
            ax = axes[cycle]
            ax.set_xlim(-0.5, cols - 0.5)
            ax.set_ylim(-0.5, rows - 0.5)
            ax.set_xticks(range(cols))
            ax.set_yticks(range(rows))
            ax.grid(True, linestyle='--', linewidth=0.5)
            ax.set_aspect('equal')
            ax.invert_yaxis()

            for node, (x, y, z) in mapping.placement.items():
                if z == cycle:
                    ax.text(y, x, f"{node}\n({x},{y},{z})", ha='center', va='center', fontsize=8, color='blue')

            # if routing:
            #     for (src, dst), path in mapping.routing.items():
            #         if mapping.placement[src][2] == cycle and mapping.placement[dst][2] == cycle:
            #             src_pos = mapping.placement[src]
            #             dst_pos = mapping.placement[dst]

            #             ax.arrow(src_pos[1], src_pos[0],
            #                     dst_pos[1] - src_pos[1],
            #                     dst_pos[0] - src_pos[0],
            #                     head_width=0.2, head_length=0.2,
            #                     fc='red', ec='red', length_includes_head=True)

            ax.set_title(f"Cycle {cycle}")
            ax.set_xlabel("Coluna (y)")
            ax.set_ylabel("Linha (x)")

        plt.tight_layout()
        plt.savefig(output_file)
        print(f"Imagem salva em {output_file}")
        plt.close(fig)

    @staticmethod
    def export_to_dot(mapping: Mapping, filename="dfg_graph.dot"):
        """
        Exporta o DFG para um arquivo DOT, apartir de dfg_edges.

        Args:
            mapping (Mapping): Objeto contendo o DFG.
            filename (str): Nome do arquivo DOT.
        """
        G = nx.DiGraph()

        for node in mapping.dfg_edges.keys():
            G.add_node(node)

        for src, targets in mapping.dfg_edges.items():
            for target in targets:
                G.add_edge(src, target)

        nx.drawing.nx_agraph.write_dot(G, filename)
        print(f"DFG exportado para {filename}")
