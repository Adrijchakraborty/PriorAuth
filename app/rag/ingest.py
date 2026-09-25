from pathlib import Path

import chromadb
from chromadb.utils.embedding_functions import (
    SentenceTransformerEmbeddingFunction
)

from app.config import VECTORSTORE_PATH
from app.services.pdf_parser import extract_pdf_text


EMBEDDING_MODEL = "all-MiniLM-L6-v2"


def get_embedding_function():
    return SentenceTransformerEmbeddingFunction(
        model_name=EMBEDDING_MODEL
    )


def chunk_text(text: str, chunk_size: int = 1200):

    chunks = []

    for start in range(0, len(text), chunk_size):

        chunk = text[start:start + chunk_size]

        if chunk.strip():
            chunks.append(chunk)

    return chunks


def ingest_patient_documents(
    patient_id: str,
    patient_directory: str
):

    client = chromadb.PersistentClient(
        path=VECTORSTORE_PATH
    )

    collection = client.get_or_create_collection(
        name="patient_records",
        embedding_function=get_embedding_function()
    )

    patient_directory = Path(patient_directory)

    pdf_files = patient_directory.glob("*.pdf")

    for pdf_path in pdf_files:

        text = extract_pdf_text(
            str(pdf_path)
        )

        chunks = chunk_text(text)

        ids = []
        documents = []
        metadatas = []

        for index, chunk in enumerate(chunks):

            chunk_id = (
                f"{patient_id}_"
                f"{pdf_path.stem}_"
                f"{index}"
            )

            ids.append(chunk_id)
            documents.append(chunk)

            metadatas.append(
                {
                    "patient_id": patient_id,
                    "document": pdf_path.name,
                    "chunk_index": index
                }
            )

        if documents:

            collection.upsert(
                ids=ids,
                documents=documents,
                metadatas=metadatas
            )

    return collection
