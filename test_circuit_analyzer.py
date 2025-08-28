#!/usr/bin/env python3
"""
Teste do CircuitAnalyzer para verificar se está funcionando corretamente
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from GUI.circuit_analyzer import CircuitAnalyzer
from Circuit import Circuit, Node, Resistor, IndependentTensionSource, IndependentCurrentSource

def test_simple_circuit():
    """Testa um circuito simples com resistor e fonte de tensão"""
    print("Testando circuito simples...")
    
    # Criar circuito manualmente
    circuit = Circuit()
    
    # Criar nós
    node1 = Node(circuit, name="N1")
    node2 = Node(circuit, name="N2")
    gnd = Node(circuit, gnd=True, name="GND")
    
    # Conectar GND ao N2
    gnd.v = 0.0
    gnd.solved = True
    
    # Criar componentes
    resistor = Resistor(10.0, node1, node2, name="R1")
    voltage_source = IndependentTensionSource(5.0, node1, gnd, name="V1")
    
    print("Circuito criado:")
    print(f"Nós: {[n.name for n in circuit.get_nodes()]}")
    print(f"Componentes: {[c.name for c in circuit.get_nodes() if hasattr(c, 'name')]}")
    
    # Testar análise nodal
    try:
        from Circuit.NodalAnalyzer import NodalAnalyzer
        analyzer = NodalAnalyzer(circuit)
        equations, aux_eqs = analyzer.get_conductances_matrix()
        
        print("\nEquações nodais:")
        for i, eq in enumerate(equations):
            if eq:
                print(f"Eq {i+1}: {eq}")
        
        print("\nEquações auxiliares:")
        for i, eq in enumerate(aux_eqs):
            if eq:
                print(f"Aux {i+1}: {eq}")
                
        return equations, aux_eqs
        
    except Exception as e:
        print(f"Erro na análise: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_circuit_analyzer():
    """Testa o CircuitAnalyzer da GUI"""
    print("\nTestando CircuitAnalyzer da GUI...")
    
    analyzer = CircuitAnalyzer()
    
    # Dados simulados de um circuito
    nodes = {
        "W1": {"type": "wire", "node": "N1", "x1": 100, "y1": 100, "x2": 200, "y2": 100},
        "W2": {"type": "wire", "node": "N2", "x1": 200, "y1": 100, "x2": 300, "y2": 100},
        "W3": {"type": "wire", "node": "GND", "x1": 300, "y1": 100, "x2": 300, "y2": 200}
    }
    
    components = {
        "R1": {
            "type": "resistor",
            "value": 10.0,
            "connections": [
                {"wire": "W1", "terminal": 1},
                {"wire": "W2", "terminal": 1}
            ]
        },
        "V1": {
            "type": "voltage_source",
            "value": 5.0,
            "connections": [
                {"wire": "W1", "terminal": 1},
                {"wire": "W3", "terminal": 1}
            ]
        }
    }
    
    try:
        solution = analyzer.solve_circuit(nodes, components)
        if solution:
            print("Circuito resolvido com sucesso!")
            equations, aux_eqs = solution
            print(f"Número de equações nodais: {len(equations)}")
            print(f"Número de equações auxiliares: {len(aux_eqs)}")
        else:
            print("Falha ao resolver circuito")
            
    except Exception as e:
        print(f"Erro no CircuitAnalyzer: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("=== Teste do CircuitAnalyzer ===\n")
    
    # Teste 1: Circuito manual
    result1 = test_simple_circuit()
    
    # Teste 2: CircuitAnalyzer da GUI
    test_circuit_analyzer()
    
    print("\n=== Teste concluído ===")
