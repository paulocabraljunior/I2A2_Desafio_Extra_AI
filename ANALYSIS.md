# Análise da Estrutura do Projeto (Alpha.03)

Este documento descreve a arquitetura final da aplicação, explicando os componentes escolhidos e como eles interagem para criar a ferramenta de Análise Exploratória de Dados (EDA).

### 1. Framework Escolhida: Streamlit

A interface do usuário (frontend) foi construída inteiramente com **Streamlit**.

*   **Por quê?** Streamlit é uma framework Python de código aberto que se destaca pela sua simplicidade e rapidez para criar aplicações web interativas, especialmente para projetos de ciência de dados. Ele permite focar na lógica da análise de dados, gerando automaticamente os componentes visuais (botões, chat, gráficos) sem a necessidade de escrever código em HTML, CSS ou JavaScript.

### 2. Estrutura da Solução: Agente de IA com Ferramentas

A solução foi arquitetada em torno de um **Agente de IA com Ferramentas (Tool-based Agent)**, uma abordagem moderna, segura e confiável.

*   **Como Funciona:**
    1.  **Interface do Usuário:** O usuário interage com a aplicação através de uma interface de chat simples.
    2.  **Definição de Ferramentas:** No backend (`app.py`), definimos um conjunto de funções Python específicas para cada tarefa de análise (ex: `get_data_summary`, `plot_correlation_matrix`, `detect_outliers`).
    3.  **Comunicação com a IA (Function Calling):**
        *   Quando o usuário envia uma pergunta, a aplicação não pede para a IA gerar código. Em vez disso, ela envia a pergunta e a **lista de ferramentas disponíveis** para a API do Google Gemini.
        *   O modelo Gemini, agindo como o "cérebro" do agente, decide qual a melhor ferramenta para responder à pergunta.
    4.  **Execução Segura:** A aplicação executa **apenas** a função pré-definida que a IA escolheu, com os argumentos que ela sugeriu. Isso evita a execução de código arbitrário e inseguro.
    5.  **Ciclo de Feedback:** O resultado da ferramenta (seja um resumo de dados ou uma mensagem de que um gráfico foi criado) é enviado de **volta** para a IA.
    6.  **Resposta Final:** Com o resultado da ferramenta em mãos, a IA gera uma resposta final, em linguagem natural, explicando as conclusões para o usuário.

*   **Por que essa estrutura?**
    *   **Segurança:** Impede que a IA execute código malicioso ou com erros, pois ela está limitada a usar apenas as ferramentas que nós criamos.
    *   **Confiabilidade:** Garante que as análises sejam sempre executadas da mesma forma, usando código testado, o que aumenta a precisão dos resultados.
    *   **Memória e Contexto:** A aplicação envia o histórico da conversa para a IA, permitindo que o agente se lembre de análises anteriores e tire conclusões mais complexas e contextuais.
    *   **Manutenibilidade:** Para adicionar novas funcionalidades, basta criar uma nova função-ferramenta e declará-la para a IA, tornando o projeto fácil de expandir.

### 3. Fluxo de Interação do Usuário

O fluxo de interação foi projetado para ser simples e intuitivo:

1.  **Configuração Inicial:** O usuário abre a aplicação e, na barra lateral, insere sua chave de API do Google Gemini e seleciona o modelo de IA que deseja usar.
2.  **Upload do Arquivo:** O usuário faz o upload de um arquivo CSV através da área de upload na barra lateral.
3.  **Início da Análise:** Uma vez que o arquivo é carregado com sucesso, a interface de chat é ativada.
4.  **Pergunta do Usuário:** O usuário digita uma pergunta em linguagem natural na caixa de chat (ex: "Qual a correlação entre as colunas?" ou "Me mostre os outliers da coluna 'idade'").
5.  **Processamento do Agente:**
    *   A aplicação envia a pergunta para a IA, que decide qual ferramenta usar (ex: `plot_correlation_matrix`).
    *   A aplicação executa a ferramenta escolhida. Se for um gráfico, ele é exibido na tela.
    *   O resultado da ferramenta é enviado de volta para a IA.
6.  **Resposta e Conclusão:** A IA interpreta o resultado da ferramenta e gera uma resposta final em texto, explicando os resultados e fornecendo conclusões. Essa resposta é exibida na interface de chat.
7.  **Ciclo Contínuo:** O usuário pode continuar fazendo mais perguntas, e o agente usará o histórico da conversa para fornecer respostas cada vez mais contextuais.