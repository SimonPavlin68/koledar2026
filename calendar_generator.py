from datetime import datetime, timedelta


def get_saturday_of_week(year, week):
    # 6 pomeni sobota v ISO (1 = ponedeljek, 7 = nedelja)
    return datetime.fromisocalendar(year, week, 6)


def parse_date(date_str):
    return datetime.strptime(date_str, "%d.%m.%Y")


def check_event_in_weekend(saturday, sunday, events):
    notes = []
    for event in events:
        event_start = parse_date(event["od"])
        event_end = parse_date(event["do"])
        # Če se dogodek začne ali konča v vikendu ali ga vikend prekriva
        if event_start <= sunday and event_end >= saturday:
            # notes.append(event["naziv"])
            notes.append(f"{event['naziv']} ({event['od']} - {event['do']})")
    return "; ".join(notes) if notes else ""


def generate_weekends_with_notes_old(start_year, start_week, end_year, end_week, events):
    weekends = []
    year, week = start_year, start_week

    while (year < end_year) or (year == end_year and week <= end_week):
        try:
            saturday = get_saturday_of_week(year, week)
            sunday = saturday + timedelta(days=1)
            note = check_event_in_weekend(saturday, sunday, events)
            weekends.append({
                "teden": f"{week}",
                "od": saturday.strftime("%d.%m.%Y"),
                "do": sunday.strftime("%d.%m.%Y"),
                "disciplina": "",
                "kraj": "",
                "organizator": "",
                "tekmovanje": "",
                "opombe": note
            })
            week += 1
            if week > 52:
                try:
                    datetime.fromisocalendar(year, week, 1)
                except ValueError:
                    week = 1
                    year += 1
        except Exception as e:
            print(f"Napaka pri tednu {week} leta {year}: {e}")
            break

    return weekends


def generate_weekends_with_notes(start_year, start_week, end_year, end_week, events, competitions):
    weekends = []
    year, week = start_year, start_week

    while (year < end_year) or (year == end_year and week <= end_week):
        try:
            saturday = get_saturday_of_week(year, week)
            sunday = saturday + timedelta(days=1)

            od_datum = saturday.strftime("%d.%m.%Y")
            do_datum = sunday.strftime("%d.%m.%Y")

            note = check_event_in_weekend(saturday, sunday, events)

            # 🔍 Poišči predlog iz competitions (če obstaja)
            matching_comp = None
            for comp in competitions:
                try:
                    comp_date = datetime.strptime(comp.get("od", ""), "%d.%m.%Y").date()
                    if comp_date == saturday.date():
                        matching_comp = comp
                        break
                except ValueError:
                    continue  # Neveljaven datum, preskoči

            # Zgradi zapis vikenda (tudi če ni predloga)
            event = {
                "teden": f"{week}",
                "od": od_datum,
                "do": do_datum,
                "disciplina": matching_comp.get("disciplina", "") if matching_comp else "",
                "kraj": matching_comp.get("kraj", "") if matching_comp else "",
                "organizator": matching_comp.get("organizator", "") if matching_comp else "",
                "tekmovanje": matching_comp.get("tekmovanje", "") if matching_comp else "",
                "opombe": note or ""
            }

            weekends.append(event)

            # Povečaj teden
            week += 1
            if week > 52:
                week = 1
                year += 1

        except Exception as e:
            print(f"❌ Napaka pri tednu {week} leta {year}: {e}")
            break

    return weekends


