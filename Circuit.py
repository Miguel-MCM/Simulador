from Node import Node
from Branch import Resistor, IndependentCurrentSource, CurrentDependantCurrentSource, TensionDependantCurrentSource, IndependantTensionSource
from Equation import Equation

class Circuit:
    def __init__(self):
        self.nodes: list[Node] = []
    
    def add_node(self, node:Node) -> None:
        self.nodes.append(node)

    def get_eq_system(self) -> list[Equation]:
        eqs: list[Equation] = [ n.get_currents_eq() for n in filter(lambda n: not n.solved, self.nodes) ]
        for solved in filter(lambda n: n.solved, self.nodes):
            for eq in eqs:
                if solved in eq:
                    eq[None] += eq[solved]*solved.v
                    eq[solved] = 0
        return eqs
        

    
if __name__ == '__main__':
    circuit = Circuit()
    n1 = Node(gnd=True)
    n2 = Node(name="v2")
    n3 = Node(name='v3')
    src = IndependantTensionSource(2, n3, n2)
    r1 = Resistor(1, n1, n2)
    r2 = Resistor(1, n3, n1)

    circuit.add_node(n1)
    circuit.add_node(n2)
    circuit.add_node(n3)
    
    for eq in circuit.get_eq_system():
        print(eq)
    



