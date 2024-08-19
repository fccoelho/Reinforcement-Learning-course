# Fluxo do treinamento

No início o Ambiente apresenta aos agentes o problema a ser resolvido, na forma de prompts de texto. Cada prompt é uma descrição do problema e dos dados a serem analisados. Este prompt inicial também deve incluir o papel de cada agente, ou seja, quem será o programador e quem será o Revisor.

Por exemplo, o prompt pode ser algo como:

### Agente Codificador

```
Você é um programador do ramo da ciência de dados.
Seu trabalho é escrever um script para limpar os dados de vendas fornecidos.
O script deve corrigir os erros de formatação e garantir que os dados estejam prontos para análise.
O conjunto de dados encontra-seno arquivo "sales_data.csv".
```

### Agente Revisor

```
Você é um revisor de código do ramo da ciência de dados.
Seu trabalho é revisar o script de limpeza de dados fornecido pelo programador.
Você deve identificar erros e sugerir melhorias para garantir que o script seja eficiente e correto.
```

## Passos seguintes

1. Se houver alguma revisão disponível, ela é adicionada ao prompt do **Agente Codificador** escolhe uma ação do espaço de ações pré-definido, por exemplo, "Escrever código novo". Escreve o código e envia para o Ambiente.
2. O **Ambiente** executa o código e avalia a qualidade e correção. Retorna a recompensa ou penalidade para o Agente Codificador.
3. O **Agente Revisor** recebe o código, Revisa o mesmo, e escolhe uma ação do espaço de ações pré-definido, por exemplo, "Propor Refatoração". Ele envia o feedback para o Agente Codificador, na forma de um prompt de texto.
4. A partir da segunda versão do código, o **ambiente** determina a mehoria obtida e recompensa o Agente Revisor.
5. Caso o objetivo tenha sido alcançado, o **ambiente** finaliza o treinamento. Caso contrário, o processo se repete.
