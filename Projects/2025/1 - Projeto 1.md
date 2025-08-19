# Implementar RL para Robô de reciclagem

Na página 52 do Livro-texto, encontra-se a descrição do problema do Robô de reciclagem (Exemplo 3.3). Sigam a descrição do problema e escolhas valores para as probabilidades $\alpha$ e $\beta$, e as recompensas $r_{search}$ e $r_{wait}$, respeitando as pecificação de $r_{search} > r_{wait}$.

Empregue o algoritmo de Temporal difference (TD), usado no problema do jogo da Velha, para o aprendizado do Robô de reciclagem. O Robô deve aprender a maximizar a recompensa total, que é a soma das recompensas obtidas em cada passo do processo de decisão.

A rotina de aprendizagem deve salvar a recompensa total obtida ao final de período de aprendizagem. Como esta é uma tarefa contínua, a recompensa total deve ser acumulada ao longo do tempo. Defina um período de aprendizagem (época) de, por exemplo $1000$ passos, e salve a recompensa total obtida ao final deste período em um arquivo chamado `rewards.txt`. Realize o treinamento por várias épocas. No final do treinamento, plote a recompensa total acumulada ao longo das épocas em um gráfico, utilizando uma biblioteca de visualização como Matplotlib ou Seaborn. Você pode repetir o treinamento várias vezes e calcular a média das curvas de  recompensa total acumulada para obter uma curva mais suave.

Plote a política ótima como um gráfico de calor (heatmap) utilizando a biblioteca Seaborn, onde cada célula representa a probabilidade da ação ótima para cada estado do robô. A política deve ser representada de forma que as ações sejam codificadas por cores diferentes, facilitando a visualização das ações preferidas pelo robô em cada estado.

Se necessário consulte o capítulo 6 do Livro-texto para entender melhor o algoritmo de Temporal difference.

## Entrega
Data de entrega: 02/09/2025

1. O código fonte do algoritmo de aprendizagem do Robô de reciclagem. 
2. Relatório em Markdown explicando o código, os resultados obtidos e as decisões tomadas durante o desenvolvimento do projeto. O relatório deve ser claro e objetivo, explicando como o algoritmo foi implementado, quais foram os parâmetros escolhidos e como os resultados foram obtidos.

