import tkinter as tk
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .canvas_widget import CircuitCanvas

class PreviewRectangle:
    def __init__(self, canvas: 'CircuitCanvas') -> None:
      self.canvas: 'CircuitCanvas' = canvas
      self.preview_id: Optional[int] = None
      self.visibility: bool = False

    def hide(self) -> None:
      if self.preview_id is not None:
        self.canvas.get_canvas().delete(self.preview_id)
        self.visibility = False
        self.preview_id = None

    def set_preview_id(self, preview_id: int) -> None:
      self.preview_id = preview_id

    def update(self, component_type: str, x: int, y: int) -> None:
      if self.preview_id is None:
        self.preview_id = self.canvas.create_preview_rectangle(component_type, x, y)
        self.visibility = True
      else:
        self.canvas.update_preview_rectangle(self.preview_id, component_type, x, y)
    