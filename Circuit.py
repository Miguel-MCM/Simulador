from Node import Node
from Branch import Resistor, IndependentCurrentSource, CurrentDependantCurrentSource, TensionDependantCurrentSource, \
                    IndependantTensionSource, CurrentDependantTensionSource ,TensionDependantTensionSource
from Equation import Equation

class Circuit:
    def __init__(self):
        self.nodes: list[Node] = []
    
    def add_node(self, node:Node) -> None:
        self.nodes.append(node)

    def get_nodal_eqs(self) -> set[Equation]:
        eqs:set[Equation] = set()
        for n in filter(lambda n: not n.solved, self.nodes):
            eqs.add(n.get_currents_eq())

        for solved in filter(lambda n: n.solved, self.nodes):
            for eq in eqs:
                if solved in eq:
                    eq[None] += eq[solved]*solved.v
                    eq[solved] = 0
        return eqs
    
    def get_aux_eqs(self) -> set[Equation]:
        eqs:set[Equation] = set()
        for n in filter(lambda n: not n.solved, self.nodes):
            for eq in n.get_aux_eqs():
                eqs.add(eq)
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
    n4 = Node(name='v4')
    src = IndependantTensionSource(1, n2, n1, name='s1')
    r1 = Resistor(1, n2, n1, name='r1')

    r2 = Resistor(1, n3, n1, name='r2')
    dep_src = TensionDependantTensionSource(2, n4, n3, n2, n1, name='s2')
    r3 = Resistor(1, n4, n1, name='r3')

    circuit.add_node(n1)
    circuit.add_node(n2)
    circuit.add_node(n3)
    circuit.add_node(n4)
    
    for eq in circuit.get_nodal_eqs():
        print(eq)
    for eq in circuit.get_aux_eqs():
        print(eq)
    



