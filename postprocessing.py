import csv
from collections import defaultdict
from datetime import datetime
import re
import os

def nalozi_prijave(csv_datoteka):
    prijave = []
    with open(csv_datoteka, 'r', encoding='cp1250') as f:
        reader = csv.reader(f, delimiter=';')
        header = next(reader)
        # odstranimo stolpca časovni žig in e-pošta
        header = header[2:]
        for row in reader:
            prijave.append(row[2:])  # odstranimo časovni žig in e-pošto
    return header, prijave

def najdi_datum(vnos):
    if not vnos:
        return None
    m = re.search(r'(\d{1,2}\.\d{1,2}\.\d{4})', vnos)
    if m:
        d = m.group(1)
        try:
            dan, mesec, leto = map(int, d.split('.'))
            return datetime(leto, mesec, dan)
        except:
            return None
    return None

def razdeli_po_vrsti_in_sort(prijave):
    tipi_index = 2  # stolpec "Vrsta tekmovanja" po odstranitvi prvih dveh
    tipi = defaultdict(list)

    for row in prijave:
        vrsta = row[tipi_index].strip() if row[tipi_index].strip() else "Nepoznana"

        # Poiščemo prvi datum v vrstici
        datum = None
        for cell in row:
            datum = najdi_datum(cell)
            if datum:
                break

        row_with_date = (datum, row)
        tipi[vrsta].append(row_with_date)

    # sortiramo po datumu
    for vrsta in tipi:
        tipi[vrsta].sort(key=lambda x: x[0] or datetime.max)

    return tipi

def shrani_csv_sort(tipi, header, izhodna_datoteka):
    os.makedirs(os.path.dirname(izhodna_datoteka), exist_ok=True)

    with open(izhodna_datoteka, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f, delimiter=';')

        for vrsta, vrstice in tipi.items():
            # preverimo, kateri stolpci niso prazni
            stolpci_aktivni = [i for i in range(len(header))
                               if any(row[i].strip() for _, row in vrstice)]

            # header in vrstice samo s aktivnimi stolpci
            header_aktivni = [header[i] for i in stolpci_aktivni]

            writer.writerow([vrsta])          # ime vrste tekmovanja
            writer.writerow(header_aktivni)   # prilagojen header

            for _, row in vrstice:
                writer.writerow([row[i] for i in stolpci_aktivni])

            writer.writerow([])  # prazna vrstica med tipi

    print(f"✅ CSV uspešno shranjen: {izhodna_datoteka}")

def main():
    header, prijave = nalozi_prijave('input/odzivi.csv')
    tipi = razdeli_po_vrsti_in_sort(prijave)
    shrani_csv_sort(tipi, header, 'output/prijave_sortirane-new.csv')

if __name__ == "__main__":
    main()
