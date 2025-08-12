import tkinter as tk
from typing import Optional, Tuple, List, TYPE_CHECKING
from .canvas_widget import CircuitCanvas
from .preview_rectangle import PreviewRectangle

if TYPE_CHECKING:
    from .component_manager import ComponentManager
    from .node_manager import NodeManager

class CanvasHandler:
    """Gerencia as interações com o canvas"""
    
    def __init__(self, canvas_widget: CircuitCanvas) -> None:
        self.canvas_widget = canvas_widget
        self.preview_rectangle: PreviewRectangle = PreviewRectangle(canvas_widget)
        self.cursor_mode: str = "default"
        self.connection_mode: bool = False
        self.connection_start: Optional[str] = None
        
        # Modo de criação de wire
        self.wire_creation_start: Optional[Tuple[int, int]] = None
        
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
    
    def on_escape_key(self, event: tk.Event, component_manager=None, node_manager=None) -> None:
        """Manipula a tecla ESC - volta ao modo padrão"""
        if component_manager and node_manager:
            self.clear_selection(component_manager, node_manager)
        self.reset_to_default_mode()
    
    def reset_to_default_mode(self) -> None:
        """Reseta o estado para o modo padrão"""
        # Voltar ao modo padrão do cursor
        self.cursor_mode = "default"
        
        # Esconder o preview rectangle
        self.preview_rectangle.hide()
        
        # Resetar modo de conexão
        self.connection_mode = False
        self.connection_start = None
        
        # Resetar modo de criação de wire
        self.wire_creation_start = None
        
        # Limpar preview de wire
        canvas = self.canvas_widget.get_canvas()
        canvas.delete("wire_preview")
    
    def set_cursor_mode(self, mode: str) -> None:
        """Define o modo do cursor"""
        if self.cursor_mode != mode:
            self.preview_rectangle.hide()
        self.cursor_mode = mode
    
    def on_canvas_click(self, event: tk.Event, 
                        component_manager: 'ComponentManager', node_manager: 'NodeManager',
                        on_component_click, on_node_click, on_wire_click) -> None:
        """Manipula cliques no canvas"""
        x: int = event.x
        y: int = event.y
        
        # Verificar modo do cursor
        if self.cursor_mode == "resistor":
            self.handle_resistor_placement(x, y, component_manager, node_manager)
            return
        elif self.cursor_mode == "voltage_source":
            self.handle_voltage_source_placement(x, y, component_manager, node_manager)
            return
        elif self.cursor_mode == "current_source":
            self.handle_current_source_placement(x, y, component_manager, node_manager)
            return
        elif self.cursor_mode == "ground":
            self.handle_ground_placement(x, y, node_manager)
            return
        elif self.cursor_mode == "update_node":
            node_manager.finish_node_editing()
            return
        elif self.cursor_mode == "wire_editing":
            # Modo de edição de wire
            if node_manager.wire_editing_mode:
                node_manager.finish_wire_editing(x, y)
            return
        elif self.cursor_mode == "wire_creation":
            # Modo de criação de wire
            self.handle_wire_creation(x, y, node_manager)
            return
        
        # Esconder o retângulo de preview e resetar o modo do cursor
        self.preview_rectangle.hide()
        self.cursor_mode = "default"
        
        # Verificar se clicou em um componente ou nó
        self.handle_canvas_item_click(x, y, on_component_click, on_node_click, on_wire_click)
    
    def handle_resistor_placement(self, x: int, y: int, component_manager: 'ComponentManager', node_manager: 'NodeManager') -> None:
        """Manipula a colocação de um resistor"""
        # Obter posições dos terminais
        terminals = self.canvas_widget.get_component_terminals('resistor')
        
        # Calcular posições absolutas dos terminais
        terminal_1 = { 'x': x + terminals[0]['x'], 'y': y + terminals[0]['y'] }
        terminal_2 = { 'x': x + terminals[1]['x'], 'y': y + terminals[1]['y'] }
        
        # Adicionar o resistor
        component_name = component_manager.add_resistor(x, y, [terminal_1, terminal_2])
        
        # Criar wires para conectar os terminais
        # Wire do terminal 1 para a esquerda
        wire1_name = node_manager.add_wire(terminal_1['x'], terminal_1['y'], terminal_1['x'] - 10, terminal_1['y'])
        
        # Wire do terminal 2 para a direita
        wire2_name = node_manager.add_wire(terminal_2['x'], terminal_2['y'], terminal_2['x'] + 10, terminal_2['y'])
        
        # Conectar os wires ao componente
        node_manager.connect_wire_to_component(wire1_name, component_name, 0)
        node_manager.connect_wire_to_component(wire2_name, component_name, 0)

        self.preview_rectangle.hide()
        self.cursor_mode = "default"
    
    def handle_voltage_source_placement(self, x: int, y: int, component_manager, node_manager) -> None:
        """Manipula a colocação de uma fonte de tensão"""
        component_name = component_manager.add_voltage_source(x, y)
        
        # Obter posições dos terminais
        terminals = self.canvas_widget.get_component_terminals('voltage_source')
        
        # Calcular posições absolutas dos terminais
        terminal_1 = { 'x': x + terminals[0]['x'], 'y': y + terminals[0]['y'] }
        terminal_2 = { 'x': x + terminals[1]['x'], 'y': y + terminals[1]['y'] }
        
        # Criar wires para conectar os terminais
        wire1_name = node_manager.add_wire(terminal_1['x'], terminal_1['y'], terminal_1['x'] - 10, terminal_1['y'])
        wire2_name = node_manager.add_wire(terminal_2['x'], terminal_2['y'], terminal_2['x'] + 10, terminal_2['y'])
        
        # Conectar os wires ao componente
        node_manager.connect_wire_to_component(wire1_name, component_name, 0)
        node_manager.connect_wire_to_component(wire2_name, component_name, 1)
        
        self.cursor_mode = "default"
    
    def handle_current_source_placement(self, x: int, y: int, component_manager, node_manager) -> None:
        """Manipula a colocação de uma fonte de corrente"""
        component_name = component_manager.add_current_source(x, y)
        
        # Obter posições dos terminais
        terminals = self.canvas_widget.get_component_terminals('current_source')
        
        # Calcular posições absolutas dos terminais
        terminal_1 = { 'x': x + terminals[0]['x'], 'y': y + terminals[0]['y'] }
        terminal_2 = { 'x': x + terminals[1]['x'], 'y': y + terminals[1]['y'] }
        
        # Criar wires para conectar os terminais
        wire1_name = node_manager.add_wire(terminal_1['x'], terminal_1['y'], terminal_1['x'] - 10, terminal_1['y'])
        wire2_name = node_manager.add_wire(terminal_2['x'], terminal_2['y'], terminal_2['x'] + 10, terminal_2['y'])
        
        # Conectar os wires ao componente
        node_manager.connect_wire_to_component(wire1_name, component_name, 0)
        node_manager.connect_wire_to_component(wire2_name, component_name, 1)
        
        self.cursor_mode = "default"
    
    def handle_ground_placement(self, x: int, y: int, node_manager) -> None:
        """Manipula a colocação de um nó terra"""
        ground_name = node_manager.add_ground(x, y)
        
        # Criar um wire vertical para o terra
        wire_name = node_manager.add_wire(x, y, x, y + 20)
        
        # Conectar o wire ao terra
        node_manager.connect_wire_to_component(wire_name, ground_name, 0)
        
        self.cursor_mode = "default"
    
    def handle_wire_creation(self, x: int, y: int, node_manager) -> None:
        """Manipula a criação de um wire"""
        # Ajustar coordenadas ao grid
        x, y = self.canvas_widget.snap_to_grid(x, y)
        
        if self.wire_creation_start is None:
            # Primeiro clique - definir posição inicial
            self.wire_creation_start = (x, y)
        else:
            # Segundo clique - criar o wire
            start_x, start_y = self.wire_creation_start
            wire_name = node_manager.add_wire(start_x, start_y, x, y)
            
            # Limpar preview
            canvas = self.canvas_widget.get_canvas()
            canvas.delete("wire_preview")
            
            # Resetar modo
            self.wire_creation_start = (x, y)
    
    def handle_canvas_item_click(self, x: int, y: int, on_component_click, on_node_click, on_wire_click) -> None:
        """Manipula clique em itens do canvas"""
        canvas = self.canvas_widget.get_canvas()
        clicked_item: Tuple[int, ...] = canvas.find_closest(x, y)
        # Verifica se o item está a mais de 10px de distância; se sim, ignora
        if clicked_item:
            coords = canvas.coords(clicked_item[0])
            # Para linhas e ovais, pega o centro aproximado
            if len(coords) >= 4:
                item_x = (coords[0] + coords[2]) / 2
                item_y = (coords[1] + coords[3]) / 2
            elif len(coords) >= 2:
                item_x = coords[0]
                item_y = coords[1]
            else:
                item_x = x
                item_y = y
            dist = ((item_x - x) ** 2 + (item_y - y) ** 2) ** 0.5
            if dist > 10:
                clicked_item = ()
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
                elif tag.startswith("wire_"):
                    wire_name: str = tag.split("_", 1)[1]
                    on_wire_click(wire_name, x, y)
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
        elif self.cursor_mode == "wire_creation" and self.wire_creation_start:
            # Mostrar preview do wire sendo criado
            self.show_wire_preview(event.x, event.y)
        elif self.cursor_mode == "wire_editing":
            node_manager.update_wire_editing(event.x, event.y)
        else:
            self.preview_rectangle.hide()
    
    def show_wire_preview(self, x: int, y: int) -> None:
        """Mostra preview do wire sendo criado"""
        if self.wire_creation_start:
            start_x, start_y = self.wire_creation_start
            
            # Ajustar coordenadas ao grid
            x, y = self.canvas_widget.snap_to_grid(x, y)
            
            # Limpar preview anterior
            canvas = self.canvas_widget.get_canvas()
            canvas.delete("wire_preview")
            
            # Desenhar preview
            canvas.create_line(start_x, start_y, x, y, fill="red", width=2, 
                             dash=(5, 5), tags="wire_preview")
    
    def on_canvas_leave(self, event: tk.Event) -> None:
        """Manipula quando o mouse sai do canvas"""
        self.preview_rectangle.hide()
        
        # Limpar preview de wire
        canvas = self.canvas_widget.get_canvas()
        canvas.delete("wire_preview")
    
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
        node_manager.set_selected_node(None)
        self.connection_start = None
        self.connection_mode = False
        self.wire_creation_start = None
        self.preview_rectangle.hide()
        
        # Limpar preview de wire
        canvas = self.canvas_widget.get_canvas()
        canvas.delete("wire_preview")
        
        # Sair do modo de edição de nó se estiver ativo
        if node_manager.node_editing_mode:
            node_manager.exit_node_editing_mode()
        
        # Sair do modo de edição de wire se estiver ativo
        if node_manager.wire_editing_mode:
            node_manager.exit_wire_editing_mode()
    
    def get_preview_rectangle(self) -> PreviewRectangle:
        """Retorna o retângulo de preview"""
        return self.preview_rectangle

