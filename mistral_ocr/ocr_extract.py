import base64
import os
from mistralai import Mistral

# API_KEY = os.getenv("MISTRAL_API_KEY")
API_KEY = "BosudCIA42Asdkp17qpYofjiGv6D1HHC"

client = Mistral(api_key=API_KEY)

def encode_pdf(pdf_path):
    try:
        with open(pdf_path, "rb") as pdf_file:
            return base64.b64encode(pdf_file.read()).decode('utf-8')
    except FileNotFoundError:
        print(f"Error: The file {pdf_path} was not found.")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def process_pdf(pdf_path):

    base64_pdf = encode_pdf(pdf_path)
    try:
        ocr_response = client.ocr.process(
            model="mistral-ocr-latest",
            document={
                "type": "document_url",
                "document_url": f"data:application/pdf;base64,{base64_pdf}"
            },
            include_image_base64=True
        )
        return ocr_response
    except Exception as e:
        print(f"OCR processing error: {e}")
        return None

def extract_content(ocr_response):

    if not ocr_response:
        return None, None, None

    markdown_content = []
    images = []
    structure_metadata = []

    for page in ocr_response.pages:
        markdown_content.append(page.markdown)
        
        for img in page.images:
            images.append({
                "id": img.id,
                "base64": img.image_base64
                # "alt": img.alt or f"Image {img.id}"
            })
        
        structure_metadata.append({
            "dpi": page.dimensions.dpi,
            "height": page.dimensions.height,
            "width": page.dimensions.width
        })

    return markdown_content, images, structure_metadata

def main(pdf_path):

    ocr_response = process_pdf(pdf_path)
    markdown_content, images, structure_metadata = extract_content(ocr_response)
    return markdown_content, images, structure_metadata

if __name__ == "__main__":
    pdf_path = "/home/pranjal/Downloads/OCR/test_4.pdf" 
    markdown_content, images, structure_metadata = main(pdf_path)
    if markdown_content:
        print("Markdown Content:", markdown_content)
        print("Images:", len(images))
        print("Structure Metadata:", structure_metadata)