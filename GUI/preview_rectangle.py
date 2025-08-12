import tkinter as tk
from typing import TYPE_CHECKING, Optional
import math

if TYPE_CHECKING:
    from .canvas_widget import CircuitCanvas

class PreviewRectangle:
    def __init__(self, canvas: 'CircuitCanvas') -> None:
      self.canvas: 'CircuitCanvas' = canvas
      self.preview_id: Optional[int] = None
      self.visibility: bool = False
      self.current_rotation: int = 0
      self.current_component_type: str = ""

    def hide(self) -> None:
      if self.preview_id is not None:
        self.canvas.get_canvas().delete(self.preview_id)
        self.visibility = False
        self.preview_id = None
        self.current_rotation = 0
        self.current_component_type = ""

    def set_preview_id(self, preview_id: int) -> None:
      self.preview_id = preview_id

    def update(self, component_type: str, x: int, y: int) -> None:
      if self.preview_id is None:
        self.preview_id = self.canvas.create_preview_rectangle(component_type, x, y, self.current_rotation)
        self.visibility = True
        self.current_component_type = component_type
      else:
        self.canvas.update_preview_rectangle(self.preview_id, component_type, x, y, self.current_rotation)
    
    def rotate(self) -> None:
        """Rotaciona o preview em 90 graus"""
        self.current_rotation = (self.current_rotation + 90) % 360
        
        # Se já existe um preview, atualizar com nova rotação
        if self.preview_id is not None and self.current_component_type:
            # Obter posição atual do preview
            canvas = self.canvas.get_canvas()
            coords = canvas.coords(self.preview_id)
            if len(coords) >= 4:
                x = coords[0]
                y = coords[1]
                # Recriar o preview com nova rotação
                canvas.delete(self.preview_id)
                self.preview_id = self.canvas.create_preview_rectangle(
                    self.current_component_type, x, y, self.current_rotation
                )
    
    def get_rotation(self) -> int:
        """Retorna a rotação atual do preview"""
        return self.current_rotation
    