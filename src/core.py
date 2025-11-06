import os
import pandas as pd
from jinja2 import Template
from weasyprint import HTML

def fill_template_with_data(template, data):
    """
    Fill one HTML template string with data.
    - template_str: The HTML template content (as string)
    - data: A dictionary (e.g., one row from Excel)
    Returns: rendered HTML string
    """
    html_filled = template.render(**data)
    return html_filled

def read_excel(excel_path):
    df = pd.read_excel(excel_path,  header=0, skiprows=[1,2])
    df = df.dropna(subset=["Name"])
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

    count = 0
    # 3️⃣ Loop through rows
    for _, row in df.iterrows():
        data = row.to_dict()  # convert the current row to a dictionary
        # Fill HTML template for this student
        html_content = fill_template_with_data(template_str, data)

        # Output file name
        student_name = str(row.get("Name", "Unknown")).replace(" ", "_")
        pdf_path = os.path.join(output_folder, f"{student_name}_bill.pdf")

        # 4️⃣ Convert to PDF
        HTML(string=html_content).write_pdf(pdf_path)
        print(f"✅ Created: {pdf_path}")
        count += 1

    print("🎉 All bills generated successfully!")