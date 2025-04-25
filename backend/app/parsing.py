import fitz
import docx
import io

def extract_text_from_file(file_content: bytes, filename: str) -> str | None:
    """
    Extracts plain text from PDF or DOCX file content.

    Args:
        file_content: The raw byte content of the file.
        filename: The original filename to determine the file type.

    Returns:
        The extracted text as a string, or None if extraction fails or format is unsupported.
    """
    text = None
    try:
        if filename.lower().endswith(".pdf"):
            pdf_document = fitz.open(stream=file_content, filetype="pdf")
            text = ""
            for page_num in range(len(pdf_document)):
                page = pdf_document.load_page(page_num)
                text += page.get_text()
            pdf_document.close()
            print(f"Successfully parsed PDF: {filename}")

        elif filename.lower().endswith(".docx"):
            doc = docx.Document(io.BytesIO(file_content))
            text = "\n".join([para.text for para in doc.paragraphs])
            print(f"Successfully parsed DOCX: {filename}")

        else:
            print(f"Unsupported file format: {filename}")

    except Exception as e:
        print(f"Error parsing file {filename}: {e}")
        return None

    return text

if __name__ == '__main__':
    try:
        with open("../tests/sample_resume.pdf", "rb") as f:
             pdf_content = f.read()
             pdf_text = extract_text_from_file(pdf_content, "sample_resume.pdf")
             if pdf_text:
                 print("\n--- PDF Text ---")
                 print(pdf_text[:500] + "...")
             else:
                 print("Failed to extract text from PDF.")
    except FileNotFoundError:
        print("Place a 'sample_resume.pdf' in a 'tests' directory sibling to 'app' to run this test.")

    try:
        with open("../tests/sample_resume.docx", "rb") as f:
             docx_content = f.read()
             docx_text = extract_text_from_file(docx_content, "sample_resume.docx")
             if docx_text:
                 print("\n--- DOCX Text ---")
                 print(docx_text[:500] + "...")
             else:
                 print("Failed to extract text from DOCX.")
    except FileNotFoundError:
        print("Place a 'sample_resume.docx' in a 'tests' directory sibling to 'app' to run this test.")