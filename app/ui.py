import streamlit as st

from app.database import (
    initialize_database,
    create_request
)

from app.workflow import build_workflow


st.set_page_config(
    page_title="PriorAuth AI",
    page_icon="🏥",
    layout="wide"
)


initialize_database()


st.title("PriorAuth AI")
st.caption(
    "Evidence-grounded Prior Authorization Assistant"
)


with st.sidebar:

    st.header("Prior Authorization")

    patient_id = st.text_input(
        "Patient ID",
        value="P001"
    )

    treatment = st.text_input(
        "Treatment",
        value="Treatment X"
    )

    insurer = st.text_input(
        "Insurance Provider",
        value="Demo Insurance"
    )

    guideline_path = st.text_input(
        "Guideline PDF",
        value="data/guidelines/sample_guideline.pdf"
    )

    run = st.button(
        "Generate Prior Authorization",
        type="primary"
    )


if run:

    request_id = create_request(
        patient_id=patient_id,
        treatment=treatment,
        insurer=insurer
    )

    st.info(
        f"Workflow started — Request #{request_id}"
    )

    workflow = build_workflow()

    initial_state = {
        "patient_id": patient_id,
        "treatment": treatment,
        "insurer": insurer,
        "guideline_path": guideline_path
    }

    with st.spinner(
        "Analyzing guideline and patient evidence..."
    ):

        result = workflow.invoke(
            initial_state
        )

    st.success("Workflow completed")

    st.subheader("Guideline Requirements")

    guideline = result["guideline"]

    for requirement in guideline.requirements:

        with st.expander(
            requirement.requirement_id
        ):

            st.write(
                requirement.description
            )

            st.write(
                "**Evidence required:**"
            )

            for item in requirement.evidence_required:

                st.write(
                    f"- {item}"
                )

    st.subheader("Evidence Matching")

    for match in result["evidence_matches"]:

        if match.status == "SATISFIED":
            st.success(
                f"{match.requirement_id}: SATISFIED"
            )

        elif match.status == "NOT_SATISFIED":
            st.error(
                f"{match.requirement_id}: NOT SATISFIED"
            )

        else:
            st.warning(
                f"{match.requirement_id}: UNKNOWN"
            )

        st.write(
            match.reasoning
        )

        for evidence in match.evidence:

            st.caption(
                f"{evidence.document} "
                f"| Page {evidence.page}"
            )

            st.write(
                evidence.text
            )

    st.subheader("Generated Prior Authorization")

    draft = result["draft"]

    st.write(
        "**Diagnosis**"
    )

    st.write(
        draft.diagnosis
    )

    st.write(
        "**Clinical Justification**"
    )

    st.write(
        draft.clinical_justification
    )

    st.write(
        "**Previous Treatments**"
    )

    for treatment_item in draft.previous_treatments:

        st.write(
            f"- {treatment_item}"
        )

    if draft.missing_information:

        st.warning(
            "Missing information"
        )

        for item in draft.missing_information:

            st.write(
                f"- {item}"
            )

    st.subheader("Validation")

    validation = result[
        "validation_result"
    ]

    if validation == "PASS":

        st.success(
            "Validation passed"
        )

    else:

        st.warning(
            validation
        )
