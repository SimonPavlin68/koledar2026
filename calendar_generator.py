from datetime import datetime, timedelta, date


def get_saturday_of_week_nok(year, week):
    # 6 pomeni sobota v ISO (1 = ponedeljek, 7 = nedelja)
    return datetime.fromisocalendar(year, week, 6)


def get_saturday_of_week(year, week):
    """Vrne soboto za dani teden v letu, kjer teden 1 začne z 1. januarjem."""
    # Prvi dan leta
    first_day = date(year, 1, 1)
    # Poišči prvo soboto v letu
    days_to_saturday = (5 - first_day.weekday()) % 7  # Sobota je weekday 5
    first_saturday = first_day + timedelta(days=days_to_saturday)
    # Dodaj (week - 1) tednov
    target_saturday = first_saturday + timedelta(weeks=week-1)
    return target_saturday


def parse_date(date_str):
    return datetime.strptime(date_str, "%d.%m.%Y")


def check_event_in_day(day: date, events: list[dict]) -> str:
    if isinstance(day, datetime):
        day = day.date()

    found_events = []

    for event in events:
        event_start_str = event.get("od")
        event_end_str = event.get("do")

        if not event_start_str or not event_end_str:
            continue

        try:
            event_start = datetime.strptime(event_start_str, "%d.%m.%Y").date()
            event_end = datetime.strptime(event_end_str, "%d.%m.%Y").date()
        except ValueError:
            continue

        if event_start <= day <= event_end:
            event_name = event.get("naziv", "Neimenovan dogodek")
            description = f"{event_name} ({event_start_str} - {event_end_str})"
            found_events.append(description)

    return "<br>".join(found_events) if found_events else ""
    # return "\n".join(found_events) if found_events else ""


def check_event_in_day_old(day: date, events: list[dict]) -> str:
    if isinstance(day, datetime):
        day = day.date()

    for event in events:
        event_start_str = event.get("od")
        event_end_str = event.get("do")

        if not event_start_str or not event_end_str:
            continue

        try:
            event_start = datetime.strptime(event_start_str, "%d.%m.%Y").date()
            event_end = datetime.strptime(event_end_str, "%d.%m.%Y").date()
        except ValueError:
            continue

        if event_start <= day <= event_end:
            event_name = event.get("naziv", "")
            event_type = event.get("tip", "dogodek")
            if event_type == "slovenski pokal":
                return f"Rezervirano: {event_name} (Slovenski pokal, {event_start_str} - {event_end_str})"
            elif event_type == "počitnice":
                return f"Počitnice: {event_name} ({event_start_str} - {event_end_str})"
            else:
                return f"{event_name} ({event_start_str} - {event_end_str})"

    return ""


from datetime import datetime, timedelta

def generate_weekends_by_day(start_year, start_week, end_year, end_week, events, competitions):
    weekends = []

    # Izračunaj začetno in končno soboto
    start_date = get_saturday_of_week(start_year, start_week)
    end_date = get_saturday_of_week(end_year, end_week)

    current_saturday = start_date
    while current_saturday <= end_date:
        try:
            saturday = current_saturday
            sunday = saturday + timedelta(days=1)

            # --- Opombe ---
            note_sobota = check_event_in_day(saturday, events)
            note_nedelja = check_event_in_day(sunday, events)

            # --- Poišči tekmovanja ---
            matching_comp_sobota = next(
                (comp for comp in competitions if safe_date_match(comp.get("od", ""), saturday)), None
            )
            matching_comp_nedelja = next(
                (comp for comp in competitions if safe_date_match(comp.get("od", ""), sunday)), None
            )

            # --- Dodaj soboto ---
            weekends.append({
                "teden": f"{saturday.isocalendar().week}",
                "datum": saturday.strftime("%d.%m.%Y"),
                "disciplina": matching_comp_sobota.get("disciplina", "") if matching_comp_sobota else "",
                "kraj": matching_comp_sobota.get("kraj", "") if matching_comp_sobota else "",
                "organizator": matching_comp_sobota.get("organizator", "") if matching_comp_sobota else "",
                "tekmovanje": matching_comp_sobota.get("tekmovanje", "") if matching_comp_sobota else "",
                "opombe": note_sobota or ""
            })

            # --- Dodaj nedeljo ---
            weekends.append({
                "teden": f"{saturday.isocalendar().week}",
                "datum": sunday.strftime("%d.%m.%Y"),
                "disciplina": matching_comp_nedelja.get("disciplina", "") if matching_comp_nedelja else "",
                "kraj": matching_comp_nedelja.get("kraj", "") if matching_comp_nedelja else "",
                "organizator": matching_comp_nedelja.get("organizator", "") if matching_comp_nedelja else "",
                "tekmovanje": matching_comp_nedelja.get("tekmovanje", "") if matching_comp_nedelja else "",
                "opombe": note_nedelja or ""
            })

            # Naslednji teden
            current_saturday += timedelta(days=7)

        except Exception as e:
            print(f"❌ Napaka pri datumu {current_saturday}: {e}")
            break

    return weekends


def safe_date_match(date_str, target_date):
    """Varnostno primerjanje datumov v obliki 'dd.mm.yyyy'."""
    try:
        return datetime.strptime(date_str, "%d.%m.%Y").date() == target_date
    except Exception:
        return False



