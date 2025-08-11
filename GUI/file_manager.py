import json
import tkinter as tk
from tkinter import filedialog, messagebox
from typing import Dict, Any, Optional, Tuple

class FileManager:
    """Gerencia salvamento e carregamento de circuitos"""
    
    def __init__(self) -> None:
        pass
    
    def save_circuit(self, nodes: Dict[str, Dict[str, Any]], components: Dict[str, Dict[str, Any]]) -> bool:
        """Salva o circuito em um arquivo JSON"""
        try:
            filename: Optional[str] = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            if filename:
                circuit_data: Dict[str, Any] = {
                    'nodes': nodes,
                    'components': components
                }
                
                with open(filename, 'w') as f:
                    json.dump(circuit_data, f, indent=2)
                
                messagebox.showinfo("Sucesso", f"Circuito salvo em {filename}")
                return True
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar circuito: {str(e)}")
            return False
        
        return False
    
    def load_circuit(self) -> Optional[Tuple[Dict[str, Dict[str, Any]], Dict[str, Dict[str, Any]]]]:
        """Carrega um circuito de um arquivo JSON"""
        try:
            filename: Optional[str] = filedialog.askopenfilename(
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            if filename:
                with open(filename, 'r') as f:
                    circuit_data: Dict[str, Any] = json.load(f)
                
                # Validar estrutura do arquivo
                if 'nodes' not in circuit_data or 'components' not in circuit_data:
                    messagebox.showerror("Erro", "Arquivo de circuito inválido")
                    return None
                
                nodes = circuit_data['nodes']
                components = circuit_data['components']
                
                messagebox.showinfo("Sucesso", f"Circuito carregado de {filename}")
                return nodes, components
                
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar circuito: {str(e)}")
            return None
        
        return None
    
    def export_circuit_data(self, nodes: Dict[str, Dict[str, Any]], components: Dict[str, Dict[str, Any]]) -> str:
        """Exporta os dados do circuito como string JSON"""
        circuit_data: Dict[str, Any] = {
            'nodes': nodes,
            'components': components
        }
        return json.dumps(circuit_data, indent=2)
    
    def import_circuit_data(self, json_string: str) -> Optional[Tuple[Dict[str, Dict[str, Any]], Dict[str, Dict[str, Any]]]]:
        """Importa dados do circuito de uma string JSON"""
        try:
            circuit_data: Dict[str, Any] = json.loads(json_string)
            
            # Validar estrutura
            if 'nodes' not in circuit_data or 'components' not in circuit_data:
                return None
            
            return circuit_data['nodes'], circuit_data['components']
            
        except json.JSONDecodeError:
            return None
        except Exception:
            return None

