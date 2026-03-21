from __future__ import annotations

import io
import logging
from dataclasses import dataclass
from typing import Any, Dict, Optional

try:
    import PyPDF2
except ImportError:  # pragma: no cover - optional dependency
    PyPDF2 = None


@dataclass
class ParsedDocument:
    text: str
    pages: Optional[int]
    metadata: Dict[str, Any]


class ParserError(Exception):
    """Raised when a file cannot be parsed."""


logger = logging.getLogger(__name__)


def parse_file(filename: str, file_bytes: bytes, mime_type: Optional[str] = None) -> ParsedDocument:
    if not file_bytes:
        raise ParserError("Uploaded file is empty.")

    extension = (filename.split(".")[-1] if "." in filename else "").lower()
    try:
        if extension == "pdf":
            logger.info("Parsing PDF '%s'", filename)
            return _parse_pdf(file_bytes, filename, mime_type)
        if extension == "txt":
            logger.info("Parsing TXT '%s'", filename)
            return _parse_txt(file_bytes, filename, mime_type)
    except ParserError:
        raise
    except Exception as exc:  # pragma: no cover - escalated to ParserError
        logger.exception("Unexpected error while parsing '%s'", filename)
        raise ParserError("Unable to parse the provided file.") from exc

    raise ParserError("Unsupported file type. Please upload a PDF or TXT file.")


def _parse_pdf(file_bytes: bytes, filename: str, mime_type: Optional[str]) -> ParsedDocument:
    if PyPDF2 is None:
        raise ParserError("PyPDF2 is required to parse PDF files.")

    try:
        reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
        pages = len(reader.pages)
        text_fragments = []
        for page in reader.pages:
            text_fragments.append(page.extract_text() or "")

        text = "\n".join(fragment.strip() for fragment in text_fragments if fragment)
        metadata = {
            "filename": filename,
            "mime_type": mime_type or "application/pdf",
            "pages": pages,
            "producer": getattr(reader.metadata, "producer", None),
        }
        return ParsedDocument(text=text, pages=pages, metadata=metadata)
    except ParserError:
        raise
    except Exception as exc:  # pragma: no cover - unexpected failure
        logger.exception("Failed to read PDF '%s'", filename)
        raise ParserError("Unable to parse PDF file.") from exc


def _parse_txt(file_bytes: bytes, filename: str, mime_type: Optional[str]) -> ParsedDocument:
    try:
        text = file_bytes.decode("utf-8")
    except UnicodeDecodeError:
        text = file_bytes.decode("latin-1", errors="ignore")

    try:
        cleaned_text = text.strip()
        metadata = {
            "filename": filename,
            "mime_type": mime_type or "text/plain",
            "length": len(cleaned_text),
        }
        return ParsedDocument(text=cleaned_text, pages=None, metadata=metadata)
    except Exception as exc:  # pragma: no cover - unexpected failure
        logger.exception("Failed to parse TXT '%s'", filename)
        raise ParserError("Unable to parse text file.") from exc
