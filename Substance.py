from Theory import up, under, isSoluble, elem_parameters, CATIONS, ANIONS, NAME, gentle, \
    charge, substance_maker, METAL_ACTIVENESS, ACID_STRENGTH, acid_maker
import sympy as sym
from math import lcm

Hydrogen = ['H', 2]
Water = ['H', 2, 'O']


class DoesNotExistError(Exception):
    pass


class Substance:
    def __init__(self, el_list, html=False):
        self.isHtml = html
        self.el_list = el_list
        self.any_error = False
        x = list(map(str, self.el_list))
        if x[0].isnumeric():
            del x[0]
        self.only_el_str = ''.join(x)
        self.__str__
        self.fpart = self.get_fpart()
        self.spart = self.get_spart()
        self.part_number = self.get_particles_number()
        self.name = str()

    def __str__(self):
        if self.isHtml:
            res = list()
            for index, elem in enumerate(self.el_list):
                if type(elem) == int and index != 0:
                    res.append(under(elem))
                else:
                    res.append(str(elem))
            self.el_str = ''.join(res)
        else:
            self.el_str = ''.join(map(str, self.el_list))
        return self.el_str

    def __add__(self, other):
        try:
            elems_list_1 = list()
            elems_list_2 = list()
            # don't forget to delete!!
            #other = Substance(other)
            if {self.get_type(), other.get_type()} in [{'Основный оксид', 'Кислотный оксид'},
                                                       {'Амфотерный оксид', 'Кислотный оксид'},
                                                       {'Основный оксид', 'Амфотерный оксид'}]:
                if (other.get_type() == 'Основный оксид'
                        and self.get_type() == ('Амфотерный оксид' or 'Кислотный оксид')):
                    begin_part = other.fpart_list
                    begin_part_number = other.get_particles_number()[0]
                    middle_part = self.fpart_list
                    middle_part_number = self.get_particles_number()[0]
                elif (other.get_type() == ('Основный оксид' or 'Амфотерный оксид')
                      and self.get_type() == 'Кислотный оксид'):
                    begin_part = other.fpart_list
                    begin_part_number = other.get_particles_number()[0]
                    middle_part = self.fpart_list
                    middle_part_number = self.get_particles_number()[0]
                elif (self.get_type() == 'Основный оксид'
                      and other.get_type() == ('Амфотерный оксид' or 'Кислотный оксид')):
                    begin_part = self.fpart_list
                    begin_part_number = self.get_particles_number()[0]
                    middle_part = other.fpart_list
                    middle_part_number = other.get_particles_number()[0]
                elif (self.get_type() == ('Основный оксид' or 'Амфотерный оксид')
                      and other.get_type() == 'Кислотный оксид'):
                    begin_part = self.fpart_list
                    begin_part_number = self.get_particles_number()[0]
                    middle_part = other.fpart_list
                    middle_part_number = other.get_particles_number()[0]

                elems_list_1.extend(begin_part)
                if begin_part_number != 1:
                    elems_list_1.append(begin_part_number)
                elems_list_1.extend(middle_part)
                if middle_part_number != 1:
                    elems_list_1.append(middle_part_number)
                elems_list_1.extend(['O', self.get_particles_number()[1] + other.get_particles_number()[1]])
                return Substance(elems_list_1, html=True),

            elif {self.get_type(), other.get_type()} in [{'Кислота', 'Основание'},
                                                         {'Кислота', 'Щёлочь'}]:
                acid = list(filter(lambda x: x.get_type() == 'Кислота', [self, other]))[0]
                alkali = list(filter(lambda x: x.get_type() != 'Кислота', [self, other]))[0]

                elems_list_1 = substance_maker(alkali.fpart_list, acid.spart_list,
                                               alkali.get_particles_number()[0], acid.get_particles_number()[1])
                if alkali.get_particles_number()[1] != 1:
                    elems_list_2.append(alkali.get_particles_number()[1])
                elems_list_2.extend(Water)

            elif {self.get_type(), other.get_type()} in [{'Основный оксид', 'Кислота'},
                                                         {'Амфотерный оксид', 'Кислота'}]:
                acid = list(filter(lambda x: x.get_type() == 'Кислота', [self, other]))[0]
                oxide = list(filter(lambda x: x.get_type() != 'Кислота', [self, other]))[0]

                elems_list_1 = substance_maker(oxide.fpart_list, acid.spart_list,
                                               oxide.get_particles_number()[0], acid.get_particles_number()[1])
                if oxide.get_particles_number()[1] != 1:
                    elems_list_2.append(oxide.get_particles_number()[1])
                elems_list_2.extend(Water)
            elif {self.get_type(), other.get_type()} in [{'Кислотный оксид', 'Щёлочь'},
                                                         {'Амфотерный оксид', 'Щёлочь'}]:
                alkali = list(filter(lambda x: x.get_type() == 'Щёлочь', [self, other]))[0]
                oxide = list(filter(lambda x: x.get_type() != 'Щёлочь', [self, other]))[0]
                if type(oxide.el_list[0]) == int:
                    ox_koef = oxide.el_list[0]
                else:
                    ox_koef = 1
                wat_koef = alkali.get_particles_number()[1] - 1
                acid = Substance(acid_maker(oxide.el_list, ox_koef, wat_koef))
                elems_list_1 = substance_maker(alkali.fpart_list, acid.spart_list,
                                               alkali.get_particles_number()[0], acid.get_particles_number()[1])
                elems_list_2 = Water

            elif {self.get_type(), other.get_type()} == {'Соль', 'Щёлочь'}:
                salt = list(filter(lambda x: x.get_type() == 'Соль', [self, other]))[0]
                alkali = list(filter(lambda x: x.get_type() != 'Соль', [self, other]))[0]

                if isSoluble(salt):
                    elems_list_1 = substance_maker(salt.fpart_list, alkali.spart_list,
                                                   salt.part_number[0], alkali.part_number[1])
                    elems_list_2 = substance_maker(alkali.fpart_list, salt.spart_list,
                                                   alkali.part_number[0], salt.part_number[1])
                    if isSoluble(Substance(elems_list_1)) and not isSoluble(Substance(elems_list_2)):
                        pass
                    elif isSoluble(Substance(elems_list_2)) and not isSoluble(Substance(elems_list_1)):
                        pass
                    else:
                        raise DoesNotExistError
            elif {self.get_type(), other.get_type()} == {'Соль', 'Кислота'}:
                salt = list(filter(lambda x: x.get_type() == 'Соль', [self, other]))[0]
                acid = list(filter(lambda x: x.get_type() != 'Соль', [self, other]))[0]

                if isSoluble(salt):
                    elems_list_1 = substance_maker(salt.fpart_list, acid.spart_list,
                                                   salt.part_number[0], acid.part_number[1])
                    elems_list_2 = substance_maker(acid.fpart_list, salt.spart_list,
                                                   acid.part_number[0], salt.part_number[1])
                    isWeaker = (ACID_STRENGTH.index(Substance(elems_list_2).only_el_str) >
                                ACID_STRENGTH.index(acid.only_el_str))
                    if isSoluble(Substance(elems_list_1)) and not isWeaker:
                        pass
                    elif isWeaker and not isSoluble(Substance(elems_list_1)):
                        pass
                    else:
                        raise DoesNotExistError
            elif (self.get_type() and other.get_type()) == 'Соль':
                f_salt = self
                s_salt = other

                if isSoluble(f_salt) and isSoluble(s_salt):
                    elems_list_1 = substance_maker(f_salt.fpart_list, s_salt.spart_list,
                                                   f_salt.get_particles_number()[0], s_salt.get_particles_number()[1])
                    elems_list_2 = substance_maker(s_salt.fpart_list, f_salt.spart_list,
                                                   s_salt.get_particles_number()[0], f_salt.get_particles_number()[1])
                    if isSoluble(Substance(elems_list_1)) and not isSoluble(Substance(elems_list_2)):
                        pass
                    elif isSoluble(Substance(elems_list_2)) and not isSoluble(Substance(elems_list_1)):
                        pass
                    else:
                        raise DoesNotExistError

            elif {self.get_type(), other.get_type()} == {'Кислотный оксид', 'Вода'}:
                water = list(filter(lambda x: x.only_el_str == 'H2O', [self, other]))[0]
                oxide = list(filter(lambda x: x.only_el_str != 'H2O', [self, other]))[0]
                if type(oxide.el_list[0]) == int:
                    ox_koef = oxide.el_list[0]
                else:
                    ox_koef = 1
                if type(water.el_list[0]) == int:
                    wat_koef = water.el_list[0]
                else:
                    wat_koef = 1
                if oxide.only_el_str != 'SiO2':
                    elems_list_1 = acid_maker(oxide.el_list, ox_koef, wat_koef)
                    return Substance(elems_list_1, html=True),
                else:
                    raise DoesNotExistError
            elif {self.get_type(), other.get_type()} == {'Основный оксид', 'Вода'}:
                water = list(filter(lambda x: x.only_el_str == 'H2O', [self, other]))[0]
                oxide = list(filter(lambda x: x.only_el_str != 'H2O', [self, other]))[0]
                if oxide.get_fpart() in METAL_ACTIVENESS[:METAL_ACTIVENESS.index('Mg')]:
                    elems_list_1 = substance_maker(oxide.fpart_list, ["O", 'H'],
                                                   oxide.get_particles_number()[0], water.get_particles_number()[0])
                    if type(elems_list_1) == str:
                        raise DoesNotExistError
                    return Substance(elems_list_1, html=True),
            else:
                print({self.get_type(), other.get_type()} in [{'Основный оксид', 'Кислота'},
                                                              {'Амфотерный оксид', 'Кислота'}])
                raise DoesNotExistError
            return Substance(elems_list_1, html=True), Substance(elems_list_2, html=True)
        except DoesNotExistError:
            return '''Ошибка ввода или невозможная реакция. 
            Возможно, опечатка в коэффициентах''',

    def get_particles_number(self):
        try:
            if type(self.el_list[0]) == int:
                koef = self.el_list[0]
            else:
                koef = 1

            if '(' in self.el_list[:self.n]:
                f_koef = int(self.el_list[self.el_list.index(')') + 1])
            elif len(self.fpart_list) == 1 and type(self.el_list[self.n + 1]) == int:
                f_koef = self.el_list[self.n + 1]
            else:
                f_koef = 1

            if self.spart == '' or self.spart is None:
                s_koef = 0
            elif '(' in self.el_list[self.n:]:
                s_koef = int(self.el_list[self.el_list.index(')', self.n + 1) + 1])
            elif len(self.spart_list) == 1 and type(self.el_list[-1]) == int:
                s_koef = self.el_list[-1]
            else:
                s_koef = 1
            return koef * f_koef, koef * s_koef
        except IndexError:
            pass

    def get_type(self):
        try:
            if self.spart == '' and elem_parameters(self.fpart)['isMetal']:
                self.name = elem_parameters(self.fpart)['rusName']
                return 'Металл'
            elif self.spart == '' and self.fpart == 'H':
                self.name = 'Водород'
                return 'Водород'
            elif self.spart == '' and self.fpart == 'O':
                self.name = 'Кислород'
                return 'Кислород'
            elif self.spart == '' and not elem_parameters(self.fpart)['isMetal']:
                self.name = elem_parameters(self.fpart)['rusName']
                return 'Неметалл'
            elif self.spart[0] == 'H':
                self.name = ('Гидрид ' +
                             gentle(elem_parameters(self.fpart)['rusName'] if self.fpart != 'NH4' else 'аммоний'))
                return 'Гидрид'
            elif self.only_el_str == 'OF2':
                self.name = ('Фторид ' +
                             gentle(elem_parameters(self.fpart)['rusName'] if self.fpart != 'NH4' else 'аммоний'))
                return 'Соль'
            elif self.fpart == 'H' and self.spart == 'O' and self.only_el_str != 'H2O2':
                self.name = 'Вода'
                return 'Вода'
            elif self.fpart == 'H' and self.spart in ANIONS and self.only_el_str == NAME[self.spart][2]:
                self.name = NAME[self.spart][1] + ' кислота'
                return 'Кислота'
            elif self.fpart in CATIONS and 'H' not in self.fpart and self.spart in ANIONS:
                self.name = (NAME[self.spart][0] + ' ' +
                             gentle(elem_parameters(self.fpart)['rusName'] if self.fpart != 'NH4' else 'аммоний'))
                return 'Соль'
            elif self.fpart in CATIONS and self.spart == 'OH':
                self.name = ('Гидроксид ' +
                             gentle(elem_parameters(self.fpart)['rusName'] if self.fpart != 'NH4' else 'аммоний'))
                if isSoluble(self) is True:
                    return 'Щёлочь'
                elif isSoluble(self) is False:
                    return 'Основание'
            elif self.spart == 'O':
                grade = int(self.part_number[1] * 2 / self.part_number[0])
                self.name = ('Оксид ' +
                             gentle(elem_parameters(self.fpart)['rusName'] if self.fpart != 'NH4' else 'аммоний'))
                if (self.fpart in ['Zn', 'Be', 'Sn', 'Pb'] or
                        (elem_parameters(self.fpart)['isMetal'] and grade in range(3, 5))):
                    return 'Амфотерный оксид'
                elif elem_parameters(self.fpart)['isMetal'] and grade in range(1, 3):
                    return 'Основный оксид'
                elif (not elem_parameters(self.fpart)['isMetal'] or
                      (elem_parameters(self.fpart)['isMetal'] and grade in range(5, 8))):
                    return 'Кислотный оксид'
                else:
                    raise DoesNotExistError
            else:
                raise DoesNotExistError
        except DoesNotExistError:
            self.any_error = True
            self.name = 'Ошибка ввода или несуществующее соединение'
            return 'Ошибка ввода'

    def get_name(self):
        self.get_type()
        return self.name.capitalize()

    def get_oxi(self):
        try:
            self.oxis = list()
            if self.spart == 'H':
                b = -1
            else:
                b = charge(self.spart)
            if (self.spart is None or self.spart == '') and len(self.fpart_list) == 1:
                self.oxis = [0]
            elif self.only_el_str == 'OF2':
                self.oxis = [1, -1]
            elif (charge(self.fpart) or b) is None:
                raise DoesNotExistError
            elif (self.part_number[0] * charge(self.fpart) +
                  self.part_number[1] * b) != 0:
                raise DoesNotExistError
            else:
                turner = False
                elems = dict()
                summer = int()
                for index, elem in enumerate(self.fpart_list):
                    if elem.isalpha():
                        if index + 1 == len(self.fpart_list) or type(self.fpart_list[index + 1]) != int:
                            number = 1
                        else:
                            number = self.fpart_list[index + 1]
                        if elem == 'O' and 'F' not in self.el_list and self.only_el_str != 'H2O2':
                            grade = -2
                        elif elem == 'H':
                            grade = 1
                        elif elem == 'F':
                            grade = -1
                        else:
                            grade = sym.var('x')
                            turner = True
                        elems[elem] = [number, grade]
                for i in elems:
                    summer += elems[i][0] * elems[i][1]
                if turner:
                    found_grade = set(sym.solveset(summer - charge(self.fpart), x)).pop()
                for item in elems:
                    self.oxis.append(elems[item][1] if type(elems[item][1]) == int else found_grade)
                if self.spart_list is not None and self.spart_list != ['']:
                    turner = False
                    elems.clear()
                    summer = int()
                    for index, elem in enumerate(self.spart_list):
                        if str(elem).isalpha():
                            if index + 1 >= len(self.spart_list) or type(self.spart_list[index + 1]) != int:
                                number = 1
                            else:
                                number = self.spart_list[index + 1]
                            if elem == 'O' and 'F' not in self.el_list and self.only_el_str != 'H2O2':
                                grade = -2
                            elif elem == 'H' and self.spart != 'OH':
                                grade = -1
                            elif elem == 'H' and self.spart == 'OH':
                                grade = 1
                            elif elem == 'F':
                                grade = -1
                            else:
                                grade = sym.var('y')
                                turner = True
                            elems[elem] = [number, grade]
                    for i in elems:
                        summer += elems[i][0] * elems[i][1]
                    if turner:
                        found_grade1 = set(sym.solveset(summer - b, y)).pop()
                    for item in elems:
                        self.oxis.append(elems[item][1] if type(elems[item][1]) == int else found_grade1)

            a = 0
            el_lister = list()
            for index, elem in enumerate(self.el_list):
                if type(elem) == int and index != 0:
                    el_lister.append(under(elem))
                else:
                    el_lister.append(str(elem))
                if str(elem).isalpha():
                    if self.oxis[a] > 0:
                        symb = '+'
                    elif self.oxis[a] == 0:
                        symb = ''
                    elif self.oxis[a] < 0:
                        symb = '-'
                    el_lister.append(up(symb + str(abs(self.oxis[a]))))
                    a += 1
            return ''.join(el_lister)
        except DoesNotExistError:
            self.any_error = True
            return 'Ошибка ввода или несуществующее соединение'
        except TypeError:
            self.any_error = True
            return 'Ошибка ввода или несуществующее соединение'

    def get_fpart(self):
        self.n = 0
        while type(self.el_list[self.n]) != str:
            self.n += 1
        if self.el_list[self.n] == 'N' or self.el_list[self.n] == '(':
            self.n += (2 if self.el_list[self.n] == 'N' else 4)
            self.fpart_list = ['N', 'H', 4]
            return 'NH4'
        else:
            self.fpart_list = [self.el_list[self.n]]
            return self.el_list[self.n]

    def get_spart(self):
        if self.n + 1 == len(self.el_list):
            elems = []
        elif '(' in self.el_list[self.n:]:
            elems = self.el_list[self.el_list.index('(', self.n + 1) + 1:self.el_list.index(')', self.n + 1)]
        elif type(self.el_list[self.n + 1]) == int:
            elems = self.el_list[self.n + 2:]
        elif self.fpart == 'NH4':
            elems = self.el_list[self.n + 1:]
        else:
            elems = self.el_list[self.n + 1:]
        if len(elems) == 2 and elems[1] != 'H':
            x = elems[0]
            elems.clear()
            elems.append(x)
        self.spart_list = elems
        return ''.join(map(str, elems))


if __name__ == '__main__':
    dioxide = Substance([2, 'Na',  'O', 'H'])
    oxire = Substance(['S', 'O', 3])
    print(' + '.join((map(str, (oxire + dioxide)))))
