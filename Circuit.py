import numpy as np
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
    
    def solve(self) -> dict:
        eqs = [*self.get_nodal_eqs() , *self.get_aux_eqs()]
        variables = set()
        for eq in eqs:
            variables.update(eq.variables)
        if None in variables:
            variables.remove(None)

        args = []
        for eq in eqs[:]:
            if not (line:=eq.get_line(variables)) in args:
                args.append(line)
            else:
                eqs.remove(eq)
        
        np_args = np.array(args)
        np_ans = np.array([-eq[None] for eq in eqs ])
        solution = np.linalg.solve(np_args, np_ans)
        answer = {}
        for v, s in zip(variables, solution):
            answer[v] = s
        return answer

    
if __name__ == '__main__':
    circuit = Circuit()
    n1 = Node(circuit, gnd=True)
    n2 = Node(circuit, name="v2")
    n3 = Node(circuit, name='v3')
    n4 = Node(circuit, name='v4')
    src = IndependantTensionSource(1, n2, n1, name='s1')
    r1 = Resistor(1, n2, n1, name='r1')

    r2 = Resistor(1, n3, n1, name='r2')
    dep_src = TensionDependantTensionSource(2, n4, n3, n2, n1, name='s2')
    r3 = Resistor(1, n4, n1, name='r3')

    solution = circuit.solve()
    for n in solution:
        if type(n) == Node:
            print(f"{n.name} = {solution[n]}")
        else:
            print(f"i_{n[0].name} = {solution[n]}")




