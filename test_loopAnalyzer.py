import Circuit
from Circuit.LoopAnalyzer import LoopAnalyzer
from Circuit.NodalAnalyzer import NodalAnalyzer

def case_1():
    print("case 1")
    """
    One loop: Tension source with two resistors (series)
    """
    circuit = Circuit.Circuit()
    gnd = Circuit.Node(circuit, gnd=True)
    v1 = Circuit.Node(circuit, name="V1")
    v2 = Circuit.Node(circuit, name="V2")
    vs = Circuit.IndependentTensionSource(12, gnd, v1, name="VS")
    r1 = Circuit.Resistor(4, v1, v2, name="R1")
    r2 = Circuit.Resistor(6, v2, gnd, name="R2")
    return circuit
    
def case_2():
    print("case 2")
    """
    Two loops: Current source with parallel/series resistors
    """
    circuit = Circuit.Circuit()
    gnd = Circuit.Node(circuit, gnd=True)
    v1 = Circuit.Node(circuit, name="V1")
    v2 = Circuit.Node(circuit, name="V2")
    isrc = Circuit.IndependentCurrentSource(2, gnd, v1, name="IS")
    r1 = Circuit.Resistor(3, v1, gnd, name="R1")
    r2 = Circuit.Resistor(5, v1, v2, name="R2")
    r3 = Circuit.Resistor(7, v2, gnd, name="R3")
    return circuit

def case_3():
    print("case 3")
    """
    Three loops: T-network with Tension source
    """
    circuit = Circuit.Circuit()
    gnd = Circuit.Node(circuit, gnd=True)
    v1 = Circuit.Node(circuit, name="V1")
    v2 = Circuit.Node(circuit, name="V2")
    v3 = Circuit.Node(circuit, name="V3")
    vs = Circuit.IndependentTensionSource(9, gnd, v1, name="VS")
    r1 = Circuit.Resistor(2, v1, v2, name="R1")
    r2 = Circuit.Resistor(3, v2, v3, name="R2")
    r3 = Circuit.Resistor(4, v3, gnd, name="R3")
    return circuit

def case_4():
    print("case 4")
    """
    Two loops with dependent source (CCCS)
    """
    circuit = Circuit.Circuit()
    gnd = Circuit.Node(circuit, gnd=True)
    v1 = Circuit.Node(circuit, name="V1")
    v2 = Circuit.Node(circuit, name="V2")
    vs = Circuit.IndependentTensionSource(5, gnd, v1, name="VS")
    r1 = Circuit.Resistor(1, v1, v2, name="R1")
    r2 = Circuit.Resistor(2, v2, gnd, name="R2")
    # Current-Dependent current source (gain=2)
    cccs = Circuit.CurrentDependentCurrentSource(2, v2, gnd, r1, v1, name="CCCS")
    return circuit

def case_5():
    print("case 5")
    """
    Three loops with mixed sources
    """
    circuit = Circuit.Circuit()
    gnd = Circuit.Node(circuit, gnd=True)
    a = Circuit.Node(circuit, name="A")
    b = Circuit.Node(circuit, name="B")
    c = Circuit.Node(circuit, name="C")
    vs1 = Circuit.IndependentTensionSource(10, gnd, a, name="VS1")
    r1 = Circuit.Resistor(3, a, b, name="R1")
    is1 = Circuit.IndependentCurrentSource(1, b, c, name="IS1")
    r2 = Circuit.Resistor(5, c, gnd, name="R2")
    vs2 = Circuit.IndependentTensionSource(8, b, gnd, name="VS2")
    return circuit

def case_6():
    print("case 6")
    """
    Four loops: Wheatstone bridge configuration
    """
    circuit = Circuit.Circuit()
    gnd = Circuit.Node(circuit, gnd=True)
    v1 = Circuit.Node(circuit, name="V1")
    v2 = Circuit.Node(circuit, name="V2")
    v3 = Circuit.Node(circuit, name="V3")
    v4 = Circuit.Node(circuit, name="V4")
    vs = Circuit.IndependentTensionSource(15, gnd, v1, name="VS")
    r1 = Circuit.Resistor(10, v1, v2, name="R1")
    r2 = Circuit.Resistor(20, v1, v3, name="R2")
    r3 = Circuit.Resistor(30, v2, v4, name="R3")
    r4 = Circuit.Resistor(40, v3, v4, name="R4")
    r5 = Circuit.Resistor(50, v2, v3, name="R5")  # Galvanômetro
    return circuit

def case_7():
    print("case 7")
    """
    Coupled loops with VCVS
    """
    circuit = Circuit.Circuit()
    gnd = Circuit.Node(circuit, gnd=True)
    in1 = Circuit.Node(circuit, name="IN")
    out1 = Circuit.Node(circuit, name="OUT")
    mid = Circuit.Node(circuit, name="MID")
    vs = Circuit.IndependentTensionSource(6, gnd, in1, name="VS")
    r1 = Circuit.Resistor(1e3, in1, mid, name="R1")
    r2 = Circuit.Resistor(2e3, mid, gnd, name="R2")
    # Tension-Dependent Tension source (gain=10)
    vcvs = Circuit.TensionDependentTensionSource(10, gnd, out1, mid, gnd, name="VCVS")
    r3 = Circuit.Resistor(5e3, out1, gnd, name="R3")
    return circuit

def case_8():
    print("case 8")
    """
    Five loops: Complex network with multiple paths
    """
    circuit = Circuit.Circuit()
    gnd = Circuit.Node(circuit, gnd=True)
    v1 = Circuit.Node(circuit, name="V1")
    v2 = Circuit.Node(circuit, name="V2")
    v3 = Circuit.Node(circuit, name="V3")
    v4 = Circuit.Node(circuit, name="V4")
    v5 = Circuit.Node(circuit, name="V5")
    
    vs = Circuit.IndependentTensionSource(24, gnd, v1, name="VS")
    r1 = Circuit.Resistor(2, v1, v2, name="R1")
    r2 = Circuit.Resistor(4, v1, v3, name="R2")
    r3 = Circuit.Resistor(3, v2, v4, name="R3")
    r4 = Circuit.Resistor(5, v3, v4, name="R4")
    r5 = Circuit.Resistor(1, v4, v5, name="R5")
    r6 = Circuit.Resistor(6, v5, gnd, name="R6")
    isrc = Circuit.IndependentCurrentSource(3, v2, v3, name="IS")
    return circuit

def case_9():
    """
    Current-Dependent Tension Source (CCVS)
    Control element: Resistor R1
    """

    print("case 9")
    circuit = Circuit.Circuit()
    gnd = Circuit.Node(circuit, gnd=True)
    v1 = Circuit.Node(circuit, name="V1")
    v2 = Circuit.Node(circuit, name="V2")
    
    # Elementos de controle
    r_sense = Circuit.Resistor(0.1, v1, v2, name="R_sense")  # Resistor sensor
    
    # Fontes independentes
    vs = Circuit.IndependentTensionSource(10, gnd, v1, name="VS")
    
    # Elementos de carga
    r_load = Circuit.Resistor(5, v2, gnd, name="R_load")
    
    # Fonte dependente (ganho = 50: V = 50 * I_R_sense)
    ccvs = Circuit.CurrentDependentTensionSource(
        50, 
        gnd, 
        v2, 
        r_sense,
        v1, 
        name="CCVS"
    )
    
    return circuit

def case_10():
    """
    Tension-Dependent Tension Source (VCVS)
    Control element: Tensão entre nós VA e VB
    """
    print("case 10")
    circuit = Circuit.Circuit()
    gnd = Circuit.Node(circuit, gnd=True)
    va = Circuit.Node(circuit, name="VA")
    vb = Circuit.Node(circuit, name="VB")
    vout = Circuit.Node(circuit, name="Vout")
    
    # Circuito de controle
    vs = Circuit.IndependentTensionSource(5, gnd, va, name="VS")
    r1 = Circuit.Resistor(1e3, va, vb, name="R1")
    r2 = Circuit.Resistor(2e3, vb, gnd, name="R2")
    
    # Fonte dependente (ganho = 10: Vout = 10 * (V_va - V_vb))
    vcvs = Circuit.TensionDependentTensionSource(
        10,
        gnd,
        vout,
        va,
        vb,
        name="VCVS"
    )
    
    # Carga de saída
    r_load = Circuit.Resistor(10e3, vout, gnd, name="R_load")
    
    return circuit

def case_11():
    """
    Current-Dependent Current Source (CCCS)
    Control element: Corrente através do resistor R_ref
    """
    print("case 11")
    circuit = Circuit.Circuit()
    gnd = Circuit.Node(circuit, gnd=True)
    vin = Circuit.Node(circuit, name="Vin")
    vref = Circuit.Node(circuit, name="Vref")
    vout = Circuit.Node(circuit, name="Vout")
    
    # Circuito de entrada
    vs = Circuit.IndependentTensionSource(12, gnd, vin, name="VS")
    r_ref = Circuit.Resistor(100, vin, gnd, name="R_ref")  # Resistor de referência
    
    # Fonte dependente (ganho = 20: I_out = 20 * I_R_ref)
    cccs = Circuit.CurrentDependentCurrentSource(
        20,
        vout,
        gnd,
        r_ref,
        vin,
        name="CCCS"
    )
    
    # Carga de saída
    r_load = Circuit.Resistor(1e3, vout, gnd, name="R_load")
    
    return circuit

def case_12():
    """
    Tension-Dependent Current Source (VCCS)
    Control element: Tensão entre nós Vctrl+ e Vctrl-
    """
    print("case 12")
    circuit = Circuit.Circuit()
    gnd = Circuit.Node(circuit, gnd=True)
    vctrl_p = Circuit.Node(circuit, name="Vctrl+")
    vctrl_n = Circuit.Node(circuit, name="Vctrl-")
    vout = Circuit.Node(circuit, name="Vout")
    
    # Circuito de controle
    vctrl = Circuit.IndependentTensionSource(2, vctrl_n, vctrl_p, name="V_ctrl")
    r1 = Circuit.Resistor(1e3, vctrl_p, gnd, name="R1")
    r2 = Circuit.Resistor(1e3, vctrl_n, gnd, name="R2")
    
    # Fonte dependente (ganho = 0.5: I_out = 0.5 * (V_ctrl+ - V_ctrl-))
    vccs = Circuit.TensionDependentCurrentSource(
        0.5,  # Transcondutância [S]
        vout,
        gnd,
        vctrl_p,
        vctrl_n,
        name="VCCS"
    )
    
    # Carga de saída
    r_load = Circuit.Resistor(500, vout, gnd, name="R_load")
    
    return circuit

def case_13():

    print("case 13")
    circuit = Circuit.Circuit()
    gnd = Circuit.Node(circuit, gnd=True)
    v1 = Circuit.Node(circuit, name="V1")
    v2 = Circuit.Node(circuit, name="V2")
    v3 = Circuit.Node(circuit, name="V3")

    r1 = Circuit.Resistor(2, v1, gnd, name="R1")
    r2 = Circuit.Resistor(2, v1, v2, name="R2")

    s1 = Circuit.IndependentCurrentSource(1, gnd, v2, name='S1')
    s2 = Circuit.IndependentCurrentSource(1, gnd, v3, name='S2')


    r3 = Circuit.Resistor(3, v2, v3, name="R3")

    r4 = Circuit.Resistor(3, v3, gnd, name="R4")


    return circuit

def case_14():
    print("case 14")
    circuit = Circuit.Circuit()
    gnd = Circuit.Node(circuit, gnd=True)
    v1 = Circuit.Node(circuit, name="V1")
    v2 = Circuit.Node(circuit, name="V2")
    v3 = Circuit.Node(circuit, name="V3")
    v4 = Circuit.Node(circuit, name="V4")

    s1 = Circuit.IndependentTensionSource(1, gnd, v1, name="S1")
    s2 = Circuit.IndependentTensionSource(1, v2, v1, name="S2")
    s3 = Circuit.IndependentTensionSource(2, v2, v3, name="S3")

    r1 = Circuit.Resistor(1, v3, v4, name="R1")
    r2 = Circuit.Resistor(1, v4, gnd, name="R2")
    return circuit

def case_15():
    print("case 15")
    circuit = Circuit.Circuit()
    gnd = Circuit.Node(circuit, gnd=True)
    v1 = Circuit.Node(circuit, name="V1")
    v2 = Circuit.Node(circuit, name="V2")
    v3 = Circuit.Node(circuit, name="V3")
    v4 = Circuit.Node(circuit, name="V4")

    r1 = Circuit.Resistor(1, gnd, v1, name="R1")
    r2 = Circuit.Resistor(1, v4, gnd, name="R2")

    s1 = Circuit.IndependentTensionSource(1, v1, v2, name="S1")
    s2 = Circuit.IndependentTensionSource(1, v3, v2, name="S2")
    s3 = Circuit.CurrentDependentTensionSource(2, v3, v4, r2, v4, name="S3")

    return circuit

def print_case(circuit):
    #loopAnalyzer = LoopAnalyzer(circuit)
    nodalAnalyzer = NodalAnalyzer(circuit)

    #for loop in loopAnalyzer.find_loops():
    #    print(loop)

    #equations, aux_eqs = loopAnalyzer.get_resistance_matrix()
    equations, aux_eqs = nodalAnalyzer.get_conductances_matrix()
    print("Eqs:")
    for e in equations:
        print(e)
    print("aux:")
    for ae in aux_eqs:
        print(ae)

    print()

print_case(case_1())
print_case(case_2())
print_case(case_3())
print_case(case_4())
print_case(case_5())
print_case(case_6())
print_case(case_7())
print_case(case_8())
print_case(case_9())
print_case(case_10())
print_case(case_11())
print_case(case_12())
print_case(case_13())
print_case(case_14())
print_case(case_15())