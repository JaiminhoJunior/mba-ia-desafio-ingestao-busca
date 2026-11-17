# Desafio técnico - MBA IA

## Ingestão e busca semântica com LangChain e Postgres

O objetivo desse desafio é desenvolver um software que seja capaz de efetuar a leitura de um arquivo PDF
e salvar o embadding desse arquivo em um banco dade dados vetorial (pgVector).
Após a conclusão da ingestão do conteúdo do arquivo, o software deverá permitir a consulta do conteúdo
por meio de um LLM.

### Tecnologias utilizadas
- Linguagem: Python
- Framework: LangChain
- Banco de dados: Postgres + pgVector
- Ambiente de banco de dados: Docker & Docker Compose

### Modelo utilizado
- Modelo de LLM: gpt-5-nano
- Modelo de embedding: text-embedding-3-small

**Importante**: Ambos os modelos estão definidos no arquivo .env.

### Como utilizar

#### Confguração do ambiente
Crie e ative um ambiente virtual antes de instalar dependências:
```
python3 -m venv venv
source venv/bin/activate
```

#### Efetuar a ingestão do PDF no banco de dados
No arquivo .env, devemos efetuar a inclusão das seguintes propriedades:
- PDF_PATH: Nome do arquivo .pdf.
- DATABASE_URL: String de conexão com o banco de dados.
- PG_VECTOR_COLLECTION_NAME: Nome do banco dade dados.
- OPENAI_EMBEDDING_MODEL: Modelo que será utilizados para realizar o embedding.

Utilize o comando abaixo para iniciar o Docker e efetuar o download da imagem do banco de dados caso ainda não tenha:
```bash
docker compose up -d
```

Para realizar a ingestão utilize o comando:
```bash
python3 src/ingest.py
```

#### Validar se o conteúdo foi inserido corretamente
No arquivo .env, devemos efetuar a inclusão das seguintes propriedades:
- OPENAI_API_KEY: A chave do Google AI Studio definida para o seu projeto.
- OPENAI_MODEL: O modelo que será utilizado pelo LLM. No projeto, estou utilizando o **gpt-5-nano**.

O arquivo chat.py tem o objetivo de efetuar uma consulta dos embeddings persistidos no banco de dados.
Esse arquivo possui uma variável chamada *question*. Altere o valor dessa variável para a pergunta desejada sobre o conteúdo do arquivo. Logo em seguida, execute o código pelo comando abaixo:
```bash
python3 src/chat.py
```
Caso a execução ocorra sem problemas, você verá no console a seguinte resposta:
```prompt
Pergunta: <Pergunta realizada pelo usuário.>
Resposta: <Resposta produzida pela LLM com base no conteúdo do arquivo pdf.>
```