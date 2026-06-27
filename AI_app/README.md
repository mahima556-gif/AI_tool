# AutoCert (Simple Version)

A very simple tool that creates certificates automatically from a list of names.

## How to run

1. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

2. Start the app:
   ```
   streamlit run app.py
   ```

3. Your browser will open at `http://localhost:8501`
   (If it doesn't open automatically, copy that link into your browser.)

## How to use

1. Prepare a CSV file with one column named `name`, listing all the people who should get a certificate.
2. Upload that CSV in the app.
3. Click **Generate Certificates**.
4. Click **Download All Certificates (ZIP)** to get all certificates at once.

## Files

- `app.py` — the main app (this is the only file you need to read to understand the project)
- `template.png` — the blank certificate design (light blue and white theme)
- `make_template.py` — the script that created `template.png` (you don't need to run this again)
- `requirements.txt` — list of required Python packages
