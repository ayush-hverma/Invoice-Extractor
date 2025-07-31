import os
import json
from .convert_pdf import convert_pdf_to_images
from .ocr import extract_text_from_image
from .extract_fields import extract_fields_from_text

def process_invoice(pdf_path):
    image_paths = convert_pdf_to_images(pdf_path, output_dir="data/images")

    results = []
    for img_path in image_paths:
        text = extract_text_from_image(img_path)
        fields = extract_fields_from_text(text)
        fields['image'] = os.path.basename(img_path)
        results.append(fields)

    os.makedirs("outputs", exist_ok=True)
    output_file = f"outputs/{os.path.splitext(os.path.basename(pdf_path))[0]}.json"
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)

    print(f" Processed: {os.path.basename(pdf_path)} → {output_file}")
    return output_file

def process_all_pdfs(folder_path):
    pdf_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.pdf')]
    total = 0
    for pdf in pdf_files:
        pdf_path = os.path.join(folder_path, pdf)
        process_invoice(pdf_path)
        total += 1

    print(f"\n Processed {total} PDF(s).")

if __name__ == "__main__":
    import sys
    folder = sys.argv[1] if len(sys.argv) > 1 else "data/raw"
    process_all_pdfs(folder)
