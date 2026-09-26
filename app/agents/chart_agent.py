from langchain_core.prompts import ChatPromptTemplate

from app.services.groq_client import get_llm
from app.models.evidence import EvidenceItem, EvidenceResponse


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

Evidence that may be relevant:

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

Your job is to find patient-record evidence that is relevant
to an insurance requirement.

IMPORTANT RULES:

1. Use ONLY the supplied patient records.

2. Never invent patient information.

3. Extract evidence that is relevant to the requirement,
   even if that evidence shows the requirement is NOT met.

4. Do NOT decide whether the insurance requirement is
   satisfied.

5. Do NOT reject evidence merely because it contradicts
   the requirement.

6. For example, if the requirement says treatment must
   have lasted at least 12 weeks and the chart says
   treatment lasted 6 weeks, the 6-week documentation
   IS relevant evidence and must be returned.

7. If relevant evidence exists, return it.

8. If no relevant evidence exists in the supplied records,
   return an empty list.

9. Do not use outside medical knowledge.

The Evidence Matcher will determine whether the
requirement is SATISFIED, NOT_SATISFIED, or UNKNOWN.

Return the evidence using the requested structured schema.
"""
                ),
                (
                    "human",
                    """
INSURANCE REQUIREMENT:

{requirement}

EVIDENCE TYPES OF INTEREST:

{evidence_required}

PATIENT RECORDS:

{context}

Find all patient-record evidence relevant to the
insurance requirement.

Remember:

You are retrieving evidence only.

Do NOT decide whether the requirement is satisfied.
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