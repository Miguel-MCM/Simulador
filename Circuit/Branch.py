from __future__ import annotations
from typing import TYPE_CHECKING
from abc import ABC, abstractmethod
from Equation import Equation

if TYPE_CHECKING:
    from .Node import Node

class Branch(ABC):
    def __init__(self, nodes: list[Node], value:float, name:str=""):
        self.name = name
        self.nodes = nodes
        [ n.connect(self) for n in self.nodes ]
        self.loops = []
        self.value:float = value

    @property
    def i(self) -> float | None:
        pass

    @abstractmethod
    def get_current_eq(self, node: 'Node') -> Equation | None:
        pass

    @abstractmethod
    def get_aux_eq(self) -> Equation | None:
        pass

    def get_tension_eq(self, from_node: 'Node') -> Equation | None:
        return None
    
    def get_tension_aux_eq(self) -> Equation | None:
        return None

    def get_loop_voltage(self, from_node: 'Node') -> float:
        """Returns the voltage contribution of this branch when traversing from from_node"""
        if from_node not in self.nodes:
            return 0
        return 0

    def get_loop_resistance(self, from_node: 'Node') -> float:
        """Returns the resistance contribution of this branch when traversing from from_node"""
        if from_node not in self.nodes:
            return 0
        return 0

class Resistor(Branch):
    def __init__(self, resistance:float, node1: 'Node', node2: 'Node', name:str=""):
        self.r = resistance
        super().__init__([node1, node2], resistance , name=name)
    
    @property
    def y(self):
        return 1/self.r
    
    @property
    def i(self) -> float | None:
        if all([n.solved for n in self.nodes]):
            tensions = [n.v for n in self.nodes if n.v]
            return self.y * (max(tensions) - min(tensions))
        else:
            return None

    def get_current_eq(self, node : 'Node') -> Equation | None:
        if node == self.nodes[0]:
            return Equation(dict_eq={node: self.y, self.nodes[1]: -self.y})     
        elif node == self.nodes[1]:
            return Equation(dict_eq={node: self.y, self.nodes[0]: -self.y})
        else:
            return None
    
    def get_aux_eq(self) -> None:
        return None
    
    def get_loop_resistance(self, from_node: 'Node') -> float:
        if from_node not in self.nodes:
            return 0
        return self.r
    
    def get_tension_eq(self, from_node: 'Node') -> Equation | None:
        if from_node not in self.nodes:
            return None
        return Equation(dict_eq=dict([ (l, 1 if l.branches[l.nodes.index(from_node)] == self else -1) for l in self.loops ])) * self.r

class IndependentCurrentSource(Branch):
    def __init__(self, current:float, node1: 'Node', node2: 'Node', name:str=""):
        super().__init__([node1, node2], current, name=name)
    
    @property
    def i(self) -> float:
        return self.value

    def get_current_eq(self, node) ->  Equation | None:
        if node == self.nodes[0]:
            return Equation(dict_eq={None : self.i})
        elif node == self.nodes[1]:
            return Equation({None : -self.i})
        else:
            return None
        
    def get_aux_eq(self) -> None:
        return None


class CurrentDependentCurrentSource(Branch):
    def __init__(self, current_mulltiplier:float, node1: 'Node', node2: 'Node', branch_of_current: Branch, current_out_of: Node, name:str=""):
        super().__init__([node1, node2], current_mulltiplier, name=name)
        self.multiplier:float = current_mulltiplier
        self.branch_of_current:Branch = branch_of_current
        self.current_out_of:Node = current_out_of
    
    @property
    def i(self) -> float | None: 
        if (branch_i:=self.branch_of_current.i) is not None:
            return self.multiplier * branch_i
        else:
            return None
        
    def get_tension_eq(self, from_node: 'Node') -> Equation | None:
        if from_node not in self.nodes:
            return None
        return Equation(dict_eq = {(self, self.nodes[0]): -1 if from_node == self.nodes[0] else 1})
    
    def get_tension_aux_eq(self) -> Equation:
        return Equation({(self, self.nodes[0]): -1}) + Equation(dict([(l, 1 if l.branches[l.nodes.index(self.current_out_of)] == self.branch_of_current else -1) for l in self.branch_of_current.loops])) * self.multiplier
    
        
    def get_aux_eq(self) -> Equation | None:
        if (eq := self.branch_of_current.get_current_eq(self.current_out_of)):
            return (eq * self.multiplier) + Equation({(self, self.nodes[0]):-1})
        else:
            return None
    
    def get_current_eq(self, node) -> Equation | None:
        if node == self.nodes[0]:
            return Equation({(self, self.nodes[0]):1})
        elif node == self.nodes[1]:
            return Equation({(self, self.nodes[0]):-1})
        else:
            return None
    
class TensionDependentCurrentSource(Branch):
    def __init__(self, conductance:float, node1: Node, node2: Node, v_plus: Node, v_minus: Node, name:str=""):
        super().__init__([node1, node2], conductance, name=name)
        self.multiplier:float = conductance
        self.v_plus:'Node' = v_plus
        self.v_minus:'Node' = v_minus
    
    @property
    def i(self) -> float | None:
        if self.v_plus.solved and self.v_minus.solved:
            return self.multiplier*(self.v_plus.v - self.v_minus.v) # type: ignore
        else:
            return None
    
    def get_aux_eq(self) -> Equation:
        return (Equation({self.v_plus:1, self.v_minus:-1}) * self.multiplier) + Equation({(self, self.nodes[0]):-1})

    def get_current_eq(self, node) -> Equation | None:
        if node == self.nodes[0]:
            return Equation({(self, self.nodes[0]):1})
        elif node == self.nodes[1]:
            return Equation({(self, self.nodes[0]):-1})
        else:
            return None
        
    def get_tension_eq(self, from_node: 'Node') -> Equation | None:
        if from_node not in self.nodes:
            return None
        return Equation(dict_eq = {(self, self.nodes[0]): -1 if from_node == self.nodes[0] else 1})
    
    def get_tension_aux_eq(self) -> Equation:
        from collections import deque

        eq = Equation({(self, self.v_minus): -1})

        queue = deque()
        queue.append((self.v_minus, []))  # (current_node, path_so_far)
        visited = set()

        path = None

        while queue:
            current_node, path_so_far = queue.popleft()

            if current_node == self.v_plus:
                path = path_so_far
                break

            visited.add(current_node)

            for branch in current_node.branches:
                if branch.nodes[0] == current_node:
                    neighbor = branch.nodes[1]
                elif branch.nodes[1] == current_node:
                    neighbor = branch.nodes[0]
                else:
                    continue

                if neighbor not in visited:
                    queue.append((neighbor, path_so_far + [(branch, current_node)]))

        if path is None:
            raise Exception(f"Não há caminho entre {self.v_minus.name} e {self.v_plus.name}")

        for branch, from_node in path:
            tension_eq = branch.get_tension_eq(from_node)
            if tension_eq is None:
                raise Exception(f"O ramo {branch.name} não suporta get_tension_eq")
            eq += tension_eq * -self.multiplier

        return eq
    
class TensionSource(Branch):
    def __init__(self, value:float, n_minus:'Node', n_plus:'Node', name:str=""):
        super().__init__([n_minus, n_plus], value, name=name)
        self.n_plus = n_plus
        self.n_minus = n_minus

        if n_plus == n_minus:
            raise Exception(f"IndependentTensionSource: {self.name} in short circuit.")
        
        self._i = None

    def get_current_eq(self, node) -> Equation | None:
        if node == self.nodes[1]:
            return Equation({(self, self.nodes[0]):1})
        elif node == self.nodes[0]:
            return Equation({(self, self.nodes[0]):-1})
        else:
            return None
        
    def get_loop_voltage(self, from_node: 'Node') -> float:
        if from_node not in self.nodes:
            return 0
        # If traversing from n_minus to n_plus, voltage is positive
        if from_node == self.n_minus:
            return self.value
        # If traversing from n_plus to n_minus, voltage is negative
        return -self.value

    @property
    def i(self) -> float | None:
        return self._i

    @i.setter
    def i(self, value):
        self._i = value


class IndependentTensionSource(TensionSource):
    def __init__(self, value:float, n_minus:'Node', n_plus:'Node', name:str=""):
        super().__init__(value, n_minus, n_plus, name=name)
        
        if n_plus.solved and n_minus.solved and (n_plus.v - n_minus.v != value): # type:ignore
            raise Exception(f"Impossible circuit!\n{n_plus.name} and {n_minus.name} cant have a IndependentTensionSource of {self.value}.")

    def get_aux_eq(self) -> Equation:
        return Equation({ self.n_plus:1, self.n_minus:-1, None:-self.value })
    
    def get_tension_eq(self, from_node: 'Node') -> Equation | None:
        if from_node not in self.nodes:
            return None
        return Equation(dict_eq = {None: -self.value if from_node == self.n_minus else self.value})

class CurrentDependentTensionSource(TensionSource):
    def __init__(self, multiplier:float, n_minus:Node, n_plus:Node, branch_of_current: Branch, current_out_of: Node, name:str=""):
        super().__init__(multiplier, n_minus, n_plus, name=name)
        self.multiplier:float = multiplier
        self.branch_of_current:Branch = branch_of_current
        self.current_out_of:Node = current_out_of

        if n_plus.solved and n_minus.solved and (branch_of_current.i is not None) \
            and (n_plus.v - n_minus.v != (branch_of_current.i if branch_of_current.nodes[0] == current_out_of else -branch_of_current.i)): # type:ignore
            raise Exception(f"Impossible circuit!\n{n_plus.name} and {n_minus.name} cant have a CurrentDependentTensionSource of {self.multiplier}.")
        
    def get_aux_eq(self) -> Equation | None:
        if (eq := self.branch_of_current.get_current_eq(self.current_out_of)):
            return (eq * self.multiplier) + Equation({(self, self.nodes[0]):-1})
        return None
    
    def get_loop_voltage(self, from_node: 'Node') -> float:
        if from_node not in self.nodes:
            return 0
        # If traversing from n_minus to n_plus, voltage is positive
        if from_node == self.n_minus:
            return 1
        # If traversing from n_plus to n_minus, voltage is negative
        return -1
    
    def get_tension_eq(self, from_node: 'Node') -> Equation | None:
        if from_node not in self.nodes:
            return None
        return Equation(dict_eq = {(self, self.n_minus): -1 if from_node == self.n_minus else 1})

    def get_tension_aux_eq(self) -> Equation:
        return Equation({(self, self.n_minus): -1}) + Equation(dict([(l, 1 if l.branches[l.nodes.index(self.current_out_of)] == self.branch_of_current else -1) for l in self.branch_of_current.loops])) * self.multiplier

class TensionDependentTensionSource(TensionSource):
    def __init__(self, multiplier:float, n_minus:Node, n_plus:Node, dep_n_plus:Node, dep_n_minus:Node, name:str=""):
        super().__init__(multiplier, n_minus, n_plus, name=name)
        self.multiplier:float = multiplier
        self.dep_n_plus:Node = dep_n_plus
        self.dep_n_minus:Node = dep_n_minus

        if n_plus.solved and n_minus.solved and dep_n_plus.solved and dep_n_minus.solved and (n_plus.v - n_minus.v != multiplier*(dep_n_plus*dep_n_minus)): # type:ignore
            raise Exception(f"Impossible circuit!\n{n_plus.name} and {n_minus.name} cant have a TensionDependentTensionSource of {self.multiplier}.")
        
    def get_aux_eq(self) -> Equation:
        return Equation({ (self, self.n_plus): -1, self.dep_n_plus:self.multiplier, self.dep_n_minus:-self.multiplier })
    
    def get_loop_voltage(self, from_node: 'Node') -> float:
        if from_node not in self.nodes:
            return 0
        # If traversing from n_minus to n_plus, voltage is positive
        if from_node == self.n_minus:
            return 1
        # If traversing from n_plus to n_minus, voltage is negative
        return -1
    
    def get_tension_eq(self, from_node: 'Node') -> Equation | None:
        if from_node not in self.nodes:
            return None
        return Equation(dict_eq = {(self, self.n_minus): -1 if from_node == self.n_minus else 1})

    def get_tension_aux_eq(self) -> Equation:
        from collections import deque

        eq = Equation({(self, self.n_minus): -1})

        queue = deque()
        queue.append((self.dep_n_minus, []))  # (current_node, path_so_far)
        visited = set()

        path = None

        while queue:
            current_node, path_so_far = queue.popleft()

            if current_node == self.dep_n_plus:
                path = path_so_far
                break

            visited.add(current_node)

            for branch in current_node.branches:
                if branch.nodes[0] == current_node:
                    neighbor = branch.nodes[1]
                elif branch.nodes[1] == current_node:
                    neighbor = branch.nodes[0]
                else:
                    continue

                if neighbor not in visited:
                    queue.append((neighbor, path_so_far + [(branch, current_node)]))

        if path is None:
            raise Exception(f"Não há caminho entre {self.dep_n_minus.name} e {self.dep_n_plus.name}")

        for branch, from_node in path:
            tension_eq = branch.get_tension_eq(from_node)
            if tension_eq is None:
                raise Exception(f"O ramo {branch.name} não suporta get_tension_eq")
            eq += tension_eq * -self.multiplier

        return eq

