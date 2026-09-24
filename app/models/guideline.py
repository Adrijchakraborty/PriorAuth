from pydantic import BaseModel, Field


class GuidelineRequirement(BaseModel):
    requirement_id: str = Field(
        description="Unique ID such as REQ-001"
    )

    description: str = Field(
        description="The insurance requirement"
    )

    mandatory: bool = Field(
        description="Whether this requirement must be satisfied"
    )

    evidence_required: list[str] = Field(
        description="Types of evidence needed to satisfy the requirement"
    )

    source_page: int = Field(
        description="Page number where the requirement was found"
    )


class Guideline(BaseModel):
    treatment_name: str = Field(
        description="Treatment or medication covered by this guideline"
    )

    requirements: list[GuidelineRequirement] = Field(
        description="List of prior authorization requirements"
    )