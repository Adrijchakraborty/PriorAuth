import os
import pymupdf


GUIDELINE_PATH = "data/guidelines/sample_guideline.pdf"

PATIENTS = {
    "P001": [
        """
PATIENT MEDICAL RECORD

Patient ID: P001

Page 1

Diagnosis:

Patient has moderate-to-severe Condition Alpha.

Diagnosis was documented during the patient's
clinical evaluation.
""",
        """
PATIENT MEDICAL RECORD

Patient ID: P001

Page 2

Previous Treatment:

Treatment A was started on January 10, 2026.

Treatment A was discontinued on April 10, 2026.

Total treatment duration: approximately 12 weeks.

The patient reported inadequate clinical response.
""",
        """
PATIENT MEDICAL RECORD

Patient ID: P001

Page 3

Treatment Outcome:

Treatment A was discontinued because of
inadequate clinical response.

The treating physician documented that the
patient did not achieve sufficient improvement.
"""
    ],

    "P002": [
        """
PATIENT MEDICAL RECORD

Patient ID: P002

Page 1

Diagnosis:

Patient has moderate-to-severe Condition Alpha.

Diagnosis was documented during the patient's
clinical evaluation.
""",
        """
PATIENT MEDICAL RECORD

Patient ID: P002

Page 2

Previous Treatment:

Treatment A was started on February 1, 2026.

Treatment A was discontinued on March 15, 2026.

Total treatment duration: approximately 6 weeks.

The patient reported inadequate clinical response.
""",
        """
PATIENT MEDICAL RECORD

Patient ID: P002

Page 3

Treatment Outcome:

Treatment A was discontinued because of
inadequate clinical response.

The treating physician documented insufficient
improvement after treatment.
"""
    ],

    "P003": [
        """
PATIENT MEDICAL RECORD

Patient ID: P003

Page 1

Diagnosis:

Patient has moderate-to-severe Condition Alpha.

Diagnosis was documented during the patient's
clinical evaluation.
""",
        """
PATIENT MEDICAL RECORD

Patient ID: P003

Page 2

Current Treatment:

Patient is currently receiving supportive
management for Condition Alpha.

No previous Treatment A is documented in
the available clinical record.
""",
        """
PATIENT MEDICAL RECORD

Patient ID: P003

Page 3

Clinical Notes:

The available record does not contain
documentation of a previous Treatment A trial.

No treatment start date, stop date, duration,
or Treatment A response is documented.
"""
    ]
}


def create_pdf(path, pages):

    os.makedirs(
        os.path.dirname(path),
        exist_ok=True
    )

    document = pymupdf.open()

    for page_text in pages:

        page = document.new_page()

        page.insert_textbox(
            pymupdf.Rect(
                50,
                50,
                550,
                750
            ),
            page_text,
            fontsize=11
        )

    document.save(path)
    document.close()


def create_guideline():

    pages = [
        """
DEMO INSURANCE COMPANY
CLINICAL POLICY

Treatment: Advanced Therapy X

Prior Authorization Requirements

Page 1

Requirement REQ-001

Patients must have a documented diagnosis of
moderate-to-severe Condition Alpha.

The diagnosis must be documented in the
patient's medical record.

This requirement is mandatory.
""",
        """
DEMO INSURANCE COMPANY
CLINICAL POLICY

Treatment: Advanced Therapy X

Page 2

Requirement REQ-002

The patient must have previously attempted
Treatment A for at least 12 weeks.

Documentation must include:

- Treatment A name
- Start date
- Stop date or treatment duration
- Clinical response

This requirement is mandatory.
""",
        """
DEMO INSURANCE COMPANY
CLINICAL POLICY

Treatment: Advanced Therapy X

Page 3

Requirement REQ-003

If Treatment A was ineffective or not tolerated,
the medical record must document the treatment
outcome.

The treatment outcome must be documented.

This requirement is mandatory.
"""
    ]

    create_pdf(
        GUIDELINE_PATH,
        pages
    )


def create_patient_charts():

    for patient_id, pages in PATIENTS.items():

        patient_path = (
            f"data/patients/{patient_id}/clinical_notes.pdf"
        )

        create_pdf(
            patient_path,
            pages
        )

        print(
            f"Created patient {patient_id}: "
            f"{patient_path}"
        )


if __name__ == "__main__":

    create_guideline()
    create_patient_charts()

    print()
    print("All mock data created successfully.")