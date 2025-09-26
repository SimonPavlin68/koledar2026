import csv
from calendar_generator import generate_weekends_with_notes
from config import START_YEAR, START_WEEK, END_YEAR, END_WEEK, OUTPUT_FILE


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
    events = [
        {"naziv": "Archery World Cup: Madrid 2026", "od": "07.07.2026", "do": "12.07.2026"},
        {"naziv": "Running Championship 2026", "od": "15.08.2026", "do": "16.08.2026"}
    ]

    # weekends = generate_weekends(START_YEAR, START_WEEK, END_YEAR, END_WEEK)
    weekends = generate_weekends_with_notes(START_YEAR, START_WEEK, END_YEAR, END_WEEK, events)
    save_to_csv(weekends, OUTPUT_FILE)


if __name__ == "__main__":
    main()
