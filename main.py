import os
from ocr_extract import main as ocr_main
from html_generator import main as html_main

def pipeline(pdf_path, image_path, html_output_path):
    
    markdown_content, images, structure_metadata, gemini_metadata = ocr_main(pdf_path, image_path)
    if not markdown_content:
        print("Failed to extract content.")
        return
    html_content = html_main(markdown_content, images, structure_metadata, gemini_metadata, html_output_path)
    if not html_content:
        print("Failed to generate HTML.")
        return
    print(f"HTML generated at {html_output_path}")

if __name__ == "__main__":
    pdf_path = "/home/pranjal/Downloads/OCR/test2.pdf"
    image_path = "/home/pranjal/Downloads/OCR/test_img.png"
    html_output_path = "output.html"
    pipeline(pdf_path, image_path, html_output_path)