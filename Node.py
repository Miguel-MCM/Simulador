from __future__ import annotations
from collections import defaultdict
from Branch import IndependantTensionSource, Branch
from Equation import Equation

class Node:
    def __init__(self, v:float=None, gnd:bool=False, name:str = ''):
        self.v = v
        self.branches : list[Branch] = []
        self.solved = False
        self.gnd = gnd
        self.name = name
        self.supernode = None

        if gnd:
            self.v = 0
            self.name = 'GND'
            self.solved = True
    
    def connect(self, branch: Branch):
        self.branches.append(branch)
    
    def get_currents_eq(self) -> Equation:
        eq = Equation()
        for branch in self.branches:
            condutances = branch.get_current_eq(self)
            if condutances is not None:
                for n in condutances:
                    eq[n] += condutances[n]
        return eq
    
    def get_aux_eqs(self) -> list[Equation]:
        return [b.get_aux_eq() for b in self.branches if b.get_aux_eq() is not None]
    

    