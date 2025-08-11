import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from typing import Dict, Any, Optional, List
from .canvas_widget import CircuitCanvas

class NodeManager:
    """Gerencia todos os nós do circuito"""
    
    def __init__(self, canvas_widget: CircuitCanvas) -> None:
        self.canvas_widget = canvas_widget
        self.nodes: Dict[str, Dict[str, Any]] = {}
        self.selected_node: Optional[str] = None
        self.node_editing_mode: bool = False
        self.editing_node: Optional[str] = None
        self.temp_lines: List[int] = []
    
    def add_node(self, x: int, y: int) -> Optional[str]:
        """Adiciona um nó ao circuito"""
        name: Optional[str] = simpledialog.askstring("Nó", "Nome do nó:")
        if name:
            self.nodes[name] = {
                'type': 'node',
                'x': x,
                'y': y,
                'gnd': False,
                'lines': []
            }
            self.canvas_widget.draw_node(name, x, y)
            return name
        return None
    
    def add_node_auto(self, x: int, y: int) -> str:
        """Adiciona um nó automaticamente com nome gerado"""
        node_count = 1
        while f"N_{node_count}" in self.nodes:
            node_count += 1
        
        name = f"N_{node_count}"
        
        self.nodes[name] = {
            'type': 'node',
            'x': x,
            'y': y,
            'gnd': False,
            'lines': []
        }
        self.canvas_widget.draw_node(name, x, y)
        return name
    
    def add_ground(self, x: int, y: int) -> str:
        """Adiciona um nó terra ao circuito"""
        self.nodes["GND"] = {
            'type': 'ground',
            'x': x,
            'y': y,
            'gnd': True,
            'lines': []
        }
        self.canvas_widget.draw_ground("GND", x, y)
        return "GND"
    
    def find_node_at_position(self, x: int, y: int, tolerance: int = 10) -> Optional[str]:
        """Encontra um nó existente na posição especificada com tolerância"""
        for node_name, node_data in self.nodes.items():
            if (abs(node_data['x'] - x) <= tolerance and 
                abs(node_data['y'] - y) <= tolerance):
                return node_name
        return None
    
    def get_node(self, node_name: str) -> Optional[Dict[str, Any]]:
        """Retorna os dados de um nó"""
        return self.nodes.get(node_name)
    
    def get_all_nodes(self) -> Dict[str, Dict[str, Any]]:
        """Retorna todos os nós"""
        return self.nodes.copy()
    
    def clear_nodes(self) -> None:
        """Limpa todos os nós"""
        self.nodes.clear()
        self.selected_node = None
        self.node_editing_mode = False
        self.editing_node = None
        self.clear_temp_lines()
    
    def set_selected_node(self, node_name: Optional[str]) -> None:
        """Define o nó selecionado"""
        self.selected_node = node_name
    
    def get_selected_node(self) -> Optional[str]:
        """Retorna o nó selecionado"""
        return self.selected_node
    
    def start_node_editing(self, node_name: str) -> None:
        """Inicia o modo de edição de nó"""
        self.node_editing_mode = True
        self.editing_node = node_name
        self.selected_node = node_name
    
    def exit_node_editing_mode(self) -> None:
        """Sai do modo de edição de nó"""
        self.node_editing_mode = False
        self.editing_node = None
        self.selected_node = None
        self.clear_temp_lines()
    
    def update_temp_node_lines(self, mouse_x: int, mouse_y: int) -> None:
        """Atualiza as linhas temporárias durante a edição de nó"""
        if not self.selected_node or self.selected_node not in self.nodes:
            return
        
        # Limpar linhas temporárias anteriores
        self.clear_temp_lines()
        
        # Obter posição do nó
        node_data = self.nodes[self.selected_node]
        node_x = node_data['x']
        node_y = node_data['y']
        
        # Calcular linhas horizontais e verticais
        lines = self.calculate_node_lines(node_x, node_y, mouse_x, mouse_y)
        
        # Desenhar linhas temporárias
        canvas = self.canvas_widget.get_canvas()
        for line_data in lines:
            line_id = canvas.create_line(
                line_data['x1'], line_data['y1'], 
                line_data['x2'], line_data['y2'],
                fill="red", width=2, dash=(5, 5), tags="temp_line"
            )
            self.temp_lines.append(line_id)
    
    def calculate_node_lines(self, node_x: int, node_y: int, mouse_x: int, mouse_y: int) -> List[Dict[str, int]]:
        """Calcula as linhas horizontais e verticais para conectar o nó ao mouse"""
        lines = []
        
        # Ajustar coordenadas ao grid
        mouse_x, mouse_y = self.canvas_widget.snap_to_grid(mouse_x, mouse_y)
        
        # Se o mouse está na mesma linha horizontal ou vertical do nó
        if abs(mouse_y - node_y) <= 5:  # Mesma linha horizontal
            # Linha horizontal direta
            lines.append({
                'x1': node_x, 'y1': node_y,
                'x2': mouse_x, 'y2': mouse_y
            })
        elif abs(mouse_x - node_x) <= 5:  # Mesma linha vertical
            # Linha vertical direta
            lines.append({
                'x1': node_x, 'y1': node_y,
                'x2': mouse_x, 'y2': mouse_y
            })
        else:
            # Criar caminho em L (duas linhas perpendiculares)
            # Primeira linha: horizontal do nó até a coluna do mouse
            lines.append({
                'x1': node_x, 'y1': node_y,
                'x2': mouse_x, 'y2': node_y
            })
            # Segunda linha: vertical da primeira linha até o mouse
            lines.append({
                'x1': mouse_x, 'y1': node_y,
                'x2': mouse_x, 'y2': mouse_y
            })
        
        return lines
    
    def clear_temp_lines(self) -> None:
        """Remove as linhas temporárias do canvas"""
        canvas = self.canvas_widget.get_canvas()
        for line_id in self.temp_lines:
            canvas.delete(line_id)
        self.temp_lines.clear()
    
    def finish_node_editing(self) -> None:
        """Finaliza a edição do nó e salva as linhas"""
        if not self.selected_node:
            return
        
        # Salvar as linhas temporárias como permanentes
        self.save_node_lines()
        
        # Sair do modo de edição
        self.exit_node_editing_mode()
    
    def save_node_lines(self) -> None:
        """Salva as linhas temporárias como permanentes para o nó"""
        if not self.selected_node or not self.temp_lines:
            return
        
        # Obter posição do nó
        node_data = self.nodes[self.selected_node]
        node_x = node_data['x']
        node_y = node_data['y']
        
        # Limpar linhas anteriores do nó
        node_data['lines'].clear()
        
        # Converter linhas temporárias para permanentes
        canvas = self.canvas_widget.get_canvas()
        for line_id in self.temp_lines:
            coords = canvas.coords(line_id)
            if len(coords) == 4:  # x1, y1, x2, y2
                line_data = {
                    'x1': int(coords[0]), 'y1': int(coords[1]),
                    'x2': int(coords[2]), 'y2': int(coords[3])
                }
                node_data['lines'].append(line_data)
        
        # Desenhar as linhas permanentes
        self.draw_node_lines(self.selected_node)
        
        # Limpar linhas temporárias
        self.clear_temp_lines()
    
    def draw_node_lines(self, node_name: str) -> None:
        """Desenha as linhas salvas de um nó"""
        if node_name not in self.nodes:
            return
        
        canvas = self.canvas_widget.get_canvas()
        
        # Remover linhas antigas do nó
        canvas.delete(f"node_lines_{node_name}")
        
        # Desenhar novas linhas
        for line_data in self.nodes[node_name]['lines']:
            canvas.create_line(
                line_data['x1'], line_data['y1'],
                line_data['x2'], line_data['y2'],
                fill="black", width=2, tags=f"node_lines_{node_name}"
            )
    
    def cancel_node_editing(self) -> None:
        """Cancela a edição de nó sem salvar as linhas"""
        if self.node_editing_mode:
            self.clear_temp_lines()
            self.exit_node_editing_mode()
            messagebox.showinfo("Cancelado", "Edição de nó cancelada!")
    
    def edit_node_properties(self, node_name: str, parent_window: tk.Tk) -> None:
        """Edita as propriedades de um nó"""
        if node_name not in self.nodes:
            return
        
        node = self.nodes[node_name]
        
        # Criar janela de edição
        edit_window = tk.Toplevel(parent_window)
        edit_window.title(f"Editar {node_name}")
        edit_window.geometry("300x150")
        edit_window.transient(parent_window)
        edit_window.grab_set()
        
        # Frame principal
        main_frame = ttk.Frame(edit_window, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Nome do nó
        ttk.Label(main_frame, text="Nome:").grid(row=0, column=0, sticky=tk.W, pady=5)
        name_entry = ttk.Entry(main_frame, width=20)
        name_entry.insert(0, node_name)
        name_entry.grid(row=0, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Botões
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=1, column=0, columnspan=2, pady=20)
        
        def save_changes():
            try:
                new_name = name_entry.get().strip()
                
                if new_name != node_name and new_name in self.nodes:
                    messagebox.showerror("Erro", "Nome já existe!")
                    return
                
                # Atualizar nome se mudou
                if new_name != node_name:
                    # Remover nó antigo
                    old_node = self.nodes.pop(node_name)
                    # Adicionar com novo nome
                    self.nodes[new_name] = old_node
                    # Atualizar canvas
                    self.canvas_widget.rename_node(node_name, new_name, old_node)
                
                edit_window.destroy()
                messagebox.showinfo("Sucesso", "Propriedades atualizadas!")
                
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao atualizar: {str(e)}")
        
        def cancel_changes():
            edit_window.destroy()
        
        ttk.Button(button_frame, text="Salvar", command=save_changes).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancelar", command=cancel_changes).pack(side=tk.LEFT, padx=5)
