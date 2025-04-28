import base64
import os
import json
from mistralai import Mistral
import google.generativeai as genai

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

mistral_client = Mistral(api_key=MISTRAL_API_KEY)
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel("gemini-1.5-flash")

def extract_with_mistral(pdf_path):
    try:
        with open(pdf_path, "rb") as pdf_file:
            base64_pdf = base64.b64encode(pdf_file.read()).decode('utf-8')
        
        ocr_response = mistral_client.ocr.process(
            model="mistral-ocr-latest",
            document={
                "type": "document_url",
                "document_url": f"data:application/pdf;base64,{base64_pdf}"
            }
        )
        return "\n\n".join([page.markdown for page in ocr_response.pages])
    except Exception as e:
        print(f"Mistral OCR error: {e}")
        return None

def extract_with_gemini(image_path):
    try:
        image_file = genai.upload_file(image_path)
        prompt = """
        Extract all visual metadata from this document image including:
        - Font styles (family, size, weight) for each text element
        - Colors (text, background)
        - Layout information (margins, spacing, alignment)
        - Structural elements (headings, paragraphs, lists, tables)
        - Any other relevant styling information
        
        Return as a detailed JSON structure.
        """
        response = gemini_model.generate_content([prompt, image_file])
        genai.delete_file(image_file.name)
        
        try:
            return json.loads(response.text)
        except json.JSONDecodeError:
            cleaned = response.text.replace('```json', '').replace('```', '').strip()
            return json.loads(cleaned)
    except Exception as e:
        print(f"Gemini extraction error: {e}")
        return None

def generate_html(text_content, metadata):
    prompt = f"""
    Create an HTML file with embedded CSS that recreates this document's content and styling.
    
    The document content is:
    {text_content}
    
    The visual metadata of the document is:
    {json.dumps(metadata, indent=2)}
    
    Requirements:
    1. Create a complete HTML file with proper structure (doctype, head, body)
    2. Use CSS to match the original document's styling as closely as possible
    3. Preserve all text content exactly
    4. Include comments explaining your styling choices
    5. Make the document responsive for different screen sizes
    6. Output JUST the HTML code with no additional commentary or markdown
    
    Return the complete HTML file wrapped in ```html ``` markers.
    """
    
    try:
        response = gemini_model.generate_content(prompt)
        if '```html' in response.text:
            return response.text.split('```html')[1].split('```')[0].strip()
        return response.text
    except Exception as e:
        print(f"HTML generation error: {e}")
        return None

def save_html(html_content, output_path):
    try:
        with open(output_path, 'w') as f:
            f.write(html_content)
        print(f"Successfully saved HTML to {output_path}")
    except Exception as e:
        print(f"Error saving HTML file: {e}")

def process_document(pdf_path, image_path, output_html_path):
    
    print("Extracting text content with Mistral OCR...")
    text_content = extract_with_mistral(pdf_path)
    if not text_content:
        print("Failed to extract text content")
        return
    
    print("Extracting visual metadata with Gemini...")
    metadata = extract_with_gemini(image_path)
    if not metadata:
        print("Failed to extract metadata")
        return
    
    print("Generating HTML...")
    html_content = generate_html(text_content, metadata)
    if not html_content:
        print("Failed to generate HTML")
        return
    
    save_html(html_content, output_html_path)

if __name__ == "__main__":
    pdf_path = "/home/pranjal/Downloads/OCR/test2.pdf"
    image_path = "/home/pranjal/Downloads/OCR/test_img.png"
    output_html_path = "/home/pranjal/Downloads/OCR/output.html"
    
    process_document(pdf_path, image_path, output_html_path)