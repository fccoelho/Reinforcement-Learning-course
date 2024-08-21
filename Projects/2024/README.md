# Instruções para o Projeto
Neste diretório você encontrará os arquivos com a descrição do projeto de conclusão do curso:

1. [Descrição](0-Descrição%20do%20Projeto.md)
2. [Definição dos Agentes](1-Agentes.md)
3. [Definindo o Ambiente](3-Ambiente.md)
4. [Treinamento dos Agentes](4-Fluxo.md)

## Dicas para execução do código.

Como os  agentes requerem o uso de um LLM, é recomendável que você tenha um ambiente de desenvolvimento com suporte a GPU. Caso não esteja ao seu alcance, você pode usar o Google Colab para treinar os agentes.

Para executar os LLMs, podemos usar a biblioteca Hugging Face [Transformers](https://huggingface.co/docs/transformers/index). Preparamos um [exemplo de uso](https://colab.research.google.com/drive/1RZJSxet4wbCeZMLpYCrds7VTbSi3dAKT?usp=sharing) para você se familiarizar com a biblioteca.

 Outra alternativa é usar a plataforma [Ollama](https://ollama.com/library). Para usar  o Ollama no Google Colab, siga [este exemplo](https://colab.research.google.com/drive/11gIyx-elOHxEVf2TdnwtZnk1YHMluLJR?usp=sharing).
 
A terceira alternativa é usar LLMs remotos via API. Existem vários provedores de LLMs que oferecem acesso via API. Um exemplo é o [OpenAI](https://beta.openai.com/docs/). 

Podemos ainda usar o [Gemini](https://colab.research.google.com/github/google/generative-ai-docs/blob/main/site/en/gemini-api/docs/get-started/python.ipynb). Para isso, você precisa de uma chave de API. no caso do Gemini existe uma versão gratuita que você pode usar para testar.