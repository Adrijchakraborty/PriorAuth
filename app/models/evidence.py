from pydantic import BaseModel, Field
from typing import Literal


class EvidenceItem(BaseModel):
    document: str = Field(
        description="Patient document containing the evidence"
    )

    page: int | None = Field(
        default=None,
        description="Page containing the evidence"
    )

    text: str = Field(
        description="Exact relevant evidence text"
    )


class EvidenceMatch(BaseModel):
    requirement_id: str

    status: Literal[
        "SATISFIED",
        "NOT_SATISFIED",
        "UNKNOWN"
    ]

    reasoning: str

    evidence: list[EvidenceItem]
