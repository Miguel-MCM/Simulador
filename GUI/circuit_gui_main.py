import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, Any, Optional
from .component_manager import ComponentManager
from .node_manager import NodeManager
from .circuit_analyzer import CircuitAnalyzer
from .file_manager import FileManager
from .ui_components import UIComponents
from .canvas_handler import CanvasHandler
from .canvas_widget import CircuitCanvas

class CircuitGUIMain:
    """Classe principal que coordena todas as funcionalidades do simulador de circuitos"""
    
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Simulador de Circuitos")
        self.root.geometry("1200x800")
        
        # Frame principal
        self.main_frame: ttk.Frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame direito - Área de desenho
        self.right_frame: ttk.Frame = ttk.Frame(self.main_frame)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Canvas para desenho do circuito
        self.canvas_widget: CircuitCanvas = CircuitCanvas(self.right_frame, self)
        
        # Inicializar gerenciadores
        self.component_manager = ComponentManager(self.canvas_widget)
        self.node_manager = NodeManager(self.canvas_widget)
        self.circuit_analyzer = CircuitAnalyzer()
        self.file_manager = FileManager()
        
        # Inicializar interface
        self.ui_components = UIComponents(self.main_frame)
        
        # Inicializar manipulador do canvas
        self.canvas_handler = CanvasHandler(self.canvas_widget)
        
        # Configurar interface
        self.setup_interface()
        
        # Configurar callbacks do canvas
        self.setup_canvas_callbacks()

        self.root.bind("<Escape>", lambda e: self.canvas_handler.on_escape_key(e, self.component_manager, self.node_manager))


        self.clear_circuit()
    
    def setup_interface(self) -> None:
        """Configura a interface de usuário"""
        # Adicionar botões de componentes
        self.ui_components.add_component_button("Nó", self.add_node)
        self.ui_components.add_component_button("Resistor", lambda: self.canvas_handler.set_cursor_mode("resistor"))
        self.ui_components.add_component_button("Fonte de Tensão", lambda: self.canvas_handler.set_cursor_mode("voltage_source"))
        self.ui_components.add_component_button("Fonte de Corrente", lambda: self.canvas_handler.set_cursor_mode("current_source"))
        self.ui_components.add_component_button("Terra (GND)", lambda: self.canvas_handler.set_cursor_mode("ground"))
        
        # Adicionar botões de conexões
        self.ui_components.add_connection_button("Conectar Componentes", self.canvas_handler.toggle_connection_mode)
        self.ui_components.add_connection_button("Limpar Seleção", lambda: self.canvas_handler.clear_selection(self.component_manager, self.node_manager))
        self.ui_components.add_connection_button("Cancelar Edição de Nó", self.node_manager.cancel_node_editing)
        
        # Adicionar botões de análise
        self.ui_components.add_analysis_button("Resolver Circuito", self.solve_circuit)
        self.ui_components.add_analysis_button("Limpar Circuito", self.clear_circuit)
        self.ui_components.add_analysis_button("Salvar Circuito", self.save_circuit)
        self.ui_components.add_analysis_button("Carregar Circuito", self.load_circuit)
    
    def setup_canvas_callbacks(self) -> None:
        """Configura os callbacks do canvas"""
        # Sobrescrever os métodos do canvas handler para incluir os managers
        original_click = self.canvas_handler.on_canvas_click
        original_double_click = self.canvas_handler.on_canvas_double_click
        original_drag = self.canvas_handler.on_canvas_drag
        original_release = self.canvas_handler.on_canvas_release
        original_motion = self.canvas_handler.on_canvas_motion
        
        # Configurar canvas com callbacks personalizados
        canvas = self.canvas_widget.get_canvas()
        canvas.bind("<Button-1>", lambda e: original_click(e, self.component_manager, self.node_manager, 
                                                          self.handle_component_click, self.handle_node_click))
        canvas.bind("<Double-Button-1>", lambda e: original_double_click(e, self.component_manager, self.node_manager))
        canvas.bind("<B1-Motion>", lambda e: original_drag(e, self.component_manager))
        canvas.bind("<ButtonRelease-1>", lambda e: original_release(e, self.component_manager))
        canvas.bind("<Motion>", lambda e: original_motion(e, self.node_manager))
    
    def add_node(self) -> None:
        """Adiciona um nó ao circuito"""
        # Usar posição padrão (será ajustada pelo usuário)
        self.node_manager.add_node(300, 200)
        self.update_info()
    
    def handle_component_click(self, component_name: str, x: int, y: int) -> None:
        """Manipula clique em componente"""
        self.component_manager.set_selected_component(component_name)
        self.node_manager.set_selected_node(None)
        self.update_info()
    
    def handle_node_click(self, node_name: str, x: int, y: int) -> None:
        """Manipula clique em nó"""
        self.node_manager.start_node_editing(node_name)
        self.component_manager.set_selected_component(None)
        self.update_info()
    
    def solve_circuit(self) -> None:
        """Resolve o circuito"""
        # Validar circuito
        is_valid, message = self.circuit_analyzer.validate_circuit(
            self.node_manager.get_all_nodes(),
            self.component_manager.get_all_components()
        )
        
        if not is_valid:
            messagebox.showerror("Erro", message)
            return
        
        # Resolver circuito
        solution = self.circuit_analyzer.solve_circuit(
            self.node_manager.get_all_nodes(),
            self.component_manager.get_all_components()
        )
        
        if solution:
            self.circuit_analyzer.show_solution(solution, self.root)
    
    def clear_circuit(self) -> None:
        """Limpa o circuito"""
        self.component_manager.clear_components()
        self.node_manager.clear_nodes()
        self.canvas_widget.clear_canvas()
        self.canvas_handler.get_preview_rectangle().hide()
        self.update_info()
    
    def save_circuit(self) -> None:
        """Salva o circuito"""
        self.file_manager.save_circuit(
            self.node_manager.get_all_nodes(),
            self.component_manager.get_all_components()
        )
    
    def load_circuit(self) -> None:
        """Carrega um circuito"""
        result = self.file_manager.load_circuit()
        if result:
            nodes, components = result
            
            # Limpar circuito atual
            self.clear_circuit()
            
            # Carregar nós
            for name, node_data in nodes.items():
                self.node_manager.nodes[name] = node_data
                if node_data['type'] == 'ground':
                    self.canvas_widget.draw_ground(name, node_data['x'], node_data['y'])
                else:
                    self.canvas_widget.draw_node(name, node_data['x'], node_data['y'])
            
            # Carregar componentes
            for name, component_data in components.items():
                self.component_manager.components[name] = component_data
                self.canvas_widget.draw_component(name, component_data['x'], component_data['y'], component_data)
            
            # Redesenhar conexões
            self.canvas_widget.redraw_connections()
            self.update_info()
    
    def update_info(self) -> None:
        """Atualiza as informações na área de texto"""
        nodes = self.node_manager.get_all_nodes()
        components = self.component_manager.get_all_components()
        
        info: str = f"Circuit Info:\n"
        info += f"Nós: {len(nodes)}\n"
        info += f"Componentes: {len(components)}\n\n"
        
        info += "Nós:\n"
        for name, node in nodes.items():
            info += f"  {name}: {node['type']}\n"
            if node.get('gnd', False):
                info += f"    Terra (GND)\n"
        
        info += "\nComponentes:\n"
        for name, component in components.items():
            info += f"  {name}: {component['type']} = {component['value']}\n"
            if component['node1']:
                info += f"    Conectado a: {component['node1']} e {component['node2']}\n"
        
        self.ui_components.update_info(info)
    
    def get_canvas_widget(self) -> CircuitCanvas:
        """Retorna o widget do canvas"""
        return self.canvas_widget
    
    def get_component_manager(self) -> ComponentManager:
        """Retorna o gerenciador de componentes"""
        return self.component_manager
    
    def get_node_manager(self) -> NodeManager:
        """Retorna o gerenciador de nós"""
        return self.node_manager
