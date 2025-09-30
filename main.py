import csv
import json
import os
from calendar_generator import generate_weekends_with_notes
from config import START_YEAR, START_WEEK, END_YEAR, END_WEEK, OUTPUT_FILE, OUTPUT_FILE_PDF
import pdfkit


def csv_to_colored_pdf(csv_file, pdf_file):
    # Preberi CSV
    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        rows = list(reader)

    # Pripravi HTML tabelo
    table_html = '<table border="1" cellspacing="0" cellpadding="5" style="border-collapse: collapse; width: 100%;">'

    # Glava tabele
    table_html += '<tr>'
    for header in reader.fieldnames:
        table_html += f'<th>{header}</th>'
    table_html += '</tr>'

    # Vrstice z barvanjem
    for row in rows:
        disciplina = row.get("DISCIPLINA", "").strip()
        if disciplina == "AH 12+12":
            bg_color = "lightgreen"
        elif disciplina == "3D krog":
            bg_color = "orange"
        elif disciplina == "70/50m krog + OK":
            bg_color = "yellow"
        else:
            bg_color = "white"
        table_html += f'<tr style="background-color:{bg_color}">'
        for header in reader.fieldnames:
            table_html += f'<td>{row.get(header, "")}</td>'
        table_html += '</tr>'

    table_html += '</table>'

    # Renderiraj PDF
    options = {
        'page-size': 'A4',
        'orientation': 'Landscape',
        'encoding': "UTF-8",
        'margin-top': '15mm',
        'margin-bottom': '15mm',
        'margin-left': '10mm',
        'margin-right': '10mm',
    }

    # Pot do wkhtmltopdf, če je Windows
    wkhtml_path = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=wkhtml_path) if os.path.exists(wkhtml_path) else None

    pdfkit.from_string(table_html, pdf_file, options=options, configuration=config)
    print(f"PDF ustvarjen: {pdf_file}")


def save_to_csv(weekends, filepath):
    with open(filepath, "w", newline="", encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(["TEDEN", "OD", "DO", "DISCIPLINA", "KRAJ", "ORGANIZATOR", "TEKMOVANJE", "OPOMBE"])
        for w in weekends:
            writer.writerow([w["teden"],
                             w["od"],
                             w["do"],
                             w["disciplina"],
                             w["kraj"],
                             w["organizator"],
                             w["tekmovanje"],
                             w.get("opombe", "")])
    print(f"CSV uspešno shranjen v: {filepath}")


def main():
    # events = [
    #    {"naziv": "Archery World Cup: Puebla 2026", "od": "07.04.2026", "do": "12.04.2026"},
    #    {"naziv": "Archery World Cup: Shanghai 2026", "od": "05.05.2026", "do": "10.05.2026"},
    #    {"naziv": "Archery World Cup: Antalya 2026", "od": "09.06.2026", "do": "14.06.2026"},
    #    {"naziv": "Archery World Cup: Madrid 2026", "od": "07.07.2026", "do": "12.07.2026"},
    #    {"naziv": "Arrowhead in 3D SP: Yankton 2026", "od": "24.09.2026", "do": "04.10.2026"},
    #    {"naziv": "Youth olympics: Dakar 2026", "od": "31.10.2026", "do": "13.11.2026"}
    # ]

    # Pot do datoteke
    pot_do_datoteke = "input/events.json"

    # Branje JSON datoteke
    with open(pot_do_datoteke, "r", encoding="utf-8") as f:
        events = json.load(f)

    pot_do_datoteke2 = "input/competitions.json"
    with open(pot_do_datoteke2, "r", encoding="utf-8") as f:
        competitions = json.load(f)

    # weekends = generate_weekends(START_YEAR, START_WEEK, END_YEAR, END_WEEK)
    weekends = generate_weekends_with_notes(START_YEAR, START_WEEK, END_YEAR, END_WEEK, events, competitions)
    save_to_csv(weekends, OUTPUT_FILE)

    csv_to_colored_pdf(OUTPUT_FILE, OUTPUT_FILE_PDF)


if __name__ == "__main__":
    main()
