from pathlib import Path

import pymupdf


def extract_pdf_text(pdf_path: str) -> str:
    """
    Extract text from a PDF document while preserving page boundaries.

    Args:
        pdf_path: Path to the PDF file.

    Returns:
        Extracted text with page markers.

    Raises:
        FileNotFoundError: If the PDF does not exist.
        ValueError: If the PDF cannot be opened.
    """

    path = Path(pdf_path)

    if not path.exists():
        raise FileNotFoundError(
            f"PDF not found: {pdf_path}"
        )

    try:
        document = pymupdf.open(path)
    except Exception as exc:
        raise ValueError(
            f"Unable to open PDF: {pdf_path}"
        ) from exc

    pages = []

    try:
        for page_number, page in enumerate(document, start=1):
            text = page.get_text()

            pages.append(
                f"\n--- PAGE {page_number} ---\n{text}"
            )
    finally:
        document.close()

    return "\n".join(pages)