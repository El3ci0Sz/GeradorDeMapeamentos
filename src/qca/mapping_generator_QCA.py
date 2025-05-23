class Mapping_generator_QCA:
    """
    Classe responsável por gerar e verificar mapeamentos aleatórios de um DFG para um CGRA.
    """

    def __init__(self, dfg_tam,bits):
      """
        Inicializa os parâmetros necessários para o mapeamento.

        Args:
            dfg_tam (int): Número de nós no DFG.
            II (int): Intervalo de inicialização (Initiation Interval) do CGRA.
            alpha (float): Probabilidade de criar conexões adicionais.
            alpha2 (float): Probabilidade de remover conexões existentes.
            cgra (CGRA): Objeto representando a arquitetura do CGRA.
        """
      self.dfg_tam = dfg_tam
      self.bits = bits

    def mapp(self, max_attempts=200000):
      """
        Realiza o mapeamento completo (placement + routing) do DFG no CGRA,
        garantindo que o mapeamento seja balanceado.

        Args:
            max_attempts (int): Número máximo de tentativas para encontrar um mapeamento balanceado.

        Returns:
            Mapping: Objeto contendo o mapeamento gerado.

        Raises:
            ValueError: Se o número máximo de tentativas for atingido sem encontrar um mapeamento balanceado.
        """
      for attempt in range(max_attempts):

         #if Graph_Processing().is_valid():
            return 
      raise ValueError(f"Não foi possível encontrar um mapeamento balanceado após {max_attempts} tentativas.")
    

  

           
    
