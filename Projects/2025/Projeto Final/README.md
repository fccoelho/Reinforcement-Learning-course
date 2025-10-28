# Ambiente Multi-Agente Speaker-Listener

Este projeto implementa um ambiente de aprendizado por reforço multi-agente baseado no [ambiente Speaker-Listener](https://pettingzoo.farama.org/environments/mpe/simple_speaker_listener), onde dois agentes colaboram para resolver tarefas de comunicação e coordenação.   Os Agentes são treinados usando o Algoritmo MATD3.   
Esta [implementação](https://docs.agilerl.com/en/latest/tutorials/pettingzoo/matd3.html#matd3-tutorial) é fornecida pelo pacote AgileRL, sem garantias de performance.

## Visão Geral

O ambiente Speaker-Listener consiste em dois agentes com papéis distintos:

- **Speaker (Falante)**: Fala mas não pode se mover.
- **Listener (Ouvinte)**: Ouve as mensagens do Speaker e precisa navegar até O alvo.

Um descrição detalhada deste ambiente pode ser encontrada [neste artigo](https://arxiv.org/pdf/1706.02275)
                              
## Características
- Ambiente colaborativo onde os agentes devem aprender a se comunicar eficazmente                     
- Treinamento usando algoritmos de aprendizado por reforço multi-agente
- Suporte para GPU via PyTorch CUDA         
- Implementação modular e extensível 
## Requisitos                               
- Python 3.x                                
- PyTorch                                   
- CUDA (opcional, para aceleração GPU) 
- **uv** (configuração do ambiente e instalação das dependências)
## Como Usar

Após copiar este diretório localmente, inicialize o ambiente virtual definido em pyproject.toml com o comando `uv`:

```bash
uv sync
```

Execute o script principal:                 
```bash                                     
python main.py
```

O sistema detectará automaticamente se CUDA está disponível e utilizará GPU quando possível. 
Ao final do treinamento, é salva a melhor configuração dos agentes treinados, e uma figura com a evolução do score médio dos agentes.

Para gerar a visualização do modelo treinado, execute o script de replay:

```bash
python replay.py
```



## Tarefa

Sua tarefa é implementar um novo algoritmo de aprendizado por reforço multi-agente para o ambiente Speaker-Listener. Este algoritmo deve ser capaz de fazer com que o listener consiga navegar até o alvo mais rápido do que o algoritmo [MATD3 original](https://docs.agilerl.com/en/latest/api/algorithms/matd3.html), ou seja, consiga alcançar um score médio maior que -60(score médio da configuração atual). Alternativamente você pode tentar melhorar a configuração do algoritmo atual de forma a superar  a performance atual.

Para saber mais sobre o algoritmo MATD3, consulte [este artigo](https://arxiv.org/abs/1910.01465).


