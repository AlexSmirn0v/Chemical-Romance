import csv
import sqlite3
from pymorphy2 import MorphAnalyzer
import sympy as sym
from math import lcm


class DoesNotExistError(Exception):
    pass


METAL_ACTIVENESS = ['Li', 'Cs', 'Rb', 'K', 'Ba', 'Sr', 'Ca', 'Na', 'Mg', 'Al', 'Ti', 'Mn', 'Zn', 'Cr',
                    'Fe', 'Cd', 'Co', 'Ni', 'Sn', 'Pb', 'H', 'Sb', 'Bi', 'Cu', 'Hg', 'Ag', 'Pd', 'Pt', 'Au']
CATIONS = ['H', 'Li', 'K', 'Na', 'NH4', 'Mg', 'Ca', 'Ba', 'Sr', 'Al', 'Cr', 'Fe', 'Fe', 'Zn', 'Ag', 'Pb',
           'Cu', 'Hg', 'Hg', 'Mn', 'Sn', 'Ni', 'Со', 'Be']
ANIONS = ['F', 'Cl', 'Br', 'I', 'S', 'SO3', 'SO4', 'PO4', 'CO3', 'SiO3', 'NO3', 'CH3COO', 'CrO4', 'ClO4', 'NO2']

NAME = {'NO3': ['Нитрат', 'Азотная', 'HNO3'], 'NO2': ['Нитрит', 'Азотистая', 'HNO2'],
        'SO4': ['Сульфат', 'Серная', 'H2SO4'], 'S2O7': ['Дисульфат', 'Дисерная', 'H2S2O7'],
        'SO3': ['Сульфит', 'Сернистая', 'H2SO3'], 'S2O3': ['Тиосульфат', 'Тиосерная', 'H2S2O3'],
        'S2': ['Сульфид', 'Сероводородная', 'H2S'], 'CO3': ['Карбонат', 'Угольная', 'H2CO3'],
        'PO4': ['Ортофосфат', 'Ортофосфорная', 'H3PO4'], 'PO3': ['Ортофосфит', 'Ортофосфористая', 'HPO3', 'H3PO3'],
        'P2O7': ['Дифосфат', 'Пирофосфорная,дифосфорная', 'H4P2O7'], 'PO2': ['Метафосфит', 'Метафосфористая', 'HPO2'],
        'BO3': ['Ортоборат', 'Ортоборная', 'H3BO3'], 'BO2': ['Метаборат', 'Метаборная', 'HBO2'],
        'SiO4': ['Ортосиликат', 'Ортокремниевая', 'H4SiO4'], 'SiO3': ['Метасиликат', 'Метакремниевая', 'H2SiO3'],
        'AsO4': ['Арсенат', 'Мышьяковая', 'H3AsO4'], 'AsO3': ['Арсенит', 'Мышьяковистая', 'H3AsO3'],
        'SeO4': ['Селенат', 'Селеновая', 'H2SeO4'], 'SeO3': ['Селенит', 'Селенистая', 'H2SeO3'],
        'CrO4': ['Хромат', 'Хромовая', 'H2CrO4'], 'Cr2O7': ['Дихромат', 'Дихромовая', 'H2Cr2O7'],
        'MnO4': ['Манганат', 'Марганцовистая', 'HMnO4', 'H2MnO4'], 'ClO4': ['Перхлорат', 'Хлорная', 'HClO4'],
        'ClO3': ['Хлорат', 'Хлорноватая', 'HClO3'], 'ClO2': ['Хлорит', 'Хлористая', 'HClO2'],
        'Cl': ['Хлорид', 'Соляная', 'HCl'], 'ClO': ['Гипохлорит', 'Хлорноватистая', 'HClO'],
        'IO6': ['Ортойодат', 'Ортойодная', 'H5IO6'],
        'IO4': ['Метайодат', 'Метайодная', 'HJO4'], 'IO': ['Гипойодит', 'Йодноватистая', 'HIO'],
        'CN': ['Цианид', 'Синильная', 'HCN'], 'F': ['Фторид', 'Плавиковая', 'HF']
        }


def under(stroke):
    return f'<sub>{str(stroke)}</sub>'


def up(stroke):
    return f'<sup>{str(stroke)}</sup>'


def gentle(stroke):
    word = MorphAnalyzer().parse(stroke)[0]
    return word.inflect({'gent'}).word.lower()


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


def charge(ion):
    with open('Solubility_table.csv', encoding='utf-8-sig') as table:
        reader = csv.DictReader(table, delimiter=';', quotechar='"')
        if ion == 'O':
            return -2
        elif ion == 'F':
            return -1
        elif ion == 'Fe':
            return 2, 3
        elif ion == 'Hg':
            return 1, 2
        elif ion in CATIONS:
            for row in reader:
                if row['Ион'] == 'Заряд +':
                    return int(row[ion])
        elif ion in ANIONS or ion == 'OH':
            for row in reader:
                if row['Ион'] == ion:
                    return int(row['Заряд -'])


def substance_maker(begin_part_list, end_part_list, begin_part_number, end_part_number):
    elems_list_1 = list()
    begin_part = ''.join(map(str, begin_part_list))
    end_part = ''.join(map(str, end_part_list))
    sum_charge = lcm(abs(charge(begin_part)), abs(charge(end_part)))
    begin_number = sum_charge // abs(charge(begin_part))
    end_number = sum_charge // abs(charge(end_part))

    if begin_part_number / begin_number == end_part_number / end_number:
        if int(begin_part_number / begin_number) != 1:
            elems_list_1.append(int(begin_part_number / begin_number))
    else:
        print(begin_part_number, end_part_number)
        print(begin_part_number / begin_number)
        print(end_part_number / end_number)
        raise DoesNotExistError

    elems_list_1.extend(begin_part_list)
    if begin_number != 1 and len(begin_part_list) > 1:
        elems_list_1.insert(0, '(')
        elems_list_1.append(')')
        elems_list_1.append(begin_number)
    elif begin_number != 1:
        elems_list_1.append(begin_number)

    if end_number != 1 and len(end_part_list) > 1:
        elems_list_1.append('(')
        elems_list_1.extend(end_part_list)
        elems_list_1.append(')')
        elems_list_1.append(end_number)
    elif end_number != 1:
        elems_list_1.extend(end_part_list)
        elems_list_1.append(end_number)
    else:
        elems_list_1.extend(end_part_list)
    return elems_list_1


if __name__ == '__main__':
    print(substance_maker(['Na'], ['S', 'O', 4], 2, 1))