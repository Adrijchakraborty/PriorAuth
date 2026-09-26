import os
import tempfile

import streamlit as st

from app.database import initialize_database, create_request
from app.rag.ingest import ingest_patient_documents
from app.workflow import build_workflow


# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------

st.set_page_config(
    page_title="PriorAuth AI",
    page_icon="🏥",
    layout="wide"
)


# ---------------------------------------------------------
# INITIALIZE DATABASE
# ---------------------------------------------------------

initialize_database()


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.title("🏥 PriorAuth AI")
st.caption(
    "Evidence-grounded Prior Authorization Assistant"
)

st.divider()


# ---------------------------------------------------------
# INPUT SECTION
# ---------------------------------------------------------

st.header("Prior Authorization Request")

col1, col2 = st.columns(2)

with col1:

    patient_id = st.text_input(
        "Patient ID",
        value="P001"
    )

    treatment = st.text_input(
        "Treatment",
        value="Advanced Therapy X"
    )


with col2:

    insurer = st.text_input(
        "Insurance Provider",
        value="Demo Insurance"
    )

    st.write("")


# ---------------------------------------------------------
# FILE UPLOADS
# ---------------------------------------------------------

st.subheader("Documents")

patient_file = st.file_uploader(
    "Upload Patient Chart (PDF)",
    type=["pdf"],
    key="patient_chart"
)

guideline_file = st.file_uploader(
    "Upload Insurance Guideline (PDF)",
    type=["pdf"],
    key="guideline"
)


# ---------------------------------------------------------
# DOCUMENT PREVIEW
# ---------------------------------------------------------

if patient_file is not None:

    st.success(
        f"Patient chart uploaded: {patient_file.name}"
    )


if guideline_file is not None:

    st.success(
        f"Insurance guideline uploaded: {guideline_file.name}"
    )


st.divider()


# ---------------------------------------------------------
# GENERATE BUTTON
# ---------------------------------------------------------

generate = st.button(
    "🚀 Generate Prior Authorization",
    type="primary",
    use_container_width=True
)


# ---------------------------------------------------------
# WORKFLOW
# ---------------------------------------------------------

if generate:

    # ---------------------------------------------
    # Validate inputs
    # ---------------------------------------------

    if not patient_id.strip():

        st.error("Please enter a Patient ID.")
        st.stop()


    if not treatment.strip():

        st.error("Please enter a treatment.")
        st.stop()


    if not insurer.strip():

        st.error("Please enter an insurance provider.")
        st.stop()


    if patient_file is None:

        st.error(
            "Please upload the patient's clinical chart PDF."
        )
        st.stop()


    if guideline_file is None:

        st.error(
            "Please upload the insurance guideline PDF."
        )
        st.stop()


    # ---------------------------------------------
    # Create temporary working directories
    # ---------------------------------------------

    temp_root = tempfile.mkdtemp(
        prefix="priorauth_"
    )

    patient_directory = os.path.join(
        temp_root,
        "patients",
        patient_id
    )

    guideline_directory = os.path.join(
        temp_root,
        "guidelines"
    )

    os.makedirs(
        patient_directory,
        exist_ok=True
    )

    os.makedirs(
        guideline_directory,
        exist_ok=True
    )


    # ---------------------------------------------
    # Save uploaded patient chart
    # ---------------------------------------------

    patient_pdf_path = os.path.join(
        patient_directory,
        patient_file.name
    )

    with open(
        patient_pdf_path,
        "wb"
    ) as file:

        file.write(
            patient_file.getbuffer()
        )


    # ---------------------------------------------
    # Save uploaded guideline
    # ---------------------------------------------

    guideline_pdf_path = os.path.join(
        guideline_directory,
        guideline_file.name
    )

    with open(
        guideline_pdf_path,
        "wb"
    ) as file:

        file.write(
            guideline_file.getbuffer()
        )


    # ---------------------------------------------
    # Create database request
    # ---------------------------------------------

    request_id = create_request(
        patient_id=patient_id,
        treatment=treatment,
        insurer=insurer
    )


    st.info(
        f"Workflow started — Request #{request_id}"
    )


    # ---------------------------------------------
    # Ingest patient chart into RAG
    # ---------------------------------------------

    try:

        with st.spinner(
            "Indexing patient chart..."
        ):

            ingest_patient_documents(
                patient_id=patient_id,
                patient_directory=patient_directory
            )

    except Exception as error:

        st.error(
            "Patient chart ingestion failed."
        )

        st.exception(error)

        st.stop()


    # ---------------------------------------------
    # Build workflow
    # ---------------------------------------------

    try:

        workflow = build_workflow()

        initial_state = {

            "patient_id": patient_id,

            "treatment": treatment,

            "insurer": insurer,

            "guideline_path": guideline_pdf_path

        }


        # -----------------------------------------
        # Run workflow
        # -----------------------------------------

        with st.spinner(
            "Analyzing guideline and patient evidence..."
        ):

            result = workflow.invoke(
                initial_state
            )


    except Exception as error:

        st.error(
            "Prior authorization workflow failed."
        )

        st.exception(error)

        st.stop()


    # ---------------------------------------------
    # WORKFLOW COMPLETED
    # ---------------------------------------------

    st.success(
        "Prior Authorization workflow completed."
    )


    # =================================================
    # GUIDELINE REQUIREMENTS
    # =================================================

    st.header("1. Guideline Requirements")

    guideline = result["guideline"]

    for requirement in guideline.requirements:

        with st.expander(
            requirement.requirement_id,
            expanded=True
        ):

            st.write(
                "**Requirement:**"
            )

            st.write(
                requirement.description
            )


            st.write(
                "**Mandatory:**"
            )

            st.write(
                "Yes"
                if requirement.mandatory
                else "No"
            )


            st.write(
                "**Evidence Required:**"
            )

            for item in requirement.evidence_required:

                st.write(
                    f"- {item}"
                )


            st.caption(
                f"Source: {requirement.source_document} "
                f"| Page: {requirement.source_page}"
            )


    # =================================================
    # EVIDENCE MATCHING
    # =================================================

    st.header("2. Evidence Matching")

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


        if match.evidence:

            st.write(
                "**Supporting Evidence:**"
            )

            for evidence in match.evidence:

                st.info(
                    f"{evidence.document} "
                    f"| Page {evidence.page}"
                )

                st.write(
                    evidence.text
                )

        else:

            st.caption(
                "No supporting evidence found."
            )


    # =================================================
    # GENERATED PRIOR AUTHORIZATION
    # =================================================

    st.header("3. Generated Prior Authorization")

    draft = result["draft"]


    st.subheader("Patient")

    st.write(
        draft.patient_id
    )


    st.subheader("Treatment")

    st.write(
        draft.treatment
    )


    st.subheader("Insurance Provider")

    st.write(
        draft.insurer
    )


    st.subheader("Diagnosis")

    st.write(
        draft.diagnosis
    )


    st.subheader("Clinical Justification")

    st.write(
        draft.clinical_justification
    )


    st.subheader("Previous Treatments")

    if draft.previous_treatments:

        for treatment_item in draft.previous_treatments:

            st.write(
                f"- {treatment_item}"
            )

    else:

        st.write(
            "No previous treatments documented."
        )


    # =================================================
    # MISSING INFORMATION
    # =================================================

    if draft.missing_information:

        st.warning(
            "Missing Information"
        )

        for item in draft.missing_information:

            st.write(
                f"- {item}"
            )


    # =================================================
    # VALIDATION
    # =================================================

    st.header("4. Validation")

    validation = result[
        "validation_result"
    ]


    if validation == "PASS":

        st.success(
            "✅ Validation passed"
        )

    else:

        st.warning(
            validation
        )


    # =================================================
    # DEBUG / WORKFLOW INFORMATION
    # =================================================

    with st.expander(
        "Developer Debug Information"
    ):

        st.write(
            "Request ID:",
            request_id
        )

        st.write(
            "Patient:",
            patient_id
        )

        st.write(
            "Treatment:",
            treatment
        )

        st.write(
            "Insurer:",
            insurer
        )

        st.write(
            "Patient chart:",
            patient_file.name
        )

        st.write(
            "Guideline:",
            guideline_file.name
        )