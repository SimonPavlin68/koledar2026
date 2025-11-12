import csv
import json
import os
from calendar_generator import generate_weekends_by_day
from config import START_YEAR, START_WEEK, END_YEAR, END_WEEK, OUTPUT_FILE, OUTPUT_FILE_PDF, INPUT_FILE_COMPETITIONS, INPUT_FILE_EVENTS
import pdfkit
import base64
from datetime import datetime


def get_base64_image(path):
    with open(path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')


def csv_to_colored_pdf(csv_file, pdf_file):
    import csv, os
    from datetime import datetime
    import pdfkit

    # Naloži vse vrstice
    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        rows = list(reader)

    # Štetje vrstic za rowspan
    teden_count = {}
    opombe_count = {}

    for row in rows:
        t = row["TEDEN"].strip()
        datum = row.get("DATUM", "").strip()
        # Ključ vključuje leto (da se tedni iz različnih let ne združijo)
        leto = datum[-4:] if len(datum) >= 4 else "0000"
        t_key = f"{t}_{leto}"

        op = row.get("OPOMBE", "").strip()

        teden_count[t_key] = teden_count.get(t_key, 0) + 1
        opombe_count[(t_key, op)] = opombe_count.get((t_key, op), 0) + 1

    # Logo za header
    logo_path = os.path.join(os.path.dirname(__file__), 'static', 'images', 'logo.png')
    logo_base64 = get_base64_image(logo_path)
    current_date = datetime.now().strftime("%d.%m.%Y")

    header_html = f"""
    <table style="width:100%; border-collapse:collapse; margin-bottom:10px;">
      <tr style="vertical-align:middle;">
        <td style="width:20%; text-align:left; padding-left:20px;">
          <img src="data:image/png;base64,{logo_base64}" alt="Logo" style="height:75px; vertical-align:middle;">
        </td>
        <td style="width:60%; text-align:center;">
          <h2 style="margin:0; font-family:Arial, sans-serif;">Predlog koledarja 2026</h2>
        </td>
        <td style="width:20%; text-align:right; padding-right:20px; font-family:Arial, sans-serif; font-size:14px; color:silver;">
          {current_date}
        </td>
      </tr>
    </table>
    """

    # Gradnja HTML tabele
    table_html = '<table border="1" cellspacing="0" cellpadding="5" style="border-collapse: collapse; width: 100%;">'
    table_html += '<tr>'
    for header in reader.fieldnames:
        table_html += f'<th>{header}</th>'
    table_html += '</tr>'

    teden_done = set()
    opombe_done = set()

    for row in rows:
        t = row["TEDEN"].strip()
        datum = row.get("DATUM", "").strip()
        leto = datum[-4:] if len(datum) >= 4 else "0000"
        t_key = f"{t}_{leto}"

        op = row.get("OPOMBE", "").strip()
        disciplina = row.get("DISCIPLINA", "").strip()

        # Barvanje glede na disciplino
        if disciplina == "AH 12+12":
            bg_color = "lightgreen"
        elif disciplina == "3D krog":
            bg_color = "#f28b82"
        elif disciplina.startswith("70/50m krog"):
            bg_color = "yellow"
        elif disciplina.startswith("Dvorana") or disciplina.startswith("Dvoranski krog"):
            bg_color = "#998AFF"
        elif disciplina == "Šolsko":
            bg_color = "orange"
        elif disciplina == "900 krogov":
            bg_color = "silver"
        else:
            bg_color = "white"

        table_html += "<tr>"

        # Prvi stolpec: TEDEN (s rowspan)
        if t_key not in teden_done:
            table_html += f'<td rowspan="{teden_count[t_key]}" style="vertical-align:top;">{t}</td>'
            teden_done.add(t_key)

        # Srednji stolpci (DATUM ... TEKMOVANJE)
        for header in reader.fieldnames:
            if header not in ["TEDEN", "OPOMBE"]:
                cell_value = row.get(header, "")
                table_html += f'<td style="background-color:{bg_color}; vertical-align:top;">{cell_value}</td>'

        # Zadnji stolpec: OPOMBE (s rowspan)
        key = (t_key, op)
        if key not in opombe_done:
            rowspan = opombe_count[key]
            table_html += f'<td rowspan="{rowspan}" style="vertical-align:top;">{op}</td>'
            opombe_done.add(key)

        table_html += "</tr>"

    table_html += "</table>"

    full_html = f"""
    <html>
      <head><meta charset="utf-8"></head>
      <body>{header_html}{table_html}</body>
    </html>
    """

    options = {
        'page-size': 'A4',
        'orientation': 'Landscape',
        'encoding': "UTF-8",
        'margin-top': '15mm',
        'margin-bottom': '15mm',
        'margin-left': '10mm',
        'margin-right': '10mm',
    }

    wkhtml_path = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
    config = pdfkit.configuration(wkhtmltopdf=wkhtml_path) if os.path.exists(wkhtml_path) else None

    pdfkit.from_string(full_html, pdf_file, options=options, configuration=config)
    print(f"✅ PDF ustvarjen: {pdf_file}")


def save_to_csv(weekends, filepath):
    with open(filepath, "w", newline="", encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        # spremenjen header: OD in DO → DATUM
        writer.writerow(["TEDEN", "DATUM", "DISCIPLINA", "KRAJ", "ORGANIZATOR", "TEKMOVANJE", "OPOMBE"])

        for w in weekends:
            writer.writerow([
                w["teden"],
                w["datum"],      # DATUM
                w["disciplina"],
                w["kraj"],
                w["organizator"],
                w["tekmovanje"],
                w.get("opombe", "")
            ])
    print(f"CSV uspešno shranjen v: {filepath}")


def main():

    # Pot do datoteke
    pot_do_datoteke = INPUT_FILE_EVENTS

    # Branje JSON datoteke
    with open(pot_do_datoteke, "r", encoding="utf-8") as f:
        events = json.load(f)

    pot_do_datoteke2 = INPUT_FILE_COMPETITIONS
    with open(pot_do_datoteke2, "r", encoding="utf-8") as f:
        competitions = json.load(f)

    # weekends = generate_weekends(START_YEAR, START_WEEK, END_YEAR, END_WEEK)
    weekends = generate_weekends_by_day(START_YEAR, START_WEEK, END_YEAR, END_WEEK, events, competitions)
    save_to_csv(weekends, OUTPUT_FILE)

    csv_to_colored_pdf(OUTPUT_FILE, OUTPUT_FILE_PDF)


if __name__ == "__main__":
    main()
