import streamlit as st
import os
import tempfile
import json
from src.convert_pdf import convert_pdf_to_images
from src.ocr import extract_text_from_image
from src.extract_fields import extract_fields_from_text
from PIL import Image

st.set_page_config(page_title="Invoice Field Extractor", layout="wide")

st.title("🧾 Invoice Field Extractor")
st.caption("Upload an image or PDF invoice to extract key fields")

uploaded_file = st.file_uploader("Upload invoice (.jpg/.png/.pdf)", type=["jpg", "jpeg", "png", "pdf"])

if uploaded_file:
    # Save uploaded file to temp file
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = os.path.join(tmpdir, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.read())

        st.success(f"Uploaded: {uploaded_file.name}")

        results = []

        if uploaded_file.name.lower().endswith(".pdf"):
            image_paths = convert_pdf_to_images(file_path, output_dir=tmpdir)
        else:
            image = Image.open(file_path)
            image_path = os.path.join(tmpdir, "invoice.jpg")
            image.save(image_path)
            image_paths = [image_path]

        for img_path in image_paths:
            st.image(img_path, caption=os.path.basename(img_path), use_column_width=True)
            text = extract_text_from_image(img_path)
            fields = extract_fields_from_text(text)
            results.append(fields)

        st.subheader("📄 Extracted Fields")
        st.json(results)

        # Download JSON
        json_output = json.dumps(results, indent=2)
        st.download_button("📥 Download JSON", json_output, file_name="invoice_data.json", mime="application/json")
