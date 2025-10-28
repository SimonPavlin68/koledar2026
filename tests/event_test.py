import unittest
from datetime import date
from calendar_generator import check_event_in_day, generate_weekends_by_day


class TestCheckEventInDay(unittest.TestCase):
    def setUp(self):
        # Podatki za testiranje (enaki kot tvoj seznam events, z dodanim ključem "tip")
        self.events = [
            {
                "naziv": "Archery World Cup: Puebla 2026",
                "od": "07.04.2026",
                "do": "12.04.2026",
                "tip": "dogodek"
            },
            {
                "naziv": "Archery World Cup: Shanghai 2026",
                "od": "05.05.2026",
                "do": "10.05.2026",
                "tip": "dogodek"
            },
            {
                "naziv": "Archery World Cup: Antalya 2026",
                "od": "09.06.2026",
                "do": "14.06.2026",
                "tip": "dogodek"
            },
            {
                "naziv": "Archery World Cup: Madrid 2026",
                "od": "07.07.2026",
                "do": "12.07.2026",
                "tip": "dogodek"
            },
            {
                "naziv": "Arrowhead and 3D SP: Yankton 2026",
                "od": "24.09.2026",
                "do": "04.10.2026",
                "tip": "dogodek"
            },
            {
                "naziv": "Youth olympics: Dakar 2026",
                "od": "31.10.2026",
                "do": "13.11.2026",
                "tip": "dogodek"
            },
            {
                "naziv": "zimske počitnice",
                "od": "14.02.2027",
                "do": "01.03.2027",
                "tip": "počitnice"
            },
            {
                "naziv": "HDH Dolenjske toplice",
                "od": "06.06.2026",
                "do": "07.06.2026",
                "tip": "slovenski pokal"
            },
            {
                "naziv": "poletne počitnice",
                "od": "01.07.2026",
                "do": "31.08.2026",
                "tip": "počitnice"
            }
        ]

    def test_zimske_pocitnice(self):
        """Preveri, ali metoda vrne zimske počitnice za datum znotraj obsega."""
        day = date(2027, 2, 15)
        result = check_event_in_day(day, self.events)
        self.assertEqual(
            result,
            "Počitnice: zimske počitnice (14.02.2027 - 01.03.2027)",
            "Metoda ni vrnila zimskih počitnic za 15.02.2027."
        )

    def test_poletne_pocitnice(self):
        """Preveri, ali metoda vrne poletne počitnice za datum znotraj obsega."""
        day = date(2026, 7, 15)
        result = check_event_in_day(day, self.events)
        self.assertEqual(
            result,
            "Počitnice: poletne počitnice (01.07.2026 - 31.08.2026)",
            "Metoda ni vrnila poletnih počitnic za 15.07.2026."
        )

    def test_slovenski_pokal(self):
        """Preveri, ali metoda vrne tekmovanje za Slovenski pokal."""
        day = date(2026, 6, 6)
        result = check_event_in_day(day, self.events)
        self.assertEqual(
            result,
            "Rezervirano: HDH Dolenjske toplice (Slovenski pokal, 06.06.2026 - 07.06.2026)",
            "Metoda ni vrnila tekmovanja za Slovenski pokal za 06.06.2026."
        )

    def test_mednarodni_dogodek(self):
        """Preveri, ali metoda vrne mednarodni dogodek."""
        day = date(2026, 4, 8)
        result = check_event_in_day(day, self.events)
        self.assertEqual(
            result,
            "Archery World Cup: Puebla 2026 (07.04.2026 - 12.04.2026)",
            "Metoda ni vrnila mednarodnega dogodka za 08.04.2026."
        )

    def test_brez_dogodka(self):
        """Preveri, ali metoda vrne prazen niz, ko ni dogodka."""
        day = date(2026, 1, 1)
        result = check_event_in_day(day, self.events)
        self.assertEqual(
            result,
            "",
            "Metoda ni vrnila praznega niza za dan brez dogodka (01.01.2026)."
        )

    @unittest.skip("Test še ni dokončan")
    def test_neveljaven_datum(self):
        """Preveri, ali metoda preskoči dogodek z neveljavnim datumom."""
        events_with_invalid_date = self.events + [
            {
                "naziv": "Neveljaven dogodek",
                "od": "32.13.2026",  # Neveljaven datum
                "do": "33.13.2026",
                "tip": "dogodek"
            }
        ]
        day = date(2027, 2, 15)
        result = check_event_in_day(day, events_with_invalid_date)
        self.assertEqual(
            result,
            "Počitnice: zimske počitnice (14.02.2026 - 01.03.2026)",
            "Metoda ni pravilno preskočila dogodka z neveljavnim datumom."
        )

    @unittest.skip("Test še ni dokončan")
    def test_manjkajoci_datum(self):
        """Preveri, ali metoda preskoči dogodek z manjkajočim datumom."""
        events_with_missing_date = self.events + [
            {
                "naziv": "Dogodek brez datuma",
                "od": "",
                "do": "",
                "tip": "dogodek"
            }
        ]
        day = date(2026, 2, 15)
        result = check_event_in_day(day, events_with_missing_date)
        self.assertEqual(
            result,
            "Počitnice: zimske počitnice (14.02.2026 - 01.03.2026)",
            "Metoda ni pravilno preskočila dogodka z manjkajočim datumom."
        )

    @unittest.skip("Test še ni dokončan")
    def test_kraten_dogodek(self):
        """Preveri, ali metoda pravilno obravnava enodnevni dogodek."""
        events_with_single_day = self.events + [
            {
                "naziv": "Enodnevni dogodek",
                "od": "20.08.2026",
                "do": "20.08.2026",
                "tip": "dogodek"
            }
        ]
        day = date(2026, 8, 20)
        result = check_event_in_day(day, events_with_single_day)
        self.assertEqual(
            result,
            "Enodnevni dogodek (20.08.2026 - 20.08.2026)",
            "Metoda ni pravilno vrnila enodnevnega dogodka za 20.08.2026."
        )

        def test_first_weekend_2027(self):
            """Preveri, ali metoda vrne prvi vikend v letu 2027 kot teden 1."""
            start_year, start_week = 2026, 50
            end_year, end_week = 2027, 2
            weekends = generate_weekends_by_day(start_year, start_week, end_year, end_week, self.events,
                                                self.competitions)

            # Preveri, ali je prvi vikend 2027 (2.–3. januar) vključen
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

            # Preveri, ali je prvi vikend 2027 v rezultatu
            self.assertIn(expected_saturday, weekends, "Prva sobota v 2027 (02.01.2027) ni v rezultatu.")
            self.assertIn(expected_sunday, weekends, "Prva nedelja v 2027 (03.01.2027) ni v rezultatu.")


if __name__ == '__main__':
    unittest.main()