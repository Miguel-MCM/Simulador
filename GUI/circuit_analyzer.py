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
        
        
        
        return circuit
    
    def get_nodes_from_wires(self, wires: Dict[str, Dict[str, Any]]) -> Dict[str, Node]:
        """Retorna os nós do circuito a partir dos fios"""
        nodes: Dict[str, Node] = {}
        for wire_name, wire_data in wires.items():
            if wire_data['type'] == 'wire':
                nodes[wire_name] = None
                for connection in wire_data['connections']:
                    if connection['node'] is not None:
                        nodes[wire_name] = connection['node']
                        break
        return nodes

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

