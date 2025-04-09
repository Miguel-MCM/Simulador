import Circuit
import Equation
import numpy as np

class NodalAnalyzer:
    def __init__(self, circuit:Circuit.Circuit):
        self.circuit = circuit
        self.solved_nodes = {circuit['GND']}

    def make_super_node(self, tension_source) -> Equation:
        eq: Equation = Equation.Equation()
        nodes = list([tension_source.n_plus, tension_source.n_minus])
        passed = set()
        while nodes:
            #print(', '.join([a.name for a in nodes]))
            n = nodes.pop()
            if n in passed:
                continue
            passed.add(n)
            for s in filter(lambda b: issubclass(type(b), Circuit.TensionSource), n.branches):
                if not s.n_plus in passed:
                    nodes.append(s.n_plus) 
                if not s.n_minus in passed:
                    nodes.append(s.n_minus)
            eq += n.get_currents_eq()
        return eq
    
    def filter_equal_eqs(self, eqs:list[Equation.Equation]):
        new = list()
        dicts = list()
        for eq in eqs:
            if not eq.dict in dicts:
                dicts.append(eq.dict)
                new.append(eq)
        return new

    def get_conductances_matrix(self) -> np.ndarray:
        nodes_eqs = self.circuit.get_nodal_eqs()
        aux_eqs = self.circuit.get_aux_eqs()

        #print("Nodes:")
        #[print(e) for e in nodes_eqs]
        #print("Aux:")
        #[print(e) for e in aux_eqs]        

        # Deal with tensios sources
        solved_nodes = {circuit["GND"]:0}
        for e in nodes_eqs.copy():
            for var in e.dict.copy():
                if type(var).__name__ in ("Node", "NoneType"):
                    continue
                elif type(var[0]).__name__ in ('CurrentDependentCurrentSource', 'TensionDependentCurrentSource'):
                    e += var[0].get_aux_eq()*e[var]
                elif type(var[0]).__name__ == 'IndependentTensionSource':
                    if e in nodes_eqs:
                        nodes_eqs.remove(e)
                    if var[0].n_minus.solved:
                        solved_nodes[var[0].n_plus] = var[0].n_minus.v + var[0].value
                    elif var[0].n_plus.solved:
                        solved_nodes[var[0].n_minus] = var[0].n_plus.v - var[0].value
                    else:
                        nodes_eqs.append(self.make_super_node(var[0]))
                elif type(var[0]).__name__ in ('CurrentDependentTensionSource' ,'TensionDependentTensionSource'):
                    if e in nodes_eqs:
                        nodes_eqs.remove(e)
                    if not (var[0].n_minus.solved or var[0].n_plus.solved):
                        nodes_eqs.append(self.make_super_node(var[0]))

        # Find alread souved equations
        for e in aux_eqs.copy():
            if len(e.variables) <= 2 and None in e.variables:
                for v in e.variables:
                    if v is not None:
                        solved_nodes[v] = -e[None]/e[v]
                aux_eqs.remove(e)

        # Substitute values for solved nodes
        for e in nodes_eqs:
            for n in solved_nodes:
                if n in e:
                    e[None] += e[n]*solved_nodes[n]
                    e[n] = 0
        
        
        print("Nodes:")
        [print(e) for e in self.filter_equal_eqs(nodes_eqs)]

        print("Aux:")
        [print(e) for e in self.filter_equal_eqs(aux_eqs)]



if __name__ == "__main__":
    circuit = Circuit.Circuit()
    gnd = Circuit.Node(circuit, gnd=True)
    v1 = Circuit.Node(circuit, name="V1")

    srcA = Circuit.IndependentTensionSource(2, gnd, v1, name="SA")
    
    r1 = Circuit.Resistor(4, v1, gnd, name="R1")

    v2 = Circuit.Node(circuit, name="V2")
    v3 = Circuit.Node(circuit, name="V3")
    r2 = Circuit.Resistor(4, v2, gnd, name="R2")
    r3 = Circuit.Resistor(4, v2, v3, name="R3")
    r4 = Circuit.Resistor(4, v3, gnd, name="R4")

    #srcB = Circuit.TensionDependentCurrentSource(2, gnd, v2, v1, gnd, name="SB")
    srcB = Circuit.IndependentTensionSource(1, v2, v3, name="SB")

    v4 = Circuit.Node(circuit, name="V4")
    srcC = Circuit.CurrentDependentTensionSource(2, v3, v4, r2, gnd, name="SC")

    nodal = NodalAnalyzer(circuit)
    print(nodal.get_conductances_matrix())