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
        self.root.bind("<Key-r>", lambda e: self.canvas_handler.on_rotate_key(e))
        self.root.bind("<Key-R>", lambda e: self.canvas_handler.on_rotate_key(e))


        self.clear_circuit()
    
    def setup_interface(self) -> None:
        """Configura a interface de usuário"""
        # Adicionar botões de componentes
        self.ui_components.add_component_button("Criar Fio", self.add_node)
        self.ui_components.add_component_button("Deletar Fio", self.delete_node)
        self.ui_components.add_component_button("Resistor", lambda: self.canvas_handler.set_cursor_mode("resistor"))
        self.ui_components.add_component_button("Fonte de Tensão", lambda: self.canvas_handler.set_cursor_mode("voltage_source"))
        self.ui_components.add_component_button("Fonte de Corrente", lambda: self.canvas_handler.set_cursor_mode("current_source"))
        self.ui_components.add_component_button("Terra (GND)", lambda: self.canvas_handler.set_cursor_mode("ground"))
        
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
                                                          self.handle_component_click, self.handle_node_click, self.handle_wire_click))
        canvas.bind("<Double-Button-1>", lambda e: original_double_click(e, self.component_manager, self.node_manager))
        canvas.bind("<B1-Motion>", lambda e: original_drag(e, self.component_manager))
        canvas.bind("<ButtonRelease-1>", lambda e: original_release(e, self.component_manager))
        canvas.bind("<Motion>", lambda e: original_motion(e, self.node_manager))
    
    def add_node(self) -> None:
        """Adiciona um nó ao circuito (agora cria um wire)"""
        self.canvas_handler.set_cursor_mode("wire_creation")
        self.update_info()

    def delete_node(self) -> None:
        """Deleta um nó do circuito"""
        self.canvas_handler.set_cursor_mode("wire_deletion")
        self.update_info()
    
    def start_wire_creation(self) -> None:
        """Inicia o modo de criação de wire"""
        self.canvas_handler.set_cursor_mode("wire_creation")
    
    def handle_component_click(self, component_name: str, x: int, y: int) -> None:
        """Manipula clique em componente"""
        self.component_manager.set_selected_component(component_name)
        self.node_manager.set_selected_node(None)
        self.update_info()
    
    def handle_wire_click(self, wire_name: str, x: int, y: int) -> None:
        """Manipula clique em fio"""
        x, y = self.canvas_widget.snap_to_grid(x, y)
        if wire_name.startswith("terminal_"):
            terminal_num = int(wire_name.split("_")[1])
            wire_name = wire_name.split("_", 2)[2]
            self.node_manager.start_wire_editing(wire_name, terminal_num, x, y)
        
        self.node_manager.set_selected_node(None)
        self.component_manager.set_selected_component(None)
        self.update_info()
    
    def handle_node_click(self, node_name: str, x: int, y: int) -> None:
        """Manipula clique em nó ou wire"""
        node_data = self.node_manager.get_node(node_name)
        wire_name = node_data['wire']
        self.handle_wire_click(f'terminal_1_{wire_name}', x, y)
    
    def solve_circuit(self) -> None:
        """Resolve o circuito"""
        self.node_manager.name_all_nodes()
        try:
            solution = self.circuit_analyzer.solve_circuit(self.node_manager.get_all_nodes(), self.component_manager.get_all_components())
            for eq in solution[0]:
                print(eq)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao resolver circuito: {str(e)}")
    
    def clear_circuit(self) -> None:
        """Limpa o circuito"""
        self.component_manager.clear_components()
        self.node_manager.clear_nodes()
        self.canvas_widget.clear_canvas()
        self.canvas_handler.get_preview_rectangle().hide()
        
        # Resetar modo de cursor para padrão
        self.canvas_handler.reset_to_default_mode()
        
        # Limpar preview de wire se existir
        canvas = self.canvas_widget.get_canvas()
        canvas.delete("wire_preview")
        
        self.update_info()
    
    def save_circuit(self) -> None:
        """Salva o circuito"""
        try:
            self.file_manager.save_circuit(
                self.node_manager.get_all_nodes(),  # Inclui nós e wires
                self.component_manager.get_all_components()
            )
            messagebox.showinfo("Sucesso", "Circuito salvo com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar circuito: {str(e)}")
    
    def load_circuit(self) -> None:
        """Carrega um circuito"""
        result = self.file_manager.load_circuit()
        if result:
            nodes, components = result
            
            # Limpar circuito atual
            self.clear_circuit()
            
            # Carregar nós e wires
            for name, node_data in nodes.items():
                if node_data['type'] == 'ground':
                    # Ground agora é um componente, não um nó
                    self.component_manager.components[name] = node_data
                    self.canvas_widget.draw_component(name, node_data['x'], node_data['y'], node_data)
                elif node_data['type'] == 'wire':
                    self.node_manager.nodes[name] = node_data
                    self.canvas_widget.draw_wire(name, node_data['x1'], node_data['y1'], 
                                               node_data['x2'], node_data['y2'])
                else:
                    self.node_manager.nodes[name] = node_data
                    self.canvas_widget.draw_node(name, node_data['x'], node_data['y'])
            
            # Carregar componentes
            for name, component_data in components.items():
                self.component_manager.components[name] = component_data
                self.canvas_widget.draw_component(name, component_data['x'], component_data['y'], component_data)
            
            # Redesenhar conexões
            self.canvas_widget.redraw_connections()
            
            # Atualizar informações
            self.update_info()
            
            messagebox.showinfo("Sucesso", "Circuito carregado com sucesso!")
    
    def update_info(self) -> None:
        """Atualiza as informações na área de texto"""
        nodes = self.node_manager.get_all_nodes()
        wires = self.node_manager.get_wires()
        actual_nodes = self.node_manager.get_nodes()
        components = self.component_manager.get_all_components()
        
        info: str = f"Circuit Info:\n"
        info += f"Nós: {len(actual_nodes)}\n"
        info += f"Wires: {len(wires)}\n"
        info += f"Componentes: {len(components)}\n\n"
        
        info += "Nós:\n"
        for name, node in actual_nodes.items():
            info += f"  {name}: {node['type']}\n"
        
        info += "\nWires:\n"
        for name, wire in wires.items():
            info += f"  {name}: ({wire['x1']}, {wire['y1']}) -> ({wire['x2']}, {wire['y2']})\n"
            connections = wire.get('connections', [])
            if connections:
                info += f"    Conectado a: "
                for conn in [ c for c in connections if c['node'] is None]:
                    info += f"{conn['component']}({conn['terminal']}) "
                info += "\n"
            else:
                info += f"    Sem conexões (livre para conectar)\n"
        
        info += "\nComponentes:\n"
        for name, component in components.items():
            info += f"  {name}: {component['type']} = {component['value']}\n"
            if component.get('node1'):
                info += f"    Conectado a: {component['node1']} e {component['node2']}\n"
            else:
                info += f"    Sem conexões\n"
        
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
