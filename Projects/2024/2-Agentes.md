# Definindo os agentes

Embora fosse possível treinar um único agente para resolver o problema, a complexidade do problema de análise de dados é tal que é mais eficiente treinar dois agentes para cooperarem na solução do problema. Isso se deve à divisão de tarefas, onde um agente escreve o código inicial e o outro agente revisa e sugere melhorias.

Desta forma, cada agente tem o seu espaço de ações finito e bem definido, o que facilita o treinamento e a convergência para uma solução ótima. Cada agente também pode manter uma memória de curto prazo para facilitar a comunicação entre eles.

## Agente Codificador

O agente codificador é responsável por escrever o código para a análise.

### Espaço de Ações

O espaço de ações do agente codificador é composto por um conjunto de ações que podem ser tomadas para escrever o código. Cada ação é uma operação de código que pode ser aplicada ao código atual.

Ação | Descrição
-----|----------
Escrever código novo | Adicionar novas linhas de código ao código atual.
Editar código | Modificar código existente, para corrigir bugs ou melhorar a qualidade.
Documentar código | Adicionar comentários ao código para facilitar a compreensão.
Pedir explicação | Pedir ao agente revisor para explicar uma sugestão de melhoria.
Implementar sugestão | Implementar uma sugestão de melhoria feita pelo agente revisor.

## Agente Revisor

O agente revisor é responsável por revisar o código escrito pelo agente codificador e sugerir melhorias.

### Espaço de Ações

O espaço de ações do agente revisor é composto por um conjunto de ações que podem ser tomadas para revisar o código. Cada ação é uma operação de revisão que pode ser aplicada ao código atual.

Ação | Descrição
-----|----------
Análise Estática | Analisar o código com [Mypy](https://mypy-lang.org/), [Ruff](https://docs.astral.sh/ruff/), [Bandit](https://bandit.readthedocs.io/en/latest/), etc.
Executar código | Executar o código atual para verificar se ele está correto, identificando bugs.
Propor Refatoração | Propor refatorações para melhorar a qualidade do código.
----------------
----------------
A ação escolhida, resultará na geração de um *prompt* contendo feedback construtivo e detalhado ao agente codificador sobre o código escrito.
