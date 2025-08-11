import tkinter as tk
from tkinter import ttk
from typing import Callable, Any, Optional

class UIComponents:
    """Gerencia a interface de usuário"""
    
    def __init__(self, parent_frame: ttk.Frame) -> None:
        self.parent_frame = parent_frame
        self.info_text: Optional[tk.Text] = None
        self.setup_ui()
    
    def setup_ui(self) -> None:
        """Configura a interface de usuário"""
        # Frame esquerdo - Controles
        self.left_frame: ttk.Frame = ttk.Frame(self.parent_frame, width=300)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # Título
        title_label: ttk.Label = ttk.Label(self.left_frame, text="Simulador de Circuitos", font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Seção de componentes
        self.setup_components_section()
        
        # Seção de conexões
        self.setup_connections_section()
        
        # Seção de análise
        self.setup_analysis_section()
        
        # Seção de informações
        self.setup_info_section()
    
    def setup_components_section(self) -> None:
        """Configura a seção de componentes"""
        components_frame: ttk.LabelFrame = ttk.LabelFrame(self.left_frame, text="Componentes", padding=10)
        components_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Botões de componentes serão adicionados dinamicamente
        self.components_frame = components_frame
    
    def setup_connections_section(self) -> None:
        """Configura a seção de conexões"""
        connections_frame: ttk.LabelFrame = ttk.LabelFrame(self.left_frame, text="Conexões", padding=10)
        connections_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Botões de conexões serão adicionados dinamicamente
        self.connections_frame = connections_frame
    
    def setup_analysis_section(self) -> None:
        """Configura a seção de análise"""
        analysis_frame: ttk.LabelFrame = ttk.LabelFrame(self.left_frame, text="Análise", padding=10)
        analysis_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Botões de análise serão adicionados dinamicamente
        self.analysis_frame = analysis_frame
    
    def setup_info_section(self) -> None:
        """Configura a seção de informações"""
        info_frame: ttk.LabelFrame = ttk.LabelFrame(self.left_frame, text="Informações", padding=10)
        info_frame.pack(fill=tk.X)
        
        self.info_text: tk.Text = tk.Text(info_frame, height=10, width=35)
        self.info_text.pack(fill=tk.BOTH, expand=True)
    
    def add_component_button(self, text: str, command: Callable[[], Any]) -> None:
        """Adiciona um botão de componente"""
        ttk.Button(self.components_frame, text=text, command=command).pack(fill=tk.X, pady=2)
    
    def add_connection_button(self, text: str, command: Callable[[], Any]) -> None:
        """Adiciona um botão de conexão"""
        ttk.Button(self.connections_frame, text=text, command=command).pack(fill=tk.X, pady=2)
    
    def add_analysis_button(self, text: str, command: Callable[[], Any]) -> None:
        """Adiciona um botão de análise"""
        ttk.Button(self.analysis_frame, text=text, command=command).pack(fill=tk.X, pady=2)
    
    def update_info(self, info: str) -> None:
        """Atualiza as informações na área de texto"""
        if self.info_text:
            self.info_text.delete(1.0, tk.END)
            self.info_text.insert(tk.END, info)
    
    def get_info_text(self) -> Optional[tk.Text]:
        """Retorna o widget de texto de informações"""
        return self.info_text
    
    def get_left_frame(self) -> ttk.Frame:
        """Retorna o frame esquerdo"""
        return self.left_frame

