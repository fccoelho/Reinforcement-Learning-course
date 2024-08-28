# Definindo o Ambiente

O ambiente de treino proporciona o contexto no qual os agentes interagem e aprendem. O resultado do trabalho dos agentes deve ser  a produção de um relatório analítico que atenda a critérios de qualidade e precisão. Os critérios de avaliação do relatório estão descritos [neste documento](Avaliação.md).

O ambiente deve fornecer as informações necessárias sobre o estado da solução, para que os agentes possam tomar decisões informadas. Para isso deve ser capaz de:
- Executar o código escrito pelo agente codificador, determinando a presença de bugs.
- Avaliar a correção da resposta, comparando com a resposta correta.
- Usar ferramentas de análise de código (linters) para avaliar a qualidade do código.
- Calcular a complexidade do código, para que o agente possa escolher entre diferentes soluções.
- Calcular o score do relatório analítico, para que os agentes possam melhorá-lo com base nestes scores.
- Determinar o fim do treinamento, com base em um score mínimo.

Estas informações são usadas para calcular a recompensa ou penalidade para cada agente, de acordo com a qualidade e correção do código. Também entrarão na geração do prompt do agente revisor ajudando-o a sugerir melhorias.

Além disso, o ambiente deve compilar as métricas de análise do código Computando as recompensas de cada agente.

## Recompensas e penalidades

Uma escala numérica de recompensas e penalidades deve ser definida para que os agentes possam aprender a maximizar a recompensa.

### Agente Codificador

- Recompensa: O agente codificador recebe uma recompensa positiva quando o código é correto e de qualidade.
- Penalidade: O agente codificador recebe uma penalidade negativa quando o código contém bugs ou é de baixa qualidade.

### Agente Revisor
- Recompensa: O agente revisor recebe uma recompensa positiva quando o relatório analítico recebe um score maior que o anterior.




