# Arquitetura do Simulador de Circuitos

## Visão Geral

O simulador de circuitos foi refatorado para melhorar a organização do código, separando responsabilidades em classes especializadas. Esta nova arquitetura torna o código mais modular, testável e fácil de manter.

## Estrutura de Classes

### 1. CircuitGUIMain (circuit_gui_main.py)
**Responsabilidade**: Classe principal que coordena todas as funcionalidades
- Inicializa e coordena todos os gerenciadores
- Configura a interface de usuário
- Gerencia o fluxo principal da aplicação

### 2. ComponentManager (component_manager.py)
**Responsabilidade**: Gerencia todos os componentes do circuito
- Adiciona, remove e edita componentes (resistores, fontes, etc.)
- Gerencia propriedades dos componentes
- Conecta componentes aos nós
- Mantém estado dos componentes selecionados

### 3. NodeManager (node_manager.py)
**Responsabilidade**: Gerencia todos os nós do circuito
- Adiciona, remove e edita nós
- Gerencia o modo de edição de nós
- Calcula e desenha linhas de conexão
- Mantém estado dos nós selecionados

### 4. CircuitAnalyzer (circuit_analyzer.py)
**Responsabilidade**: Análise e resolução do circuito
- Compila o circuito visual em objetos do circuito
- Valida se o circuito pode ser resolvido
- Resolve o circuito usando as classes do módulo Circuit
- Exibe resultados da análise

### 5. FileManager (file_manager.py)
**Responsabilidade**: Persistência de dados
- Salva circuitos em arquivos JSON
- Carrega circuitos de arquivos JSON
- Exporta/importa dados do circuito

### 6. UIComponents (ui_components.py)
**Responsabilidade**: Interface de usuário
- Configura e gerencia todos os elementos da interface
- Organiza botões em seções lógicas
- Gerencia a área de informações

### 7. CanvasHandler (canvas_handler.py)
**Responsabilidade**: Interações com o canvas
- Gerencia eventos do mouse no canvas
- Coordena a colocação de componentes
- Gerencia o modo do cursor
- Coordena com os gerenciadores de componentes e nós

## Fluxo de Dados

```
CircuitGUIMain
    ↓
├── UIComponents (Interface)
├── CanvasHandler (Interações)
├── ComponentManager (Componentes)
├── NodeManager (Nós)
├── CircuitAnalyzer (Análise)
└── FileManager (Persistência)
```

## Benefícios da Nova Arquitetura

### 1. **Separação de Responsabilidades**
- Cada classe tem uma responsabilidade específica e bem definida
- Facilita a manutenção e debugging

### 2. **Modularidade**
- Classes podem ser testadas independentemente
- Fácil adicionar novas funcionalidades sem afetar outras partes

### 3. **Reutilização**
- Classes podem ser reutilizadas em outros contextos
- Interface bem definida entre as classes

### 4. **Manutenibilidade**
- Código mais organizado e legível
- Mudanças localizadas em classes específicas

### 5. **Testabilidade**
- Cada classe pode ser testada isoladamente
- Mocks e stubs mais fáceis de implementar

## Como Usar

### Execução Principal
```python
from GUI.circuit_gui_main import CircuitGUIMain

root = tk.Tk()
app = CircuitGUIMain(root)
root.mainloop()
```

### Uso Individual das Classes
```python
from GUI.component_manager import ComponentManager
from GUI.node_manager import NodeManager

# Criar instâncias
component_manager = ComponentManager(canvas_widget)
node_manager = NodeManager(canvas_widget)

# Usar funcionalidades
component_manager.add_resistor(x, y, node1, node2)
node_manager.add_node(x, y)
```

## Extensibilidade

### Adicionar Novos Componentes
1. Adicionar método em `ComponentManager`
2. Adicionar botão em `UIComponents`
3. Adicionar lógica de colocação em `CanvasHandler`

### Adicionar Novas Funcionalidades
1. Criar nova classe especializada
2. Integrar com `CircuitGUIMain`
3. Adicionar interface necessária

## Convenções de Nomenclatura

- **Classes**: PascalCase (ex: `ComponentManager`)
- **Métodos**: snake_case (ex: `add_component`)
- **Variáveis**: snake_case (ex: `component_name`)
- **Constantes**: UPPER_CASE (ex: `GRID_SIZE`)

## Dependências

- **tkinter**: Interface gráfica
- **Circuit**: Módulo de análise de circuitos
- **json**: Persistência de dados
- **typing**: Anotações de tipo

