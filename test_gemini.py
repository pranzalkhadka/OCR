import google.generativeai as genai
import json
import os

API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")  

image_path = "/home/pranjal/Downloads/OCR/test_img.png"  

prompt = """
Extract all text from the provided image along with all possbile metadata such as font, color, placement, lines and so on. 
"""

image_file = genai.upload_file(image_path)

try:
    response = model.generate_content([prompt, image_file])
    
    extracted_data = response.text
    
    try:
        result = json.loads(extracted_data)
        print("Extracted Data:")
        print(json.dumps(result, indent=2))
    except json.JSONDecodeError:
        print("Raw Extracted Text:")
        print(extracted_data)

finally:
    genai.delete_file(image_file.name)
