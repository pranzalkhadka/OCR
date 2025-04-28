from markdown import markdown
import base64

def generate_html_css(markdown_content, images, structure_metadata):
    
    html_content = []
    for page_md in markdown_content:
        html_page = markdown(page_md, extensions=['tables', 'fenced_code'])
        html_content.append(html_page)

    css = """
    body {
        font-family: Arial, sans-serif;
        font-size: 16px;
        line-height: 1.6;
        margin: 40px;
    }
    h1 {
        font-family: 'Times New Roman', serif;
        font-size: 32px;
        font-weight: bold;
        margin-bottom: 20px;
    }
    h2 {
        font-family: 'Times New Roman', serif;
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 15px;
    }
    p {
        margin-bottom: 10px;
    }
    table {
        border-collapse: collapse;
        width: 100%;
        margin-bottom: 20px;
    }
    th, td {
        border: 1px solid #ddd;
        padding: 8px;
        text-align: left;
    }
    th {
        background-color: #f2f2f2;
        font-weight: bold;
    }
    img {
        max-width: 100%;
        height: auto;
        margin: 10px 0;
    }
    .page {
        page-break-after: always;
        margin-bottom: 40px;
    }
    """

    html_pages = []
    default_metadata = {"dpi": 200, "width": 1700, "height": 2200}  
    for i, html_page in enumerate(html_content):
        for img in images:
            img_tag = f'<img src="{img["base64"]}" alt="{img["alt"]}"/>'
            html_page = html_page.replace(f'![{img["id"]}]({img["id"]})', img_tag)
        
        metadata = structure_metadata[i] if i < len(structure_metadata) else default_metadata
        page_width = metadata['width'] / metadata['dpi'] * 72
        page_html = f"""
        <div class="page" style="width: {page_width}px;">
            {html_page}
        </div>
        """
        html_pages.append(page_html)

    full_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Extracted Document</title>
        <style>{css}</style>
    </head>
    <body>
        {''.join(html_pages)}
    </body>
    </html>
    """

    return full_html

def save_html(html_content, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

def main(markdown_content, images, structure_metadata, output_html_path):

    html_content = generate_html_css(markdown_content, images, structure_metadata)
    save_html(html_content, output_html_path)
    return html_content

if __name__ == "__main__":
    from ocr_extract import main as ocr_main
    pdf_path = "/home/pranjal/Downloads/OCR/test.pdf"  
    markdown_content, images, structure_metadata = ocr_main(pdf_path)
    output_html_path = "output.html"
    if markdown_content:
        html_content = main(markdown_content, images, structure_metadata, output_html_path)
        print(f"HTML saved to {output_html_path}")
    else:
        print("Failed to extract content from PDF.")