# Calculadora de Correção Monetária

Uma aplicação web simples para calcular a correção de valores com base em índices de inflação do Brasil. O projeto utiliza a biblioteca `ipeadatapy` para buscar os dados diretamente da API do IPEA, garantindo informações atualizadas e confiáveis.

---

### 🚀 [Acesse a aplicação ao vivo aqui!](https://calculadora-correcao-monetaria.onrender.com)

---

## ✨ Funcionalidades

-   Cálculo de correção monetária entre duas datas.
-   Utiliza dados oficiais do IPEA (Instituto de Pesquisa Econômica Aplicada).
-   Interface web simples e intuitiva.

## 🛠️ Tecnologias Utilizadas

-   **Backend:** Python, Flask
-   **Servidor de Produção:** Gunicorn
-   **Fonte de Dados:** `ipeadatapy` para consumir a API do IPEADATA.
-   **Frontend:** HTML, CSS

## ⚙️ Como Executar Localmente

Siga os passos abaixo para rodar o projeto em sua máquina.

**Pré-requisitos:**
*   [Python 3](https://www.python.org/downloads/)
*   `pip` (gerenciador de pacotes do Python)

**Passos:**

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/kenjitobr/calculadora_correcao_monetaria.git
    ```

2.  **Navegue até o diretório do projeto:**
    ```bash
    cd calculadora_correcao_monetaria
    ```

3.  **Crie e ative um ambiente virtual (virtualenv):**
    ```bash
    # Criar o ambiente
    python -m venv venv

    # Ativar no Windows
    .\venv\Scripts\activate

    # Ativar no Linux ou macOS
    source venv/bin/activate
    ```

4.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Execute a aplicação:**
    ```bash
    flask run
    ```

6.  **Abra seu navegador e acesse:**
    [http://127.0.0.1:5000](http://127.0.0.1:5000)

## 📊 Fonte dos Dados

Os dados de inflação são obtidos através da API do [IPEADATA](http://www.ipeadata.gov.br/), um serviço mantido pelo Instituto de Pesquisa Econômica Aplicada (IPEA).
