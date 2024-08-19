# Agentes Cooperativos para análise de dados

Neste projeto é treinar dois agentes LLM para cooperarem na solução de problemas de análise de dados. O ambiente de treinamento é um ambiente customizado, onde os agentes devem aprender a cooperar para maximizar a recompensa.

Para resolver esta classe de problemas, é necessária dois tipos de agentes: um agente que escreve o código inicial e um agente que revisa e sugere melhorias. O agente revisor deve ser capaz de identificar erros e sugerir melhorias no código. O agente que escreve o código deve ser capaz de corrigir os erros e melhorar o código.

O fluxograma básico do processo é o seguinte:

```mermaid
graph TD
    A[Problem Set] --> B[Data Analysis Problem]
    B --> C[Coder Agent Writes Initial Code]
    C --> D[Reviewer Agent Reviews & Suggests Improvements]
    D --> E{Correct & Quality Code?}
    E -- Yes --> F[Reward: Code Quality & Accuracy]
    E -- No --> G[Penalty: Bugs & Errors]
    F --> I[Iterate Process for Next Segment]
    G --> I[Iterate Process for Next Segment]
    I --> J{Completed?}
    J -- No --> B
    J -- Yes --> K[Validate Solution Quality & Accuracy]
    K --> L{{Automated Evaluation}}
    L --> M[[Feedback to Agents]]
    M --> N[Update Policies using Reinforcement Learning]

    style A fill:#f9f,stroke:#333,stroke-width:2px;
    style B fill:#9f9,stroke:#333,stroke-width:2px;
    style C fill:#9f9,stroke:#333,stroke-width:2px;
    style D fill:#9f9,stroke:#333,stroke-width:2px;
    style E fill:#fc3,stroke:#333,stroke-width:2px;
    style F fill:#9f9,stroke:#333,stroke-width:2px;
    style G fill:#f99,stroke:#333,stroke-width:2px;
    style H fill:#fc3,stroke:#333,stroke-width:2px;
    style I fill:#fc3,stroke:#333,stroke-width:2px;
    style J fill:#fc3,stroke:#333,stroke-width:2px;
    style K fill:#9f9,stroke:#333,stroke-width:2px;
    style L fill:#9f9,stroke:#333,stroke-width:2px;
    style M fill:#fc3,stroke:#333,stroke-width:2px;
    style N fill:#9f9,stroke:#333,stroke-width:2px;
```
