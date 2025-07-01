from Circuit import *
from Equation import Equation
import numpy as np

class NodalAnalyzer:
    def __init__(self, circuit:Circuit):
        self.circuit = circuit
        self.solved_nodes:set[Node] = {circuit['GND']} # type:ignore
        self.map_solved_nodes(circuit['GND']) # type: ignore

    def map_solved_nodes(self, node:Node):
        curr = node
        if not curr:
            return
        for b in curr.branches:
            if type(b).__name__ == 'IndependentTensionSource':
                other = b.nodes[0] if b.nodes[0] != curr else b.nodes[1]
                self.solved_nodes.add(other)  # type: ignore
                if not other or other.solved:
                    continue
                other.solved = True
                other.v = (curr.v + b.value) if other == b.nodes[1] else curr.v - b.value # type:ignore
                self.map_solved_nodes(other)

    def make_super_node(self, tension_source) -> Equation:
        eq: Equation = Equation()
        nodes = [tension_source.n_plus, tension_source.n_minus]
        passed = set()
        while nodes:
            #print(', '.join([a.name for a in nodes]))
            n = nodes.pop()
            if n in passed:
                continue
            passed.add(n)
            for s in filter(lambda b: issubclass(type(b), TensionSource), n.branches):
                if not s.n_plus in passed:
                    nodes.append(s.n_plus) 
                if not s.n_minus in passed:
                    nodes.append(s.n_minus)
            eq += n.get_currents_eq()
        return eq
    
    def filter_equal_eqs(self, eqs:list[Equation]) -> list[Equation]:
        new = list()
        dicts = list()
        for eq in eqs:
            if not eq.dict in dicts:
                dicts.append(eq.dict)
                new.append(eq)
        return new

    def get_conductances_matrix(self) -> tuple[list[Equation], list[Equation]]:
        nodes_eqs = self.circuit.get_nodal_eqs()
        aux_eqs = self.circuit.get_aux_eqs()

        for e in nodes_eqs.copy():
            for var in e.dict.copy():
                if type(var).__name__ in ("Node", "NoneType"):
                    continue
                elif type(var[0]).__name__ == 'IndependentTensionSource':
                    if e in nodes_eqs:
                        nodes_eqs.remove(e)
                    if not (var[0].n_plus.solved or var[0].n_minus.solved):
                        nodes_eqs.append(self.make_super_node(var[0]))
                elif type(var[0]).__name__ in ('CurrentDependentTensionSource' ,'TensionDependentTensionSource'):
                    if e in nodes_eqs:
                        nodes_eqs.remove(e)
                    if not (var[0].n_minus.solved or var[0].n_plus.solved):
                        nodes_eqs.append(self.make_super_node(var[0]))
                    nodes_eqs.append(Equation( { var[0].n_plus:1, var[0].n_minus:-1, var: -1 } ))

        for e in nodes_eqs:
            e[self.circuit["GND"]] = 0
            if not set(e.variables):
                nodes_eqs.remove(e)
        
        for n in self.solved_nodes:
            if n.name == 'GND':
                continue
            nodes_eqs.append(Equation({n:1, None:-n.v})) # type:ignore

        return self.filter_equal_eqs(nodes_eqs), self.filter_equal_eqs(aux_eqs)
