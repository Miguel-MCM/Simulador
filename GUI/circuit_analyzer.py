import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, Any, Optional
from Circuit import Circuit as CircuitClass, Node, Resistor, IndependentCurrentSource, IndependentTensionSource

class CircuitAnalyzer:
    """Responsável pela análise e resolução do circuito"""
    
    def __init__(self) -> None:
        pass
    
    def compile_circuit(self, nodes: Dict[str, Dict[str, Any]], components: Dict[str, Dict[str, Any]]) -> CircuitClass:
        """Compila o circuito visual em objetos do circuito"""
        circuit: CircuitClass = CircuitClass()
        node_objects: Dict[str, Node] = {}
        
        # Criar objetos Node para cada nó visual
        for name, node_data in nodes.items():
            node = Node(circuit, name=name)
            node_objects[name] = node
        
        # Criar componentes do circuito
        for name, component_data in components.items():
            if component_data['type'] == 'ground':
                # Ground é um componente especial que cria um nó terra
                ground_node: Node = Node(circuit, gnd=True, name=name)
                node_objects[name] = ground_node
            elif component_data['node1'] and component_data['node2']:
                node1: Node = node_objects[component_data['node1']]
                node2: Node = node_objects[component_data['node2']]
                
                if component_data['type'] == 'resistor':
                    resistor: Resistor = Resistor(component_data['value'], node1, node2, name=name)
                elif component_data['type'] == 'voltage_source':
                    voltage_source: IndependentTensionSource = IndependentTensionSource(component_data['value'], node1, node2, name=name)
                elif component_data['type'] == 'current_source':
                    current_source: IndependentCurrentSource = IndependentCurrentSource(component_data['value'], node1, node2, name=name)
        
        return circuit
    
    def solve_circuit(self, nodes: Dict[str, Dict[str, Any]], components: Dict[str, Dict[str, Any]]) -> Optional[Dict[Any, float]]:
        """Resolve o circuito e retorna a solução"""
        try:
            # Compilar circuito
            circuit: CircuitClass = self.compile_circuit(nodes, components)
            
            # Resolver circuito
            solution: Dict[Any, float] = circuit.solve()
            
            return solution
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao resolver circuito: {str(e)}")
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

