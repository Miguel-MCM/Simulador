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
    
    def get_currents_eq(self, ignore_supenode:bool=False) -> Equation:
        if self.supernode is not None and not ignore_supenode:
            return self.supernode.get_current_eq()
        eq = Equation()
        for branch in self.branches:
            condutances = branch.get_current_eq(self)
            if condutances is not None:
                for n in condutances:
                    eq[n] += condutances[n]
        return eq
    

    