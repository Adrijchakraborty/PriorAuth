from langchain_core.prompts import ChatPromptTemplate

from app.services.groq_client import get_llm


class Validator:

    def __init__(self):
        self.llm = get_llm()

    def validate_required_fields(
        self,
        draft
    ) -> list[str]:

        errors = []

        if not draft.patient_id:
            errors.append("Missing patient ID")

        if not draft.treatment:
            errors.append("Missing treatment")

        if not draft.insurer:
            errors.append("Missing insurer")

        if not draft.diagnosis:
            errors.append("Missing diagnosis")

        if not draft.clinical_justification:
            errors.append(
                "Missing clinical justification"
            )

        return errors

    def validate_claims(
        self,
        draft,
        evidence_matches
    ):

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
You are the final validation layer for a
Prior Authorization system.

Check whether the claims in the generated draft
are supported by the supplied evidence.

Return:

PASS
if all important claims are supported.

FAIL
if an important claim is unsupported or contradicted.

Do not evaluate whether the treatment itself is medically
appropriate.

Do not introduce new medical knowledge.
"""
                ),
                (
                    "human",
                    """
GENERATED DRAFT:

{draft}

SUPPORTING EVIDENCE:

{evidence_matches}
"""
                )
            ]
        )

        response = (
            prompt | self.llm
        ).invoke(
            {
                "draft": draft.model_dump_json(),
                "evidence_matches": evidence_matches
            }
        )

        return response.content
