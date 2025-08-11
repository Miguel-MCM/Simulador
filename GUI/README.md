# GUI - Interface Gráfica do Simulador de Circuitos

## Estrutura dos Arquivos

### `window.py`
Classe principal da interface gráfica (`CircuitGUI`):
- Gerencia a janela principal e todos os controles
- Coordena a comunicação entre o canvas e a lógica do circuito
- Responsável pelos botões, campos de texto e organização da interface

### `canvas_widget.py`
Classe especializada para o canvas (`CircuitCanvas`):
- Gerencia toda a renderização visual do circuito
- Responsável pelo grid, desenho de componentes e conexões
- Manipula eventos de mouse (clique, arrastar, soltar)
- Implementa snap-to-grid e movimentação de componentes

## Separação de Responsabilidades

### CircuitGUI (window.py)
- **Controles da Interface**: Botões, campos de texto, menus
- **Lógica de Negócio**: Adição de componentes, conexões, análise
- **Gerenciamento de Estado**: Circuito, nós, componentes
- **Comunicação**: Coordena entre interface e canvas

### CircuitCanvas (canvas_widget.py)
- **Renderização**: Desenho de todos os elementos visuais
- **Interação**: Eventos de mouse e teclado
- **Layout**: Grid, posicionamento, snap-to-grid
- **Visualização**: Componentes, conexões, nós

## Benefícios da Separação

1. **Modularidade**: Cada classe tem uma responsabilidade específica
2. **Manutenibilidade**: Mudanças no canvas não afetam a lógica da interface
3. **Reutilização**: O canvas pode ser usado em outras interfaces
4. **Testabilidade**: Cada componente pode ser testado independentemente
5. **Escalabilidade**: Fácil adicionar novos tipos de componentes

## Fluxo de Dados

```
User Action → CircuitGUI → CircuitCanvas → Visual Update
     ↓
CircuitGUI ← CircuitCanvas ← Mouse Event
     ↓
Circuit Analysis → Results Display
```

## Como Adicionar Novos Componentes

1. **No CircuitCanvas**: Adicionar método `draw_[component_type]`
2. **No CircuitGUI**: Adicionar método `add_[component_type]`
3. **Atualizar**: Botões na interface e lógica de conexão

## Como Adicionar Novas Funcionalidades

1. **Eventos de Mouse**: Implementar em `CircuitCanvas`
2. **Lógica de Negócio**: Implementar em `CircuitGUI`
3. **Comunicação**: Usar referência `self.canvas_widget` ou `self.circuit_gui`

## Exemplo de Uso

```python
# Criar interface
root = tk.Tk()
gui = CircuitGUI(root)

# Adicionar componente
gui.add_resistor()

# O canvas automaticamente desenha o componente
# e gerencia a interação
```

## Padrões Utilizados

- **Observer Pattern**: Canvas observa mudanças no circuito
- **MVC Pattern**: Model (Circuit), View (Canvas), Controller (GUI)
- **Separation of Concerns**: Cada classe tem uma responsabilidade específica 