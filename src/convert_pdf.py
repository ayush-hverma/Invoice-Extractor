from pdf2image import convert_from_path
import os

def convert_pdf_to_images(pdf_path, output_dir):
    images = convert_from_path(pdf_path)
    image_paths = []

    for i, image in enumerate(images):
        image_path = os.path.join(output_dir, f"page_{i}.png")
        image.save(image_path, "PNG")
        image_paths.append(image_path)

    return image_paths
