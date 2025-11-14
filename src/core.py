import os
import sys
import tempfile
import shutil
import pdfkit
import pandas as pd
from jinja2 import Template
from PyPDF2 import PdfMerger
from datetime import date
from src.const import ROOT_PATH
from src.const import DEBUG, WKHTMLTOPDF_PATH, IS_FROZEN
from src.utils import no_accent_vietnamese, format_vnd, clean_decimal

# ---------------------------
# Handle font embedding
# ---------------------------


def prepare_wkhtmltopdf_font(wkhtmltopdf_path):

    config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)
    FONT_SRC_PATH = os.path.join(
        sys._MEIPASS if IS_FROZEN else ROOT_PATH, 'fonts', "DejaVuSans.ttf"
    )
    # Copy font to temp folder so wkhtmltopdf can access it
    TEMP_FONT_PATH = os.path.join(tempfile.gettempdir(), "DejaVuSans.ttf")
    shutil.copyfile(FONT_SRC_PATH, TEMP_FONT_PATH)

    FONT_SRC_QR = os.path.join(
        sys._MEIPASS if IS_FROZEN else ROOT_PATH, 'images', "qr.png"
    )
    TEMP_QR_PATH = os.path.join(tempfile.gettempdir(), "qr.png")
    shutil.copyfile(FONT_SRC_QR, TEMP_QR_PATH)

    return config, TEMP_FONT_PATH, TEMP_QR_PATH


config, TEMP_FONT_PATH, TEMP_QR_PATH = prepare_wkhtmltopdf_font(wkhtmltopdf_path=WKHTMLTOPDF_PATH)


def _fill_template_with_data(template, data):
    """
    Fill one HTML template string with data.
    - template_str: The HTML template content (as string)
    - data: A dictionary (e.g., one row from Excel)
    Returns: rendered HTML string
    """
    html_filled = template.render(**data)
    return html_filled


def read_excel(excel_path):
    df = pd.read_excel(excel_path, header=0, skiprows=[1, 2])
    df = df.dropna(subset=["Name"])
    df['Month'] = df['Month'].apply(clean_decimal)
    df['DateStart'] = df['DateStart'].dt.strftime('%d/%m/%Y')
    df['DateEnd']   = df['DateEnd'].dt.strftime('%d/%m/%Y')
    df['LEFT'] = df['LEFT'].apply(clean_decimal)
    df['DAYS'] = df['DAYS'].apply(clean_decimal)
    df['LUNCH_UT'] = df['LUNCH_UT'].apply(format_vnd)
    df['LUNCH_QT'] = df['LUNCH_QT'].apply(clean_decimal)
    df['LUNCH_VALUE'] = df['LUNCH_VALUE'].apply(format_vnd)
    df['TUITION_VALUE'] = df['TUITION_VALUE'].apply(format_vnd)
    df['BOARDING_VALUE'] = df['BOARDING_VALUE'].apply(format_vnd)
    df['CLEANING_VALUE'] = df['CLEANING_VALUE'].apply(format_vnd)
    df['CAMERA_VALUE'] = df['CAMERA_VALUE'].apply(format_vnd)
    df['OVERTIME_UT'] = df['OVERTIME_UT'].apply(format_vnd)
    df['OVERTIME_QT'] = df['OVERTIME_QT'].apply(clean_decimal)
    df['OVERTIME_VALUE'] = df['OVERTIME_VALUE'].apply(format_vnd)
    df['TOTAL'] = df['TOTAL'].apply(format_vnd)

    today = date.today()
    df['DAY_CURRENT'] = today.day
    df['MONTH_CURRENT'] = today.month
    df['YEAR_CURRENT'] = today.year
    return df


def generate_bills_from_html(excel_path, template_path, output_folder):
    """
    Generate all student bills using one HTML template (read once).
    """
    # 1️⃣ Read Excel file
    df = read_excel(excel_path)

    os.makedirs(output_folder, exist_ok=True)

    # 2️⃣ Read HTML template only once
    with open(template_path, encoding="utf-8") as f:
        template_str = Template(f.read())

    options = {
        "encoding": "UTF-8",
        "enable-local-file-access": None,
        "page-size": "A4",
        "margin-top": "10mm",
        "margin-right": "10mm",
        "margin-bottom": "10mm",
        "margin-left": "10mm",
    }

    # 3️⃣ Loop through rows
    for i, row in df.iterrows():
        data = row.to_dict()  # convert the current row to a dictionary
        # Fill HTML template for this student
        html_content = _fill_template_with_data(template_str, data)

        # Embed font dynamically
        font_url = f"file:///{TEMP_FONT_PATH.replace(os.sep, '/').replace(' ', '%20')}"
        html_content = html_content.replace("../fonts/DejaVuSans.ttf", font_url)
        qr_url = f"file:///{TEMP_QR_PATH.replace(os.sep, '/').replace(' ', '%20')}"
        html_content = html_content.replace("../images/qr.png", qr_url)


        # Output file name
        student_name = no_accent_vietnamese(str(data.get("Name", f"Unknown")))
        pdf_path = os.path.join(output_folder, f"{i}_{student_name}_bill.pdf")

        if DEBUG:
            with open("debug.html", "w", encoding="utf-8") as f:
                f.write(html_content)

        # 4️⃣ Convert to PDF
        pdfkit.from_string(html_content, pdf_path, configuration=config, options=options)
        print(f"Created: {pdf_path}")

    print("All bills generated successfully!")


def merge_pdfs_in_folder(folder_path, output_path):
    # Get all PDF files in the folder
    pdf_files = [f for f in os.listdir(folder_path) if f.lower().endswith(".pdf")]
    pdf_files.sort()  # optional: sort by name

    if not pdf_files:
        print("No PDF files found in folder.")
        return

    merger = PdfMerger()

    for pdf in pdf_files:
        pdf_path = os.path.join(folder_path, pdf)
        merger.append(pdf_path)

    merger.write(output_path)
    merger.close()
