# Projeto de Automação de Testes — API Petstore e Web SauceDemo

![Python](https://img.shields.io/badge/Python-3.12%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![pytest](https://img.shields.io/badge/pytest-tests-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)
![Selenium](https://img.shields.io/badge/Selenium-WebDriver-43B02A?style=for-the-badge&logo=selenium&logoColor=white)
![Requests](https://img.shields.io/badge/requests-API%20tests-20232A?style=for-the-badge)
![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-CI-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)

Projeto de automação de testes desenvolvido em Python para demonstrar cobertura funcional em dois contextos comuns de QA: testes de API REST e testes end-to-end em interface web.

A solução valida operações da **Swagger Petstore API** e um fluxo completo de compra no **SauceDemo**, utilizando boas práticas como reutilização de cliente HTTP, Page Object Model, execução headless, evidências em screenshots e pipeline de integração contínua com GitHub Actions.

---

## Objetivo do projeto

O objetivo deste projeto é apresentar uma estrutura prática de automação de testes capaz de:

- validar contratos e comportamentos de uma API REST pública;
- automatizar um fluxo web completo em navegador real;
- organizar testes de forma legível e reutilizável;
- gerar evidências em falhas de interface;
- executar a suíte localmente ou em ambiente de CI.

Este repositório pode ser usado como base de estudo, demonstração técnica ou peça de portfólio para práticas de automação com Python.

---

## Tecnologias utilizadas

- **Python 3.12+** — linguagem principal do projeto
- **pytest** — framework de execução e organização dos testes
- **requests** — biblioteca para chamadas HTTP nos testes de API
- **Selenium WebDriver** — automação de navegador para testes web
- **pytest-html** — geração de relatório HTML da execução
- **python-dotenv** — leitura opcional de configurações locais
- **GitHub Actions** — pipeline de integração contínua

---

## Escopo dos testes

### API — Swagger Petstore

A suíte de API cobre os principais domínios da Petstore:

#### Pet

- criação de pet;
- atualização de pet;
- consulta de pet por ID;
- remoção de pet;
- consulta de pet inexistente;
- listagem de pets por status.

#### Store

- criação de pedido;
- consulta de pedido por ID;
- remoção de pedido;
- consulta de pedido inexistente;
- consulta do inventário da loja.

#### User

- criação de usuário;
- consulta de usuário;
- remoção de usuário;
- consulta de usuário inexistente.

Os testes usam identificadores únicos por execução para reduzir colisões de dados na API pública.

### Web — SauceDemo

A suíte web cobre um fluxo funcional de compra e validações negativas de autenticação:

- login com usuário padrão;
- adição do produto **Sauce Labs Backpack** ao carrinho;
- validação do produto no carrinho;
- preenchimento do checkout;
- validação de subtotal, imposto e total;
- finalização da compra;
- validação da mensagem final `Thank you for your order!`;
- login com campos obrigatórios vazios;
- login com credenciais inválidas;
- login com usuário bloqueado.

---

## Estrutura do projeto

```text
api/                    Cliente HTTP reutilizável da Petstore
pages/                  Page Objects e helpers Selenium
tests/api/              Testes automatizados da API Petstore
tests/web/              Testes automatizados do SauceDemo
screenshots/            Evidências automáticas de falhas web
docs/assets/            Prints usados neste README
.github/workflows/      Pipeline de CI
```

A estrutura separa responsabilidades para facilitar manutenção:

- testes de API ficam isolados dos testes web;
- interações com páginas ficam nos Page Objects;
- configurações são centralizadas por variáveis de ambiente;
- screenshots de falha são gerados automaticamente.

---

## Instalação

### 1. Clonar o repositório

```bash
git clone <url-do-repositorio>
cd PRojeto-automacao
```

### 2. Criar ambiente virtual

No Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

No Linux, macOS ou Git Bash:

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Instalar dependências

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

---

## Configuração

A execução local funciona com valores padrão públicos já configurados no projeto. Caso seja necessário sobrescrever algum valor, o projeto aceita variáveis de ambiente.

Variáveis disponíveis:

```env
PETSTORE_BASE_URL=https://petstore.swagger.io/v2
SAUCEDEMO_BASE_URL=https://www.saucedemo.com/
SAUCEDEMO_STANDARD_USER=standard_user
SAUCEDEMO_LOCKED_USER=locked_out_user
SAUCEDEMO_PASSWORD=secret_sauce
SAUCEDEMO_HEADLESS=false
SCREENSHOT_DIR=screenshots
```

Para execução sem abrir a janela do navegador, use:

```env
SAUCEDEMO_HEADLESS=true
```

O arquivo `env.example` contém um exemplo completo das variáveis suportadas.

---

## Execução dos testes

### Executar suíte completa

No Windows PowerShell:

```powershell
$env:SAUCEDEMO_HEADLESS="true"
pytest -q
```

No Linux, macOS ou Git Bash:

```bash
SAUCEDEMO_HEADLESS=true pytest -q
```

### Executar somente testes de API

```bash
pytest tests/api -q
```

### Executar somente testes Web

No Windows PowerShell:

```powershell
$env:SAUCEDEMO_HEADLESS="true"
pytest tests/web -q
```

No Linux, macOS ou Git Bash:

```bash
SAUCEDEMO_HEADLESS=true pytest tests/web -q
```

### Gerar relatório HTML

```bash
SAUCEDEMO_HEADLESS=true pytest tests/web -q --html=report.html --self-contained-html
```

O relatório será gerado como `report.html`.

---

## Evidências visuais do fluxo web

Os prints abaixo foram capturados durante a execução real do fluxo automatizado no SauceDemo.

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

## Evidências automáticas em falhas

Quando um teste web falha, o projeto salva automaticamente um screenshot da tela no momento da falha.

Diretório padrão:

```text
screenshots/
```

Os arquivos `.png` dessa pasta são ignorados pelo git para evitar versionar evidências temporárias de execução. A pasta permanece no repositório com `.gitkeep`.

Essa estratégia ajuda na análise de falhas em execuções locais e em pipeline CI.

---

## Integração contínua

O projeto possui pipeline configurado com GitHub Actions.

A execução acontece em:

- `push`;
- `pull_request`;
- execução manual via `workflow_dispatch`.

A pipeline possui dois jobs principais:

### API tests

- instala as dependências;
- configura a URL base da Petstore;
- executa `pytest tests/api -q`.

### Web tests

- instala as dependências;
- configura o Chrome;
- executa os testes web em modo headless;
- gera relatório HTML;
- publica relatório e screenshots como artifact da execução.

---

## Estratégia técnica

### Testes de API

Os testes de API utilizam um cliente HTTP reutilizável para centralizar:

- URL base;
- métodos `GET`, `POST`, `PUT` e `DELETE`;
- timeout padrão;
- conversão de resposta para JSON;
- logs de request e response;
- mensagens diagnósticas com método, endpoint, status esperado, status recebido e body da resposta.

Essa abordagem reduz repetição, melhora a legibilidade dos testes e facilita investigação de falhas.

### Testes Web

Os testes web seguem o padrão **Page Object Model**.

Com essa abordagem:

- seletores ficam encapsulados nas classes de página;
- ações comuns ficam centralizadas;
- esperas explícitas reduzem instabilidade;
- os testes descrevem o comportamento esperado em alto nível.

Isso torna a suíte mais fácil de manter quando a interface muda.

---

## Resultado esperado

Uma execução completa bem-sucedida deve finalizar com todos os testes passando.

Exemplo de comando:

```bash
SAUCEDEMO_HEADLESS=true pytest -q
```

Exemplo de resultado atual:

```text
14 passed
```

A quantidade de testes pode mudar conforme novos cenários forem adicionados.

---

## Pontos de destaque

- Cobertura combinando API REST e Web UI.
- Separação entre testes, clientes e Page Objects.
- Configuração por variáveis de ambiente.
- Screenshots automáticos em falhas web.
- Execução headless para CI.
- Pipeline com relatório HTML e artifacts.
- Mensagens de erro com contexto para facilitar análise.
