from __future__ import annotations
from abc import ABC, abstractmethod
from Equation import Equation

class Node:
    pass

class Branch(ABC):
    def __init__(self, nodes: list['Node'], name:str=""):
        self.name = name
        self.nodes = nodes
        [ n.connect(self) for n in self.nodes ]

    @property
    def i(self) -> float:
        pass

    @abstractmethod
    def get_current_eq(self, node: 'Node') -> Equation:
        pass

    @abstractmethod
    def get_aux_eq(self) -> Equation:
        pass

class Resistor(Branch):
    def __init__(self, resistance:float, node1: 'Node', node2: 'Node', name:str=""):
        self.r = resistance
        super().__init__([node1, node2], name=name)
    
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
    
    def get_aux_eq(self):
        return None
        
class IndependentCurrentSource(Branch):
    def __init__(self, current:float, node1: 'Node', node2: 'Node', name:str=""):
        self.value = current
        super().__init__([node1, node2], name=name)
    
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
        
    def get_aux_eq(self):
        return None


class CurrentDependentCurrentSource(Branch):
    def __init__(self, current_mulltiplier:float, node1: 'Node', node2: 'Node', branch_of_current: Branch, current_out_of: Node, name:str=""):
        super().__init__([node1, node2], name=name)
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
        return (self.branch_of_current.get_current_eq(self.current_out_of) * self.multiplier) + Equation({(self, self.nodes[0]):-1})
    
    def get_current_eq(self, node) -> Equation:
        if node == self.nodes[0]:
            return Equation({(self, self.nodes[0]):1})
        elif node == self.nodes[1]:
            return Equation({(self, self.nodes[0]):-1})
        else:
            return None
    
class TensionDependentCurrentSource(Branch):
    def __init__(self, conductance:float, node1: 'Node', node2: 'Node', v_plus: 'Node', v_minus: 'Node', name:str=""):
        super().__init__([node1, node2], name=name)
        self.multiplier:float = conductance
        self.v_plus:'Node' = v_plus
        self.v_minus:'Node' = v_minus
    
    @property
    def i(self) -> float:
        if self.v_plus.solved and self.v_minus.solved:
            return self.multiplier*(self.v_plus.v - self.v_minus.v)
        else:
            return None
    
    def get_aux_eq(self) -> Equation:
        return (Equation({self.v_plus:1, self.v_minus:-1}) * self.multiplier) + Equation({(self, self.nodes[0]):-1})

    def get_current_eq(self, node) -> Equation:
        if node == self.nodes[0]:
            return Equation({(self, self.nodes[0]):1})
        elif node == self.nodes[1]:
            return Equation({(self, self.nodes[0]):-1})
        else:
            return None

class TensionSource(Branch):
    def __init__(self, value:float, n_minus:'Node', n_plus:'Node', name:str=""):
        super().__init__([n_minus, n_plus], name=name)
        self.value:float = value
        self.n_plus = n_plus
        self.n_minus = n_minus

        if n_plus == n_minus:
            raise Exception(f"IndependentTensionSource: {self.name} in short circuit.")

    def get_current_eq(self, node):
        if node == self.nodes[1]:
            return Equation({(self, self.nodes[0]):1})
        elif node == self.nodes[0]:
            return Equation({(self, self.nodes[0]):-1})
        else:
            return None


class IndependentTensionSource(TensionSource):
    def __init__(self, value:float, n_minus:'Node', n_plus:'Node', name:str=""):
        super().__init__(value, n_minus, n_plus, name=name)
        
        if n_plus.solved and n_minus.solved and (n_plus.v - n_minus.v != value):
            raise Exception(f"Impossible circuit!\n{n_plus.name} and {n_minus.name} cant have a IndependentTensionSource of {self.value}.")

    def get_aux_eq(self) -> Equation:
        return Equation({ self.n_plus:1, self.n_minus:-1, None:-self.value })
    
class CurrentDependentTensionSource(TensionSource):
    def __init__(self, multiplier:float, n_minus:Node, n_plus:Node, branch_of_current: Branch, current_out_of: Node, name:str=""):
        super().__init__(multiplier, n_minus, n_plus, name=name)
        self.multiplier:float = multiplier
        self.branch_of_current:Branch = branch_of_current
        self.current_out_of:Node = current_out_of

        if n_plus.solved and n_minus.solved and (branch_of_current.i is not None) and (n_plus.v - n_minus.v != (branch_of_current.i if branch_of_current.nodes[0] == current_out_of else -branch_of_current.i)):
            raise Exception(f"Impossible circuit!\n{n_plus.name} and {n_minus.name} cant have a CurrentDependentTensionSource of {self.multiplier}.")
        
    def get_aux_eq(self) -> Equation:
        return (self.branch_of_current.get_current_eq(self.current_out_of) * -self.multiplier) + Equation({ self.n_plus:1, self.n_minus:-1})

class TensionDependentTensionSource(TensionSource):
    def __init__(self, multiplier:float, n_minus:Node, n_plus:Node, dep_n_plus:Node, dep_n_minus:Node, name:str=""):
        super().__init__(multiplier, n_minus, n_plus, name=name)
        self.multiplier:float = multiplier
        self.dep_n_plus:Node = dep_n_plus
        self.dep_n_minus:Node = dep_n_minus

        if n_plus.solved and n_minus.solved and dep_n_plus.solved and dep_n_minus.solved and (n_plus.v - n_minus.v != multiplier*(dep_n_plus*dep_n_minus)):
            raise Exception(f"Impossible circuit!\n{n_plus.name} and {n_minus.name} cant have a TensionDependentTensionSource of {self.multiplier}.")
        
    def get_aux_eq(self) -> Equation:
        return Equation({ self.n_plus:1, self.n_minus:-1, self.dep_n_plus:-self.multiplier, self.dep_n_minus:self.multiplier })