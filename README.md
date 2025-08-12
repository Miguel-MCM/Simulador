# Simulador de Circuitos

Um simulador de circuitos elétricos desenvolvido em Python com interface gráfica Tkinter.

## Funcionalidades

### Componentes Suportados
- **Resistores**: Com suporte a rotação
- **Fontes de Tensão**: Com suporte a rotação  
- **Fontes de Corrente**: Com suporte a rotação
- **Wires**: Para conexões entre componentes
- **Nós**: Para pontos de conexão

### Rotação de Componentes
- **Tecla R**: Rotaciona o componente em 90° antes de ser colocado
- **Suporte a 4 orientações**: 0°, 90°, 180°, 270°
- **Preview rotacionado**: O retângulo de preview mostra a orientação atual
- **Wires automáticos**: Os fios são criados na direção correta baseada na rotação

### Interface
- **Canvas interativo**: Para desenho e edição de circuitos
- **Grid automático**: Ajuste automático das posições ao grid
- **Modo de colocação**: Clique nos botões para entrar no modo de colocação de componentes
- **Modo de conexão**: Para conectar componentes manualmente

## Como Usar

### Rotação de Componentes
1. Clique em um botão de componente (Resistor, Fonte de Tensão, Fonte de Corrente)
2. Pressione **R** para rotacionar o componente (90° por vez)
3. Mova o mouse para ver o preview rotacionado
4. Clique no canvas para colocar o componente
5. Os wires serão criados automaticamente na direção correta

### Controles
- **ESC**: Sai do modo atual e volta ao modo padrão
- **R**: Rotaciona o componente preview (apenas antes da colocação)
- **Clique esquerdo**: Coloca componentes ou seleciona itens
- **Arrastar**: Move componentes selecionados

## Estrutura do Projeto

```
Simulador/
├── Circuit/           # Lógica do circuito
├── GUI/              # Interface gráfica
│   ├── component_manager.py    # Gerenciamento de componentes
│   ├── canvas_widget.py        # Widget do canvas com rotação
│   ├── preview_rectangle.py    # Preview rotacionado
│   └── canvas_handler.py       # Manipulação de eventos
├── run_gui.py        # Arquivo principal para execução
└── test_rotation.py  # Teste da funcionalidade de rotação
```

## Execução

```bash
# Executar o simulador principal
python run_gui.py

# Executar teste de rotação
python test_rotation.py
```

## Dependências

- Python 3.7+
- Tkinter (incluído com Python)
- Matemática (math) para cálculos de rotação

## Arquitetura

O sistema de rotação foi implementado com:

1. **Canvas com suporte a rotação**: Métodos para desenhar componentes rotacionados
2. **Preview rotacionado**: Retângulo de preview que mostra a orientação atual
3. **Gerenciamento de rotação**: Controle da rotação atual e reset automático
4. **Wires inteligentes**: Criação automática de fios na direção correta
5. **Eventos de teclado**: Binding da tecla R para rotação

A rotação é aplicada apenas antes da colocação do componente, garantindo que o preview seja sempre visível e que os wires sejam criados corretamente. 