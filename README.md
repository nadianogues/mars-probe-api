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
routers/probes.py       → Recebe e valida a requisição (Pydantic)
     ↓
services/probe_service.py → Executa a lógica de negócio
     ↓
models/probe.py          → Representa o estado da sonda
     ↓
HTTP Response            → JSON serializado automaticamente pelo FastAPI
```

### 🎯 Princípios Aplicados

- **Separação entre `models` e `schemas`:** `models` representa o domínio interno, `schemas` representa o contrato com o cliente HTTP
- **Single Responsibility:** Cada arquivo tem uma única responsabilidade
- **Clean Code:** Código legível, com type hints e docstrings em todas as funções

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

- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

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

## 🎮 Comandos de Movimento

| Comando | Descrição |
|---|---|
| `M` | Move a sonda 1 espaço na direção atual |
| `L` | Rotaciona 90° para a esquerda (sem mover) |
| `R` | Rotaciona 90° para a direita (sem mover) |

### Tabela de Rotação

| Direção Atual | L | R |
|---|---|---|
| NORTH | WEST | EAST |
| EAST | NORTH | SOUTH |
| SOUTH | EAST | WEST |
| WEST | SOUTH | NORTH |

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

O projeto possui **12 testes** cobrindo todos os endpoints e casos de erro:

- ✅ Lançar sonda com configuração válida
- ✅ Mover sonda com sequência válida
- ✅ Rejeitar movimento que ultrapassa os limites do planalto
- ✅ Retornar 404 para sonda inexistente
- ✅ Rejeitar comandos inválidos
- ✅ Listar sondas (vazia, uma, múltiplas)

---

## 🔧 Tecnologias Utilizadas

| Tecnologia | Uso |
|---|---|
| Python 3.11+ | Linguagem principal |
| FastAPI | Framework web |
| Pydantic | Validação de dados |
| Uvicorn | Servidor ASGI |
| Pytest | Testes automatizados |
| Poetry | Gerenciamento de dependências (fonte da verdade) |
| requirements.txt | Gerado pelo Poetry para compatibilidade sem Poetry instalado |
| Docker | Containerização |

---

## 🌿 Git Flow

O projeto foi desenvolvido seguindo Git Flow com branches separadas por feature:

```
main
 └── develop
      ├── feat/launch-probe
      ├── feat/move-probe
      └── feat/list-probes
```

Cada branch foi mergeada na `develop` após os testes passarem, e ao final mergeada na `main`.
