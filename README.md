# Mars Probe API

API REST para controlar sondas que exploram um planalto retangular em Marte.

## Tecnologias utilizadas

- **Python 3.11+**
- **FastAPI** — framework web
- **Uvicorn** — servidor ASGI
- **Pytest + HTTPX** — testes automatizados
- **Poetry** — gerenciamento de dependências (opcional, `requirements.txt` também disponível)

---

## Endpoints

| Método | Caminho | Descrição |
|--------|---------|-----------|
| `POST` | `/probes` | Lança uma sonda e configura o planalto |
| `PATCH` | `/probes/{id}/commands` | Envia comandos de movimento para uma sonda |
| `GET` | `/probes` | Lista todas as sondas e suas posições |

### Lançar uma sonda

```http
POST /probes
Content-Type: application/json

{
  "x": 5,
  "y": 5,
  "direction": "NORTH"
}
```

`x` e `y` definem o canto superior direito do planalto. A sonda sempre inicia em `(0, 0)`.

Direções válidas: `NORTH`, `EAST`, `SOUTH`, `WEST`.

### Mover uma sonda

```http
PATCH /probes/{id}/commands
Content-Type: application/json

{
  "commands": "MRM"
}
```

Comandos válidos: `M` (mover para frente), `L` (girar à esquerda), `R` (girar à direita).

Retorna `422` caso algum comando faça a sonda sair dos limites do planalto.

### Listar todas as sondas

```http
GET /probes
```

---

## Executando localmente

### Com pip

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux / macOS
source .venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Com Poetry

```bash
poetry install
poetry run uvicorn app.main:app --reload
```

A API estará disponível em `http://localhost:8000`.  
Documentação interativa: `http://localhost:8000/docs`.

---

## Executando os testes

```bash
pytest
```

---

## Executando com Docker

```bash
docker compose up --build
```
