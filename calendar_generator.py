from datetime import datetime, timedelta


def get_saturday_of_week(year, week):
    return datetime.strptime(f'{year}-W{week}-6', "%Y-W%W-%w")


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


def generate_weekends_with_notes(start_year, start_week, end_year, end_week, events):
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


def generate_weekends1(start_year, start_week, end_year, end_week):
    weekends = []
    year, week = start_year, start_week

    while (year < end_year) or (year == end_year and week <= end_week):
        try:
            saturday = get_saturday_of_week(year, week)
            sunday = saturday + timedelta(days=1)
            weekends.append({
                "teden": f"{week}",
                "od": saturday.strftime("%d.%m.%Y"),
                "do": sunday.strftime("%d.%m.%Y"),
                "disciplina": "",
                "kraj": "",
                "organizator": "",
                "tekmovanje": ""
            })
            week += 1
            if week > 52:
                week = 1
                year += 1
        except Exception as e:
            print(f"Napaka pri tednu {week} leta {year}: {e}")
            break

    return weekends
