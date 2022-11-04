import csv
import sqlite3

METAL_ACTIVENESS = ['Li', 'Cs', 'Rb', 'K', 'Ba', 'Sr', 'Ca', 'Na', 'Mg', 'Al', 'Ti', 'Mn', 'Zn', 'Cr',
                    'Fe', 'Cd', 'Co', 'Ni', 'Sn', 'Pb', 'H', 'Sb', 'Bi', 'Cu', 'Hg', 'Ag', 'Pd', 'Pt', 'Au']
CATIONS = ['H', 'Li', 'K', 'Na', 'NH4', 'Mg', 'Ca', 'Ba', 'Sr', 'Al', 'Cr', 'Fe', 'Fe', 'Zn', 'Ag', 'Pb',
           'Cu', 'Hg', 'Hg', 'Mn', 'Sn', 'Ni', 'Со', 'Be']
ANIONS = ['F', 'Cl', 'Br', 'I', 'S', 'SO3', 'SO4', 'PO4', 'CO3', 'SiO3', 'NO3', 'CH3COO', 'CrO4', 'ClO4', 'NO2']


def under(stroke):
    return f'<sub>{str(stroke)}</sub>'


def up(stroke):
    return f'<sup>{str(stroke)}</sup>'


def elem_parameters(name):
    connection = sqlite3.connect('Theory.db')
    a = connection.cursor().execute("""SELECT * FROM elements WHERE symbol = ?""", (name,)).fetchone()
    connection.commit()
    return {
        'number': a[0],
        'symbol': a[1],
        'name': a[2],
        'weight': a[3],
        'electronegativity': a[4],
        'isMetal': a[5],
        'group': a[6],
        'period': a[7],
        'rusName': a[8]
    }


def isSoluble(sub):
    with open('Solubility_table.csv', encoding='utf-8-sig') as table:
        reader = csv.DictReader(table, delimiter=';', quotechar='"')
        for row in reader:
            if row['Ион'] == sub.get_spart():
                if row[sub.get_fpart()].strip() == 'True':
                    return True
                elif row[sub.get_fpart()].strip() == 'False':
                    return False
                elif row[sub.get_fpart()].strip() == 'None':
                    return None