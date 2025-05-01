import base64
import os
from anthropic import Anthropic

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def extract_form_metadata(api_key, image_path):
    client = Anthropic(api_key=api_key)
    
    try:
        base64_image = encode_image(image_path)
        
        response = client.messages.create(
            model="claude-3-opus-20240229", 
            max_tokens=4000,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/png",
                                "data": base64_image
                            }
                        },
                        {
                            "type": "text",
                            "text": """Extract every text from the image along with layout."""
                        }
                    ]
                }
            ]
        )
        return response.content[0].text
    
    except Exception as e:
        print(f"Extraction error: {e}")
        return None

def main():
    API_KEY = "api-key"
    IMAGE_PATH = "/home/pranjal/Downloads/OCR/data/test4.png"
    
    # Step 1: Extract form metadata
    print("Analyzing form structure...")
    result = extract_form_metadata(API_KEY, IMAGE_PATH)
    
    if result:
        with open("claude_output.html", "w", encoding="utf-8") as f:
            f.write(result)
        print("Successfully saved to claude_output.html")
    else:
        print("Failed to generate HTML form")

if __name__ == '__main__':
    main()