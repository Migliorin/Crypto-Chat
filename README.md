# 1. Crypto-Chat

CryptChat é uma aplicação de chat segura que utiliza criptografia de ponta a ponta para garantir a privacidade das mensagens. A aplicação é construída em Python e utiliza a biblioteca FastAPI para fornecer uma interface web interativa.

# 2. Estrutura do Projeto
O projeto está organizado nas seguintes pastas:

- **crypto**: Contém o código responsável pela criptografia de mensagens e geração de chaves pública e estrangeira.
- **interface**: Contém o código da interface gráfica do CryptChat.
- **notebooks**: Contém Jupyter Notebooks utilizados para testar funcionalidades, mas não é essencial para o projeto.
- **server**: Contém o código responsável pelo controle dos dados do servidor.
- **user**: Contém o código do objeto de usuário para facilitar a manipulação das informações.
- **main.py**: Arquivo principal responsável por iniciar o servidor FastAPI.

```plaintext
CryptChat/
    |-- crypto/
    |   |-- (código para criptografia e geração de chaves)
    |
    |-- interface/
    |   |-- (código da interface gráfica)
    |
    |-- notebooks/
    |   |-- (Jupyter Notebooks para testes)
    |
    |-- server/
    |   |-- (código de controle dos dados do servidor)
    |
    |-- user/
    |   |-- (código do objeto de usuário)
    |
    |-- main.py
```

# 3. Instalação
1. Clone o repositório
   ```bash
    git clone https://github.com/seu-usuario/CryptChat.git
    cd CryptChat
   ```
2. Instale as dependências
   1. Somente a interface gráfica (front-end)
   ```bash
   pip install PySimpleGUI
   pip install requests
   ```
   2. Somente o servidor (back-end)
   ```bash
   pip install fastapi
   pip install "uvicorn[standard]"
   ```

# 4. Execução dos codigos
Para executar cada parte do projeto, siga as instruções abaixo:

## 4.1 Front-end
Certifique-se de estar na raiz do projeto antes de executar o seguinte comando:

```bash
python interface/main.py
```

Este comando iniciará a interface gráfica do CryptChat.

## 4.2 Back-end
Certifique-se de estar na raiz do projeto antes de executar o seguinte comando:

```bash
uvicorn main:app --reload
```

Este comando iniciará o servidor FastAPI, permitindo a comunicação entre a interface gráfica e os componentes de criptografia do CryptChat.

Lembre-se de executar esses comandos em terminais separados para garantir que tanto o front-end quanto o back-end estejam em execução simultaneamente.