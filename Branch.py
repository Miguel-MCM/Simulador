from abc import ABC, abstractmethod
from Equation import Equation

class Node:
    pass

class Branch(ABC):
    def __init__(self, nodes: list['Node']):
        self.nodes = nodes
        [ n.connect(self) for n in self.nodes ]

    @property
    def i(self) -> float:
        pass

    @abstractmethod
    def get_current_eq(self, node: 'Node') -> Equation:
        pass

class Resistor(Branch):
    def __init__(self, resistance:float, node1: 'Node', node2: 'Node'):
        self.r = resistance
        super().__init__([node1, node2])
    
    @property
    def y(self):
        return 1/self.r
    
    @property
    def i(self) -> float:
        if all([n.solved for n in self.nodes]):
            return self.y * (max(self.nodes)-min(self.nodes))
        else:
            return None

    def get_current_eq(self, node : 'Node') -> Equation:
        if node == self.nodes[0]:
            return Equation(dict_eq={node: self.y, self.nodes[1]: -self.y})     
        elif node == self.nodes[1]:
            return Equation(dict_eq={node: self.y, self.nodes[0]: -self.y})
        else:
            return None
        
class IndependentCurrentSource(Branch):
    def __init__(self, current:float, node1: 'Node', node2: 'Node'):
        self.value = current
        super().__init__([node1, node2])
    
    @property
    def i(self) -> float:
        return self.value

    def get_current_eq(self, node) ->  Equation:
        if node == self.nodes[0]:
            return Equation(dict_eq={None : self.i})
        elif node == self.nodes[1]:
            return Equation({None : -self.i})
        else:
            return None


class CurrentDependantCurrentSource(Branch):
    def __init__(self, current_mulltiplier:float, node1: 'Node', node2: 'Node', branch_of_current: Branch, current_out_of: Node):
        super().__init__([node1, node2])
        self.multiplier:float = current_mulltiplier
        self.branch_of_current:Branch = branch_of_current
        self.current_out_of:Node = current_out_of
    
    @property
    def i(self) -> float:
        if (branch_i:=self.branch_of_current.i) is not None:
            return self.multiplier * branch_i
        else:
            return None
    
        
    def get_aux_eq(self) -> Equation:
        return self.branch_of_current.get_current_eq(self.current_out_of)
    
    def get_current_eq(self, node) -> Equation:
        eq = self.get_aux_eq()
        multiplier = -self.multiplier if node == self.nodes[1] else self.multiplier
        eq *= multiplier
        if node in self.nodes:
            return eq
        else:
            return None
    
class TensionDependantCurrentSource(Branch):
    def __init__(self, conductance:float, node1: 'Node', node2: 'Node', v_plus: 'Node', v_minus: 'Node'):
        super().__init__([node1, node2])
        self.multiplier:float = conductance
        self.v_plus:'Node' = v_plus
        self.v_minus:'Node' = v_minus
    
    @property
    def i(self) -> float:
        if self.v_plus.solved and self.v_minus.solved:
            return self.multiplier*(self.v_plus - self.v_minus)
        else:
            return None
    
    def get_aux_eq(self) -> Equation:
        return Equation({self.v_plus:1, self.v_minus:-1})

    def get_current_eq(self, node) -> Equation:
        eq = self.get_aux_eq()
        multiplier = -self.multiplier if node == self.nodes[1] else self.multiplier
        eq *= multiplier
        if node in self.nodes:
            return eq
        else:
            return None
        
class SuperNode:
    def __init__(self, tension_src:Branch, n_plus:Node, n_minus:Node):
        self.n_plus:Node = n_plus
        self.n_minus:Node = n_minus
        self.tension_src:Branch = tension_src
        self.state = 0

        n_plus.supernode = self
        n_minus.supernode = self
    
    def get_current_eq(self) -> Equation:
        if self.state == 0:
            self.state = 1
            return self.n_plus.get_currents_eq(True) + self.n_minus.get_currents_eq(True)
        if self.state == 1:
            self.state = 2
            return self.tension_src.get_aux_eq()
class IndependantTensionSource(Branch):
    def __init__(self, value:float, n_plus:'Node', n_minus:'Node'):
        super().__init__([n_plus, n_minus])
        self.value:float = value
        self.n_plus = n_plus
        self.n_minus = n_minus
        
        if n_plus.solved and n_minus.solved and (n_plus.v - n_minus.v != value):
            raise Exception(f"Impossible circuit!\n{n_plus.name} and {n_minus.name} cant have a IndependantTensionSource of {self.value}.")
        
        if n_plus.solved:
            n_minus.v = n_plus.v-value
            n_minus.solved = True
        elif n_minus.solved:
            n_plus.v = n_minus.v+value
            n_plus.solved = True
        else:
            SuperNode(self, n_plus, n_minus)
    
    def get_current_eq(self, node):
        return None

    def get_aux_eq(self) -> Equation:
        return Equation({ self.n_plus:1, self.n_minus:-1, None:-self.value })        
    