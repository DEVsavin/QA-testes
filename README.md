# Automação de Testes — Petstore API & SauceDemo
 
![Python](https://img.shields.io/badge/Python-3.12%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![pytest](https://img.shields.io/badge/pytest-testes-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)
![Selenium](https://img.shields.io/badge/Selenium-WebDriver-43B02A?style=for-the-badge&logo=selenium&logoColor=white)
![Requests](https://img.shields.io/badge/requests-API%20tests-20232A?style=for-the-badge)
![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-CI-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)
 
Projeto de automação de testes cobrindo dois cenários comuns no dia a dia de QA:
 
- **Testes de API** usando a [Swagger Petstore](https://petstore.swagger.io/)
- **Testes Web** usando o [SauceDemo](https://www.saucedemo.com/)
O caminho principal de API segue o guia de Postman e GitHub Actions — uma collection é executada via Newman, localmente e na pipeline. Testes complementares em Python cobrem mais cenários com `pytest` e `requests`. Os testes web automatizam um fluxo completo de compra com Selenium e Page Object Model.
 
---
 
## Índice
 
- [O que é testado](#o-que-é-testado)
- [Tecnologias](#tecnologias)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [Como rodar](#como-rodar)
- [Evidências do fluxo web](#evidências-do-fluxo-web)
- [GitHub Actions](#github-actions)
---
 
## O que é testado
 
### API — Swagger Petstore
 
O caminho principal usa a collection Postman executada com Newman. Ela faz a requisição **Listar Pets Disponíveis** e valida:
 
- resposta com status `200`
- corpo da resposta é uma lista de pets
Os testes Python complementares cobrem os três recursos da API:
 
**Pet**
- Criar, atualizar, consultar e remover pet
- Consultar pet inexistente (espera `404`)
- Listar pets por status
**Store**
- Criar, consultar e remover pedido
- Consultar pedido inexistente (espera `404`)
- Consultar inventário da loja
**User**
- Criar, consultar e remover usuário
- Consultar usuário inexistente (espera `404`)
> Os dados são gerados de forma única a cada execução para evitar conflito com a API pública.
 
---
 
### Web — SauceDemo
 
**Fluxo de compra completo**
 
1. Login com usuário válido
2. Adicionar o produto **Sauce Labs Backpack** ao carrinho
3. Validar produto no carrinho
4. Preencher formulário de checkout
5. Conferir subtotal, imposto e total
6. Finalizar a compra
7. Validar mensagem `Thank you for your order!`
**Testes negativos de login**
 
- Campos obrigatórios vazios
- Credenciais inválidas
- Usuário bloqueado
> Quando um teste web falha, um screenshot da tela é salvo automaticamente em `screenshots/`.
 
---
 
## Tecnologias
 
| Ferramenta | Uso |
|---|---|
| Python 3.12+ | Linguagem principal |
| pytest | Organização e execução dos testes |
| requests | Chamadas HTTP nos testes de API |
| Postman / Newman | Collection e execução da API principal |
| Selenium WebDriver | Automação dos testes web |
| pytest-html | Relatório HTML da execução web |
| python-dotenv | Variáveis de ambiente |
| GitHub Actions | Integração contínua |
 
---
 
## Estrutura do projeto
 
```
api/                        Cliente HTTP da Petstore (testes Python)
pages/                      Page Objects dos testes web
│   ├── base_page.py
│   ├── login_page.py
│   ├── cart_page.py
│   └── checkout_page.py
tests/
│   ├── api/
│   │   ├── test_pet.py
│   │   ├── test_store.py
│   │   ├── test_user.py
│   │   ├── test_api_support.py
│   │   └── helpers.py
│   └── web/
│       ├── test_compra.py
│       └── test_login_negativo.py
screenshots/                Screenshots automáticos em falhas web
docs/assets/                Prints do fluxo web (para o README)
.github/workflows/          Pipeline do GitHub Actions
petstore_collection.json    Collection Postman usada pelo Newman
config.py                   Configurações do projeto
conftest.py                 Fixtures do pytest
requirements.txt            Dependências Python
pytest.ini                  Configurações do pytest
env.example                 Variáveis de ambiente disponíveis
```
 
---
 
## Instalação
 
### 1. Clonar o repositório
 
```bash
git clone https://github.com/DEVsavin/QA-testes.git
cd QA-testes
```
 
### 2. Criar ambiente virtual
 
**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```
 
**Linux / macOS / Git Bash:**
```bash
python -m venv venv
source venv/bin/activate
```
 
### 3. Instalar dependências
 
```bash
pip install --upgrade pip
pip install -r requirements.txt
```
 
> Para rodar a collection Postman não é necessário instalar o Newman manualmente. O `npx` baixa e executa automaticamente.
 
---
 
## Configuração
 
O projeto funciona com os valores padrão das APIs públicas. Se precisar ajustar algo, crie um arquivo `.env` na raiz do projeto baseado no `env.example`:
 
```env
PETSTORE_BASE_URL=https://petstore.swagger.io/v2
SAUCEDEMO_BASE_URL=https://www.saucedemo.com/
SAUCEDEMO_STANDARD_USER=standard_user
SAUCEDEMO_LOCKED_USER=locked_out_user
SAUCEDEMO_PASSWORD=secret_sauce
SAUCEDEMO_HEADLESS=false
SCREENSHOT_DIR=screenshots
```
 
Para rodar os testes web sem abrir o navegador, defina:
 
```env
SAUCEDEMO_HEADLESS=true
```
 
---
 
## Como rodar
 
### API principal — Postman/Newman
 
```bash
npx newman run petstore_collection.json --reporters cli
```
 
Resultado esperado:
```
requests: executed 1, failed 0
assertions: executed 2, failed 0
```
 
As duas validações da collection são:
- `Status code é 200`
- `A resposta deve ser uma lista de pets`
---
 
### Testes de API — pytest
 
```bash
pytest tests/api -v
```
 
---
 
### Testes web
 
**Windows (PowerShell):**
```powershell
$env:SAUCEDEMO_HEADLESS="true"
pytest tests/web -v
```
 
**Linux / macOS / Git Bash:**
```bash
SAUCEDEMO_HEADLESS=true pytest tests/web -v
```
 
---
 
### Suite completa (API + Web)
 
```bash
SAUCEDEMO_HEADLESS=true pytest -v
```
 
---
 
### Relatório HTML
 
```bash
SAUCEDEMO_HEADLESS=true pytest tests/web -v --html=report.html --self-contained-html
```
 
O relatório será gerado em `report.html`.
 
---
 
## Evidências do fluxo web
 
### 1. Tela de login
 
![Tela de login do SauceDemo](docs/assets/saucedemo-login.png)
 
### 2. Lista de produtos após login
 
![Lista de produtos do SauceDemo](docs/assets/saucedemo-produtos.png)
 
### 3. Produto adicionado ao carrinho
 
![Carrinho com produto adicionado](docs/assets/saucedemo-carrinho.png)
 
### 4. Revisão do checkout
 
![Revisão do checkout](docs/assets/saucedemo-checkout.png)
 
### 5. Compra finalizada
 
![Confirmação da compra finalizada](docs/assets/saucedemo-confirmacao.png)
 
---
 
## GitHub Actions
 
A pipeline roda automaticamente em `push`, `pull_request` e execução manual via `workflow_dispatch`.
 
Ela tem **dois jobs independentes**:
 
**Job 1 — Testes de API (Postman/Newman)**
- Instala Node.js
- Instala Newman
- Executa `petstore_collection.json`
- Valida as duas assertions da collection
**Job 2 — Testes Web**
- Instala dependências Python
- Configura o Chrome em modo headless
- Executa os testes web com pytest
- Gera relatório HTML
- Publica relatório e screenshots como artifact do workflow
---
 
## Screenshots em falha
 
Quando um teste web falha, o projeto salva automaticamente um screenshot da tela no diretório `screenshots/`. Os arquivos `.png` não são versionados — a pasta existe no repositório com um `.gitkeep` apenas para manter a estrutura.
