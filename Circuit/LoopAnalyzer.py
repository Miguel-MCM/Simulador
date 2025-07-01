import Circuit
from Loop import Loop
import numpy as np
from Equation import Equation

class LoopAnalyzer:
    def __init__(self, circuit: Circuit.Circuit):
        self.circuit: Circuit.Circuit = circuit

        self.visited = set()
        self.loops:list[Loop] = []
        self.necessary_loops:set[Loop] = set()

        self.super_loops:list[set[Loop]] = []

    def addLoop(self, loop: Loop):
        if any([set(loop.nodes) == set(l.nodes) and set(loop.branches) == set(l.branches) for l in self.loops]):
            return
        [ b.loops.append(loop) for b in loop.branches ]
        self.loops.append(loop)

    def _dfs(self, node, path, branches):
        if node in path:
            loop_start_index = path.index(node)
            self.addLoop(Loop(f"Loop {len(self.loops) + 1}", (path[loop_start_index:], branches[loop_start_index:])))
            return
        

        self.visited.add(node)
        path.append(node)

        for neighbor, branch in self.circuit.get_neighbours_with_branches(node):
            if branch == branches[-1] if branches else None:
                continue
            self._dfs(neighbor, path[:], branches[:] + [branch])

    def remove_loop(self, loop: Loop):
        """
        Removes a loop from the list of loops and updates the branches accordingly.
        Args:
            loop (Loop): The loop to remove.
        """
        if loop in self.loops:
            self.loops.remove(loop)
            for branch in loop.branches:
                branch.loops.remove(loop)

    def find_loops(self) -> list[Loop]:
        for node in self.circuit.get_nodes():
            if node not in self.visited:
                self._dfs(node, [], [])

        self.loops.sort(key=lambda l: len(l.branches))
        
        seen_nodes = set()
        seen_branches = set()
        for loop in self.loops[:]:
            if set(loop.nodes).issubset(seen_nodes) and set(loop.branches).issubset(seen_branches):
                self.remove_loop(loop)
            else:
                seen_nodes.update(set(loop.nodes))
                seen_branches.update(set(loop.branches))

        self.n = len(self.loops)

        return self.loops
    
    def super_loop_eq(self, current_source:'Branch') -> Equation:
        """
        Creates an equation for a super loop, which is a loop that contains multiple loops
        Args:
            loops (list[Loop]): List of loops to create the super loop equation
        Returns:
            Equation: The equation for the super loop
        """
        if type(current_source).__name__ == "IndependentCurrentSource":
            eq = Equation({None: -current_source.value})
        else:
            eq = current_source.get_tension_eq(current_source.nodes[0])

        for loop in current_source.loops:
            # Check direction: node[0] → node[1] is positive
            node_index = loop.nodes.index(current_source.nodes[0]) if current_source.nodes[0] in loop.nodes else -1
            branch_index = loop.branches.index(current_source) if current_source in loop.branches else -1

            if node_index == branch_index:
                coef = 1
            else:
                coef = -1

            eq += Equation({loop: coef})

        return eq

    
    def get_resistance_matrix(self) -> tuple[np.ndarray, np.ndarray]:
        """
        Returns the resistance matrix and Tension vector for mesh analysis
        Returns:
            tuple[np.ndarray, np.ndarray]: (R, V) where R is the resistance matrix and V is the Tension vector
        """
        if not self.loops:
            self.find_loops()

        equations = []
        aux_eqs = []
        solved_loops = {}
        super_loops_eqs = []
        loops_in_super_loops = []
        loop_to_eq = {}
        
        # Fill diagonal elements with sum of resistances in each loop
        for i in range(self.n):
            loop = self.loops[i]
            current_eq = Equation()
            if loop in loops_in_super_loops:
                continue
            #equations.append(Equation(dict_eq={loop : 0}))
            for node, branch in zip(loop.nodes, loop.branches):
                if type(branch).__name__ == "Resistor":
                    current_eq += branch.get_tension_eq(node)
                elif type(branch).__name__ == "IndependentTensionSource":
                    current_eq += branch.get_tension_eq(node)
                elif type(branch).__name__ in ('CurrentDependentTensionSource' ,'TensionDependentTensionSource'):
                    current_eq += branch.get_tension_eq(node)
                    aux_eqs.append(branch.get_tension_aux_eq())
                elif type(branch).__name__ == "IndependentCurrentSource":
                    if len(branch.loops) == 1:
                        solved_loops[loop] = branch.value if node == branch.nodes[0] else -branch.value
                        current_eq = Equation({loop: 1, None: -branch.value if node == branch.nodes[0] else branch.value})
                        break
                    else:
                        if branch.loops not in self.super_loops:
                            new = True
                            for l in branch.loops:
                                if l in loops_in_super_loops:
                                    new = False
                                    # extend super loop with branch loops
                                    index = [ lp for lp, sl in enumerate(self.super_loops) if l in sl ]
                                    for i in index:
                                        self.super_loops[i].update(branch.loops)
                                    break
                            if new:
                                self.super_loops.append(set(branch.loops))
                            loops_in_super_loops.extend(branch.loops)
                        aux_eqs.append(self.super_loop_eq(branch))
                elif type(branch).__name__ in ('CurrentDependentCurrentSource', 'TensionDependentCurrentSource'):
                    if len(branch.loops) == 1:
                        solved_loops[loop] = branch.value if node == branch.nodes[0] else -branch.value
                        current_eq = Equation({loop: 1}) + branch.get_tension_eq(node)
                        aux_eqs.append(branch.get_tension_aux_eq())
                        break
                    else:
                        if branch.loops not in self.super_loops:
                            new = True
                            for l in branch.loops:
                                if l in loops_in_super_loops:
                                    new = False
                                    # extend super loop with branch loops
                                    index = [ lp for lp, sl in enumerate(self.super_loops) if l in sl ]
                                    for i in index:
                                        self.super_loops[i].update(branch.loops)
                                    break
                            if new:
                                aux_eqs.append(branch.get_tension_aux_eq())
                                self.super_loops.append(set(branch.loops))
                            loops_in_super_loops.extend(branch.loops)
                        aux_eqs.append(self.super_loop_eq(branch))

            if current_eq.variables:
                loop_to_eq[loop] = current_eq
                
        for superloop_group in self.super_loops:
            eq = Equation()

            for loop in superloop_group:
                # Build equation if not yet built (can happen if skipped above)
                if loop not in loop_to_eq:
                    temp_eq = Equation({loop: 0})
                    for node, branch in zip(loop.nodes, loop.branches):
                        branch_type = type(branch).__name__
                        if branch_type == "Resistor":
                            temp_eq += branch.get_tension_eq(node)
                        elif branch_type == "IndependentTensionSource":
                            temp_eq += branch.get_tension_eq(node)
                        elif branch_type in ('CurrentDependentTensionSource', 'TensionDependentTensionSource'):
                            temp_eq += branch.get_tension_eq(node)
                            aux_eqs.append(branch.get_tension_aux_eq())

                    loop_to_eq[loop] = temp_eq

                eq += loop_to_eq[loop]
            equations.append(eq)
        
        # Add non-superloop equations
        for loop, eq in loop_to_eq.items():
            if loop not in loops_in_super_loops:
                equations.append(eq)

        for i, eq1 in enumerate(equations[:]):
            for j, eq2 in enumerate(equations[:]):
                if i != j:
                    if eq1.equal(eq2):
                        equations.remove(eq2)
                        break

        return equations, aux_eqs
