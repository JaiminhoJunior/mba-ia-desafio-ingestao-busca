import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector

load_dotenv()

PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""

def validate_required_system_variables():
    for key in (
        "DATABASE_URL", 
        "PG_VECTOR_COLLECTION_NAME", 
        "OPENAI_EMBEDDING_MODEL",
        "OPENAI_MODEL"
    ):
        if not os.getenv(key):
            raise ValueError(
                f"O valor da variável {key} precisa ser definida!"
            )

def search_prompt(question = None):
    validate_required_system_variables()

    if not question:
        raise ValueError("É necessário informar uma pergunta!")

    embeddings = OpenAIEmbeddings(
        model = os.getenv("OPENAI_EMBEDDING_MODEL")
    )

    store = PGVector(
        embeddings = embeddings,
        collection_name = os.getenv("PG_VECTOR_COLLECTION_NAME"),
        connection = os.getenv("DATABASE_URL"),
        use_jsonb = True
    )

    result = store.similarity_search_with_score(
        question,
        k = 10
    )

    question_template = PromptTemplate(
        input_variables = [ "contexto", "pergunta" ],
        template=PROMPT_TEMPLATE
    )

    model = ChatOpenAI(
        model = os.getenv("OPENAI_MODEL"), 
        temperature = 0.2
    )
    chain = question_template | model
    result = chain.invoke(
        {
            "contexto" : result,
            "pergunta" : question
        }
    )

    return result