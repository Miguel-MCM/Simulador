import tkinter as tk
from tkinter import messagebox, ttk
import math
from typing import Dict, Any, Optional, Tuple, List, TYPE_CHECKING
import json

if TYPE_CHECKING:
    from GUI.circuit_gui import CircuitGui

class CircuitCanvas:
    def __init__(self, parent: ttk.Frame, circuit_gui:'CircuitGui') -> None:
        self.parent = parent
        self.circuit_gui = circuit_gui
        
        # Configurações de desenho
        self.grid_size: int = 5
        self.component_size: int = 40
        self.line_width: int = 2
        
        # Canvas para desenho do circuito
        self.canvas: tk.Canvas = tk.Canvas(parent, bg="white", width=800, height=600)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbars
        v_scrollbar: tk.Scrollbar = tk.Scrollbar(parent, orient=tk.VERTICAL, command=self.canvas.yview)
        h_scrollbar: tk.Scrollbar = tk.Scrollbar(parent, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        # Carregar ícones de componentes
        import os
        icon_path = os.path.join(os.path.dirname(__file__), 'components_icons.json')
        with open(icon_path, 'r') as f:
            self.component_icons: Dict[str, List[Dict[str, Any]]] = json.load(f)
        
        # Grid no canvas
        self.draw_grid()
    
    def get_component_terminals(self, component_type: str) -> List[Dict[str, Any]]:
        """Retorna os terminais de um componente"""
        return self.component_icons[component_type]['terminals']
    
    def draw_grid(self) -> None:
        """Desenha o grid de fundo"""
        width: int = self.canvas.winfo_width()
        height: int = self.canvas.winfo_height()
        
        # Linhas verticais
        for x in range(0, width, self.grid_size):
            self.canvas.create_line(x, 0, x, height, fill="#f0f0f0", width=1)
        
        # Linhas horizontais
        for y in range(0, height, self.grid_size):
            self.canvas.create_line(0, y, width, y, fill="#f0f0f0", width=1)
    
    def snap_to_grid(self, x: float, y: float) -> Tuple[int, int]:
        """Ajusta coordenadas ao grid"""
        return (round(x / self.grid_size) * self.grid_size,
                round(y / self.grid_size) * self.grid_size)
    
    def draw_node(self, name: str, x: int, y: int) -> None:
        """Desenha um nó no canvas"""
        x, y = self.snap_to_grid(x, y)
        
        # Círculo do nó
        node_id: int = self.canvas.create_oval(x-5, y-5, x+5, y+5, fill="black", tags=f"node_{name}")
        
        # Texto do nome
        text_id: int = self.canvas.create_text(x, y+15, text=name, font=("Arial", 10), tags=f"node_{name}")
    
    def draw_wire(self, name: str, x1: int, y1: int, x2: int, y2: int) -> None:
        """Desenha um fio no canvas"""
        x1, y1 = self.snap_to_grid(x1, y1)
        x2, y2 = self.snap_to_grid(x2, y2)
        
        # Linha do fio
        wire_id: int = self.canvas.create_line(x1, y1, x2, y2, fill="black", width=2, tags=f"wire_{name}")
        # pontos de conexão
        self.canvas.create_oval(x1-2, y1-2, x1+2, y1+2, fill="black", tags=[f"wire_terminal_1_{name}", f"wire_{name}"])
        self.canvas.create_oval(x2-2, y2-2, x2+2, y2+2, fill="black", tags=[f"wire_terminal_2_{name}", f"wire_{name}"])
    
    def redraw_wire(self, name: str, x1: int, y1: int, x2: int, y2: int) -> None:
        """Redesenha um fio existente no canvas"""
        x1, y1 = self.snap_to_grid(x1, y1)
        x2, y2 = self.snap_to_grid(x2, y2)
        
        # Remover wire antigo
        self.canvas.delete(f"wire_{name}")
        
        # Desenhar novo wire
        self.draw_wire(name, x1, y1, x2, y2)
    

    
    def draw_component(self, name: str, x: int, y: int, component_data: Optional[Dict[str, Any]] = None) -> None:
        """Desenha um componente no canvas"""
        x, y = self.snap_to_grid(x, y)
        
        # Se não foi fornecido component_data, tentar obter do circuit_gui (compatibilidade)
        if component_data is None and self.circuit_gui and hasattr(self.circuit_gui, 'components'):
            component_data = self.circuit_gui.components.get(name)
        
        if component_data is None:
            # Dados padrão se não houver informações
            component_data = {'type': 'unknown', 'value': 0}
        
        canvas_id: int
        icon: List[Dict[str, Any]] = self.component_icons[component_data['type']]['icon']
        for item in icon:
            points: List[int] = [
                x + item['points'][0]['x'],
                y + item['points'][0]['y'],
                x + item['points'][1]['x'],
                y + item['points'][1]['y']
            ]
            canvas_id = self.canvas.create_line(points, fill="blue", width=self.line_width, tags=f"component_{name}")
        
        # Texto do nome e valor
        value_text: str = f"{component_data['value']}"
        if component_data['type'] == 'resistor':
            value_text += "Ω"
        elif component_data['type'] == 'voltage_source':
            value_text += "V"
        elif component_data['type'] == 'current_source':
            value_text += "A"
        
        # Criar texto do componente
        text_id: int = self.canvas.create_text(x, y+25, text=f"{name}\n{value_text}", 
                                              font=("Arial", 8), tags=f"component_{name}")
        
        # Armazenar text_id no component_data se possível
        if component_data is not None:
            component_data['text_id'] = text_id
    
    def draw_ground(self, name: str, x: int, y: int) -> None:
        """Desenha um nó terra no canvas"""
        x, y = self.snap_to_grid(x, y)
        
        # Símbolo de terra (linhas horizontais)
        ground_id: int = self.canvas.create_line(x-10, y, x+10, y, fill="black", width=3, tags=f"ground_{name}")
        self.canvas.create_line(x-7, y+3, x+7, y+3, fill="black", width=2, tags=f"ground_{name}")
        self.canvas.create_line(x-4, y+6, x+4, y+6, fill="black", width=1, tags=f"ground_{name}")
        
        # Texto
        text_id: int = self.canvas.create_text(x, y+20, text=name, font=("Arial", 10), tags=f"ground_{name}")
        
        self.circuit_gui.nodes[name].update({'canvas_id': ground_id, 'text_id': text_id, 'x': x, 'y': y})
    
    def move_component(self, component_name: str, x: int, y: int) -> None:
        """Move um componente para uma nova posição"""
        x, y = self.snap_to_grid(x, y)
        
        # Obter a posição atual do componente
        if not self.circuit_gui or not hasattr(self.circuit_gui, 'component_manager'):
            return
        
        component_manager = self.circuit_gui.component_manager
        component_data = component_manager.get_component(component_name)
        
        if not component_data:
            return
        
        old_x = component_data['x']
        old_y = component_data['y']
        
        # Calcular offset de movimento
        offset_x = x - old_x
        offset_y = y - old_y
        
        # Encontrar todos os elementos do componente
        component_items = self.canvas.find_withtag(f"component_{component_name}")
        
        if not component_items:
            return
        
        # Mover todos os elementos do componente
        for item in component_items:
            self.canvas.move(item, offset_x, offset_y)
        
        # Atualizar posição no component_manager
        component_manager.update_component_position(component_name, x, y)
        
        # Mover os wires conectados aos terminais
        self.move_connected_wires(component_name, offset_x, offset_y)
    
    def move_connected_wires(self, component_name: str, offset_x: int, offset_y: int) -> None:
        """Move os wires conectados aos terminais de um componente"""
        if not self.circuit_gui or not hasattr(self.circuit_gui, 'node_manager'):
            return
        component = self.circuit_gui.component_manager.get_component(component_name)
        terminals = self.get_component_terminals(component['type'])
        for terminal in terminals:
            self.circuit_gui.node_manager.update_wire_positions_for_component(component_name, offset_x, offset_y)
    
    def redraw_connections(self) -> None:
        """Redesenha todas as conexões do circuito"""
        # Limpar conexões existentes
        self.canvas.delete("connection")
        
        # Este método agora é um placeholder
        # As conexões são gerenciadas pelos managers
        # Pode ser implementado para redesenhar todas as conexões se necessário
        pass
    
    def clear_canvas(self) -> None:
        """Limpa o canvas"""
        self.canvas.delete("all")
        self.draw_grid()
    
    def get_canvas(self) -> tk.Canvas:
        """Retorna o canvas para uso externo"""
        return self.canvas 
    
    def get_root(self) -> tk.Tk:
        """Retorna a janela raiz (root) do Tkinter"""
        return self.canvas.winfo_toplevel()
    
    def create_preview_rectangle(self, component_type: str, x: int, y: int) -> int:
        """Cria um retângulo de preview para o componente especificado"""
        x, y = self.snap_to_grid(x, y)
        
        # Obter dimensões do componente do arquivo de ícones
        if component_type in self.component_icons:
            width = self.component_icons[component_type]['width']
            height = self.component_icons[component_type]['height']
        else:
            # Valores padrão se o tipo não for encontrado
            width = 40
            height = 40
        
        # Calcular posição do retângulo 
        x1 = x
        y1 = y
        x2 = x + width
        y2 = y + height

        x1, y1 = self.snap_to_grid(x1, y1)
        
        # Criar retângulo de preview
        preview_id = self.canvas.create_rectangle(
            x1, y1, x2, y2,
            outline="blue",
            width=2,
            dash=(5, 5),
            tags="preview_rectangle"
        )
        
        return preview_id
    
    def update_preview_rectangle(self, preview_id: int, component_type: str, x: int, y: int) -> None:
        """Atualiza a posição do retângulo de preview existente"""
        x, y = self.snap_to_grid(x, y)
        
        # Obter dimensões do componente
        if component_type in self.component_icons:
            width = self.component_icons[component_type]['width']
            height = self.component_icons[component_type]['height']
        else:
            width = 40
            height = 40
        
        # Calcular nova posição
        x1 = x
        y1 = y
        x2 = x + width
        y2 = y + height
        
        # Atualizar coordenadas do retângulo
        self.canvas.coords(preview_id, x1, y1, x2, y2)
    
    def rename_component(self, old_name: str, new_name: str, component_data: Optional[Dict[str, Any]] = None) -> None:
        """Renomeia um componente no canvas"""
        # Atualizar tags de todos os elementos do componente
        self.canvas.addtag_withtag(f"component_{new_name}", f"component_{old_name}")
        self.canvas.dtag(f"component_{old_name}", f"component_{old_name}")
        
        # Se não foi fornecido component_data, tentar obter do circuit_gui (compatibilidade)
        if component_data is None and self.circuit_gui and hasattr(self.circuit_gui, 'components'):
            component_data = self.circuit_gui.components.get(new_name)
        
        if component_data:
            # Atualizar texto do componente
            value_text = f"{component_data['value']}"
            if component_data['type'] == 'resistor':
                value_text += "Ω"
            elif component_data['type'] == 'voltage_source':
                value_text += "V"
            elif component_data['type'] == 'current_source':
                value_text += "A"
            
            # Atualizar o texto com o novo nome
            if 'text_id' in component_data:
                self.canvas.itemconfig(component_data['text_id'], text=f"{new_name}\n{value_text}")
    
    def rename_node(self, old_name: str, new_name: str, node_data: Optional[Dict[str, Any]] = None) -> None:
        """Renomeia um nó no canvas"""
        # Atualizar tags de todos os elementos do nó
        self.canvas.addtag_withtag(f"node_{new_name}", f"node_{old_name}")
        self.canvas.dtag(f"node_{old_name}", f"node_{old_name}")
        
        # Se não foi fornecido node_data, tentar obter do circuit_gui (compatibilidade)
        if node_data is None and self.circuit_gui and hasattr(self.circuit_gui, 'nodes'):
            node_data = self.circuit_gui.nodes.get(new_name)
        
        # Atualizar texto do nó
        if node_data and 'text_id' in node_data:
            self.canvas.itemconfig(node_data['text_id'], text=new_name)
    
    def update_component_value(self, component_name: str, new_value: float, component_data: Optional[Dict[str, Any]] = None) -> None:
        """Atualiza o valor de um componente no canvas"""
        # Se não foi fornecido component_data, tentar obter do circuit_gui (compatibilidade)
        if component_data is None and self.circuit_gui and hasattr(self.circuit_gui, 'components'):
            component_data = self.circuit_gui.components.get(component_name)
        
        if component_data:
            value_text = f"{new_value}"
            if component_data['type'] == 'resistor':
                value_text += "Ω"
            elif component_data['type'] == 'voltage_source':
                value_text += "V"
            elif component_data['type'] == 'current_source':
                value_text += "A"
            
            # Atualizar o texto com o novo valor
            if 'text_id' in component_data:
                self.canvas.itemconfig(component_data['text_id'], text=f"{component_name}\n{value_text}") 
    