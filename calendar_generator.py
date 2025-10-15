from datetime import datetime, timedelta, date


def get_saturday_of_week(year, week):
    # 6 pomeni sobota v ISO (1 = ponedeljek, 7 = nedelja)
    return datetime.fromisocalendar(year, week, 6)


def parse_date(date_str):
    return datetime.strptime(date_str, "%d.%m.%Y")


def check_event_in_day(day: date, events: list[dict]) -> str:
    for event in events:
        event_start_str = event.get("od")  # Datum začetka v string obliki (npr. "07.04.2026")
        event_end_str = event.get("do")   # Datum konca v string obliki (npr. "12.04.2026")

        # Preskoči, če manjka datum
        if not event_start_str or not event_end_str:
            continue

        # Pretvori string v datetime.date
        try:
            event_start = datetime.strptime(event_start_str, "%d.%m.%Y").date()
            event_end = datetime.strptime(event_end_str, "%d.%m.%Y").date()
        except ValueError:
            continue  # Če je datum neveljaven, preskoči

        # Poskrbi, da so vsi datumi v formatu datetime.date
        if isinstance(day, datetime):
            day = day.date()  # Pretvori day v datetime.date, če je datetime

        # Zdaj varno primerjamo (ker so vsi datumi v obliki datetime.date)
        if event_start <= day <= event_end:
            # print("bingo 2")  # To naj bi zdaj delovalo, če najdeš dogodek v tem dnevu
            # return event.get("naziv", "")  # Lahko vrneš "naziv" ali "opombe", odvisno od tega, kaj želiš
            event_name = event.get("naziv", "")
            return f"{event_name} ({event_start_str} - {event_end_str})"
    return ""  # Če ni nobenega dogodka v tem dnevu


def check_event_in_day_old(day: date, events: list[dict]) -> str:
    for event in events:
        event_start = event.get("start")
        event_end = event.get("end")

        # preskoči, če manjka datum
        if not event_start or not event_end:
            continue

        # pretvori v date, če je datetime
        if isinstance(event_start, datetime):
            event_start = event_start.date()
        if isinstance(event_end, datetime):
            event_end = event_end.date()

        # zdaj varno primerjamo
        if event_start <= day <= event_end:
            # return event.get("note", "")
            event_name = event.get("naziv", "")
            return f"{event_name} ({event_start} - {event_end})"
    return ""


from datetime import datetime, timedelta, date

def generate_weekends_by_day(start_year, start_week, end_year, end_week, events, competitions):
    weekends = []
    year, week = start_year, start_week

    while (year < end_year) or (year == end_year and week <= end_week):
        try:
            # Pridobi soboto za trenutni teden
            saturday = get_saturday_of_week(year, week)
            sunday = saturday + timedelta(days=1)

            # Pridobi opombe za soboto in nedeljo posebej
            note_sobota = check_event_in_day(saturday, events)
            note_nedelja = check_event_in_day(sunday, events)

            # Poišči predlog iz competitions
            matching_comp = None
            for comp in competitions:
                try:
                    comp_date = datetime.strptime(comp.get("od", ""), "%d.%m.%Y").date()
                    if comp_date == saturday.date():
                        matching_comp = comp
                        break
                except ValueError:
                    continue

            # Zgradi zapis vikenda za soboto in nedeljo
            event_sobota = {
                "teden": f"{week}",
                "datum": saturday.strftime("%d.%m.%Y"),
                "disciplina": matching_comp.get("disciplina", "") if matching_comp else "",
                "kraj": matching_comp.get("kraj", "") if matching_comp else "",
                "organizator": matching_comp.get("organizator", "") if matching_comp else "",
                "tekmovanje": matching_comp.get("tekmovanje", "") if matching_comp else "",
                "opombe": note_sobota or ""
            }
            event_nedelja = {
                "teden": f"{week}",
                "datum": sunday.strftime("%d.%m.%Y"),
                "disciplina": matching_comp.get("disciplina", "") if matching_comp else "",
                "kraj": matching_comp.get("kraj", "") if matching_comp else "",
                "organizator": matching_comp.get("organizator", "") if matching_comp else "",
                "tekmovanje": matching_comp.get("tekmovanje", "") if matching_comp else "",
                "opombe": note_nedelja or ""
            }

            weekends.append(event_sobota)
            weekends.append(event_nedelja)

            # Povečaj teden in upoštevaj prehod v novo leto
            week += 1
            if week > 52:
                week = 1
                year += 1

                # Zajamči, da bomo pravilno začeli z 1. tednom v naslednjem letu
                if year == 2027:
                    week = 1

        except Exception as e:
            print(f"❌ Napaka pri tednu {week} leta {year}: {e}")
            break

    return weekends


