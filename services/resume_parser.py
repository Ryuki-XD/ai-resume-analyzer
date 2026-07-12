"""Resume file parser — extracts text from PDF and DOCX uploads.

Handles binary file objects from Streamlit's ``st.file_uploader`` and
returns plain text suitable for NLP analysis.
"""

from __future__ import annotations

from io import BytesIO
from typing import BinaryIO

import docx
from PyPDF2 import PdfReader

from utils.logger import get_logger

logger = get_logger(__name__)


def parse_pdf(file: BinaryIO) -> str:
    """Extract text from a PDF file.

    Args:
        file: A binary file-like object containing PDF data.

    Returns:
        Extracted plain text.

    Raises:
        ValueError: If the PDF contains no extractable text.
    """
    try:
        reader = PdfReader(file)
        pages: list[str] = []

        for page_num, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                pages.append(text)
            else:
                logger.warning("Page %d yielded no text.", page_num + 1)

        full_text = "\n".join(pages).strip()

        if not full_text:
            raise ValueError(
                "The PDF file contains no extractable text. "
                "It may be a scanned image — try uploading a DOCX instead."
            )

        logger.info(
            "Extracted %d characters from %d PDF pages.",
            len(full_text),
            len(reader.pages),
        )
        return full_text

    except ValueError:
        raise
    except Exception as exc:
        logger.error("PDF parsing failed: %s", exc)
        raise ValueError(f"Failed to read the PDF file: {exc}") from exc


def parse_docx(file: BinaryIO) -> str:
    """Extract text from a DOCX file.

    Args:
        file: A binary file-like object containing DOCX data.

    Returns:
        Extracted plain text.

    Raises:
        ValueError: If the document contains no text.
    """
    try:
        document = docx.Document(file)
        paragraphs = [para.text for para in document.paragraphs if para.text.strip()]
        full_text = "\n".join(paragraphs).strip()

        if not full_text:
            raise ValueError("The DOCX file contains no readable text content.")

        logger.info(
            "Extracted %d characters from DOCX (%d paragraphs).",
            len(full_text),
            len(paragraphs),
        )
        return full_text

    except ValueError:
        raise
    except Exception as exc:
        logger.error("DOCX parsing failed: %s", exc)
        raise ValueError(f"Failed to read the DOCX file: {exc}") from exc


def parse_resume(file: BinaryIO, filename: str) -> str:
    """Route to the correct parser based on file extension.

    Args:
        file: The uploaded binary file object.
        filename: Original filename (used to detect extension).

    Returns:
        Extracted text from the resume.

    Raises:
        ValueError: If the file type is unsupported or parsing fails.
    """
    name_lower = filename.lower()

    if name_lower.endswith(".pdf"):
        return parse_pdf(file)
    elif name_lower.endswith(".docx"):
        return parse_docx(file)
    else:
        raise ValueError(
            f"Unsupported file format: '{filename}'. "
            "Please upload a PDF or DOCX file."
        )
