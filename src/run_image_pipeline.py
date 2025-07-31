import os
import json
from src.ocr import extract_text_from_image
from src.extract_fields import extract_fields_from_text

def process_invoice_image(image_path):
    text = extract_text_from_image(image_path)
    fields = extract_fields_from_text(text)
    fields['image'] = os.path.basename(image_path)
    return fields

def process_all_images(folder_path):
    os.makedirs("outputs", exist_ok=True)
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    all_results = []

    for image_file in image_files:
        image_path = os.path.join(folder_path, image_file)
        print(f" Processing {image_file}")
        result = process_invoice_image(image_path)
        
        output_file = os.path.join("outputs", f"{os.path.splitext(image_file)[0]}.json")
        with open(output_file, "w") as f:
            json.dump(result, f, indent=2)
        
        print(f" Saved: {output_file}")
        all_results.append(result)
    
    print(f"\n Processed {len(all_results)} images.")
    return all_results

if __name__ == "__main__":
    import sys
    folder_path = sys.argv[1] if len(sys.argv) > 1 else "data/images"
    process_all_images(folder_path)
