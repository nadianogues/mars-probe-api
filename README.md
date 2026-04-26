# Mars Probe API 🔴

Uma API REST desenvolvida em Python com FastAPI para controlar sondas enviadas em missão a Marte. O projeto explora um planalto retangular usando uma malha de coordenadas X e Y, com foco em código limpo, testável e bem estruturado.

---

## 📋 Funcionalidades

- **Lançar Sonda:** Cria uma nova sonda com ID único e define o tamanho do planalto
- **Mover Sonda:** Executa comandos de movimento (M), rotação à esquerda (L) e rotação à direita (R)
- **Listar Sondas:** Retorna o estado atual de todas as sondas lançadas
- **Validação Robusta:** Controle de limites do planalto, validação de comandos e tratamento de erros

---

## 🏗️ Arquitetura

O projeto segue uma **arquitetura em camadas** com separação clara de responsabilidades:

```
mars-probe-api/
├── app/
│   ├── main.py                  # Entry point da aplicação
│   ├── models/
│   │   └── probe.py             # Entidades de domínio (Probe, Direction)
│   ├── schemas/
│   │   └── probe.py             # Contratos HTTP (request/response)
│   ├── services/
│   │   └── probe_service.py     # Lógica de negócio
│   └── routers/
│       └── probes.py            # Endpoints REST
├── tests/
│   ├── conftest.py              # Fixtures compartilhadas
│   └── test_probes.py           # Testes automatizados
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
└── requirements.txt
```

### 🔄 Fluxo de Dados

```
HTTP Request
     ↓
routers/probes.py         → Recebe e valida a requisição (Pydantic)
     ↓
services/probe_service.py → Executa a lógica de negócio
     ↓
models/probe.py           → Representa o estado da sonda
     ↓
HTTP Response             → JSON serializado automaticamente pelo FastAPI
```

---

## 💾 Armazenamento

O projeto utiliza **armazenamento em memória** (dicionário Python). Essa escolha foi intencional — o desafio não exige persistência e mantém o foco na arquitetura e na lógica de negócio. Em produção, a camada de serviço poderia ser facilmente adaptada para usar PostgreSQL ou Redis sem alterar os endpoints.

---

## 🚀 Como Executar

### 🐳 Opção 1: Docker (Recomendado)

```bash
# Construir e executar
docker compose up --build

# Parar quando terminar
docker compose down
```

### 💻 Opção 2: Execução Local

```bash
# 1. Criar ambiente virtual
python -m venv .venv

# Windows
.venv\Scripts\activate
# Linux / macOS
source .venv/bin/activate

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Executar a aplicação
uvicorn app.main:app --reload
```

A API estará disponível em `http://localhost:8000`.

---

## 📚 Documentação Interativa

Com a aplicação rodando, acesse:

- **Swagger UI:** `http://localhost:8000/docs` — testar endpoints interativamente
- **ReDoc:** `http://localhost:8000/redoc` — documentação detalhada

---

## 🔌 Endpoints

### 1. Lançar Sonda

```
POST /probes
```

```json
{
  "x": 5,
  "y": 5,
  "direction": "NORTH"
}
```

`x` e `y` definem o canto superior direito do planalto. A sonda sempre inicia em `(0, 0)`.

Resposta:

```json
{
  "id": "abc123",
  "x": 0,
  "y": 0,
  "direction": "NORTH"
}
```

---

### 2. Mover Sonda

```
POST /probes/{id}/commands
```

```json
{
  "commands": "MRM"
}
```

Resposta:

```json
{
  "id": "abc123",
  "x": 1,
  "y": 1,
  "direction": "EAST"
}
```

---

### 3. Listar Todas as Sondas

```
GET /probes
```

Resposta:

```json
{
  "probes": [
    {
      "id": "abc123",
      "x": 1,
      "y": 1,
      "direction": "EAST"
    }
  ]
}
```

---

## 🗺️ Funcionamento do Plateau

A sonda sempre inicia em `(0, 0)` no canto inferior esquerdo. O plateau é definido pelo canto superior direito `(x, y)`:

```
Y
5 +---+---+---+---+---+---+(5,5)
  |   |   |   |   |   |   |
4 +---+---+---+---+---+---+
  |   |   |   |   |   |   |
3 +---+---+---+---+---+---+
  |   |   |   |   |   |   |
2 +---+---+---+---+---+---+
  |   |   |   |   |   |   |
1 +---+---+---+---+---+---+
  |   | > |   |   |   |   |   ← após "MRM" (1,1,EAST)
0 +---+---+---+---+---+---+
  0   1   2   3   4   5   X
```

Se qualquer comando da sequência fizer a sonda sair dos limites, **nenhum comando é executado** e a API retorna erro `400`.

---

## 🎮 Comandos de Movimento

| Comando | Descrição |
|---|---|
| `M` | Move a sonda 1 espaço na direção atual |
| `L` | Rotaciona 90° para a esquerda (sem mover) |
| `R` | Rotaciona 90° para a direita (sem mover) |

| Direção Atual | L | R |
|---|---|---|
| NORTH | WEST | EAST |
| EAST | NORTH | SOUTH |
| SOUTH | EAST | WEST |
| WEST | SOUTH | NORTH |

---

## ⚠️ Exemplos de Erro

### Sonda não encontrada (404)
```bash
curl -X POST "http://localhost:8000/probes/id-inexistente/commands" \
     -H "Content-Type: application/json" \
     -d '{"commands": "M"}'
```
```json
{ "detail": "Probe not found." }
```

### Movimento fora dos limites (400)
```bash
curl -X POST "http://localhost:8000/probes/{id}/commands" \
     -H "Content-Type: application/json" \
     -d '{"commands": "LLM"}'
```
```json
{ "detail": "Command 'M' at (0, 0) facing SOUTH would move the probe out of the plateau bounds." }
```

### Dados inválidos (422)
```bash
curl -X POST "http://localhost:8000/probes" \
     -H "Content-Type: application/json" \
     -d '{"x": 5, "y": 5, "direction": "INVALIDA"}'
```
```json
{ "detail": "Input should be 'NORTH', 'EAST', 'SOUTH' or 'WEST'" }
```

---

## 💡 Exemplos com cURL

```bash
# 1. Lançar uma sonda
curl -X POST "http://localhost:8000/probes" \
     -H "Content-Type: application/json" \
     -d '{"x": 5, "y": 5, "direction": "NORTH"}'

# 2. Mover a sonda (substitua {id} pelo id retornado)
curl -X POST "http://localhost:8000/probes/{id}/commands" \
     -H "Content-Type: application/json" \
     -d '{"commands": "MRM"}'

# 3. Listar todas as sondas
curl -X GET "http://localhost:8000/probes"
```

---

## 🧪 Testes

```bash
# Executar todos os testes
pytest

# Com detalhes
pytest -v

# Com cobertura
pytest --cov=app
```

O projeto possui **15 testes** cobrindo todos os endpoints e casos de erro:

- ✅ Lançar sonda com configuração válida
- ✅ Garantir que cada sonda recebe um id único
- ✅ Rejeitar direção inválida
- ✅ Rejeitar plateau com tamanho inválido
- ✅ Mover sonda com sequência válida
- ✅ Garantir que sonda não move após sequência inválida
- ✅ Retornar 404 para sonda inexistente
- ✅ Rejeitar comandos inválidos
- ✅ Acumular movimentos em sequências múltiplas
- ✅ Listar sondas (vazia, uma, múltiplas)
- ✅ Rejeitar movimento fora dos limites em todas as direções (NORTH, EAST, WEST)

---

## ⚙️ Solução de Problemas

### Erro `unrecognized arguments: --cov=app`
O plugin de cobertura não está instalado. Ative o ambiente virtual e instale:
```bash
# Windows
.venv\Scripts\activate

# Linux / macOS
source .venv/bin/activate

# Instalar o plugin
pip install pytest-cov
```

### Erro `command not found: uvicorn` ou `pytest`
O ambiente virtual não está ativado. Ative antes de rodar qualquer comando:
```bash
# Windows
.venv\Scripts\activate

# Linux / macOS
source .venv/bin/activate
```

### Erro `Port 8000 already in use`
Outra aplicação está usando a porta. Encerre o processo atual e tente novamente:

```bash
# Se estiver rodando local
Ctrl+C

# Se estiver rodando no Docker
docker compose down
```

Ou troque a porta:
```bash
uvicorn app.main:app --reload --port 8001
```

### Erro `ModuleNotFoundError`
As dependências não foram instaladas. Rode:
```bash
pip install -r requirements.txt
```

### Docker: `docker compose` não reconhecido
Versões antigas do Docker usam `docker-compose` (com hífen):
```bash
docker-compose up --build
```

---

## 🔧 Tecnologias Utilizadas

| Tecnologia | Uso |
|---|---|
| Python 3.11+ | Linguagem principal |
| FastAPI | Framework web |
| Pydantic | Validação de dados |
| Uvicorn | Servidor ASGI |
| Pytest | Testes automatizados |
| Poetry | Gerenciamento de dependências |
| Docker | Containerização |

---

## 🌿 Git Flow

O projeto foi desenvolvido com branches separadas por feature:

```
main
 └── develop
      ├── feat/launch-probe
      ├── feat/move-probe
      ├── feat/list-probes
      └── feat/improve-tests
```

Cada branch foi mergeada na `develop` após os testes passarem, e ao final mergeada na `main`.
