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

    def set_name(self, name:str):
        self.name = name

    def reverse(self):
        self.nodes = [self.nodes[0], *self.nodes[:0:-1]]
        self.branches = self.branches[::-1]