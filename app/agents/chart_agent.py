from langchain_core.prompts import ChatPromptTemplate

from app.models.evidence import EvidenceItem
from app.services.groq_client import get_llm


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

Your job is to identify evidence from patient records
that is relevant to an insurance requirement.

Rules:

1. Use ONLY the supplied patient records.
2. Do not invent patient information.
3. Do not make unsupported medical conclusions.
4. Return only evidence relevant to the requirement.
5. Preserve the source document.
6. If no useful evidence exists, return an empty list.
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

        chain = prompt | structured_llm

        result = chain.invoke(
            {
                "requirement": requirement,
                "evidence_required": evidence_required,
                "context": context
            }
        )

        return result.evidence


class EvidenceResponse:

    # Placeholder intentionally removed below.
    pass
