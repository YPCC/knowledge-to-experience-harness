# Document & PowerPoint Ingestion Path

The Knowledge-to-Experience Harness accepts **any content**, not only GitHub repositories.

## Supported Inputs

| Source Type | Ingestion Method | Notes |
|-------------|------------------|-------|
| GitHub repository | Clone + parse README, docs/, source structure | Primary path; extract concepts, architecture, key files |
| PDF | pdfplumber / pdftotext / OCR (pytesseract) | Full text + tables; skill available |
| Word / .docx | python-docx or pandoc | Extract headings, body, images |
| PowerPoint / .pptx | python-pptx (or LibreOffice conversion to PDF then text) | Extract slide titles, bullet text, speaker notes |
| Existing video | ffmpeg extract audio → transcript (Whisper or TTS timestamps) | Link back to original |
| Markdown / plain text | Direct read | Simplest path |
| Web page / paper URL | browse_page + summarizer | Optional |

## Recommended Flow

1. **Detect type** from extension or user input.
2. **Extract text + structure** (headings, sections, key claims).
3. **Produce concise source summary** + list of candidate video topics.
4. **Hand off** to script generation stage (same as GitHub path).

All extracted text becomes the source of truth for scripts, tags, and grounded chat. No invented PHI or proprietary content is stored.
