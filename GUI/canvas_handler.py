import tkinter as tk
from typing import Optional, Tuple, List
from .canvas_widget import CircuitCanvas
from .preview_rectangle import PreviewRectangle

class CanvasHandler:
    """Gerencia as interações com o canvas"""
    
    def __init__(self, canvas_widget: CircuitCanvas) -> None:
        self.canvas_widget = canvas_widget
        self.preview_rectangle: PreviewRectangle = PreviewRectangle(canvas_widget)
        self.cursor_mode: str = "default"
        self.connection_mode: bool = False
        self.connection_start: Optional[str] = None
        
        # Configurar bindings do canvas
        self.setup_canvas_bindings()
    
    def setup_canvas_bindings(self) -> None:
        """Configura os bindings do canvas"""
        canvas = self.canvas_widget.get_canvas()
        canvas.bind("<Button-1>", self.on_canvas_click)
        canvas.bind("<Double-Button-1>", self.on_canvas_double_click)
        canvas.bind("<B1-Motion>", self.on_canvas_drag)
        canvas.bind("<ButtonRelease-1>", self.on_canvas_release)
        canvas.bind("<Motion>", self.on_canvas_motion)
        canvas.bind("<Leave>", self.on_canvas_leave)
    
    def set_cursor_mode(self, mode: str) -> None:
        """Define o modo do cursor"""
        if self.cursor_mode != mode:
            self.preview_rectangle.hide()
        self.cursor_mode = mode
    
    def on_canvas_click(self, event: tk.Event, 
                        component_manager, node_manager,
                        on_component_click, on_node_click) -> None:
        """Manipula cliques no canvas"""
        x: int = event.x
        y: int = event.y
        
        # Verificar modo do cursor
        if self.cursor_mode == "resistor":
            self.handle_resistor_placement(x, y, component_manager, node_manager)
            return
        elif self.cursor_mode == "voltage_source":
            self.handle_voltage_source_placement(x, y, component_manager)
            return
        elif self.cursor_mode == "current_source":
            self.handle_current_source_placement(x, y, component_manager)
            return
        elif self.cursor_mode == "ground":
            self.handle_ground_placement(x, y, node_manager)
            return
        elif self.cursor_mode == "update_node":
            node_manager.finish_node_editing()
            return
        
        # Esconder o retângulo de preview e resetar o modo do cursor
        self.preview_rectangle.hide()
        self.cursor_mode = "default"
        
        # Verificar se clicou em um componente ou nó
        self.handle_canvas_item_click(x, y, on_component_click, on_node_click)
    
    def handle_resistor_placement(self, x: int, y: int, component_manager, node_manager) -> None:
        """Manipula a colocação de um resistor"""
        # Obter posições dos terminais
        terminals = self.canvas_widget.get_component_terminals('resistor')
        
        # Calcular posições absolutas dos terminais
        terminal1_x = x + terminals[0]['x']
        terminal1_y = y + terminals[0]['y']
        terminal2_x = x + terminals[1]['x']
        terminal2_y = y + terminals[1]['y']
        
        # Verificar se já existem nós nas posições dos terminais
        node1_name = node_manager.find_node_at_position(terminal1_x, terminal1_y)
        node2_name = node_manager.find_node_at_position(terminal2_x, terminal2_y)
        
        # Criar nós se não existirem
        if not node1_name:
            node1_name = node_manager.add_node_auto(terminal1_x, terminal1_y)
        
        if not node2_name:
            node2_name = node_manager.add_node_auto(terminal2_x, terminal2_y)
        
        # Adicionar o resistor
        component_name = component_manager.add_resistor(x, y, node1_name, node2_name)
        
        # Conectar o resistor aos nós
        component_manager.connect_component_to_node(component_name, node1_name)
        component_manager.connect_component_to_node(component_name, node2_name)
        
        self.preview_rectangle.hide()
        self.cursor_mode = "default"
    
    def handle_voltage_source_placement(self, x: int, y: int, component_manager) -> None:
        """Manipula a colocação de uma fonte de tensão"""
        component_manager.add_voltage_source(x, y)
        self.cursor_mode = "default"
    
    def handle_current_source_placement(self, x: int, y: int, component_manager) -> None:
        """Manipula a colocação de uma fonte de corrente"""
        component_manager.add_current_source(x, y)
        self.cursor_mode = "default"
    
    def handle_ground_placement(self, x: int, y: int, node_manager) -> None:
        """Manipula a colocação de um nó terra"""
        node_manager.add_ground(x, y)
        self.cursor_mode = "default"
    
    def handle_canvas_item_click(self, x: int, y: int, on_component_click, on_node_click) -> None:
        """Manipula clique em itens do canvas"""
        canvas = self.canvas_widget.get_canvas()
        clicked_item: Tuple[int, ...] = canvas.find_closest(x, y)
        if clicked_item:
            tags: Tuple[str, ...] = canvas.gettags(clicked_item[0])
            
            for tag in tags:
                if tag.startswith("component_"):
                    component_name: str = tag.split("_", 1)[1]
                    on_component_click(component_name, x, y)
                    return
                elif tag.startswith("node_"):
                    node_name: str = tag.split("_", 1)[1]
                    on_node_click(node_name, x, y)
                    return
                elif tag.startswith("ground_"):
                    ground_node_name: str = tag.split("_", 1)[1]
                    on_node_click(ground_node_name, x, y)
                    return
    
    def on_canvas_double_click(self, event: tk.Event, 
                               component_manager, node_manager) -> None:
        """Manipula duplo clique no canvas para editar propriedades"""
        x: int = event.x
        y: int = event.y
        
        # Verificar se clicou em um componente ou nó
        canvas = self.canvas_widget.get_canvas()
        clicked_item: Tuple[int, ...] = canvas.find_closest(x, y)
        if clicked_item:
            tags: Tuple[str, ...] = canvas.gettags(clicked_item[0])
            
            for tag in tags:
                if tag.startswith("component_"):
                    component_name: str = tag.split("_", 1)[1]
                    component_manager.edit_component_properties(component_name, self.canvas_widget.get_root())
                    return
                elif tag.startswith("node_"):
                    node_name: str = tag.split("_", 1)[1]
                    node_manager.edit_node_properties(node_name, self.canvas_widget.get_root())
                    return
                elif tag.startswith("ground_"):
                    ground_node_name: str = tag.split("_", 1)[1]
                    node_manager.edit_node_properties(ground_node_name, self.canvas_widget.get_root())
                    return
    
    def on_canvas_drag(self, event: tk.Event, component_manager) -> None:
        """Manipula arrastar no canvas"""
        selected_component = component_manager.get_selected_component()
        if selected_component:
            x: int
            y: int
            x, y = self.canvas_widget.snap_to_grid(event.x, event.y)
            self.canvas_widget.move_component(selected_component, x, y)
    
    def on_canvas_release(self, event: tk.Event, component_manager) -> None:
        """Manipula soltar no canvas"""
        component_manager.set_selected_component(None)
    
    def on_canvas_motion(self, event: tk.Event, node_manager) -> None:
        """Manipula movimento do mouse no canvas"""
        if self.cursor_mode == "resistor":
            self.preview_rectangle.update("resistor", event.x, event.y)
        elif node_manager.get_selected_node():
            # Atualizar linhas temporárias durante edição de nó
            node_manager.update_temp_node_lines(event.x, event.y)
        else:
            self.preview_rectangle.hide()
    
    def on_canvas_leave(self, event: tk.Event) -> None:
        """Manipula quando o mouse sai do canvas"""
        self.preview_rectangle.hide()
    
    def toggle_connection_mode(self) -> None:
        """Alterna o modo de conexão"""
        self.connection_mode = not self.connection_mode
        if self.connection_mode:
            # Mostrar mensagem informativa
            pass
        else:
            self.connection_start = None
    
    def clear_selection(self, component_manager, node_manager) -> None:
        """Limpa a seleção atual"""
        component_manager.set_selected_component(None)
        self.connection_start = None
        self.connection_mode = False
        self.preview_rectangle.hide()
        
        # Sair do modo de edição de nó se estiver ativo
        if node_manager.node_editing_mode:
            node_manager.exit_node_editing_mode()
    
    def get_preview_rectangle(self) -> PreviewRectangle:
        """Retorna o retângulo de preview"""
        return self.preview_rectangle

