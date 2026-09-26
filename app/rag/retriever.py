import chromadb
from chromadb.utils.embedding_functions import (
    SentenceTransformerEmbeddingFunction
)

from app.config import VECTORSTORE_PATH


EMBEDDING_MODEL = "all-MiniLM-L6-v2"


class PatientRetriever:

    def __init__(self):

        self.client = chromadb.PersistentClient(
            path=VECTORSTORE_PATH
        )

        self.collection = self.client.get_or_create_collection(
            name="patient_records",
            embedding_function=SentenceTransformerEmbeddingFunction(
                model_name=EMBEDDING_MODEL
            )
        )

    def search(
        self,
        patient_id: str,
        query: str,
        top_k: int = 5
    ):

        results = self.collection.query(
            query_texts=[query],
            n_results=top_k,
            where={
                "patient_id": patient_id
            }
        )

        documents = results.get(
            "documents",
            [[]]
        )[0]

        metadatas = results.get(
            "metadatas",
            [[]]
        )[0]

        output = []

        for document, metadata in zip(
            documents,
            metadatas
        ):

            output.append(
                {
                    "document": metadata["document"],
                    "page": None,
                    "text": document
                }
            )

        return output
