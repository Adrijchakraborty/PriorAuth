from langchain_core.prompts import ChatPromptTemplate

from app.services.groq_client import get_llm
from app.models.evidence import (
    EvidenceItem,
    EvidenceResponse
)


class ChartAgent:

    def __init__(self, retriever):

        self.retriever = retriever
        self.llm = get_llm()

    def find_evidence(
        self,
        patient_id: str,
        requirement: str,
        evidence_required: list[str]
    ) -> list[EvidenceItem]:

        query = f"""
Insurance requirement:
{requirement}

Evidence needed:
{", ".join(evidence_required)}
"""

        retrieved = self.retriever.search(
            patient_id=patient_id,
            query=query,
            top_k=5
        )

        if not retrieved:
            return []

        context = "\n\n".join(
            [
                f"""
DOCUMENT: {item["document"]}
PAGE: {item.get("page")}
TEXT:
{item["text"]}
"""
                for item in retrieved
            ]
        )

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
You are the Chart Reviewer in a Prior Authorization system.

Use ONLY the supplied patient records.

Do not invent patient information.

Return only evidence that is relevant to the
insurance requirement.

If there is no relevant evidence, return an empty list.
"""
                ),
                (
                    "human",
                    """
REQUIREMENT:

{requirement}

EVIDENCE REQUIRED:

{evidence_required}

PATIENT RECORDS:

{context}
"""
                )
            ]
        )

        structured_llm = self.llm.with_structured_output(
            EvidenceResponse
        )

        result = (
            prompt | structured_llm
        ).invoke(
            {
                "requirement": requirement,
                "evidence_required": evidence_required,
                "context": context
            }
        )

        return result.evidence
