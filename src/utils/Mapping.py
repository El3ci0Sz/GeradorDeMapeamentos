class Mapping:
  def __init__(self,vertices):
    self.routing = []
    self.placement: dict = {}
    self.dfg_edges: dict = {}
    self.dfg_vertices = vertices
