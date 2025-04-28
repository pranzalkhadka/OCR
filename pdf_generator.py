import pdfkit

def generate_pdf(html_path, output_pdf_path):
    try:
        pdfkit.from_file(html_path, output_pdf_path)
        print(f"PDF generated at {output_pdf_path}")
    except Exception as e:
        print(f"PDF generation error: {e}")

def main(html_path, output_pdf_path):
    generate_pdf(html_path, output_pdf_path)

if __name__ == "__main__":
    html_path = "output.html"
    output_pdf_path = "output_extractable.pdf"
    main(html_path, output_pdf_path)