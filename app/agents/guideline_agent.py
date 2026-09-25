from langchain_core.prompts import ChatPromptTemplate

from app.models.guideline import Guideline
from app.services.groq_client import get_llm
from app.services.pdf_parser import extract_pdf_text


SYSTEM_PROMPT = """
You are the Guidelines Reader for a Prior Authorization system.

Your job is to extract prior authorization requirements
from an insurance company's clinical policy.

IMPORTANT RULES:

1. Extract requirements ONLY from the supplied document.
2. Do not use outside medical knowledge.
3. Do not invent requirements.
4. Preserve the meaning of the insurance policy.
5. Identify whether each requirement is mandatory.
6. Identify what evidence would be needed to prove each requirement.
7. Record the source document and page number.
8. If information is unclear, represent the uncertainty rather
   than inventing information.
9. Do not decide whether a patient qualifies.
10. Do not interpret patient information.

You are extracting policy requirements only.

Return the information using the requested structured schema.
"""


def create_guideline_agent():

    llm = get_llm()

    structured_llm = llm.with_structured_output(
        Guideline
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                SYSTEM_PROMPT
            ),
            (
                "human",
                """
Analyze the following insurance policy.

The requested treatment is:

{treatment_name}

Extract all prior authorization requirements
relevant to this treatment.

INSURANCE POLICY:

{policy_text}
"""
            )
        ]
    )

    return prompt | structured_llm


def run_guideline_agent(
    pdf_path: str,
    treatment_name: str
) -> Guideline:

    policy_text = extract_pdf_text(pdf_path)

    agent = create_guideline_agent()

    result = agent.invoke(
        {
            "policy_text": policy_text,
            "treatment_name": treatment_name
        }
    )

    return result
