import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, Any, Optional, Set, Tuple
from Circuit import Circuit as CircuitClass, Node, Resistor, IndependentCurrentSource, IndependentTensionSource, NodalAnalyzer, LoopAnalyzer    
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# Configurar matplotlib para usar TkAgg
matplotlib.use('TkAgg')

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

    def nodal_analysis(self, nodes: Dict[str, Dict[str, Any]], components: Dict[str, Dict[str, Any]]) -> Optional[Tuple[list, list]]:
        """Resolve o circuito e retorna as equações do sistema"""
        try:
            # Compilar circuito
            circuit: CircuitClass = self.compile_circuit(nodes, components)

            # Obter equações do sistema
            nodal_analyzer: NodalAnalyzer = NodalAnalyzer(circuit)
            return nodal_analyzer.get_conductances_matrix()
            
        except Exception as e:
            print(e)
            return None

    def loop_analysis(self, nodes: Dict[str, Dict[str, Any]], components: Dict[str, Dict[str, Any]]) -> Optional[Tuple[list, list]]:
        """Resolve o circuito e retorna as equações do sistema"""
        try:
            # Compilar circuito
            circuit: CircuitClass = self.compile_circuit(nodes, components)

            # Obter equações do sistema
            loop_analyzer: LoopAnalyzer = LoopAnalyzer(circuit)
            return loop_analyzer.get_resistance_matrix()
            
        except Exception as e:
            print(e)
            return None

    def show_solution(self, solution: Tuple[list, list], parent_window: tk.Tk) -> None:
        """Mostra a solução do circuito com as equações do sistema em LaTeX e a solução numérica"""
        if not solution:
            messagebox.showerror("Erro", "Não foi possível resolver o circuito")
            return
            
        equations, aux_equations = solution
        
        # Criar janela para mostrar as equações
        result_window: tk.Toplevel = tk.Toplevel(parent_window)
        result_window.title("Solução do Circuito")
        result_window.geometry("1400x900")
        
        # Frame principal
        main_frame = ttk.Frame(result_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame superior para equações (lado esquerdo)
        equations_frame = ttk.Frame(main_frame)
        equations_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Frame inferior para solução (lado direito)
        solution_frame = ttk.Frame(main_frame)
        solution_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # ===== LADO ESQUERDO: EQUAÇÕES =====
        
        # Título das equações
        equations_title = ttk.Label(equations_frame, text="Sistema de Equações", font=("Arial", 16, "bold"))
        equations_title.pack(pady=(0, 20))
        
        # Frame para equações principais
        main_eq_frame = ttk.LabelFrame(equations_frame, text="Equações Principais", padding=10)
        main_eq_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Criar figura matplotlib para equações principais
        main_fig = matplotlib.figure.Figure(figsize=(8, 6), dpi=100)
        main_ax = main_fig.add_subplot(111)
        
        # Configurar eixo para não mostrar coordenadas
        main_ax.get_xaxis().set_visible(False)
        main_ax.get_yaxis().set_visible(False)
        main_ax.set_xlim(0, 1)
        main_ax.set_ylim(0, 1)
        
        # Renderizar equações principais
        y_position = 0.95
        for i, eq in enumerate(equations):
            if eq:  # Verificar se a equação não está vazia
                latex_text = eq.to_latex()
                main_ax.text(0.05, y_position, f"${latex_text}$", fontsize=12)
                y_position -= 0.12
        
        # Adicionar canvas matplotlib para equações principais
        main_canvas = FigureCanvasTkAgg(main_fig, master=main_eq_frame)
        main_canvas.draw()
        main_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Frame para equações auxiliares
        aux_eq_frame = ttk.LabelFrame(equations_frame, text="Equações Auxiliares", padding=10)
        aux_eq_frame.pack(fill=tk.BOTH, expand=True)
        
        if aux_equations:
            # Criar figura matplotlib para equações auxiliares
            aux_fig = matplotlib.figure.Figure(figsize=(8, 6), dpi=100)
            aux_ax = aux_fig.add_subplot(111)
            
            # Configurar eixo para não mostrar coordenadas
            aux_ax.get_xaxis().set_visible(False)
            aux_ax.get_yaxis().set_visible(False)
            aux_ax.set_xlim(0, 1)
            aux_ax.set_ylim(0, 1)
            
            # Renderizar equações auxiliares
            y_position = 0.95
            for i, eq in enumerate(aux_equations):
                if eq:  # Verificar se a equação não está vazia
                    latex_text = eq.to_latex()
                    aux_ax.text(0.05, y_position, f"${latex_text}$", fontsize=12)
                    y_position -= 0.12
            
            # Adicionar canvas matplotlib para equações auxiliares
            aux_canvas = FigureCanvasTkAgg(aux_fig, master=aux_eq_frame)
            aux_canvas.draw()
            aux_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        else:
            # Se não há equações auxiliares
            no_aux_label = ttk.Label(aux_eq_frame, text="Não há equações auxiliares", 
                                    font=("Arial", 12), foreground="gray")
            no_aux_label.pack(pady=50)
        
        # ===== LADO DIREITO: SOLUÇÃO NUMÉRICA =====
        
        # Título da solução
        solution_title = ttk.Label(solution_frame, text="Solução", font=("Arial", 16, "bold"))
        solution_title.pack(pady=(0, 20))
        
        try:
            # Converter equações para matrizes numpy
            A, b, variables = self._equations_to_matrix(equations, aux_equations)
            
            if A is not None and b is not None:
                # Resolver o sistema linear
                solution_values = np.linalg.solve(A, b)
                
                # Criar figura para mostrar a solução
                solution_fig = matplotlib.figure.Figure(figsize=(8, 10), dpi=100)
                solution_ax = solution_fig.add_subplot(111)
                
                # Configurar eixo para não mostrar coordenadas
                solution_ax.get_xaxis().set_visible(False)
                solution_ax.get_yaxis().set_visible(False)
                solution_ax.set_xlim(0, 1)
                solution_ax.set_ylim(0, 1)
                                
                y_pos = 0.95
                for i, (var, val) in enumerate(zip(variables, solution_values)):
                    if i < 10:  # Mostrar no máximo 10 variáveis
                        if hasattr(var, 'name'):
                            var_name = var.name
                        else:
                            var_name = str(var)
                        solution_ax.text(0.05, y_pos, f"${var_name} = {val:.6f}$", fontsize=12)
                        y_pos -= 0.12
                
                if len(variables) > 10:
                    solution_ax.text(0.05, y_pos, "...", fontsize=12)
                
                # Adicionar canvas matplotlib à solução
                solution_canvas = FigureCanvasTkAgg(solution_fig, master=solution_frame)
                solution_canvas.draw()
                solution_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
                
            else:
                # Se não foi possível converter para matriz
                error_label = ttk.Label(solution_frame, text="Não foi possível converter as equações para matriz numérica", 
                                      font=("Arial", 12), foreground="red")
                error_label.pack(pady=50)
                
        except np.linalg.LinAlgError:
            # Erro na resolução do sistema
            error_label = ttk.Label(solution_frame, text="Erro: Sistema singular ou mal condicionado", 
                                  font=("Arial", 12), foreground="red")
            error_label.pack(pady=50)
        except Exception as e:
            # Outro erro
            error_label = ttk.Label(solution_frame, text=f"Erro ao resolver o sistema: {str(e)}", 
                                  font=("Arial", 12), foreground="red")
            error_label.pack(pady=50)
        
        # Botão para fechar (centralizado na parte inferior)
        close_button = ttk.Button(main_frame, text="Fechar", command=result_window.destroy)
        close_button.pack(side=tk.BOTTOM, pady=(10, 0))
    
    def _equations_to_matrix(self, equations: list, aux_equations: list) -> tuple[np.ndarray, np.ndarray, list]:
        """
        Converte as equações do sistema para matrizes numpy (A*x = b)
        
        Returns:
            tuple: (A, b, variables) onde A é a matriz dos coeficientes, b é o vetor independente
                   e variables é a lista de variáveis na ordem correspondente
        """
        if not equations:
            return None, None, []
        
        # Coletar todas as variáveis únicas das equações
        all_variables = set()
        for eq in equations + aux_equations:
            if eq:
                for var in eq.variables:
                    if var is not None:
                        all_variables.add(var)
        
        # Ordenar variáveis para manter consistência
        variables = sorted(list(all_variables), key=lambda x: str(x))
        n_vars = len(variables)
        
        if n_vars == 0:
            return None, None, []
        
        # Criar mapeamento de variáveis para índices
        var_to_index = {var: i for i, var in enumerate(variables)}
        
        # Inicializar matriz A e vetor b
        n_eqs = len(equations) + len(aux_equations)
        A = np.zeros((n_eqs, n_vars))
        b = np.zeros(n_eqs)
        
        # Preencher matriz A e vetor b com as equações principais
        for i, eq in enumerate(equations):
            if eq:
                for var, coeff in eq.dict.items():
                    if var is not None:
                        if var in var_to_index:
                            A[i, var_to_index[var]] = coeff
                    else:
                        # Termo independente
                        b[i] = -coeff
        
        # Preencher com equações auxiliares
        for i, eq in enumerate(aux_equations):
            if eq:
                row_idx = len(equations) + i
                for var, coeff in eq.dict.items():
                    if var is not None:
                        if var in var_to_index:
                            A[row_idx, var_to_index[var]] = coeff
                    else:
                        # Termo independente
                        b[row_idx] = -coeff
        
        # Remover linhas e colunas com todos os elementos zero
        # Encontrar linhas não-zero
        non_zero_rows = np.any(A != 0, axis=1)
        A = A[non_zero_rows]
        b = b[non_zero_rows]
        
        # Encontrar colunas não-zero
        non_zero_cols = np.any(A != 0, axis=0)
        A = A[:, non_zero_cols]
        variables = [var for i, var in enumerate(variables) if non_zero_cols[i]]
        
        # Remover nós de referência (GND) que têm tensão fixa
        reference_nodes = []
        for i, var in enumerate(variables):
            if hasattr(var, 'gnd') and var.gnd:
                reference_nodes.append(i)
        
        if reference_nodes:
            # Remover colunas e linhas correspondentes aos nós de referência
            keep_cols = [i for i in range(A.shape[1]) if i not in reference_nodes]
            A = A[:, keep_cols]
            variables = [var for i, var in enumerate(variables) if i not in reference_nodes]
        
        # Verificar se a matriz é quadrada
        if A.shape[0] != A.shape[1]:
            # Se não for quadrada, adicionar linhas ou colunas de zeros
            if A.shape[0] < A.shape[1]:
                # Adicionar linhas de zeros
                zeros = np.zeros((A.shape[1] - A.shape[0], A.shape[1]))
                A = np.vstack([A, zeros])
                b = np.append(b, np.zeros(A.shape[1] - len(b)))
            else:
                # Adicionar colunas de zeros
                zeros = np.zeros((A.shape[0], A.shape[0] - A.shape[1]))
                A = np.hstack([A, zeros])
        
        return A, b, variables
    
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

