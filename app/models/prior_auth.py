from pydantic import BaseModel, Field


class PriorAuthRequest(BaseModel):
    patient_id: str
    treatment: str
    insurer: str


class PriorAuthDraft(BaseModel):
    patient_id: str
    treatment: str
    insurer: str

    diagnosis: str = Field(
        description="Patient diagnosis supported by the chart"
    )

    clinical_justification: str = Field(
        description="Clinical justification for the requested treatment"
    )

    previous_treatments: list[str] = Field(
        description="Relevant previous treatments and outcomes"
    )

    missing_information: list[str] = Field(
        description="Required information that could not be established"
    )
