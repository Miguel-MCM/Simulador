import Circuit

class Loop:
    def __init__(self, name:str, path:tuple[list[Circuit.Node], list[Circuit.Branch]]):
        self.nodes = path[0]
        self.branches = path[1]
        self.name = name
    
    def __str__(self):
        string:str = f"{self.name} : "
        for n, b in zip(self.nodes, self.branches):
            string += f"{n.name}-->{b.name}-->"
        return string + self.nodes[0].name
    
    def get_tension_eqs(self):
        pass