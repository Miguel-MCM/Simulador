# Simulador de Circuitos Elétricos

Um simulador de circuitos elétricos desenvolvido em Python com interface gráfica Tkinter e análise avançada de circuitos usando métodos nodais e de malhas.

## 🚀 Funcionalidades

### 🎯 Componentes Suportados
- **Resistores**: Com suporte a rotação e valores configuráveis
- **Fontes de Tensão Independentes**: Com suporte a rotação
- **Fontes de Corrente Independentes**: Com suporte a rotação
- **Fontes Dependentes**: Tensão-dependente de tensão, corrente-dependente de corrente, etc.
- **Wires**: Para conexões entre componentes
- **Nós**: Para pontos de conexão com análise automática

### 🔄 Rotação de Componentes
- **Tecla R**: Rotaciona o componente em 90° antes de ser colocado
- **Suporte a 4 orientações**: 0°, 90°, 180°, 270°
- **Preview rotacionado**: O retângulo de preview mostra a orientação atual
- **Wires automáticos**: Os fios são criados na direção correta baseada na rotação

### ⚡ Análise de Circuitos
- **Análise Nodal**: Resolução automática usando método nodal modificado
- **Análise de Malhas**: Suporte a análise por correntes de malha
- **Fontes Dependentes**: Suporte completo a fontes controladas
- **Resolução Numérica**: Usando NumPy para sistemas lineares
- **Validação**: Verificação automática de circuitos solucionáveis

### 🎨 Interface Gráfica
- **Canvas interativo**: Para desenho e edição de circuitos
- **Grid automático**: Ajuste automático das posições ao grid
- **Modo de colocação**: Clique nos botões para entrar no modo de colocação de componentes
- **Modo de conexão**: Para conectar componentes manualmente
- **Arrastar e soltar**: Movimentação intuitiva de componentes

## 🏗️ Arquitetura do Projeto

O projeto foi desenvolvido com uma arquitetura modular e bem estruturada:

```
Simulador/
├── Circuit/                    # Módulo de análise de circuitos
│   ├── Circuit.py             # Classe principal do circuito
│   ├── Node.py                # Representação de nós
│   ├── Branch.py              # Componentes e ramos
│   ├── Equation.py            # Sistema de equações
│   ├── NodalAnalyzer.py       # Análise nodal
│   └── LoopAnalyzer.py        # Análise de malhas
├── GUI/                       # Interface gráfica modular
│   ├── circuit_gui_main.py    # Classe principal da GUI
│   ├── component_manager.py   # Gerenciamento de componentes
│   ├── node_manager.py        # Gerenciamento de nós
│   ├── circuit_analyzer.py    # Análise visual do circuito
│   ├── canvas_handler.py      # Manipulação de eventos
│   ├── canvas_widget.py       # Widget do canvas
│   ├── ui_components.py       # Componentes da interface
│   └── file_manager.py        # Persistência de dados
├── run_gui.py                 # Script principal de execução
└── test_*.py                  # Testes automatizados
```

### 🔧 Módulo Circuit
- **Circuit**: Classe principal que gerencia nós e resolve o circuito
- **Node**: Representa nós elétricos com tensões e conexões
- **Branch**: Componentes elétricos (resistores, fontes)
- **Equation**: Sistema de equações lineares para resolução
- **Analyzers**: Implementações de métodos de análise

### 🎨 Módulo GUI
- **CircuitGUIMain**: Coordena todos os gerenciadores
- **ComponentManager**: Gerencia componentes do circuito
- **NodeManager**: Gerencia nós e conexões
- **CircuitAnalyzer**: Conecta interface com análise
- **CanvasHandler**: Gerencia interações no canvas

## 📦 Instalação e Execução

### Pré-requisitos
- Python 3.7+
- Tkinter (incluído com Python)
- NumPy (para cálculos numéricos)

### Execução
```bash
# Executar o simulador principal
python run_gui.py

# Executar testes
python -m pytest test_*.py
```

## 🎮 Como Usar

### 1. Colocação de Componentes
1. Clique em um botão de componente (Resistor, Fonte de Tensão, etc.)
2. Pressione **R** para rotacionar o componente (90° por vez)
3. Mova o mouse para ver o preview rotacionado
4. Clique no canvas para colocar o componente
5. Os wires serão criados automaticamente na direção correta

### 2. Análise do Circuito
1. Construa o circuito desejado
2. Clique em "Analisar Circuito" para resolver
3. Os resultados serão exibidos na interface
4. Tensões dos nós e correntes dos ramos são calculadas automaticamente

### 3. Controles
- **ESC**: Sai do modo atual e volta ao modo padrão
- **R**: Rotaciona o componente preview (apenas antes da colocação)
- **Clique esquerdo**: Coloca componentes ou seleciona itens
- **Arrastar**: Move componentes selecionados

## 🧪 Testes

O projeto inclui uma suíte abrangente de testes:

- **test_circuit.py**: Testes dos componentes e análise nodal
- **test_circuit_analyzer.py**: Testes da interface de análise
- **test_loopAnalyzer.py**: Testes da análise de malhas

### Executar Testes
```bash
# Todos os testes
python -m pytest

# Teste específico
python -m pytest test_circuit.py

# Com detalhes
python -m pytest -v
```

## 🔬 Exemplos de Circuitos

### Circuito Simples com Fonte de Corrente
```python
from Circuit import *

circuit = Circuit()
gnd = Node(circuit, gnd=True)
n1 = Node(circuit, name="Node1")
src = IndependentCurrentSource(10, gnd, n1, name="Src")
r1 = Resistor(5, gnd, n1, name="R1")

solution = circuit.solve()
print(f"Tensão no nó 1: {solution[n1]}V")
print(f"Corrente no resistor: {r1.i}A")
```

### Circuito com Fontes Dependentes
```python
# Fonte de corrente controlada por tensão
src = TensionDependentCurrentSource(0.002, v2, gnd, v2, v3, name="SC")
```

## 🚀 Funcionalidades Avançadas

### Análise Nodal Modificada
- Suporte a fontes de tensão
- Fontes dependentes
- Nós de referência (GND)

### Análise de Malhas
- Correntes de malha independentes
- Equações de malha automáticas
- Suporte a fontes de corrente

### Persistência de Dados
- Salvar/carregar circuitos em JSON
- Exportar resultados de análise
- Histórico de circuitos

## 🤝 Contribuição

### Estrutura para Novos Componentes
1. Adicionar classe em `Circuit/Branch.py`
2. Implementar método em `GUI/component_manager.py`
3. Adicionar botão em `GUI/ui_components.py`
4. Criar testes em `test_*.py`

### Padrões de Código
- **Classes**: PascalCase
- **Métodos**: snake_case
- **Variáveis**: snake_case
- **Constantes**: UPPER_CASE

## 🐛 Problemas Conhecidos

- Circuitos com laços de fontes de tensão podem não ter solução única
- Fontes dependentes complexas podem requerer análise manual
- Circuitos muito grandes podem ser lentos para resolver

## 📄 Licença

Este projeto foi desenvolvido como parte do PIBITI (Programa Institucional de Bolsas de Iniciação em Desenvolvimento Tecnológico e Inovação).

## 👥 Autores

Desenvolvido por estudantes de engenharia elétrica como projeto de iniciação científica.

---

**Nota**: Este simulador é uma ferramenta educacional para análise de circuitos elétricos. Para aplicações profissionais, sempre valide os resultados com outras ferramentas. 