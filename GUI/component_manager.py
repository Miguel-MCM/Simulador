import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from typing import Dict, Any, Optional, Tuple, List
from .canvas_widget import CircuitCanvas

class ComponentManager:
    """Gerencia todos os componentes do circuito"""
    
    def __init__(self, canvas_widget: CircuitCanvas) -> None:
        self.canvas_widget = canvas_widget
        self.components: Dict[str, Dict[str, Any]] = {}
        self.selected_component: Optional[str] = None
    
    def add_resistor(self, x: int, y: int, connection_points: List[Dict[str, Any]], rotation: int = 0) -> str:
        """Adiciona um resistor ao circuito"""
        # Gerar nome automático para o resistor
        resistor_count = 1
        while f"R_{resistor_count}" in self.components:
            resistor_count += 1
        
        name = f"R_{resistor_count}"
        
        # Adicionar o resistor ao circuito
        self.components[name] = {
            'type': 'resistor',
            'value': 1.0,  # Valor padrão
            'connections': connection_points,
            'x': x,
            'y': y,
            'rotation': rotation,  # Rotação em graus (0, 90, 180, 270)
            'canvas_id': None
        }
        
        # Desenhar o componente
        self.canvas_widget.draw_component(name, x, y, self.components[name])
        
        return name
    
    def add_voltage_source(self, x: int, y: int, connection_points: List[Dict[str, Any]], rotation: int = 0) -> Optional[str]:
        """Adiciona uma fonte de tensão ao circuito"""
        # Gerar nome automático para o resistor
        voltage_source_count = 1
        while f"S_{voltage_source_count}" in self.components:
            voltage_source_count += 1
        
        name = f"S_{voltage_source_count}"
        
        # Adicionar a fonte de tensão ao circuito
        self.components[name] = {
            'type': 'voltage_source',
            'value': 1.0,  # Valor padrão
            'connections': connection_points,
            'x': x,
            'y': y,
            'rotation': rotation,  # Rotação em graus (0, 90, 180, 270)
            'canvas_id': None
        }
        
        # Desenhar o componente
        self.canvas_widget.draw_component(name, x, y, self.components[name])
        
        return name
    
    def add_current_source(self, x: int, y: int, connection_points: List[Dict[str, Any]], rotation: int = 0) -> Optional[str]:
        """Adiciona uma fonte de corrente ao circuito"""
        # Gerar nome automático para o resistor
        current_source_count = 1
        while f"S_{current_source_count}" in self.components:
            current_source_count += 1
        
        name = f"S_{current_source_count}"
        
        # Adicionar a fonte de corrente ao circuito
        self.components[name] = {
            'type': 'current_source',
            'value': 1.0,  # Valor padrão
            'connections': connection_points,
            'x': x,
            'y': y,
            'rotation': rotation,
            'canvas_id': None
        }
        
        # Desenhar o componente
        self.canvas_widget.draw_component(name, x, y, self.components[name])
        
        return name
    
    def add_current_dependent_current_source(self, x: int, y: int, connection_points: List[Dict[str, Any]], rotation: int = 0) -> Optional[str]:
        """Adiciona uma fonte de corrente dependente ao circuito"""
        # Gerar nome automático para o resistor
        current_dependent_current_source_count = 1
        while f"S_{current_dependent_current_source_count}" in self.components:
            current_dependent_current_source_count += 1
        
        name = f"S_{current_dependent_current_source_count}"
        
        # Adicionar a fonte de corrente dependente ao circuito
        self.components[name] = {
            'type': 'current_dependent_current_source',
            'value': 0,  # Valor padrão
            'connections': connection_points,
            'x': x,
            'y': y,
            'rotation': rotation,
            'canvas_id': None,
            'component_current': None,
        }
        
        # Desenhar o componente
        self.canvas_widget.draw_component(name, x, y, self.components[name])
        
        return name
    
    def add_ground(self, x: int, y: int, rotation: int = 0, wire_name: str = None) -> str:
        """Adiciona um ground ao circuito"""
        # Gerar nome automático para o ground
        ground_count = 1
        while f"GND_{ground_count}" in self.components:
            ground_count += 1
        
        name = f"GND_{ground_count}"
        terminals = self.canvas_widget.get_component_terminals('ground', 0)
        
        # Adicionar o ground ao circuito
        self.components[name] = {
            'type': 'ground',
            'value': 0.0,  # Ground sempre tem potencial 0V
            'connections': [{'x': x + terminals[0]['x'], 'y': y + terminals[0]['y'], 'wire': wire_name}],  # Terminal único no centro superior
            'x': x,
            'y': y,
            'rotation': rotation,
            'canvas_id': None
        }
        
        # Desenhar o componente
        self.canvas_widget.draw_component(name, x, y, self.components[name])
        
        return name
    
    def add_current_dependent_tension_source(self, x: int, y: int, connection_points: List[Dict[str, Any]], rotation: int = 0) -> Optional[str]:
        """Adiciona uma fonte de tensão dependente ao circuito"""
        # Gerar nome automático para a fonte
        current_dependent_tension_source_count = 1
        while f"S_{current_dependent_tension_source_count}" in self.components:
            current_dependent_tension_source_count += 1
        
        name = f"S_{current_dependent_tension_source_count}"
        
        # Adicionar a fonte de tensão dependente ao circuito
        self.components[name] = {
            'type': 'current_dependent_tension_source',
            'value': 0,  # Valor padrão
            'connections': connection_points,
            'x': x,
            'y': y,
            'rotation': rotation,
            'canvas_id': None,
            'component_current': None,
        }
        
        # Desenhar o componente
        self.canvas_widget.draw_component(name, x, y, self.components[name])
        
        return name
    
    def add_tension_dependent_current_source(self, x: int, y: int, connection_points: List[Dict[str, Any]], rotation: int = 0) -> Optional[str]:
        """Adiciona uma fonte de corrente dependente de tensão ao circuito"""
        # Gerar nome automático para a fonte
        tension_dependent_current_source_count = 1
        while f"S_{tension_dependent_current_source_count}" in self.components:
            tension_dependent_current_source_count += 1
        
        name = f"S_{tension_dependent_current_source_count}"
        
        # Adicionar a fonte de corrente dependente de tensão ao circuito
        self.components[name] = {
            'type': 'tension_dependent_current_source',
            'value': 0,  # Valor padrão
            'connections': connection_points,
            'x': x,
            'y': y,
            'rotation': rotation,
            'canvas_id': None,
            'tension_nodes': None,  # Tupla de nomes de nós (nó1, nó2) ou None
        }
        
        # Desenhar o componente
        self.canvas_widget.draw_component(name, x, y, self.components[name])
        
        return name
    
    def add_tension_dependent_tension_source(self, x: int, y: int, connection_points: List[Dict[str, Any]], rotation: int = 0) -> Optional[str]:
        """Adiciona uma fonte de tensão dependente de tensão ao circuito"""
        # Gerar nome automático para a fonte
        tension_dependent_tension_source_count = 1
        while f"S_{tension_dependent_tension_source_count}" in self.components:
            tension_dependent_tension_source_count += 1
        
        name = f"S_{tension_dependent_tension_source_count}"
        
        # Adicionar a fonte de tensão dependente de tensão ao circuito
        self.components[name] = {
            'type': 'tension_dependent_tension_source',
            'value': 0,  # Valor padrão
            'connections': connection_points,
            'x': x,
            'y': y,
            'rotation': rotation,
            'canvas_id': None,
            'tension_nodes': None,  # Tupla de nomes de nós (nó1, nó2) ou None
        }
        
        # Desenhar o componente
        self.canvas_widget.draw_component(name, x, y, self.components[name])
        
        return name
    
    def connect_component_to_node(self, component_name: str, node_name: str) -> bool:
        """Conecta um componente a um nó"""
        if component_name in self.components:
            component: Dict[str, Any] = self.components[component_name]
            
            if component['node1'] is None:
                component['node1'] = node_name
                return True
            elif component['node2'] is None:
                component['node2'] = node_name
                return True
        
        return False
    
    def get_component(self, component_name: str) -> Optional[Dict[str, Any]]:
        """Retorna os dados de um componente"""
        return self.components.get(component_name)
    
    def get_all_components(self) -> Dict[str, Dict[str, Any]]:
        """Retorna todos os componentes"""
        return self.components.copy()
    
    def clear_components(self) -> None:
        """Limpa todos os componentes"""
        self.components.clear()
        self.selected_component = None
    
    def set_selected_component(self, component_name: Optional[str]) -> None:
        """Define o componente selecionado"""
        self.selected_component = component_name
    
    def get_selected_component(self) -> Optional[str]:
        """Retorna o componente selecionado"""
        return self.selected_component
    
    def edit_component_properties(self, component_name: str, parent_window: tk.Tk) -> None:
        """Edita as propriedades de um componente"""
        if component_name not in self.components or self.components[component_name]['type'] == 'ground':
            return
        
        component = self.components[component_name]
        
        # Criar janela de edição
        edit_window = tk.Toplevel(parent_window)
        edit_window.title(f"Editar {component_name}")
        
        # Ajustar tamanho da janela baseado no tipo de componente
        if component['type'] in ['current_dependent_current_source', 'current_dependent_tension_source', 
                                'tension_dependent_current_source', 'tension_dependent_tension_source']:
            edit_window.geometry("400x350")
        else:
            edit_window.geometry("300x200")
            
        edit_window.transient(parent_window)
        edit_window.grab_set()
        
        # Frame principal
        main_frame = ttk.Frame(edit_window, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Nome do componente
        ttk.Label(main_frame, text="Nome:").grid(row=0, column=0, sticky=tk.W, pady=5)
        name_entry = ttk.Entry(main_frame, width=20)
        name_entry.insert(0, component_name)
        name_entry.grid(row=0, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Valor do componente
        ttk.Label(main_frame, text="Valor:").grid(row=1, column=0, sticky=tk.W, pady=5)
        value_entry = ttk.Entry(main_frame, width=20)
        value_entry.insert(0, str(component['value']))
        value_entry.grid(row=1, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Unidade baseada no tipo
        unit = "Ω" if component['type'] == 'resistor' else "V" if component['type'] == 'voltage_source' else "A"
        ttk.Label(main_frame, text=f"({unit})").grid(row=1, column=2, sticky=tk.W, pady=5, padx=(5, 0))
        
        # Campo para seleção do componente dependente (apenas para fontes dependentes de corrente)
        if component['type'] in ['current_dependent_current_source', 'current_dependent_tension_source']:
            ttk.Label(main_frame, text="Componente dependente:").grid(row=2, column=0, sticky=tk.W, pady=5)
            
            # Lista de componentes disponíveis (excluindo o próprio e grounds)
            available_components = []
            for comp_name, comp_data in self.components.items():
                if (comp_name != component_name and 
                    comp_data['type'] not in ['ground', 'current_dependent_current_source', 'current_dependent_tension_source',
                                            'tension_dependent_current_source', 'tension_dependent_tension_source']):
                    available_components.append(comp_name)
            
            # Combobox para seleção do componente
            component_var = tk.StringVar()
            if component.get('component_current') in available_components:
                component_var.set(component['component_current'])
            elif available_components:
                component_var.set(available_components[0])
            
            component_combo = ttk.Combobox(main_frame, textvariable=component_var, values=available_components, state="readonly", width=20)
            component_combo.grid(row=2, column=1, sticky=tk.W, pady=5, padx=(10, 0))
            
            # Mensagem de ajuda
            help_text = "Selecione o componente cuja corrente a fonte depende"
            ttk.Label(main_frame, text=help_text, font=("Arial", 8), foreground="gray").grid(
                row=3, column=0, columnspan=3, sticky=tk.W, pady=(0, 10)
            )
        
        # Campo para seleção de nós (apenas para fontes dependentes de tensão)
        if component['type'] in ['tension_dependent_current_source', 'tension_dependent_tension_source']:
            # Nomear todos os nós antes de editar
            if hasattr(self.canvas_widget, 'circuit_gui') and self.canvas_widget.circuit_gui:
                if hasattr(self.canvas_widget.circuit_gui, 'node_manager'):
                    self.canvas_widget.circuit_gui.node_manager.name_all_nodes()
            
            ttk.Label(main_frame, text="Nó 1:").grid(row=2, column=0, sticky=tk.W, pady=5)
            ttk.Label(main_frame, text="Nó 2:").grid(row=3, column=0, sticky=tk.W, pady=5)
            
            # Obter lista de nós disponíveis
            available_nodes = []
            if hasattr(self.canvas_widget, 'circuit_gui') and self.canvas_widget.circuit_gui:
                if hasattr(self.canvas_widget.circuit_gui, 'node_manager'):
                    nodes = self.canvas_widget.circuit_gui.node_manager.get_all_nodes()
                    for node_name, node_data in nodes.items():
                        if node_data['type'] == 'node':  # Apenas nós, não wires
                            available_nodes.append(node_name.split('_', 1)[1])
            
            # Comboboxes para seleção dos nós
            node1_var = tk.StringVar()
            node2_var = tk.StringVar()
            
            # Definir valores iniciais
            if component.get('tension_nodes') and len(component['tension_nodes']) == 2:
                node1_var.set(component['tension_nodes'][0])
                node2_var.set(component['tension_nodes'][1])
            elif available_nodes:
                if len(available_nodes) >= 2:
                    node1_var.set(available_nodes[0])
                    node2_var.set(available_nodes[1])
                elif len(available_nodes) == 1:
                    node1_var.set(available_nodes[0])
                    node2_var.set(available_nodes[0])
            
            node1_combo = ttk.Combobox(main_frame, textvariable=node1_var, values=available_nodes, state="readonly", width=20)
            node1_combo.grid(row=2, column=1, sticky=tk.W, pady=5, padx=(10, 0))
            
            node2_combo = ttk.Combobox(main_frame, textvariable=node2_var, values=available_nodes, state="readonly", width=20)
            node2_combo.grid(row=3, column=1, sticky=tk.W, pady=5, padx=(10, 0))
            
            # Mensagem de ajuda
            help_text = "Selecione os nós entre os quais a tensão será medida"
            ttk.Label(main_frame, text=help_text, font=("Arial", 8), foreground="gray").grid(
                row=4, column=0, columnspan=3, sticky=tk.W, pady=(0, 10)
            )
        
        # Botões
        button_frame = ttk.Frame(main_frame)
        if component['type'] in ['current_dependent_current_source', 'current_dependent_tension_source']:
            button_frame.grid(row=4, column=0, columnspan=3, pady=20)
        elif component['type'] in ['tension_dependent_current_source', 'tension_dependent_tension_source']:
            button_frame.grid(row=5, column=0, columnspan=3, pady=20)
        else:
            button_frame.grid(row=2, column=0, columnspan=3, pady=20)
        
        def save_changes():
            try:
                new_name = name_entry.get().strip()
                new_value = float(value_entry.get())
                
                if new_name != component_name and new_name in self.components:
                    messagebox.showerror("Erro", "Nome já existe!")
                    return
                
                if new_name == "":  # Allow empty name for new components
                    new_name = component_name
                
                if component['type'] == 'resistor' and new_value <= 0:
                    messagebox.showerror("Erro", "Valor deve ser maior que zero!")
                    return
                
                # Atualizar nome se mudou
                if new_name != component_name:
                    # Remover componente antigo
                    old_component = self.components.pop(component_name)
                    # Adicionar com novo nome
                    self.components[new_name] = old_component
                    # Atualizar canvas
                    self.canvas_widget.rename_component(component_name, new_name, old_component)
                
                # Atualizar valor
                self.components[new_name]['value'] = new_value
                
                # Atualizar componente dependente se for fonte dependente de corrente
                if component['type'] in ['current_dependent_current_source', 'current_dependent_tension_source']:
                    selected_component = component_var.get()
                    if selected_component:
                        self.components[new_name]['component_current'] = selected_component
                
                # Atualizar nós dependentes se for fonte dependente de tensão
                if component['type'] in ['tension_dependent_current_source', 'tension_dependent_tension_source']:
                    selected_node1 = node1_var.get()
                    selected_node2 = node2_var.get()
                    if selected_node1 and selected_node2:
                        self.components[new_name]['tension_nodes'] = (selected_node1, selected_node2)
                
                # Atualizar canvas
                self.canvas_widget.update_component_value(new_name, new_value, self.components[new_name])
                
                edit_window.destroy()
                
            except ValueError:
                messagebox.showerror("Erro", "Valor inválido!")
        
        def cancel_changes():
            edit_window.destroy()
        
        ttk.Button(button_frame, text="Salvar", command=save_changes).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancelar", command=cancel_changes).pack(side=tk.LEFT, padx=5)

    def update_component_position(self, component_name: str, new_x: int, new_y: int) -> None:
        """Atualiza a posição de um componente e recalcula as posições dos terminais"""
        if component_name not in self.components:
            return
        
        component = self.components[component_name]
        old_x = component['x']
        old_y = component['y']
        
        # Calcular offset de movimento
        offset_x = new_x - old_x
        offset_y = new_y - old_y
        
        # Atualizar posição do componente
        component['x'] = new_x
        component['y'] = new_y
        
        # Atualizar posições dos terminais se existirem
        if 'connections' in component:
            for terminal in component['connections']:
                terminal['x'] += offset_x
                terminal['y'] += offset_y
