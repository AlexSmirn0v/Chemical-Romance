import csv
import sqlite3
from pymorphy2 import MorphAnalyzer

METAL_ACTIVENESS = ['Li', 'Cs', 'Rb', 'K', 'Ba', 'Sr', 'Ca', 'Na', 'Mg', 'Al', 'Ti', 'Mn', 'Zn', 'Cr',
                    'Fe', 'Cd', 'Co', 'Ni', 'Sn', 'Pb', 'H', 'Sb', 'Bi', 'Cu', 'Hg', 'Ag', 'Pd', 'Pt', 'Au']
CATIONS = ['H', 'Li', 'K', 'Na', 'NH4', 'Mg', 'Ca', 'Ba', 'Sr', 'Al', 'Cr', 'Fe', 'Fe', 'Zn', 'Ag', 'Pb',
           'Cu', 'Hg', 'Hg', 'Mn', 'Sn', 'Ni', 'Со', 'Be']
ANIONS = ['F', 'Cl', 'Br', 'I', 'S', 'SO3', 'SO4', 'PO4', 'CO3', 'SiO3', 'NO3', 'CH3COO', 'CrO4', 'ClO4', 'NO2']

NAME = {'NO3': ['Нитрат', 'Азотная'], 'NO2': ['Нитрит', 'Азотистая'], 'SO4': ['Сульфат', 'Серная'],
        'S2O7': ['Дисульфат', 'Дисерная'], 'SO3': ['Сульфит', 'Сернистая'], 'S2O3': ['Тиосульфат', 'Тиосерная'],
        'S2': ['Сульфид', 'Сероводородная'], 'CO3': ['Карбонат', 'Угольная'], 'PO4': ['Ортофосфат', 'Ортофосфорная'],
        'PO3': ['Ортофосфит', 'Ортофосфористая'], 'P2O7': ['Дифосфат', 'Пирофосфорная,дифосфорная'],
        'PO2': ['Метафосфит', 'Метафосфористая'], 'BO3': ['Ортоборат', 'Ортоборная'],
        'BO2': ['Метаборат', 'Метаборная'], 'SiO4': ['Ортосиликат', 'Ортокремниевая'],
        'SiO3': ['Метасиликат', 'Метакремниевая'], 'AsO4': ['Арсенат', 'Мышьяковая'],
        'AsO3': ['Арсенит', 'Мышьяковистая'], 'SeO4': ['Селенат', 'Селеновая'],
        'SeO3': ['Селенит', 'Селенистая'], 'CrO4': ['Хромат', 'Хромовая'],
        'Cr2O7': ['Дихромат', 'Дихромовая'], 'MnO4': ['Манганат', 'Марганцовистая'],
        'ClO4': ['Перхлорат', 'Хлорная'], 'ClO3': ['Хлорат', 'Хлорноватая'],
        'ClO2': ['Хлорит', 'Хлористая'], 'ClO': ['Гипохлорит', 'Хлорноватистая'],
        'IO6': ['Ортойодат', 'Ортойодная'], 'IO4': ['Метайодат', 'Метайодная'],
        'IO': ['Гипойодит', 'Йодноватистая'], 'CN': ['Цианид', 'Синильная'], 'F': ['Фторид', 'Плавиковая']
        }

stroke = '''HNO3 Азотная NO3 Нитрат
HNO2 Азотистая NO2 Нитрит
H2SO4 Серная SO4 Сульфат
H2S2O7 Дисерная S2O7 Дисульфат
H2SO3 Сернистая SO3 Сульфит
H2S2O3 Тиосерная S2O3 Тиосульфат
H2S Сероводородная S2 Сульфид
H2CO3 Угольная CO3 Карбонат
H3PO4 Ортофосфорная PO4 Ортофосфат
HPO3 Метафосфорная PO3 метафосфат
H4P2O7 Пирофосфорная,дифосфорная P2O7 Дифосфат
H3PO3 Ортофосфористая PO3 Ортофосфит
HPO2 Метафосфористая PO2 Метафосфит
H3BO3 Ортоборная BO3 Ортоборат
HBO2 Метаборная BO2 Метаборат
H4SiO4 Ортокремниевая SiO4 Ортосиликат
H2SiO3 Метакремниевая SiO3 Метасиликат
H3AsO4 Мышьяковая AsO4 Арсенат
H3AsO3 Мышьяковистая AsO3 Арсенит
H2SeO4 Селеновая SeO4 Селенат
H2SeO3 Селенистая SeO3 Селенит
H2CrO4 Хромовая CrO4 Хромат
H2Cr2O7 Дихромовая Cr2O7 Дихромат
HMnO4 Марганцовая MnO4 Перманганат
H2MnO4 Марганцовистая MnO4 Манганат
HClO4 Хлорная ClO4 Перхлорат
HClO3 Хлорноватая ClO3 Хлорат
HClO2 Хлористая ClO2 Хлорит
HClO Хлорноватистая ClO Гипохлорит
H5IO6 Ортойодная IO6 Ортойодат
HJO4 Метайодная IO4 Метайодат
HIO Йодноватистая IO Гипойодит
HCN Синильная CN Цианид
HF Плавиковая F Фторид'''


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