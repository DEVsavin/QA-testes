# Projeto de Automação — API Petstore + Web SauceDemo

 automação de testes com **pytest**, **requests** e **Selenium**.

O projeto cobre dois alvos:

- **API:** Swagger Petstore (`https://petstore.swagger.io/v2`)
- **Web:** SauceDemo (`https://www.saucedemo.com/`)

A automação foi organizada com cliente reutilizável para API, Page Objects para Web, screenshots automáticos em falhas Web e workflow GitHub Actions preparado para execução em CI.

## Tecnologias

- Python
- pytest
- requests
- Selenium
- webdriver-manager
- python-dotenv
- GitHub Actions

## Estrutura principal

```text
api/
  petstore_client.py        # Cliente HTTP reutilizável da Swagger Petstore
pages/
  base_page.py              # Helpers Selenium com esperas explícitas
  login_page.py             # Page Object de login SauceDemo
  cart_page.py              # Page Object de carrinho
  checkout_page.py          # Page Object de checkout
screenshots/
  .gitkeep                  # Pasta usada para evidências de falha Web
tests/
  api/
    test_pet.py             # Cobertura do domínio Pet
    test_store.py           # Cobertura do domínio Store
    test_user.py            # Cobertura do domínio User
  web/
    test_compra.py          # Fluxo completo de compra SauceDemo
    test_login_negativo.py  # Negativos de login
.github/workflows/
  tests.yml                 # Pipeline API + Web headless
```

## Instalação

### 1. Criar e ativar ambiente virtual

No Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

No Git Bash/Linux/macOS:

```bash
python -m venv venv
source venv/bin/activate
```

### 2. Instalar dependências

```bash
python -m pip install -r requirements.txt
```

## Configuração por ambiente

O arquivo `env.example` mostra todas as variáveis suportadas.

Valores padrão públicos de treino já existem no código, então a execução local funciona sem `.env` na maioria dos casos. Se quiser sobrescrever algo, crie um `.env` local com base no `env.example`.

Principais variáveis:

```env
PETSTORE_BASE_URL=https://petstore.swagger.io/v2
SAUCEDEMO_BASE_URL=https://www.saucedemo.com/
SAUCEDEMO_STANDARD_USER=standard_user
SAUCEDEMO_LOCKED_USER=locked_out_user
SAUCEDEMO_PASSWORD=secret_sauce
SAUCEDEMO_HEADLESS=false
SCREENSHOT_DIR=screenshots
```

Para CI ou execução sem abrir navegador, use:

```env
SAUCEDEMO_HEADLESS=true
```

## Como executar os testes

### API Petstore

```bash
pytest tests/api -q
```

Cobertura prática:

- `Pet`: criar, atualizar, consultar, remover, buscar por status e validar pet inexistente.
- `Store`: criar pedido, consultar pedido, remover pedido, consultar inventário e validar pedido inexistente.
- `User`: criar usuário, consultar usuário, remover usuário e validar usuário inexistente.

Os testes usam dados únicos por execução para reduzir colisão na Petstore pública.

### Web SauceDemo

No Windows:

```powershell
$env:SAUCEDEMO_HEADLESS="true"
pytest tests/web -q
```

No Git Bash/Linux/macOS:

```bash
SAUCEDEMO_HEADLESS=true pytest tests/web -q
```

Cobertura Web:

- Login com usuário padrão.
- Adição do produto Sauce Labs Backpack ao carrinho.
- Checkout com nome, sobrenome e CEP.
- Revisão de subtotal, imposto e total.
- Finalização da compra.
- Validação da confirmação final: `Thank you for your order!`.
- Negativos de login:
  - campos obrigatórios vazios;
  - credenciais inválidas;
  - usuário bloqueado.

### Suíte completa

No Windows:

```powershell
$env:SAUCEDEMO_HEADLESS="true"
pytest -q
```

No Git Bash/Linux/macOS:

```bash
SAUCEDEMO_HEADLESS=true pytest -q
```

## Screenshots de falha Web

Falhas em testes Web que usam a fixture `driver` geram screenshots automaticamente na pasta:

```text
screenshots/
```

Os arquivos `.png` gerados são ignorados pelo git para evitar sujeira no repositório. A pasta é preservada por `screenshots/.gitkeep`.

No GitHub Actions, screenshots são enviados como artifact chamado `web-test-screenshots` quando o job Web falha.

## GitHub Actions

A workflow está em:

```text
.github/workflows/tests.yml
```

Ela roda em:

- `push`
- `pull_request`
- execução manual por `workflow_dispatch`

Jobs configurados:

1. **API tests**
   - instala dependências;
   - executa `pytest tests/api -q`.

2. **Web tests**
   - instala dependências;
   - define `SAUCEDEMO_HEADLESS=true`;
   - executa `pytest tests/web -q`;
   - publica `screenshots/` como artifact se houver falha.

A workflow não usa `continue-on-error`; falhas reais quebram o pipeline.

## Estratégia de automação

### API

A API usa `api/petstore_client.py` para centralizar:

- base URL;
- métodos `GET`, `POST`, `PUT`, `DELETE`;
- timeout padrão;
- parsing JSON;
- mensagens diagnósticas com método, endpoint, status esperado, status recebido e body.

Isso evita `requests` espalhado pelos testes e deixa as falhas mais claras.

### Web

A Web usa Page Object Model:

- `BasePage` concentra esperas explícitas e ações comuns;
- `LoginPage`, `CartPage` e `CheckoutPage` concentram seletores e interações;
- os testes ficam focados no comportamento esperado.



