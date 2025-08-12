import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from typing import Dict, Any, Optional, List, Tuple
from .canvas_widget import CircuitCanvas

class NodeManager:
    """Gerencia todos os nós e wires do circuito"""
    
    def __init__(self, canvas_widget: CircuitCanvas) -> None:
        self.canvas_widget = canvas_widget
        self.nodes: Dict[str, Dict[str, Any]] = {}
        self.selected_node: Optional[str] = None
        self.node_editing_mode: bool = False
        self.editing_node: Optional[str] = None
        self.temp_lines: List[int] = []
        
        # Modo de edição de wire
        self.wire_editing_mode: bool = False
        self.editing_wire: Optional[str] = None
        self.wire_connection_start: Optional[Tuple[int, int]] = None
        self.editing_wire_terminal: Optional[int] = 1
    
    def add_wire(self, x1: int, y1: int, x2: int, y2: int) -> str:
        """Adiciona um fio ao circuito"""
        wire_name = f"W_{len(self.nodes)}"
        self.nodes[wire_name] = {
            'type': 'wire',
            'x1': x1,
            'y1': y1,
            'x2': x2,
            'y2': y2,
            'connections': []  # Lista de componentes conectados
        }
        self.canvas_widget.draw_wire(wire_name, x1, y1, x2, y2)
        return wire_name

    def start_wire_editing(self, wire_name: str, terminal_num: int, x: int, y: int) -> None:
        """Inicia o modo de edição de wire"""
        terminal_num = 1 if terminal_num == 2 else 2
        if wire_name in self.nodes and self.nodes[wire_name]['type'] == 'wire':
            print(terminal_num)
            if ( 0 if terminal_num == 2 else 1) in [connection['terminal'] for connection in self.nodes[wire_name]['connections']]:
                return

            self.wire_editing_mode = True
            self.editing_wire = wire_name
            self.selected_node = wire_name
            self.editing_wire_terminal = terminal_num
            self.wire_connection_start = (self.nodes[self.editing_wire][f'x{terminal_num}'], self.nodes[self.editing_wire][f'y{terminal_num}'])
            self.nodes[self.editing_wire][f'x{self.editing_wire_terminal}'] = self.wire_connection_start[0]
            self.nodes[self.editing_wire][f'y{self.editing_wire_terminal}'] = self.wire_connection_start[1]
            
            # Definir modo de cursor para wire_editing
            if hasattr(self.canvas_widget, 'circuit_gui') and self.canvas_widget.circuit_gui:
                if hasattr(self.canvas_widget.circuit_gui, 'canvas_handler'):
                    self.canvas_widget.circuit_gui.canvas_handler.cursor_mode = "wire_editing"

    def update_wire_editing(self, x: int, y: int) -> None:
        """Atualiza a posição do wire"""
        if self.wire_editing_mode and self.editing_wire:
            terminal_num = 1 if self.editing_wire_terminal == 2 else 2
            self.nodes[self.editing_wire][f'x{terminal_num}'] = x
            self.nodes[self.editing_wire][f'y{terminal_num}'] = y
            self.canvas_widget.redraw_wire(self.editing_wire, self.nodes[self.editing_wire]['x1'], self.nodes[self.editing_wire]['y1'], x, y)
            
    
    def finish_wire_editing(self, x: int, y: int) -> None:
        """Finaliza a edição do wire"""
        if not self.wire_editing_mode or not self.editing_wire:
            return
        
        wire_data = self.nodes[self.editing_wire]
        
        if self.wire_connection_start:
            # Atualizar posição final do wire
            other_terminal = 1 if self.editing_wire_terminal == 2 else 2
            wire_data[f'x{self.editing_wire_terminal}'] = self.wire_connection_start[0]
            wire_data[f'y{self.editing_wire_terminal}'] = self.wire_connection_start[1]
            wire_data[f'x{other_terminal}'] = x
            wire_data[f'y{other_terminal}'] = y
            
            # Redesenhar o wire
            self.canvas_widget.redraw_wire(self.editing_wire, wire_data['x1'], wire_data['y1'], x, y)
            
            # Sair do modo de edição
            self.exit_wire_editing_mode()
        else:
            # Definir posição inicial
            self.wire_connection_start = (x, y)
            wire_data[f'x{self.editing_wire_terminal}'] = x
            wire_data[f'y{self.editing_wire_terminal}'] = y
    
    def exit_wire_editing_mode(self) -> None:
        """Sai do modo de edição de wire"""
        self.wire_editing_mode = False
        self.editing_wire = None
        self.selected_node = None
        self.wire_connection_start = None
        
        # Resetar modo do cursor
        if hasattr(self.canvas_widget, 'circuit_gui') and self.canvas_widget.circuit_gui:
            if hasattr(self.canvas_widget.circuit_gui, 'canvas_handler'):
                self.canvas_widget.circuit_gui.canvas_handler.cursor_mode = "default"
    
    def cancel_wire_editing(self) -> None:
        """Cancela a edição de wire"""
        if self.wire_editing_mode:
            self.exit_wire_editing_mode()
    
    def redraw_wire(self, wire_name: str) -> None:
        """Redesenha um wire específico"""
        if wire_name in self.nodes and self.nodes[wire_name]['type'] == 'wire':
            wire_data = self.nodes[wire_name]
            self.canvas_widget.redraw_wire(wire_name, wire_data['x1'], wire_data['y1'], wire_data['x2'], wire_data['y2'])
    
    def connect_wire_to_component(self, wire_name: str, component_name: str, terminal_index: int) -> None:
        """Conecta um wire a um terminal de componente"""
        if wire_name in self.nodes and self.nodes[wire_name]['type'] == 'wire':
            connection = {
                'component': component_name,
                'terminal': terminal_index
            }
            if connection not in self.nodes[wire_name]['connections']:
                self.nodes[wire_name]['connections'].append(connection)
    
    def get_wire_connections(self, wire_name: str) -> List[Dict[str, Any]]:
        """Retorna as conexões de um wire"""
        if wire_name in self.nodes and self.nodes[wire_name]['type'] == 'wire':
            return self.nodes[wire_name].get('connections', [])
        return []
    
    def find_wire_at_position(self, x: int, y: int, tolerance: int = 5) -> Optional[str]:
        """Encontra um wire na posição especificada"""
        for wire_name, wire_data in self.nodes.items():
            if wire_data['type'] == 'wire':
                # Verificar se o ponto está próximo da linha do wire
                if self.point_near_line(x, y, wire_data['x1'], wire_data['y1'], 
                                      wire_data['x2'], wire_data['y2'], tolerance):
                    return wire_name
        return None
    
    def point_near_line(self, px: int, py: int, x1: int, y1: int, x2: int, y2: int, tolerance: int) -> bool:
        """Verifica se um ponto está próximo de uma linha"""
        # Calcular distância do ponto à linha
        A = px - x1
        B = py - y1
        C = x2 - x1
        D = y2 - y1
        
        dot = A * C + B * D
        len_sq = C * C + D * D
        
        if len_sq == 0:
            # Ponto está no mesmo local que x1,y1
            return (px - x1) ** 2 + (py - y1) ** 2 <= tolerance ** 2
        
        param = dot / len_sq
        
        if param < 0:
            # Ponto mais próximo é x1,y1
            xx, yy = x1, y1
        elif param > 1:
            # Ponto mais próximo é x2,y2
            xx, yy = x2, y2
        else:
            # Ponto mais próximo está na linha
            xx = x1 + param * C
            yy = y1 + param * D
        
        # Calcular distância
        dx = px - xx
        dy = py - yy
        distance = (dx * dx + dy * dy) ** 0.5
        
        return distance <= tolerance
    
    def edit_wire_properties(self, wire_name: str, parent_window: tk.Tk) -> None:
        """Edita as propriedades de um wire"""
        if wire_name not in self.nodes or self.nodes[wire_name]['type'] != 'wire':
            return
        
        wire = self.nodes[wire_name]
        
        # Criar janela de edição
        edit_window = tk.Toplevel(parent_window)
        edit_window.title(f"Editar Wire {wire_name}")
        edit_window.geometry("400x300")
        edit_window.transient(parent_window)
        edit_window.grab_set()
        
        # Frame principal
        main_frame = ttk.Frame(edit_window, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Coordenadas do wire
        ttk.Label(main_frame, text="Coordenadas:", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))
        
        ttk.Label(main_frame, text="Início (x1, y1):").grid(row=1, column=0, sticky=tk.W, pady=5)
        start_frame = ttk.Frame(main_frame)
        start_frame.grid(row=1, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        x1_entry = ttk.Entry(start_frame, width=8)
        x1_entry.insert(0, str(wire['x1']))
        x1_entry.pack(side=tk.LEFT, padx=(0, 5))
        
        y1_entry = ttk.Entry(start_frame, width=8)
        y1_entry.insert(0, str(wire['y1']))
        y1_entry.pack(side=tk.LEFT)
        
        ttk.Label(main_frame, text="Fim (x2, y2):").grid(row=2, column=0, sticky=tk.W, pady=5)
        end_frame = ttk.Frame(main_frame)
        end_frame.grid(row=2, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        x2_entry = ttk.Entry(end_frame, width=8)
        x2_entry.insert(0, str(wire['x2']))
        x2_entry.pack(side=tk.LEFT, padx=(0, 5))
        
        y2_entry = ttk.Entry(end_frame, width=8)
        y2_entry.insert(0, str(wire['y2']))
        y2_entry.pack(side=tk.LEFT)
        
        # Conexões
        ttk.Label(main_frame, text="Conexões:", font=("Arial", 12, "bold")).grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=(20, 10))
        
        connections_text = tk.Text(main_frame, height=6, width=40)
        connections_text.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Preencher conexões existentes
        connections_info = ""
        for conn in wire.get('connections', []):
            connections_info += f"Componente: {conn['component']}, Terminal: {conn['terminal']}\n"
        
        if connections_info:
            connections_text.insert(tk.END, connections_info)
        else:
            connections_text.insert(tk.END, "Nenhuma conexão")
        
        connections_text.config(state=tk.DISABLED)
        
        # Botões
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=20)
        
        def save_changes():
            try:
                # Atualizar coordenadas
                new_x1 = int(x1_entry.get())
                new_y1 = int(y1_entry.get())
                new_x2 = int(x2_entry.get())
                new_y2 = int(y2_entry.get())
                
                # Validar coordenadas
                if new_x1 < 0 or new_y1 < 0 or new_x2 < 0 or new_y2 < 0:
                    messagebox.showerror("Erro", "Coordenadas devem ser positivas!")
                    return
                
                # Atualizar wire
                wire['x1'] = new_x1
                wire['y1'] = new_y1
                wire['x2'] = new_x2
                wire['y2'] = new_y2
                
                # Redesenhar wire
                self.canvas_widget.redraw_wire(wire_name, new_x1, new_y1, new_x2, new_y2)
                
                edit_window.destroy()
                messagebox.showinfo("Sucesso", "Propriedades do wire atualizadas!")
                
            except ValueError:
                messagebox.showerror("Erro", "Coordenadas devem ser números inteiros!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao atualizar: {str(e)}")
        
        def delete_wire():
            if messagebox.askyesno("Confirmar", f"Deseja deletar o wire {wire_name}?"):
                self.delete_wire(wire_name)
                edit_window.destroy()
                messagebox.showinfo("Sucesso", f"Wire {wire_name} deletado!")
        
        def cancel_changes():
            edit_window.destroy()
        
        ttk.Button(button_frame, text="Salvar", command=save_changes).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Deletar", command=delete_wire).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancelar", command=cancel_changes).pack(side=tk.LEFT, padx=5)
    
    def delete_wire(self, wire_name: str) -> None:
        """Deleta um wire do circuito"""
        if wire_name in self.nodes and self.nodes[wire_name]['type'] == 'wire':
            # Remover do canvas
            canvas = self.canvas_widget.get_canvas()
            canvas.delete(f"wire_{wire_name}")
            
            # Remover dos nós
            del self.nodes[wire_name]
            
            # Limpar seleção se necessário
            if self.selected_node == wire_name:
                self.selected_node = None
    
    def get_terminal_at(self, x: int, y: int) -> Optional[str]:
        """Retorna o nome do terminal (nó ou wire) mais próximo de uma posição"""
        for node_name, node_data in self.nodes.items():
            if node_data['type'] == 'wire':
                # Para wires, verificar se o ponto está próximo da linha
                if self.point_near_line(x, y, node_data['x1'], node_data['y1'], 
                                      node_data['x2'], node_data['y2'], 5):
                    return node_name
            else:
                # Para nós normais, verificar distância dos terminais
                if abs(node_data['x'] - x) <= 5 and abs(node_data['y'] - y) <= 5:
                    return node_name
        return None
    
    

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
        """Encontra um nó ou wire na posição especificada com tolerância"""
        for node_name, node_data in self.nodes.items():
            if node_data['type'] == 'wire':
                # Para wires, verificar se o ponto está próximo da linha
                if self.point_near_line(x, y, node_data['x1'], node_data['y1'], 
                                      node_data['x2'], node_data['y2'], tolerance):
                    return node_name
            else:
                # Para nós normais, verificar distância do ponto
                if (abs(node_data['x'] - x) <= tolerance and 
                    abs(node_data['y'] - y) <= tolerance):
                    return node_name
        return None
    
    def get_node(self, node_name: str) -> Optional[Dict[str, Any]]:
        """Retorna os dados de um nó"""
        return self.nodes.get(node_name)
    
    def get_all_nodes(self) -> Dict[str, Dict[str, Any]]:
        """Retorna todos os nós e wires"""
        return self.nodes.copy()
    
    def get_wires(self) -> Dict[str, Dict[str, Any]]:
        """Retorna apenas os wires do circuito"""
        return {name: data for name, data in self.nodes.items() if data['type'] == 'wire'}
    
    def get_nodes(self) -> Dict[str, Dict[str, Any]]:
        """Retorna apenas os nós (não wires) do circuito"""
        return {name: data for name, data in self.nodes.items() if data['type'] != 'wire'}
    
    def clear_nodes(self) -> None:
        """Limpa todos os nós e wires"""
        self.nodes.clear()
        self.selected_node = None
        self.node_editing_mode = False
        self.editing_node = None
        self.clear_temp_lines()
        
        # Limpar modo de edição de wire
        self.wire_editing_mode = False
        self.editing_wire = None
        self.wire_connection_start = None
    
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

    def update_wire_positions_for_component(self, component_name: str, offset_x: int, offset_y: int) -> None:
        """Atualiza as posições dos wires conectados a um componente quando ele é movido"""
        # Encontrar todos os wires que estão conectados a este componente
        offset_x = offset_x/2
        offset_y = offset_y/2
        for wire_name, wire_data in self.nodes.items():
            if wire_data['type'] == 'wire':
                connections = wire_data.get('connections', [])
                
                for connection in connections:
                    if connection['component'] == component_name:
                        # Este wire está conectado ao componente
                        terminal_index = connection['terminal']
                        
                        # Determinar qual terminal do wire mover baseado no índice
                        if terminal_index == 0:
                            # Terminal 1 (x1, y1)
                            wire_data['x1'] += offset_x
                            wire_data['y1'] += offset_y
                        elif terminal_index == 1:
                            # Terminal 2 (x2, y2)
                            wire_data['x2'] += offset_x
                            wire_data['y2'] += offset_y
                        
                        # Redesenhar o wire com as novas coordenadas
                        self.canvas_widget.redraw_wire(wire_name, wire_data['x1'], wire_data['y1'], 
                                                     wire_data['x2'], wire_data['y2'])
