from app.agents.guideline_agent import run_guideline_agent


PDF_PATH = "data/guidelines/sample_guideline.pdf"


def main():
    print("Reading insurance guideline...\n")

    guideline = run_guideline_agent(PDF_PATH)

    print("=" * 60)
    print("EXTRACTED GUIDELINE")
    print("=" * 60)

    print(
        f"\nTreatment: {guideline.treatment_name}"
    )

    for requirement in guideline.requirements:
        print("\n----------------------------------------")

        print(
            f"ID: {requirement.requirement_id}"
        )

        print(
            f"Requirement: {requirement.description}"
        )

        print(
            f"Mandatory: {requirement.mandatory}"
        )

        print(
            f"Evidence required: "
            f"{', '.join(requirement.evidence_required)}"
        )

        print(
            f"Source page: {requirement.source_page}"
        )


if __name__ == "__main__":
    main()