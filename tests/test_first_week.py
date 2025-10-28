import unittest
from datetime import date, timedelta, datetime
from calendar_generator import generate_weekends_by_day


# Predpostavljam, da imamo metode check_event_in_day in get_saturday_of_week
def check_event_in_day(day: date, events: list[dict]) -> str:
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


class TestCheckEventInDay(unittest.TestCase):
    def setUp(self):
        self.events = [
            {
                "naziv": "zimske počitnice",
                "od": "14.02.2026",
                "do": "01.03.2026",
                "tip": "počitnice"
            },
            {
                "naziv": "HDH Dolenjske toplice",
                "od": "06.06.2026",
                "do": "07.06.2026",
                "tip": "slovenski pokal"
            }
        ]
        self.competitions = [
            {
                "od": "06.06.2026",
                "disciplina": "Lokostrelstvo",
                "kraj": "Dolenjske Toplice",
                "organizator": "LK Dolenjske Toplice",
                "tekmovanje": "Slovenski pokal"
            }
        ]

    def test_first_weekend_2027(self):
        """Preveri, ali metoda vrne prvi vikend v letu 2027 kot teden 1."""
        start_year, start_week = 2026, 50
        end_year, end_week = 2027, 2
        weekdays = generate_weekends_by_day(start_year, start_week, end_year, end_week, self.events, self.competitions)

        expected_saturday = {
            "teden": "1",
            "datum": "02.01.2027",
            "disciplina": "",
            "kraj": "",
            "organizator": "",
            "tekmovanje": "",
            "opombe": ""
        }
        expected_sunday = {
            "teden": "1",
            "datum": "03.01.2027",
            "disciplina": "",
            "kraj": "",
            "organizator": "",
            "tekmovanje": "",
            "opombe": ""
        }

        self.assertIn(expected_saturday, weekdays, "Prva sobota v 2027 (02.01.2027) ni v rezultatu.")
        self.assertIn(expected_sunday, weekdays, "Prva nedelja v 2027 (03.01.2027) ni v rezultatu.")


if __name__ == '__main__':
    unittest.main()