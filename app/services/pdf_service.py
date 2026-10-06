import pymupdf

from app.schemas.documents import ExtractedPage


class PDFExtractionError(Exception):
    """Raised when text cannot be extracted from a PDF."""


def extract_pages(pdf_bytes: bytes) -> list[ExtractedPage]:
    pages: list[ExtractedPage] = []

    try:
        with pymupdf.open(stream=pdf_bytes, filetype="pdf") as document:
            if document.needs_pass:
                raise PDFExtractionError(
                    "Password-protected PDFs are not supported"
                )

            for page_number, page in enumerate(document, start=1):
                pages.append(
                    ExtractedPage(
                        page=page_number,
                        text=page.get_text("text"),
                    )
                )
    except pymupdf.FileDataError as error:
        raise PDFExtractionError(
            "The PDF could not be read"
        ) from error

    return pages