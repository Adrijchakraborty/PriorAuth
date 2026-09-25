from langchain_core.prompts import ChatPromptTemplate

from app.models.prior_auth import PriorAuthDraft
from app.services.groq_client import get_llm


class FormWriter:

    def __init__(self):
        self.llm = get_llm()

    def generate(
        self,
        patient_id: str,
        treatment: str,
        insurer: str,
        guideline,
        evidence_matches
    ) -> PriorAuthDraft:

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
You are the Form Writer for a Prior Authorization system.

Create a prior authorization draft using ONLY the
validated evidence supplied to you.

Rules:

1. Never invent patient information.
2. Never invent clinical history.
3. Do not claim that a requirement is satisfied unless
   the evidence explicitly supports it.
4. Include missing information when evidence is unavailable.
5. Write a concise professional justification.
6. Do not make new medical decisions.
"""
                ),
                (
                    "human",
                    """
PATIENT:
{patient_id}

TREATMENT:
{treatment}

INSURER:
{insurer}

GUIDELINE:
{guideline}

VALIDATED EVIDENCE:
{evidence_matches}
"""
                )
            ]
        )

        structured_llm = self.llm.with_structured_output(
            PriorAuthDraft
        )

        return (
            prompt | structured_llm
        ).invoke(
            {
                "patient_id": patient_id,
                "treatment": treatment,
                "insurer": insurer,
                "guideline": guideline,
                "evidence_matches": evidence_matches
            }
        )
