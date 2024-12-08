Objetivo: Criar gerador de mapementos.

1. input(|DFG|, Grafo(Arestas), II, alpha(limiar de conexões durante a busca), dimensões cgra)
    Output: (DFG), dimensoes CGRA, Arestas(CGRA), II, alpha, arch_name

2. Limpar grafos isomorficos
3. Aumento de dados:
    Flip(eixo =  Horizontal ou Vertical)
    Shift(atd shifts por eixo(x,y))
    Rotate(degrees = 90,180,270)
    Invert()
    prune(allow_disconnected : bool)