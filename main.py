import os
from ocr_extract import main as ocr_main
from html_generator import main as html_main
from pdf_generator import main as pdf_main

def pipeline(pdf_path, html_output_path, pdf_output_path):
    
    markdown_content, images, structure_metadata = ocr_main(pdf_path)
    if not markdown_content:
        print("Failed to extract content.")
        return

    html_content = html_main(markdown_content, images, structure_metadata, html_output_path)
    if not html_content:
        print("Failed to generate HTML.")
        return

    pdf_main(html_output_path, pdf_output_path)

if __name__ == "__main__":
    pdf_path = "test.pdf" 
    html_output_path = "output.html"
    pdf_output_path = "output_extractable.pdf"
    pipeline(pdf_path, html_output_path, pdf_output_path)