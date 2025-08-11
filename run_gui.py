#!/usr/bin/env python3
"""
Script principal para executar o simulador de circuitos
"""

import tkinter as tk
import sys
import os

# Adicionar o diretório atual ao path para importar os módulos
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from GUI.circuit_gui_main import CircuitGUIMain

def main() -> None:
    root: tk.Tk = tk.Tk()
    app: CircuitGUIMain = CircuitGUIMain(root)
    root.mainloop()

if __name__ == "__main__":
    main() 