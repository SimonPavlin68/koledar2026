import pdfkit
from datetime import datetime
import base64

version = "6"

def get_base64_image(path):
    with open(path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

def json_to_colored_pdf(data, pdf_file):
    # --- Header (logo + naslov + datum) ---
    logo_path = os.path.join(os.path.dirname(__file__), 'static', 'images', 'logo.png')
    logo_base64 = get_base64_image(logo_path)
    # current_date = datetime.now().strftime("%d.%m.%Y")
    current_date = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

    header_html = f"""
   <table style="width:100%; border-collapse:collapse; margin-bottom:10px;">
  <tr>
    <td style="width:20%; text-align:left; padding-left:20px; vertical-align:middle;">
      <img src="data:image/png;base64,{logo_base64}" alt="Logo" style="height:60px; vertical-align:middle;">
    </td>
    <td style="width:60%; text-align:center; vertical-align:middle;">
      <h3 style="margin:0; font-family:Arial, sans-serif; margin-left:-150px;">
        Koledar tekmovanj za leto 2026
      </h3>
    </td>
  </tr>
</table>



    """

    footer_html = f"""
        <table style="width:100%; border-collapse:collapse; margin-top:20px;">
          <tr>
          <td style="text-align:left; padding-left:20px; font-family:Arial; font-size:12px; color:silver;">* Termini so bili določeni s strani Strokovnega sveta v koledarju 2025.</td>
          </tr>
          <tr>
          <td style="text-align:left; padding-left:20px; font-family:Arial; font-size:12px; color:silver;">** prestavljen datum 18.4. -> 19.4.</td>
          </tr>
          <tr>
          <td style="text-align:left; padding-left:20px; font-family:Arial; font-size:12px; color:silver;">*** prestavljen datum 20.6. -> 21.6.</td>
          </tr>
          <tr>
          <td style="text-align:left; padding-left:20px; font-family:Arial; font-size:12px; color:silver;">Koledar potrjen na 3. redni seji IO 17.2.2026</td></tr>
        </table>
        <table style="width:100%; border-collapse:collapse; margin-top:50px;">
        <tr>
            <td style="text-align:left; padding-left:20px; font-family:Arial; font-size:8px; color:silver;">
                © 2026 Lokostrelska zveza Slovenije – koledar V{version} (verzija za interne potrebe)
            </td>
            <td style="width:20%; text-align:right; padding-right:20px; font-family:Arial, sans-serif; font-size:8px; color:silver;">
          generirano: {current_date}
        </td>
         <tr>
            <td style="text-align:left; padding-left:20px; font-family:Arial; font-size:8px; color:white;">by Simon</td>
            <td style="width:20%; text-align:right; padding-right:20px; font-family:Arial, sans-serif; font-size:8px; color:white;"></td>
          </tr>
          
        </table>
    """

    # --- Sortiranje po datumu ---
    def parse_date(d):
        try:
            return datetime.strptime(d, "%d.%m.%Y")
        except:
            return datetime.max
    data_sorted = sorted(data, key=lambda x: parse_date(x.get("od","")))

    # --- HTML tabela (1px robovi, nastavljeno na th in td) ---
    table_html = """
   <table cellspacing="0" cellpadding="5"
       style="border-collapse: collapse; width: 100%; font-family: Arial; font-size: 10px;">
      <tr>
        <th style="border: 1px solid black;">OD</th>
        <th style="border: 1px solid black;">DO</th>
        <th style="border: 1px solid black;">DISCIPLINA</th>
        <th style="border: 1px solid black;">KRAJ</th>
        <th style="border: 1px solid black;">ORGANIZATOR</th>
        <th style="border: 1px solid black;">TEKMOVANJE</th>
        <th style="border: 1px solid black;">I@nseo id</th>
      </tr>
    """

    # Barvanje glede na disciplino
    def barva_disciplina(disciplina, organizator):
        if not organizator:
            return "white"
        if disciplina == "AH 12+12":
            return "lightgreen"
        elif disciplina == "3D krog":
            return "#f28b82"
        elif disciplina.startswith("70/50m krog"):
            return "yellow"
        elif disciplina == "Dvoranski krog 25m + 18m":
            return "#DDDDDD"
        elif disciplina.startswith("Dvorana") or disciplina.startswith("Dvoranski krog"):
            return "#998AFF"
        elif disciplina == "Šolsko" or disciplina == "Šolsko tekmovanje":
            return "orange"
        elif disciplina == "900 krogov":
            return "#DDDDDD"   # svetlejša siva (namesto silver)
        else:
            return "white"

    # Vrstice
    for row in data_sorted:
        disciplina = (row.get("disciplina") or "").strip()
        tekmovanje = row.get("tekmovanje", "")
        organizator = row.get("organizator", "")
        if tekmovanje == "Veronikin pokal 2026":
            bgcolor = "#DDDDDD"
        else:
            bgcolor = barva_disciplina(disciplina, organizator)

        od_val = row.get("od", "")
        do_raw = row.get("do", "")

        # Če sta od in do enaka → do je prazen
        do_val = "" if do_raw == od_val else do_raw
        id = (row.get("ianseo_id") or "").strip()
        table_html += f'<tr style="background-color:{bgcolor};">'
        table_html += f'<td style="border:1px solid black; vertical-align:top;">{od_val}</td>'
        table_html += f'<td style="border:1px solid black; vertical-align:top;">{do_val}</td>'
        table_html += f'<td style="border:1px solid black; vertical-align:top;">{disciplina}</td>'
        table_html += f'<td style="border:1px solid black; vertical-align:top;">{row.get("kraj", "")}</td>'
        table_html += f'<td style="border:1px solid black; vertical-align:top;">{organizator}</td>'
        table_html += f'<td style="border:1px solid black; vertical-align:top;">{tekmovanje}</td>'
        table_html += f'<td style="border:1px solid black; vertical-align:top;">{id}</td>'
        table_html += "</tr>"

    table_html += "</table>"

    # --- Celoten HTML ---
    full_html = f"""
    <html>
    <head><meta charset="utf-8"></head>
    <body>
      {header_html}
      {table_html}
      {footer_html}
    </body>
    </html>
    """

    # --- PDF generiranje (robustne opcije) ---
    options = {
        'page-size': 'A4',
        'encoding': "UTF-8",
        'margin-top': '15mm',
        'margin-bottom': '15mm',
        'margin-left': '10mm',
        'margin-right': '10mm'
    }

    wkhtml_path = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
    config = pdfkit.configuration(wkhtmltopdf=wkhtml_path) if os.path.exists(wkhtml_path) else None

    pdfkit.from_string(full_html, pdf_file, options=options, configuration=config)
    print(f"✅ PDF ustvarjen: {pdf_file}")




def main1():
    # naložiš svoj JSON
    with open("input/competitions-final.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    json_to_colored_pdf(data, "output/koledar_tekem-final.pdf")

import json
import os

def main():
    # glavni input
    with open("input/competitions-final.json", "r", encoding="utf-8") as f:
        competitions = json.load(f)

    # dodatni dogodki (events.json)
    events_path = "input/events-final.json"
    if os.path.exists(events_path):
        with open(events_path, "r", encoding="utf-8") as f:
            extra_events = json.load(f)
    else:
        print("events.json ni najden — nadaljujem samo z competitions-final.json")
        extra_events = []

    # združimo v skupni seznam
    combined_events = competitions + extra_events

    # generiranje PDF koledarja
    json_to_colored_pdf(combined_events, f"output/koledar_tekem-final-{version}.pdf")
    print("PDF generiran.")

if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()