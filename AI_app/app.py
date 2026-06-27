
import streamlit as st
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import io
import zipfile

# ---------- Basic page setup (light theme colors) ----------
st.set_page_config(page_title="Auto-Certificate Generator", page_icon="🎓")
st.markdown("""
<style>

/* Background */
.stApp {
    background-color: #EAF6FF;
}

/* Headings */
h1, h2, h3 {
    color: #0D47A1 !important;
    text-align: center;
}

/* Normal text */
p, label, span {
    color: #0D47A1 !important;
}

/* File uploader text */
div[data-testid="stFileUploader"] {
    color: #0D47A1 !important;
    background-color: white;
    border: 2px solid #90CAF9;
    border-radius: 12px;
    padding: 12px;
}

/* Table */
table {
    border-collapse: collapse !important;
}

table th {
    color: #0D47A1 !important;
    background-color: #D6ECFF !important;
    border: 1px solid #90CAF9 !important;
}

table td {
    color: #0D47A1 !important;
    border: 1px solid #90CAF9 !important;
}

/* Generate Button */
.stButton > button {
    width: 100%;
    background-color: #0D47A1 !important;
    color: white !important;
    font-size: 18px !important;
    font-weight: bold !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px 20px !important;
}

/* Force button text to white */
.stButton > button * {
    color: white !important;
}

/* Download Button */
.stDownloadButton > button {
    width: 100%;
    background-color: #0D47A1 !important;
    color: white !important;
    font-size: 18px !important;
    font-weight: bold !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px 20px !important;
}

/* Force download button text to white */
.stDownloadButton > button * {
    color: white !important;
}

/* Success Message */
div[data-testid="stAlert"] {
    background-color: #D6ECFF !important;
}

div[data-testid="stAlert"] p {
    color: #0D47A1 !important;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)

# Light theme color codes (used when drawing text on the certificate)
TEXT_COLOR = "#0B3D91"   # dark grey, easy to read
LINE_Y = 460             # vertical position (in pixels) where the name is printed

FONT_PATH = "Roboto-Regular.ttf.ttx"


# ---------- Function: create one certificate image ----------

def make_certificate(name):
    # Open the blank template

    from pathlib import Path
    BASE_DIR = Path(__file__).parent
    img = Image.open(BASE_DIR / "template.png").convert("RGB")
    draw = ImageDraw.Draw(img)

    # Choose font and size for the name
    font = ImageFont.truetype(FONT_PATH, 55)

    # Find text width so we can center it
    bbox = draw.textbbox((0, 0), name, font=font)
    text_width = bbox[2] - bbox[0]
    image_width = img.size[0]
    x_position = (image_width - text_width) / 2

    # Draw the name onto the certificate
    draw.text((x_position, LINE_Y - 70), name, font=font, fill=TEXT_COLOR)

    return img


# ---------- App title ----------
st.title("🎓 Auto-Certificate Generator")

# ---------- File upload ----------
uploaded_csv = st.file_uploader("Upload your CSV file here", type=["csv"])

if uploaded_csv is not None:
    # Read the CSV into a table
    data = pd.read_csv(uploaded_csv)

    # Check that the "name" column exists
    if "name" not in data.columns:
        st.error("Your CSV must have a column named 'name'.")
    else:
        names_list = data["name"].dropna().tolist()
        st.success(f"Found {len(names_list)} name(s) in the file.")
        st.dataframe(data, use_container_width=True)

        # ---------- Generate button ----------
        if st.button("Generate Certificates"):

            # This will store all certificate images in memory before zipping
            zip_buffer = io.BytesIO()

            with zipfile.ZipFile(zip_buffer, "w") as zip_file:
                for person_name in names_list:
                    cert_image = make_certificate(person_name)

                    # Convert image to bytes so it can go inside the ZIP
                    image_bytes = io.BytesIO()
                    cert_image.save(image_bytes, format="PNG")

                    # Add this certificate to the ZIP file
                    file_name = person_name.replace(" ", "_") + "_certificate.png"
                    zip_file.writestr(file_name, image_bytes.getvalue())

            st.success("All certificates generated!")

            # Show a preview of the last certificate made
            st.write("Preview:")
            st.image(cert_image, width=500)

            # ---------- Download button ----------
            st.download_button(
                label="Download All Certificates (ZIP)",
                data=zip_buffer.getvalue(),
                file_name="certificates.zip",
                mime="application/zip"
            )
