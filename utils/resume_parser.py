import os
from pypdf import PdfReader
from docx import Document


def extract_text(file_path):

    file_extension = os.path.splitext(file_path)[1].lower()

    # PDF file
    if file_extension == ".pdf":

        reader = PdfReader(file_path)

        text = ""

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        return text

    # DOCX file
    elif file_extension == ".docx":

        document = Document(file_path)

        text = ""

        for paragraph in document.paragraphs:
            text += paragraph.text + "\n"

        return text

    else:
        return "Unsupported file format."