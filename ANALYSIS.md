### 1. A Framework Escolhida

A framework principal escolhida para construir a interface de usuário e a interatividade da aplicação foi o **Streamlit**.

O Streamlit é uma framework de código aberto em Python que permite criar e compartilhar aplicações web para ciência de dados e machine learning de forma rápida e com poucas linhas de código. Ele foi utilizado aqui para criar todos os elementos visuais, como a barra lateral, os botões, a área de upload de arquivos e a interface de chat.

### 2. Como a Solução foi Estruturada

A solução foi estruturada em um único arquivo principal (`app.py`) que gerencia tanto a interface do usuário quanto a lógica do backend. A estrutura pode ser dividida da seguinte forma:

*   **Interface do Usuário (Frontend):**
    *   **Barra Lateral:** Contém todos os controles principais: a seleção de idioma (com as bandeiras), o campo para a chave da API do Google Gemini, o seletor de modelo de IA e o uploader de arquivos CSV.
    *   **Painel Principal:** Exibe o título, a descrição da aplicação e, o mais importante, a interface de chat onde o histórico da conversa é exibido e o usuário pode inserir novas perguntas.

*   **Lógica da Aplicação (Backend):**
    *   **Gerenciamento de Estado:** O Streamlit utiliza o `st.session_state` para manter o estado da aplicação entre as interações do usuário, como o idioma selecionado, o histórico do chat e o DataFrame do CSV carregado.
    *   **Internacionalização:** A aplicação suporta múltiplos idiomas (Português, Inglês, Espanhol) através de arquivos JSON localizados na pasta `locales/`. O texto da interface é carregado dinamicamente com base no idioma selecionado.
    *   **Análise de Dados com IA:**
        1.  Quando o usuário envia uma pergunta, a aplicação a envia para a **API do Google Gemini**, juntamente com o contexto dos dados do CSV (nomes das colunas e primeiras linhas).
        2.  A IA é instruída a gerar um código Python para responder à pergunta. Para garantir a confiabilidade, a IA foi instruída a usar apenas um conjunto específico de bibliotecas (`pandas`, `numpy`, `matplotlib`, `seaborn`, `scikit-learn`).
        3.  O código Python retornado pela IA é executado em um ambiente seguro.
    *   **Execução e Exibição de Resultados:**
        1.  Qualquer saída de texto do código (como a visualização de dados com `print(df.head())`) é capturada e exibida na interface de chat.
        2.  Se o código gerar um gráfico (`matplotlib` ou `seaborn`), o gráfico é renderizado e exibido diretamente na aplicação.

*   **Gerenciamento de Dependências:**
    *   Todas as bibliotecas Python necessárias para o funcionamento do projeto (`streamlit`, `pandas`, `google-generativeai`, etc.) estão listadas no arquivo `requirements.txt`, facilitando a instalação e a configuração do ambiente.