import matplotlib.pyplot as plt
import networkx as nx

class Graph_Visualizer:
    
    @staticmethod
    def export_to_dot(mapping, filename="graph.dot"):
        """
        Exporta o grafo gerado para um arquivo DOT.

        Args:
            mapping (Mapping): Objeto contendo o mapeamento.
            filename (str): Nome do arquivo DOT.
        """
        G = nx.DiGraph()

        # Adiciona os nós e suas posições
        for node, pos in mapping.placement.items():
            G.add_node(node, pos=f"{pos}")

        # Adiciona as arestas
        for src, neighbors in mapping.dfg_edges.items():
            for dst in neighbors:
                G.add_edge(src, dst)

        nx.drawing.nx_agraph.write_dot(G, filename)
        print(f"Grafo exportado para {filename}")

    @staticmethod
    def generate_image_from_dot(dot_file, output_file="graph.png"):
        """
        Gera uma imagem do grafo a partir de um arquivo DOT.

        Args:
            dot_file (str): Caminho para o arquivo DOT.
            output_file (str): Nome do arquivo de saída da imagem.
        """
        import os
        os.system(f"dot -Tpng {dot_file} -o {output_file}")
        print(f"Imagem gerada: {output_file}")

    @staticmethod
    def plot_cgra(mapping, cgra_dim, routing=True, output_file="cgra.png"):
        """
        Gera uma representação gráfica do CGRA.

        Args:
            mapping (Mapping): Objeto contendo o mapeamento.
            cgra_dim (tuple): Dimensões do CGRA (linhas, colunas).
            routing (bool): Se True, desenha as conexões de roteamento.
            output_file (str): Nome do arquivo para salvar a imagem.
        """
        rows, cols = cgra_dim
        fig, ax = plt.subplots(figsize=(cols, rows))

        # Configurações da grade
        ax.set_xlim(-0.5, cols - 0.5)
        ax.set_ylim(-0.5, rows - 0.5)
        ax.set_xticks(range(cols))
        ax.set_yticks(range(rows))
        ax.grid(True, linestyle='--', linewidth=0.5)
        ax.set_aspect('equal')
        ax.invert_yaxis()

        # Adiciona os nós do placement
        for node, (x, y, z) in mapping.placement.items():
            ax.text(y, x, f"{node}\n({x},{y},{z})", ha='center', va='center', fontsize=8, color='blue')

        # Adiciona conexões do roteamento, se solicitado
        if routing:
            for src, dst in mapping.routing:
                src_pos = mapping.placement[src]
                dst_pos = mapping.placement[dst]

                # Conexão (x, y)
                ax.arrow(src_pos[1], src_pos[0], dst_pos[1] - src_pos[1], dst_pos[0] - src_pos[0],
                         head_width=0.2, head_length=0.2, fc='red', ec='red', length_includes_head=True)

        # Títulos e rótulos
        title = "CGRA: Placement e Roteamento" if routing else "CGRA: Placement"
        ax.set_title(title)
        ax.set_xlabel("Coluna (y)")
        ax.set_ylabel("Linha (x)")

        # Salva a figura
        plt.savefig(output_file)
        print(f"Imagem salva em {output_file}")
        plt.close(fig)
