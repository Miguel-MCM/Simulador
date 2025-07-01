import numpy as np
from Node import Node
from Branch import Resistor, IndependentCurrentSource, CurrentDependentCurrentSource, TensionDependentCurrentSource, \
                    IndependentTensionSource, CurrentDependentTensionSource ,TensionDependentTensionSource, TensionSource, Branch
from Equation import Equation

class Circuit:
    def __init__(self):
        self.nodes: list[Node] = []
        self.solved = False

    def get_nodes(self) -> list[Node]:
        return self.nodes
    
    def get_neighbours_with_branches(self, node:Node) -> list[tuple[Node, 'Branch']]:
        neighbours = []
        for b in node.branches:
            for n in b.nodes:
                if n != node and (n, b) not in neighbours:
                    neighbours.append((n, b))
        return neighbours

    def unsolve(self):
        self.solved = False
        for n in self.nodes:
            if not n.gnd:
                n.unsolve()

    
    def add_node(self, node:Node) -> None:
        self.nodes.append(node)
        if self.solved:
            self.unsolve()

    def __getitem__(self, name:str):
        for n in self.nodes:
            if n.name == name:
                return n
        return None

    def get_nodal_eqs(self) -> list[Equation]:
        eqs:list[Equation] = list()
        for n in filter(lambda n: not n.solved, self.nodes):
            eqs.append(n.get_currents_eq())

        for solved in filter(lambda n: n.solved, self.nodes):
            for eq in eqs:
                if solved in eq:
                    eq[None] += eq[solved]*solved.v
                    eq[solved] = 0
        return eqs
    
    def get_aux_eqs(self) -> list[Equation]:
        eqs:list[Equation] = list()
        for n in filter(lambda n: not n.solved, self.nodes):
            for eq in n.get_aux_eqs():
                eqs.append(eq)
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
        ans = []
        for eq in eqs[:]:
            if not (line:=eq.get_line(variables)) in args:
                args.append(line)
                ans.append(-eq[None])
            else:
                eqs.remove(eq)
        
        np_args = np.array(args)
        np_ans = np.array(ans)
        solution = np.linalg.solve(np_args, np_ans)

        answer = {}
        for v, s in zip(variables, solution):
            answer[v] = s

        for var in variables:
            if type(var) == Node:
                var.v = answer[var]
                var.solved = True
            elif issubclass(type(var[0]), TensionSource):
                var[0].i = answer[var]        

        self.solved = True

        return answer
