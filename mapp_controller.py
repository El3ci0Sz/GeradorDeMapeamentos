from src.cgra.mapping_generator_CGRA import Mapping_generator_CGRA
from src.qca.mapping_generator_QCA import Mapping_generator_QCA
from src.utils.Graph_Visualizer import Graph_Visualizer
from math import ceil
import argparse
import random
import os

class Mapp_Controler:
   #0 cgra, 1 qca
   @staticmethod
   def get_parameters():
      parser = argparse.ArgumentParser(description='Gerar mapeamentos de grafos.')
      parser.add_argument('--k', type=int, default=5, help='Número de grafos a gerar.')
      parser.add_argument('--graph_range', type=int, nargs=2, default=(2, 5), help='Intervalo de tamanhos de grafos.')
      parser.add_argument('--tam_arch', type=int, nargs='+', default=[4, 4, 8, 8], help='Tamanhos possíveis de arquitetura (ex: 4x4 8x8).')
      parser.add_argument('--alpha', type=float, default=0.8, help='Valor de alpha.')
      parser.add_argument('--alpha2', type=float, default=0.4, help='Valor de alpha2.')
      parser.add_argument('--bits', type=str, default='1000', help='Bits de interconexão (ex: 1100).')
      parser.add_argument('--tec', type=str, default='0', choices=['0', '1'], help='Tecnologia: 0 = CGRA, 1 = QCA.')
    
      args = parser.parse_args()
      
      tam_arch = [(args.tam_arch[i], args.tam_arch[i+1]) for i in range(0, len(args.tam_arch), 2)]
      
      Mapp_Controler.mapping(args.k, tuple(args.graph_range), tam_arch, args.alpha, args.alpha2, args.bits, args.tec)

   @staticmethod
   def mapping(k, graph_range, tam_arch,alpha, alpha2, bits, tecnology):
      if tecnology == "0":
         initial , final = graph_range
         num_graphs = 0
         
         while num_graphs < k:
            num_vertices = random.randint(initial, final)
            
            row , col = random.choice(tam_arch)
            II = ceil(num_vertices/(row * col))

            if row * col < num_vertices:
               print(f"[AVISO] Arquitetura {row}x{col} não suporta {num_vertices} vértices. Pulando.")
               continue
            mapping_generator = Mapping_generator_CGRA(num_vertices, II, alpha, alpha2, (row,col), bits)
                        
            try:
                  mapping = mapping_generator.mapp()
            except ValueError as e:
                  continue

            num_edges = sum(len([v for v in targets if v in mapping.dfg_vertices]) for targets in mapping.dfg_edges.values())

            directory = f"mappings/{row}x{col}/{num_vertices}/{num_edges}"
            os.makedirs(directory, exist_ok=True)
            path = f"{directory}/graph_{num_vertices}_{num_edges}.dot"
            
            Graph_Visualizer.export_to_dot(mapping, path)
            print(f"Mapa {num_graphs+1}/{k} salvo em {path}")
            Graph_Visualizer.generate_image_from_dot(path)
            num_graphs += 1
            
      if tecnology == "1":
         pass

if __name__ == "__main__":
   Mapp_Controler.get_parameters()






