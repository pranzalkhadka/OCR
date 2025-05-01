import google.generativeai as genai
import os

import pdfkit

def generate_pdf(html_path, output_pdf_path):
    try:
        pdfkit.from_file(html_path, output_pdf_path)
        print(f"PDF generated at {output_pdf_path}")
    except Exception as e:
        print(f"PDF generation error: {e}")

API_KEY = "AIzaSyBXiMNmOVmrCnOCP-sjGcaPnL1bTfzDI2Y"
genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-1.5-pro")

image_path = "/home/pranjal/Downloads/OCR/data/test4.png"
# extraction_prompt = """Analyze the provided image. Generate HTML code with embedded CSS (within a <style> tag in the <head>) that closely mimics the visual appearance and layout of the image.

# Focus on accurately reproducing:
# - The positioning and dimensions of all elements (text blocks, lines, boxes, form fields, etc.).
# - The text content itself, placed correctly.
# - Font characteristics like size, weight (bold/normal), and alignment (left/center/right). Use standard web fonts that visually approximate the original.
# - Colors used for text, backgrounds, and borders.
# - Border styles (solid, dashed, etc.) and thickness.
# - Spacing between elements (margins and padding).

# Represent any images or complex graphical elements with appropriately sized placeholder divs or image tags. The goal is a static HTML/CSS structure that visually matches the input image as faithfully as possible when rendered in a browser. Output the complete HTML code.
# """

extraction_prompt = """Analyze the provided image meticulously. Generate a single HTML file containing both the structure (HTML) and the styling (CSS within a <style> tag in the <head>) to visually replicate the image with high fidelity. Output the complete HTML code within a single ` ```html ... ``` ` block.

Pay close attention to replicating these specific details:
1.  **Layout & Positioning:** Recreate the exact positioning (consider using CSS position, flexbox, or grid where appropriate), dimensions (width/height in pixels or relative units if applicable), margins, and padding of all visible elements relative to each other and the page.
2.  **Text Content & Typography:** Extract all text accurately. Match font sizes (e.g., in `px` or `pt`), font weights (`bold`, `normal`), text alignment (`left`, `center`, `right`, `justify`), and text colors. If the font family is obvious (like a standard serif/sans-serif), use a common web-safe equivalent (e.g., Arial, Helvetica, Times New Roman); otherwise, use a default sans-serif.
3.  **Colors:** Capture background colors (for the page or specific elements) and border colors precisely, preferably using hexadecimal (`#RRGGBB`) values.
4.  **Borders & Lines:** Reproduce all borders and separating lines, matching their style (`solid`, `dashed`, `dotted`), thickness (`px`), and color. Include `border-radius` for rounded corners if present.
5.  **Structural Elements:** Use appropriate HTML tags (e.g., `div`, `span`, `p`, `h1`-`h6`, `table`, `tr`, `td`, `th`, `ul`, `ol`, `li`).
6.  **Form Elements:** If form elements like input fields, checkboxes, radio buttons, dropdowns (`select`), or buttons are present, represent them using the corresponding HTML tags (`<input>`, `<select>`, `<button>`, etc.), attempting to match their visual style and size.

The primary objective is visual accuracy in the static rendering. The generated HTML/CSS should look almost identical to the provided image when viewed in a web browser.
"""

image_file = genai.upload_file(image_path)

try:
    extraction_response = model.generate_content([extraction_prompt, image_file])
    extracted_data = extraction_response.text
    
    output_path = "gemini_output.html"
    with open(output_path, "w") as f:
        f.write(extracted_data)
    
    print(f"HTML form successfully saved to {output_path}")

    pdf_output_path = "gemini_output.pdf"
    generate_pdf(output_path, pdf_output_path)
    print(f"PDF form successfully saved to {pdf_output_path}")

finally:
    genai.delete_file(image_file.name)