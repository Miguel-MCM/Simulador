# Simulador de Circuitos

Um simulador de circuitos elétricos com interface gráfica desenvolvido em Python usando Tkinter.

## Arquitetura

O simulador foi projetado com uma arquitetura modular que separa a interface gráfica da lógica de análise do circuito:

### GUI (Interface Gráfica)
- **Arquivos**: `GUI/window.py`, `GUI/canvas_widget.py`
- **Responsabilidade**: Interface visual, manipulação de componentes, salvamento/carregamento
- **Dados**: Trabalha apenas com dicionários Python para representar nós e componentes
- **Compilação**: Converte os dados visuais em objetos do circuito para análise

### Circuit (Lógica do Circuito)
- **Arquivos**: `Circuit/` (todos os arquivos do módulo)
- **Responsabilidade**: Análise nodal, resolução de equações, simulação
- **Dados**: Objetos Python (Node, Resistor, etc.) para cálculos

## Como Funciona

1. **Interface Visual**: O usuário cria e conecta componentes através da GUI
2. **Armazenamento**: Todos os dados são mantidos como dicionários Python
3. **Compilação**: Quando solicitada a análise, a GUI "compila" os dicionários em objetos do circuito
4. **Análise**: O módulo Circuit resolve o circuito e retorna os resultados
5. **Exibição**: Os resultados são mostrados na interface

## Vantagens da Arquitetura

- **Separação de Responsabilidades**: GUI e lógica de análise são independentes
- **Flexibilidade**: Fácil adicionar novos tipos de componentes
- **Manutenibilidade**: Código mais limpo e organizado
- **Performance**: Análise só é executada quando necessário
- **Persistência**: Dados salvos em JSON são simples e portáveis

## Estrutura dos Dados

### Nós (Nodes)
```python
{
    'type': 'node' | 'ground',
    'x': int,           # Posição X no canvas
    'y': int,           # Posição Y no canvas
    'gnd': bool,        # Se é terra (apenas para ground)
    'canvas_id': int,   # ID do elemento no canvas
    'text_id': int      # ID do texto no canvas
}
```

### Linhas dos Nós (Node Lines)
```python
# Estrutura das linhas salvas para cada nó
'node_lines': {
    'node_name': [
        {
            'x1': int, 'y1': int,  # Ponto inicial da linha
            'x2': int, 'y2': int   # Ponto final da linha
        }
    ]
}

# Exemplo de uso:
# - node_lines['N_1'] = [{'x1': 100, 'y1': 100, 'x2': 200, 'y2': 100}]
# - Representa uma linha horizontal do nó N_1 até x=200
```

### Componentes
```python
{
    'type': 'resistor' | 'voltage_source' | 'current_source',
    'value': float,     # Valor do componente
    'node1': str,       # Nome do primeiro nó conectado
    'node2': str,       # Nome do segundo nó conectado
    'x': int,           # Posição X no canvas
    'y': int,           # Posição Y no canvas
    'canvas_id': int,   # ID do elemento no canvas
    'text_id': int      # ID do texto no canvas
}
```

## Como Usar

### Executar o Simulador
```bash
python run_gui.py
```

### Funcionalidades da GUI

1. **Adicionar Componentes**:
   - Clique nos botões para adicionar nós, resistores, fontes de tensão/corrente
   - Digite o nome e valor quando solicitado

2. **Conectar Componentes**:
   - Clique em "Conectar Componentes"
   - Clique em dois elementos para conectá-los
   - Nós intermediários são criados automaticamente

3. **Mover Componentes**:
   - Clique e arraste componentes para movê-los
   - As conexões são atualizadas automaticamente

4. **Analisar Circuito**:
   - Clique em "Resolver Circuito" para obter os resultados
   - Tensões dos nós e correntes são calculadas

5. **Editar Nós**:
   - Clique em um nó para entrar no modo de edição
   - Mova o mouse para ver linhas temporárias (horizontais e verticais)
   - Clique novamente para salvar as linhas
   - Use "Cancelar Edição de Nó" para sair sem salvar

6. **Salvar/Carregar**:
   - Use "Salvar Circuito" para salvar em JSON (inclui linhas dos nós)
   - Use "Carregar Circuito" para carregar um circuito salvo

### Exemplo de Uso

1. Adicione um nó terra (GND)
2. Adicione uma fonte de tensão de 12V
3. Adicione um resistor de 100Ω
4. Conecte a fonte ao resistor e o resistor ao terra
5. Clique em "Resolver Circuito" para ver os resultados

### Edição de Nós com Linhas

A funcionalidade de edição de nós permite criar conexões visuais personalizadas:

1. **Entrar no Modo de Edição**:
   - Clique em qualquer nó para ativar o modo de edição
   - O cursor muda para indicar que está editando
   - As informações mostram qual nó está sendo editado

2. **Visualizar Linhas Temporárias**:
   - Mova o mouse para ver linhas que conectam o nó ao cursor
   - As linhas são sempre horizontais ou verticais (formato em L)
   - Linhas temporárias aparecem em vermelho tracejado

3. **Salvar as Linhas**:
   - Clique novamente no nó para salvar as linhas
   - As linhas temporárias se tornam permanentes (pretas)
   - O modo de edição é desativado automaticamente

4. **Cancelar Edição**:
   - Use o botão "Cancelar Edição de Nó" para sair sem salvar
   - Todas as linhas temporárias são removidas

**Tipos de Linhas**:
- **Linha Direta**: Se o mouse estiver na mesma linha horizontal ou vertical do nó
- **Caminho em L**: Duas linhas perpendiculares quando o mouse está em posição diferente

## Estrutura do Projeto

```
Simulador/
├── Circuit/                 # Módulo de análise do circuito
│   ├── __init__.py
│   ├── Circuit.py          # Classe principal do circuito
│   ├── Node.py             # Classe dos nós
│   ├── Branch.py           # Classe dos ramos
│   ├── Loop.py             # Análise de malhas
│   ├── LoopAnalyzer.py     # Analisador de malhas
│   ├── NodalAnalyzer.py    # Analisador nodal
│   └── Equation.py         # Sistema de equações
├── GUI/                    # Interface gráfica
│   ├── window.py           # Janela principal
│   └── canvas_widget.py    # Widget do canvas
├── run_gui.py              # Script principal
└── README.md               # Este arquivo
```

## Dependências

- Python 3.7+
- tkinter (incluído no Python)
- math (biblioteca padrão)
- json (biblioteca padrão)

## Desenvolvimento

### Adicionando Novos Componentes

1. **GUI**: Adicione o botão e método em `window.py`
2. **Canvas**: Adicione o desenho em `canvas_widget.py`
3. **Circuit**: Adicione a classe do componente em `Circuit/`
4. **Compilação**: Atualize o método `compile_circuit()` em `window.py`

### Estrutura de Dados

- **GUI**: Sempre use dicionários para dados visuais
- **Circuit**: Use objetos Python para análise
- **Conversão**: Método `compile_circuit()` faz a ponte entre os dois

## Licença

Este projeto é de código aberto e pode ser usado livremente para fins educacionais e de pesquisa. 