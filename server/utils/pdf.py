import fitz 


def extract_text_from_pdf_content(pdf_content):
    try:
        text_per_page = []
        pdf_document = fitz.open("pdf", pdf_content)
        for page_num in range(pdf_document.page_count):
            page = pdf_document[page_num]
            text_per_page.append(page.get_text())

        pdf_document.close()

        return text_per_page
    except Exception as e:
        print(f"Error: {e}")
        return None
