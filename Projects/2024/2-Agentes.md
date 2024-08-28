# Definindo os agentes

Embora fosse possível treinar um único agente para resolver o problema, a complexidade do problema de análise de dados é tal que é mais eficiente treinar dois agentes para cooperarem na solução do problema. Isso se deve à divisão de tarefas, onde um agente escreve o código inicial e o outro agente revisa e sugere melhorias.

Desta forma, cada agente tem o seu espaço de ações finito e bem definido, o que facilita o treinamento e a convergência para uma solução ótima. Cada agente também pode manter uma memória de curto prazo para facilitar a comunicação entre eles.

## Agente Codificador

O agente codificador é responsável por escrever o código para a análise.

### Espaço de Ações

O espaço de ações do agente codificador é composto por um conjunto de ações que podem ser tomadas para escrever o código. Cada ação é uma operação de código que pode ser aplicada ao código atual.

Ação | Descrição
-----|----------
processamento dos dados | Limpar, transformar e preparar os dados para análise.
Analisar os dados | Realizar análises estatísticas, ou contruir modelos de aprendizado de máquina.
Visualizar os resultados | Gerar gráficos e visualizações dos dados.
Interpretar a análise | Interpretar os resultados, produzindo um texto que inclua os resultados da análise na forma de figuras e tabelas.


## Agente Revisor

O agente revisor é responsável por revisar o código escrito pelo agente codificador e sugerir melhorias.

### Espaço de Ações

O espaço de ações do agente revisor é composto por um conjunto de ações que podem ser tomadas para revisar o código. Cada ação é uma operação de revisão que pode ser aplicada ao código atual.

Ação | Descrição
-----|----------
Análise Estática | Analisar o código com [Mypy](https://mypy-lang.org/), [Ruff](https://docs.astral.sh/ruff/), [Bandit](https://bandit.readthedocs.io/en/latest/), etc.
Executar código | Executar o código atual para verificar se ele está correto, identificando bugs.
Propor Refatoração | Propor refatorações para melhorar a qualidade do código.
Aprovar código | Aprovar o código como correto e de qualidade.
Melhorar o Relatório | Escrever um relatório analítico sobre a análise realizada. Caso já exista uma versão do relatório, deve melhorá-lo.
----------------
 A escolha da ação deve ser feita levando em conta os scores produzidos pelo ambiente sobre o estado atual Relatório Analítico.

A ação escolhida, resultará na geração de um *prompt* contendo feedback construtivo e detalhado ao agente codificador sobre o código escrito.
