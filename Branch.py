from abc import ABC, abstractmethod
from Equation import Equation

class Node:
    pass

class Branch(ABC):
    def __init__(self, nodes: list['Node']):
        self.nodes = nodes
        [ n.connect(self) for n in self.nodes ]

    @property
    @abstractmethod
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
    
    def get_current_eq(self, node) -> Equation:
        eq = self.branch_of_current.get_current_eq(self.current_out_of)
        multiplier = -self.multiplier if node == self.nodes[1] else self.multiplier
        eq *= multiplier
        if node in self.nodes:
            return eq
        else:
            return None
        
    def get_aux_eq(self) -> Equation:
        return self.branch_of_current.get_current_eq(self.current_out_of)