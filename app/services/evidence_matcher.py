from langchain_core.prompts import ChatPromptTemplate

from app.models.evidence import EvidenceMatch
from app.services.groq_client import get_llm


class EvidenceMatcher:

    def __init__(self):
        self.llm = get_llm()

    def match(
        self,
        requirement_id: str,
        requirement: str,
        evidence_required: list[str],
        evidence
    ) -> EvidenceMatch:

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
You are the Evidence Matcher for a Prior Authorization system.

Determine whether patient evidence satisfies an insurance
requirement.

Use ONLY the supplied evidence.

Possible statuses:

SATISFIED
- Evidence clearly demonstrates the requirement is met.

NOT_SATISFIED
- Evidence demonstrates that the requirement is not met.

UNKNOWN
- Evidence is insufficient to determine whether it is met.

Never guess.

Do not use outside medical knowledge.
"""
                ),
                (
                    "human",
                    """
REQUIREMENT ID:
{requirement_id}

REQUIREMENT:
{requirement}

EVIDENCE REQUIRED:
{evidence_required}

PATIENT EVIDENCE:
{evidence}
"""
                )
            ]
        )

        structured_llm = self.llm.with_structured_output(
            EvidenceMatch
        )

        return (
            prompt | structured_llm
        ).invoke(
            {
                "requirement_id": requirement_id,
                "requirement": requirement,
                "evidence_required": evidence_required,
                "evidence": evidence
            }
        )
