import os
from dotenv import load_dotenv
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_postgres import PGVector

load_dotenv()

def validate_required_system_variables():
    for key in (
        "PDF_PATH", 
        "DATABASE_URL", 
        "PG_VECTOR_COLLECTION_NAME", 
        "OPENAI_EMBEDDING_MODEL"
    ):
        if not os.getenv(key):
            raise ValueError(
                f"O valor da variável {key} precisa ser definida!"
            )

def load_pdf_content():
    resourse_path = Path(__file__).resolve().parent.parent
    pdf_file = os.getenv("PDF_PATH")
    loader = PyPDFLoader(f"{resourse_path}/{pdf_file}")
    return loader.load()

def ingest_pdf():
    validate_required_system_variables()
    content = load_pdf_content()

    if not content:
        raise RuntimeError(
            f"Não foi possível carregar o arquivo PDF"
        )

    chunks = RecursiveCharacterTextSplitter(
        chunk_size = 1000, 
        chunk_overlap = 150
    ).split_documents(content)

    if not chunks:
        raise RuntimeError(
            f"Não foi possível gerar o chunk a partir do conteúdo do PDF"
        )

    enriched_content = [
        Document(
            page_content = d.page_content,
            metadata = {
                k: v for k, v in d.metadata.items() if v not in ("", None)
            }
        )
        for d in chunks
    ]

    content_ids = [f"doc-{i}" for i in range(len(enriched_content))]
    embeddings = OpenAIEmbeddings(
        model = os.getenv("OPENAI_EMBEDDING_MODEL")
    )

    store = PGVector(
        embeddings = embeddings,
        collection_name = os.getenv("PG_VECTOR_COLLECTION_NAME"),
        connection = os.getenv("DATABASE_URL"),
        use_jsonb = True
    )

    store.add_documents(
        documents = enriched_content, 
        ids = content_ids
    )

if __name__ == "__main__":
    ingest_pdf()