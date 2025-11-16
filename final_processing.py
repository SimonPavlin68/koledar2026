import json
import os
import pdfkit
from datetime import datetime
import base64


def get_base64_image(path):
    with open(path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

def json_to_colored_pdf(data, pdf_file):
    # --- Header (logo + naslov + datum) ---
    logo_path = os.path.join(os.path.dirname(__file__), 'static', 'images', 'logo.png')
    logo_base64 = get_base64_image(logo_path)
    current_date = datetime.now().strftime("%d.%m.%Y")

    header_html = f"""
    <table style="width:100%; border-collapse:collapse; margin-bottom:10px;">
      <tr style="vertical-align:middle;">
        <td style="width:20%; text-align:left; padding-left:20px;">
          <img src="data:image/png;base64,{logo_base64}" alt="Logo" style="height:60px; vertical-align:middle;">
        </td>
        <td style="width:60%; text-align:center;">
          <h3 style="margin:0; font-family:Arial, sans-serif;">Koledar tekmovanj za leto 2026</h2>
        </td>
        <td style="width:20%; text-align:right; padding-right:20px; font-family:Arial, sans-serif; font-size:8px; color:silver;">
          {current_date}
        </td>
      </tr>
    </table>
    """

    # --- Sortiranje po datumu ---
    def parse_date(d):
        try:
            return datetime.strptime(d, "%d.%m.%Y")
        except:
            return datetime.max  # če ni datuma, na konec
    data_sorted = sorted(data, key=lambda x: parse_date(x.get("od","")))

    # --- HTML tabela ---
    table_html = """
   <table cellspacing="0" cellpadding="5"
       style="border-collapse: collapse; width: 100%; font-family: Arial; font-size: 10px; border: 0.5px solid black;">
      <tr>
        <th style="border: 0.5px solid black;">OD</th>
        <th style="border: 0.5px solid black;">DO</th>
        <th style="border: 0.5px solid black;">DISCIPLINA</th>
        <th style="border: 0.5px solid black;">KRAJ</th>
        <th style="border: 0.5px solid black;">ORGANIZATOR</th>
        <th style="border: 0.5px solid black;">TEKMOVANJE</th>
    </tr>
    """

    # Barvanje glede na disciplino
    def barva_disciplina(disciplina):
        if disciplina == "AH 12+12":
            return "lightgreen"
        elif disciplina == "3D krog":
            return "#f28b82"
        elif disciplina.startswith("70/50m krog"):
            return "yellow"
        elif disciplina == "Dvorana 25m":
            return "#f5f5f5"
        elif disciplina.startswith("Dvorana") or disciplina.startswith("Dvoranski krog"):
            return "#998AFF"
        elif disciplina == "Šolsko tekmovanje":
            return "orange"
        elif disciplina == "900 krogov":
            return "silver"
        else:
            return "white"

    # Vrstice
    for row in data_sorted:
        disciplina = row.get("disciplina", "")
        bgcolor = barva_disciplina(disciplina)

        table_html += f'<tr style="background-color:{bgcolor};">'

        table_html += f'<td style="border: 0.5px solid black;">{row.get("od", "")}</td>'
        table_html += f'<td style="border: 0.5px solid black;">{row.get("do", "")}</td>'
        table_html += f'<td style="border: 0.5px solid black;">{row.get("disciplina", "")}</td>'
        table_html += f'<td style="border: 0.5px solid black;">{row.get("kraj", "")}</td>'
        table_html += f'<td style="border: 0.5px solid black;">{row.get("organizator", "")}</td>'
        table_html += f'<td style="border: 0.5px solid black;">{row.get("tekmovanje", "")}</td>'

        table_html += "</tr>"

    table_html += "</table>"

    # --- Celoten HTML ---
    full_html = f"""
    <html>
    <head><meta charset="utf-8"></head>
    <body>
      {header_html}
      {table_html}
    </body>
    </html>
    """

    # --- PDF generiranje ---
    wkhtml_path = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
    config = pdfkit.configuration(wkhtmltopdf=wkhtml_path)

    pdfkit.from_string(full_html, pdf_file, configuration=config)
    print(f"✅ PDF ustvarjen: {pdf_file}")



def main():
    # naložiš svoj JSON
    with open("input/competitions-final.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    json_to_colored_pdf(data, "output/koledar_tekem-final.pdf")


if __name__ == "__main__":
    main()