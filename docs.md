# Documentação da API

Esta documentação tem como finalidade apresentar os endpoints disponíveis na API de Catálogo Musical, detalhando seu funcionamento, os parâmetros necessários, os formatos de requisição e resposta, além dos possíveis erros retornados. A API foi desenvolvida para fornecer acesso a um catálogo musical com funcionalidades de rede social, permitindo a consulta de artistas, lançamentos, faixas, avaliações e perfis de usuários.

## Primeiros Passos

1. **Clone o repositório**  
   ```bash
   git clone <URL_DO_SEU_REPO>
   cd <PASTA_DO_REPO>
    ```

2. **Crie o arquivo `.env` na raiz do projeto**
   Preencha com suas credenciais:

   ```env
   MONGODB_USERNAME=
   MONGODB_PASSWORD=
   NEO4J_USERNAME=
   NEO4J_PASSWORD=
   ```

3. **Instale as dependências**

   ```bash
   pip install -r requirements.txt
   ```

4. **Inicie a aplicação**

   ```bash
   python src/app/main.py
   ```

5. **Acesse no navegador**
   A API estará disponível em:

   ```
   http://127.0.0.1:5000
   ```

## ENDPOINTS

### 🎤 Artistas
#### `GET /v1/artists/<artist_id>`
**Descrição**  
Retorna as informações de um artista (nome, gêneros, bio, seguidores, média de avaliações e prévia de lançamentos).

**Parâmetros de rota**  
- `artist_id` (string): ID do artista no MongoDB.

**Resposta 200 OK**  
```json
{
  "id": "abc123",
  "name": "Arctic Monkeys",
  "genres": ["rock","indie"],
  "bio": "Banda inglesa formada em Sheffield...",
  "qt_followers": 824,
  "average_rating": 4.2,
  "releases": [
    {
      "id": "rel001",
      "name": "AM",
      "release_year": 2013
    }
  ]
}
````

**Erros possíveis**

* `404 Not Found`: artista não encontrado.

---

#### `GET /v1/artists/<artist_id>/tracks`

**Descrição**
Retorna todas as faixas de um artista, agrupadas por nome da faixa e listando em quais lançamentos ela aparece, ordenadas alfabeticamente.

**Parâmetros de rota**

* `artist_id` (string): ID do artista.

**Resposta 200 OK**

```json
{
  "artist": {
    "id": "abc123",
    "name": "Arctic Monkeys"
  },
  "items": [
    {
      "name": "Do I Wanna Know?",
      "releases": [
        {
          "id": "rel001",
          "name": "AM"
        }
      ]
    }
  ]
}

```


**Erros possíveis**

* `404 Not Found`: artista não encontrado.

---

### 💿 Lançamentos (Releases)

#### `GET /v1/releases/<release_id>`

**Descrição**
Retorna detalhes de um lançamento (nome, data, artista, lista de faixas e média de avaliações).

**Parâmetros de rota**

* `release_id` (string): ID do lançamento.

**Resposta 200 OK**

```json
{
  "id": "rel001",
  "name": "AM",
  "artist": {
    "id": "abc123",
    "name": "Arctic Monkeys"
  },
  "release_date": "2013-09-09",
  "rating_average": 4.4,
  "tracks": [
    {
      "index": 1,
      "name": "Do I Wanna Know?",
      "duration": 272
    }
  ]
}
```

**Erros possíveis**

* `404 Not Found`: lançamento não encontrado.

---

#### `GET /v1/releases/<release_id>/ratings`

**Descrição**
Retorna todas as avaliações de usuários para um lançamento.

**Parâmetros de rota**

* `release_id` (string): ID do lançamento.

**Resposta 200 OK**

```json
{
  "release": {
    "id": "rel001",
    "name": "AM",
    "artist": "Arctic Monkeys"
  },
  "items": [
    {
      "username": "user123",
      "rating": 4.5
    }
  ]
}
```

**Erros possíveis**

* `404 Not Found`: lançamento não encontrado.

---

### 🧑‍🤝‍🧑 Usuários (Users)

#### `GET /v1/users/<username>`

**Descrição**
Retorna dados do usuário (username, nome, bio, quantidade de amigos, avaliações e follows).

**Parâmetros de rota**

* `username` (string)

**Resposta 200 OK**

```json
{
  "username": "johndoe",
  "name": "John Doe",
  "bio": "Apaixonado por música...",
  "qt_friends": 5,
  "qt_ratings": 10,
  "qt_follows": 3
}
```

**Erros possíveis**

* `404 Not Found`: usuário não encontrado.

---

#### `GET /v1/users/<username>/friends`

**Descrição**
Lista todos os amigos de um usuário.

**Parâmetros de rota**

* `username` (string)

**Resposta 200 OK**

```json
{
  "username": "johndoe",
  "items": ["alice","bob","charlie"]
}
```

**Erros possíveis**

* `404 Not Found`: usuário não encontrado.

---

#### `GET /v1/users/<username>/ratings`

**Descrição**
Lista todas as avaliações feitas por um usuário.

**Parâmetros de rota**

* `username` (string)

**Resposta 200 OK**

```json
{
  "username": "johndoe",
  "items": [
    {"id":"rel001","artist":"Arctic Monkeys","name":"AM","rating":4.5},
    ...
  ]
}
```

**Erros possíveis**

* `404 Not Found`: usuário não encontrado.

---

#### `GET /v1/users/<username>/follows`

**Descrição**
Lista todos os artistas seguidos por um usuário.

**Parâmetros de rota**

* `username` (string)

**Resposta 200 OK**

```json
{
  "username": "johndoe",
  "items": [
    {"id":"art123","name":"Arctic Monkeys"},
    ...
  ]
}
```

**Erros possíveis**

* `404 Not Found`: usuário não encontrado.

---

#### `POST /v1/users`

**Descrição**
Registra um novo usuário.

**Body (JSON)**

```json
{
  "username": "johndoe",
  "password": "senha123",
  "name": "John Doe",       // opcional
  "bio": "Ama rock clássico" // opcional
}
```

**Resposta 201 Created**

* Sem conteúdo no body.

**Erros possíveis**

* `400 Bad Request`: campo obrigatório faltando.
* `409 Conflict`: usuário já existe.

---


#### `DELETE /v1/users/<username>`
**Descrição**  
Remove completamente um usuário, suas amizades, avaliações e follows, tanto em MongoDB quanto em Neo4j.

**Parâmetros de rota**  
- `username` (string): nome de usuário a ser deletado.

**Resposta 200 OK**  
- Sem conteúdo no body.

**Erros possíveis**  
- `404 Not Found`: usuário não encontrado.

---

#### `PATCH /v1/users/<username>`
**Descrição**  
Atualiza senha, nome ou bio de um usuário. Campos não informados permanecem inalterados; valores vazios removem o campo.

**Parâmetros de rota**  
- `username` (string): nome de usuário a ser atualizado.

**Body (JSON)**  
```json
{
  "password": "novasenha",  // opcional
  "name": "Novo Nome",      // opcional (string vazia para remover)
  "bio": "Nova bio"         // opcional (string vazia para remover)
}
````

**Resposta 200 OK**

* Sem conteúdo no body.

**Erros possíveis**

* `404 Not Found`: usuário não encontrado.
* `400 Bad Request`: nenhum campo válido fornecido.

---

#### `POST /v1/users/<username>/ratings`

**Descrição**
Adiciona uma avaliação a um lançamento para o usuário, atualizando MongoDB e Neo4j.

**Parâmetros de rota**

* `username` (string): nome de usuário que avalia.

**Body (JSON)**

```json
{
  "id": "rel001",     // ID do release
  "rating": 4.5       // nota (número)
}
```


**Resposta 201 Created**

* Sem conteúdo no body.

**Erros possíveis**

* `400 Bad Request`: campo obrigatório faltando (`id` ou `rating`).
* `404 Not Found`: usuário ou release não encontrados.
* `409 Conflict`: avaliação já existe para este usuário e release.

---

#### `DELETE /v1/users/<username>/ratings/<release_id>`

**Descrição**
Remove a avaliação de um lançamento feito pelo usuário, tanto em MongoDB quanto em Neo4j.

**Parâmetros de rota**

* `username` (string)
* `release_id` (string)

**Resposta 200 OK**

* Sem conteúdo no body.

**Erros possíveis**

* `404 Not Found`: usuário, release ou avaliação não encontrados.

---

#### `POST /v1/users/<username>/follows`

**Descrição**
Faz o usuário seguir um artista. Incrementa contador de seguidores e cria relacionamento em Neo4j.

**Parâmetros de rota**

* `username` (string)

**Body (JSON)**

```json
{
  "id": "art123"   // ID do artista
}
```

**Resposta 201 Created**

* Sem conteúdo no body.

**Erros possíveis**

* `400 Bad Request`: campo `id` faltando.
* `404 Not Found`: usuário ou artista não encontrados.
* `409 Conflict`: já existe follow para este usuário e artista.

---

#### `DELETE /v1/users/<username>/follows/<artist_id>`

**Descrição**
Faz o usuário deixar de seguir um artista. Decrementa contador de seguidores e remove relacionamento em Neo4j.

**Parâmetros de rota**

* `username` (string)
* `artist_id` (string)

**Resposta 200 OK**

* Sem conteúdo no body.

**Erros possíveis**

* `404 Not Found`: usuário, artista ou relacionamento follow não encontrados.

---

#### `POST /v1/users/<username>/friends`

**Descrição**
Adiciona outro usuário como amigo (bidirecional) em MongoDB e cria relacionamento em Neo4j.

**Parâmetros de rota**

* `username` (string)

**Body (JSON)**

```json
{
  "username": "friendUser"   // nome de usuário do amigo
}
```

**Resposta 201 Created**

* Sem conteúdo no body.

**Erros possíveis**

* `400 Bad Request`: campo `username` faltando.
* `404 Not Found`: usuário ou amigo não encontrados.
* `409 Conflict`: amizade já existe.

---

#### `DELETE /v1/users/<username>/friends/<friend_username>`

**Descrição**
Remove a amizade entre dois usuários, tanto em MongoDB quanto em Neo4j.

**Parâmetros de rota**

* `username` (string)
* `friend_username` (string)

**Resposta 200 OK**

* Sem conteúdo no body.

**Erros possíveis**

* `404 Not Found`: usuário, amigo ou relacionamento de amizade não encontrados.

---

### 🔁 Recomendações (Recs)

#### `GET /v1/recs/<username>/artists`
**Descrição**  
Sugere um artista baseado no gênero musical mais seguido pelo usuário.

**Parâmetros de rota**  
- `username` (string): nome do usuário.

**Resposta 200 OK**  
```json
{
  "artist": {
    "id": "art123",
    "name": "Arctic Monkeys",
    "bio": "Banda inglesa formada em Sheffield..."
  },
  "by": {
    "genre": "rock"
  }
}
````

**Erros possíveis**

* `404 Not Found`: usuário não existe.
* `404 Not Found`: sem dados de gênero (usuário não segue artistas).
* `404 Not Found`: sem recomendações para o gênero.

---

#### `GET /v1/recs/<username>/releases/friends`

**Descrição**
Sugere um lançamento que algum amigo avaliou positivamente (nota ≥ 6).

**Parâmetros de rota**

* `username` (string): nome do usuário.

**Resposta 200 OK**

```json
{
  "release": {
    "id": "rel001",
    "name": "AM",
    "artist": "Arctic Monkeys"
  },
  "by": {
    "username": "alice",
    "rating": 9
  }
}
```

**Erros possíveis**

* `404 Not Found`: usuário não existe.
* `404 Not Found`: nenhum friend review encontrado.

---

#### `GET /v1/recs/<username>/friends?by=<método>`

**Descrição**
Recomenda outros usuários (amigos em potencial) com base em afinidade de gênero ou avaliações em comum.

**Query parameters**

* `by` (string, obrigatório):

  * `genre` — sugere usuários que seguem artistas do mesmo gênero mais comum do solicitante.
  * `reviews` — sugere usuários que avaliaram positivamente os mesmos lançamentos.

**Parâmetros de rota**

* `username` (string): nome do usuário.

**Resposta 200 OK**

```json
// Exemplo para by=genre
{
  "user": {
    "username": "bob",
    "name": "Bob Smith",
    "bio": "Curte indie rock"
  },
  "by": {
    "genre": "indie"
  }
}

// Exemplo para by=reviews
{
  "user": {
    "username": "carol",
    "name": "Carol Jones",
    "bio": null
  },
  "by": {
    "id": "rel002",
    "name": "1989",
    "artist": "Taylor Swift",
    "rating": 8
  }
}
```

**Erros possíveis**

* `400 Bad Request`: parâmetro `by` não informado ou inválido.
* `404 Not Found`: usuário não existe.
* `404 Not Found`: sem dados para recomendações (nenhum gênero, review ou friend rec encontrado).

