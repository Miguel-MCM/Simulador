import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, Any, Optional, Set
from Circuit import Circuit as CircuitClass, Node, Resistor, IndependentCurrentSource, IndependentTensionSource, NodalAnalyzer

class CircuitAnalyzer:
    """Responsável pela análise e resolução do circuito"""
    
    def __init__(self) -> None:
        pass
    
    def compile_circuit(self, nodes: Dict[str, Dict[str, Any]], components: Dict[str, Dict[str, Any]]) -> CircuitClass:
        """Compila o circuito visual em objetos do circuito"""
        circuit: CircuitClass = CircuitClass()
        node_objects: Dict[str, Node] = {}
        for node_name in self.get_nodes_from_wires(nodes):
            node_objects[node_name] = Node(circuit, gnd=node_name == 'GND', name=node_name)
        for component_name, component_data in components.items():
            if component_data['type'] == 'resistor':
                node1 = node_objects[nodes[component_data['connections'][0]['wire']]['node']]
                node2 = node_objects[nodes[component_data['connections'][1]['wire']]['node']]
                resistor: Resistor = Resistor(component_data['value'], node1, node2, name=component_name)
            elif component_data['type'] == 'voltage_source':
                node1 = node_objects[nodes[component_data['connections'][0]['wire']]['node']]
                node2 = node_objects[nodes[component_data['connections'][1]['wire']]['node']]
                voltage_source: IndependentTensionSource = IndependentTensionSource(component_data['value'], node2, node1, name=component_name)
            elif component_data['type'] == 'current_source':
                node1 = node_objects[nodes[component_data['connections'][0]['wire']]['node']]
                node2 = node_objects[nodes[component_data['connections'][1]['wire']]['node']]
                current_source: IndependentCurrentSource = IndependentCurrentSource(component_data['value'], node2, node1, name=component_name)
        return circuit
    
    def get_nodes_from_wires(self, wires: Dict[str, Dict[str, Any]]) -> Set[str]:
        """Retorna os nós do circuito a partir dos fios"""
        nodes: Set[str] = set()
        for wire_name, wire_data in wires.items():
            if wire_data['type'] == 'wire':
                if wire_data['node'] is not None:
                    nodes.add(wire_data['node'])
        return nodes

    def solve_circuit(self, nodes: Dict[str, Dict[str, Any]], components: Dict[str, Dict[str, Any]]) -> Optional[Dict[Any, float]]:
        """Resolve o circuito e retorna a solução"""
        try:
            # Compilar circuito
            circuit: CircuitClass = self.compile_circuit(nodes, components)

            # Resolver circuito
            nodal_analyzer: NodalAnalyzer = NodalAnalyzer(circuit)
            return nodal_analyzer.get_conductances_matrix()
            
        except Exception as e:
            print(e)
            return None
    
    def show_solution(self, solution: Dict[Any, float], parent_window: tk.Tk) -> None:
        """Mostra a solução do circuito em uma janela"""
        result_text: str = "Resultados da Análise:\n\n"
        
        for variable, value in solution.items():
            if isinstance(variable, Node):
                result_text += f"Nó {variable.name}: {value:.4f} V\n"
            else:
                result_text += f"Corrente {variable[0].name}: {value:.4f} A\n"
        
        # Mostrar em janela separada
        result_window: tk.Toplevel = tk.Toplevel(parent_window)
        result_window.title("Resultados")
        result_window.geometry("400x300")
        
        text_widget: tk.Text = tk.Text(result_window, wrap=tk.WORD)
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        text_widget.insert(tk.END, result_text)
        text_widget.config(state=tk.DISABLED)
    
    def validate_circuit(self, nodes: Dict[str, Dict[str, Any]], components: Dict[str, Dict[str, Any]]) -> tuple[bool, str]:
        """Valida se o circuito pode ser resolvido"""
        if not nodes:
            return False, "Circuito deve ter pelo menos um nó"
        
        if not components:
            return False, "Circuito deve ter pelo menos um componente"
        
        # Verificar se todos os componentes estão conectados
        for comp_name, comp_data in components.items():
            if not comp_data.get('node1') or not comp_data.get('node2'):
                return False, f"Componente {comp_name} não está conectado a dois nós"
        
        # Verificar se há pelo menos um nó terra
        has_ground = any(comp_data.get('type') == 'ground' for comp_data in components.values())
        if not has_ground:
            return False, "Circuito deve ter pelo menos um componente terra (GND)"
        
        return True, "Circuito válido"

