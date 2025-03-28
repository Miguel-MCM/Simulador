import Circuit
import pytest

def test_independent_current_source():
    circuit = Circuit.Circuit()
    gnd = Circuit.Node(circuit, gnd=True)
    n1 = Circuit.Node(circuit, name="Node1")
    src = Circuit.IndependentCurrentSource(10, gnd, n1, name="Src")
    r1 = Circuit.Resistor(5, gnd, n1, name="R1")

    assert circuit.solve()[n1] == 50, "Should be 50"
    assert r1.i == src.i == 10, "Current in all branches in the loop should be equal"

def test_independent_tension_source():
    circuit = Circuit.Circuit()
    gnd = Circuit.Node(circuit, gnd=True)
    n1 = Circuit.Node(circuit, name="Node1")
    src = Circuit.IndependentTensionSource(2, gnd, n1, name="Src")
    r1 = Circuit.Resistor(5, gnd, n1, name="R1")

    assert circuit.solve()[n1] == 2, "Should be 2"
    assert r1.i == -src.i == 2/5, "Current in all branches in the loop should be equal"
# Using Irwin Examples

# Example 3.1
def test_modified_nodal_Independent_current_sources_2nodes():
    circuit = Circuit.Circuit()
    gnd = Circuit.Node(circuit, gnd=True)
    v1 = Circuit.Node(circuit, name="V1")
    v2 = Circuit.Node(circuit, name="V2")

    src1 = Circuit.IndependentCurrentSource(1*(10**-3), gnd, v1, name="S1")
    src2 = Circuit.IndependentCurrentSource(4*(10**-3), v2, gnd, name="S2")
    
    r1 = Circuit.Resistor(12*(10**3), gnd, v1, name="R1")
    r2 = Circuit.Resistor(6*(10**3), v1, v2, name="R2")
    r3 = Circuit.Resistor(6*(10**3), v2, gnd, name="R3")

    solution = circuit.solve()
    assert abs(solution[v1] - (-6)) < 6/100
    assert abs(solution[v2] - (-15)) < 15/100
    assert abs(r1.i - 1/2*10**-3) < (1/2*10**-3)/100
    assert abs(r2.i - 3/2*10**-3) < (3/2*10**-3)/100
    assert abs(r3.i - 5/2*10**-3) < (5/2*10**-3)/100

# Example 3.2
def test_modified_nodal_Independent_current_sources_4nodes():
    circuit = Circuit.Circuit()
    gnd = Circuit.Node(circuit, gnd=True)
    v1 = Circuit.Node(circuit, name="V1")
    v2 = Circuit.Node(circuit, name="V2")
    v3 = Circuit.Node(circuit, name="V3")

    srcA = Circuit.IndependentCurrentSource(4*(10**-3), v1, v2, name="SA")
    srcB = Circuit.IndependentCurrentSource(2*(10**-3), v2, gnd, name="SB")
    
    r1 = Circuit.Resistor(2*(10**3), v1, v3, name="R1")
    r2 = Circuit.Resistor(2*(10**3), v1, gnd, name="R2")
    r3 = Circuit.Resistor(4*(10**3), v2, gnd, name="R3")
    r4 = Circuit.Resistor(4*(10**3), v2, v3, name="R4")
    r5 = Circuit.Resistor(1*(10**3), v3, gnd, name="R5")

    solution = circuit.solve()
    assert abs(solution[v1] - (-4.3636)) < 4.3636/100 , f'V1 = {solution[v1]}, Should be 4.3636'
    assert abs(solution[v2] - (3.6364)) < 3.6364/100 , f'V2 = {solution[v2]}, Should be 3.6364'
    assert abs(solution[v3] - (-0.7273)) < 0.7273/100 , f'V3 = {solution[v3]}, Should be -0.7273'

# Example 3.3
def test_modified_nodal_current_dependent_current_source():
    circuit = Circuit.Circuit()
    gnd = Circuit.Node(circuit, gnd=True)
    v1 = Circuit.Node(circuit, name="V1")
    v2 = Circuit.Node(circuit, name="V2")

    srcA = Circuit.IndependentCurrentSource(2*(10**-3), gnd, v2, name="SA")
    
    r1 = Circuit.Resistor(12*(10**3), v1, gnd, name="R1")
    r2 = Circuit.Resistor(6*(10**3), v1, v2, name="R2")
    r3 = Circuit.Resistor(3*(10**3), v2, gnd, name="R3")

    srcB = Circuit.CurrentDependentCurrentSource(2, v1, gnd, r3, v2, name="SB")

    solution = circuit.solve()
    assert abs(solution[v1] - (-4.8)) < 4.8/100 , f'V1 = {solution[v1]}, Should be -4.8'
    assert abs(solution[v2] - (2.4)) < 2.4/100 , f'V2 = {solution[v2]}, Should be 2.4'

# Example 3.4
def test_modified_nodal_tension_dependent_current_source():
    circuit = Circuit.Circuit()
    gnd = Circuit.Node(circuit, gnd=True)
    v1 = Circuit.Node(circuit, name="V1")
    v2 = Circuit.Node(circuit, name="V2")
    v3 = Circuit.Node(circuit, name="V3")

    srcA = Circuit.IndependentCurrentSource(2*(10**-3), v2, v1, name="SA")
    srcB = Circuit.IndependentCurrentSource(4*(10**-3), gnd, v3, name="SB")
    srcC = Circuit.TensionDependentCurrentSource(0.002, v2, gnd, v2, v3, name="SC")
    
    r1 = Circuit.Resistor(1*(10**3), v1, v2, name="R1")
    r2 = Circuit.Resistor(2*(10**3), v2, v3, name="R2")
    r3 = Circuit.Resistor(2*(10**3), v1, gnd, name="R3")
    r4 = Circuit.Resistor(4*(10**3), v3, gnd, name="R4")


    solution = circuit.solve()
    assert abs(solution[v1] - (8.5714)) < 8.5714/100 , f'V1 = {solution[v1]}, Should be 8.5714'
    assert abs(solution[v2] - (10.8571)) < 10.8571/100 , f'V2 = {solution[v2]}, Should be 10.8571'
    assert abs(solution[v3] - (12.5714)) < 12.5714/100 , f'V3 = {solution[v3]}, Should be -12.5714'

# Example 3.7
def test_modified_nodal_independent_tension_source():
    circuit = Circuit.Circuit()
    gnd = Circuit.Node(circuit, gnd=True)
    v1 = Circuit.Node(circuit, name="V1")
    v2 = Circuit.Node(circuit, name="V2")
    v3 = Circuit.Node(circuit, name="V3")
    v4 = Circuit.Node(circuit, name="V4")

    srcA = Circuit.IndependentTensionSource(6, v2, gnd, name="SA")
    srcB = Circuit.IndependentTensionSource(12, v3, v1, name="SB")
    srcC = Circuit.IndependentTensionSource(12, gnd, v4, name="SC")
    
    r1 = Circuit.Resistor(2*(10**3), v1, v2, name="R1")
    r2 = Circuit.Resistor(1*(10**3), v2, v3, name="R2")
    r3 = Circuit.Resistor(2*(10**3), v3, gnd, name="R3")
    r4 = Circuit.Resistor(1*(10**3), v3, v4, name="R4")
    r5 = Circuit.Resistor(2*(10**3), v4, v1, name="R5")


    solution = circuit.solve()
    assert abs(solution[v1] - (11.1429)) < 11.1429/100 , f'V1 = {solution[v1]}, Should be 11.1429'
    assert abs(solution[v2] - (-6)) < 6/100 , f'V2 = {solution[v2]}, Should be -6'
    assert abs(solution[v3] - (-0.857143)) < 0.857143/100 , f'V3 = {solution[v3]}, Should be -0.857143'
    assert abs(solution[v4] - (12)) < 12/100 , f'V3 = {solution[v3]}, Should be 12'

# Example 3.8
def test_modified_nodal_current_dependent_tension_source():
    circuit = Circuit.Circuit()
    gnd = Circuit.Node(circuit, gnd=True)
    v1 = Circuit.Node(circuit, name="V1")
    v2 = Circuit.Node(circuit, name="V2")

    srcA = Circuit.IndependentCurrentSource(4*(10**-3), gnd, v2, name="SA")
    
    r1 = Circuit.Resistor(2*(10**3), v1, gnd, name="R1")
    r2 = Circuit.Resistor(2*(10**3), v1, v2, name="R2")
    r3 = Circuit.Resistor(1*(10**3), v2, gnd, name="R3")

    srcB = Circuit.CurrentDependentTensionSource(2*1000, gnd, v1, r3, v2, name="SB")

    solution = circuit.solve()
    assert abs(solution[v1] - (16)) < 16/100 , f'V1 = {solution[v1]}, Should be 16'
    assert abs(solution[v2] - (8)) < 8/100 , f'V2 = {solution[v2]}, Should be 8'

# Example 3.11
def test_modified_nodal_tension_dependent_tension_source():
    circuit = Circuit.Circuit()
    gnd = Circuit.Node(circuit, gnd=True)
    v1 = Circuit.Node(circuit, name="V1")
    v2 = Circuit.Node(circuit, name="V2")
    v3 = Circuit.Node(circuit, name="V3")
    v4 = Circuit.Node(circuit, name="V4")
    v5 = Circuit.Node(circuit, name="V5")

    srcA = Circuit.IndependentTensionSource(12, gnd, v2, name="SA")
    srcB = Circuit.TensionDependentTensionSource(2, gnd, v3, v1, v2, name="SB")
    srcC = Circuit.IndependentTensionSource(6, v1, v4, name="SC")

    r1 = Circuit.Resistor(1*(10**3), v1, v2, name="R1")
    r2 = Circuit.Resistor(1*(10**3), v2, v3, name="R2")
    r3 = Circuit.Resistor(1*(10**3), v1, v3, name="R3")
    r4 = Circuit.Resistor(1*(10**3), v3, v4, name="R4")
    r5 = Circuit.Resistor(1*(10**3), v4, gnd, name="R5")
    r6 = Circuit.Resistor(1*(10**3), v4, v5, name="R6")
    r7 = Circuit.Resistor(1*(10**3), v5, gnd, name="R7")

    srcD = Circuit.CurrentDependentCurrentSource(2, v1, v5, r5, v4, name="SD")

    solution = circuit.solve()
    assert abs(solution[v1] - (-38)) < 38/100 , f'V1 = {solution[v1]}, Should be -38'
    assert abs(solution[v2] - (12)) < 12/100 , f'V1 = {solution[v1]}, Should be 12'
    assert abs(solution[v3] - (-100)) < 100/100 , f'V1 = {solution[v1]}, Should be -100'
    assert abs(solution[v4] - (-32)) < 32/100 , f'V2 = {solution[v2]}, Should be -32'
    assert abs(solution[v5] - (-48)) < 48/100 , f'V3 = {solution[v3]}, Should be -48'

def test_modified_nodal_resistance_in_short_circuit():
    circuit = Circuit.Circuit()
    gnd = Circuit.Node(circuit, gnd=True)
    v1 = Circuit.Node(circuit, name="V1")

    src = Circuit.IndependentTensionSource(3, gnd, v1, name="S")
    r1 = Circuit.Resistor(100, v1, v1, name="R1")
    r2 = Circuit.Resistor(10, v1, gnd, name="R2")

    solution = circuit.solve()
    assert abs(solution[v1] - 3) < 3/100,  f'V1 = {solution[v1]}, Should be 3'

def test_modified_nodal_tension_source_in_short_circuit():
    circuit = Circuit.Circuit()
    gnd = Circuit.Node(circuit, gnd=True)
    v1 = Circuit.Node(circuit, name="V1")

    with pytest.raises(Exception):
        src = Circuit.IndependentTensionSource(3, gnd, gnd, name="S")

    with pytest.raises(Exception) as e_info:
        src = Circuit.IndependentTensionSource(3, v1, v1, name="S")

def test_modified_nodal_current_source_in_short_circuit():
    circuit = Circuit.Circuit()
    gnd = Circuit.Node(circuit, gnd=True)
    v1 = Circuit.Node(circuit, name="V1")

    src = Circuit.IndependentCurrentSource(3, gnd, gnd, name="S")
    r1 = Circuit.Resistor(6, gnd, v1, name="R")

    solution = circuit.solve()
    assert solution[v1] == 0,  f'V1 = {solution[v1]}, Should be 0'

def test_modifed_nodal_resistor_in_open_circuit():
    circuit = Circuit.Circuit()
    gnd = Circuit.Node(circuit, gnd=True)
    v1 = Circuit.Node(circuit, name="V1")
    v2 = Circuit.Node(circuit, name="V2")

    src = Circuit.IndependentTensionSource(1, gnd, v1, name="S")
    r1 = Circuit.Resistor(2, v1, gnd, name="R1")
    r2 = Circuit.Resistor(1, v1, v2, name="R2")

    solution = circuit.solve()
    assert solution[v1] == solution[v2],  f'V1 = {solution[v1]}, Should be equal V2 = {solution[v2]}'

def test_modified_nodal_tension_source_in_open_circuit():
    circuit = Circuit.Circuit()
    gnd = Circuit.Node(circuit, gnd=True)
    v1 = Circuit.Node(circuit, name="V1")

    src = Circuit.IndependentTensionSource(1, gnd, v1, name="S")

    solution = circuit.solve()
    assert solution[v1] == 1,  f'V1 = {solution[v1]}, Should be 1'

def test_modified_nodal_current_source_in_open_circuit():
    circuit = Circuit.Circuit()
    gnd = Circuit.Node(circuit, gnd=True)
    v1 = Circuit.Node(circuit, name="V1")

    src = Circuit.IndependentCurrentSource(1, gnd, v1, name="S")

    with pytest.raises(Exception) as e_info:
        solution = circuit.solve()

def test_modified_nodal_unconected_node():
    circuit = Circuit.Circuit()
    gnd = Circuit.Node(circuit, gnd=True)
    v1 = Circuit.Node(circuit, name="V1")
    v2 = Circuit.Node(circuit, name="V2")

    src = Circuit.IndependentTensionSource(1, gnd, v1, name="S")
    r1 = Circuit.Resistor(2, v1, gnd, name="R1")

    with pytest.raises(Exception) as e_info:
        solution = circuit.solve()
