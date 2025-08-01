import streamlit as st
import os
import json
import tempfile
from PIL import Image
from src.convert_pdf import convert_pdf_to_images
from src.ocr import extract_text_from_image
from src.extract_fields import extract_fields_from_text

st.title("🧾 Invoice Field Extractor")

uploaded_file = st.file_uploader("Upload an invoice (PDF or Image)", type=["pdf", "jpg", "png"])

if uploaded_file:
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = os.path.join(tmpdir, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.read())

        image_paths = []

        if uploaded_file.name.lower().endswith(".pdf"):
            image_paths = convert_pdf_to_images(file_path, tmpdir)
        else:
            image = Image.open(file_path)
            image_path = os.path.join(tmpdir, "invoice.jpg")
            image.save(image_path)
            image_paths = [image_path]

        all_fields = []
        for img_path in image_paths:
            text = extract_text_from_image(img_path)
            fields = extract_fields_from_text(text)
            all_fields.append(fields)
            st.image(img_path, caption="Page Image", use_column_width=True)
            st.json(fields)

        st.download_button("📥 Download JSON", json.dumps(all_fields, indent=2), file_name="invoice_data.json")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8501))
    os.system(f"streamlit run app.py --server.port={port} --server.enableCORS=false")
