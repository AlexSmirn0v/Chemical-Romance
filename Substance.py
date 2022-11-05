from Theory import up, under, isSoluble, elem_parameters, CATIONS, ANIONS, NAME, gentle, charge
import sympy as sym


class DoesNotExistError(Exception):
    pass


class Substance:
    def __init__(self, el_list):
        self.el_list = el_list
        self.__str__()
        self.fpart = self.get_fpart()
        self.spart = self.get_spart()
        self.part_number = self.get_particles_number()
        self.name = str()

    def __str__(self):
        x = list(map(str, self.el_list))
        self.el_str = ''.join(x)
        if x[0].isnumeric():
            del x[0]
        self.only_el_str = ''.join(x)
        return self.el_str

    def __add__(self, other):
        return str(self) + ' + ' + str(other)

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
            elif self.spart[0] == 'F':
                self.name = ('Фторид ' +
                             gentle(elem_parameters(self.fpart)['rusName'] if self.fpart != 'NH4' else 'аммоний'))
                return 'Фторид'
            elif self.fpart == 'H' and self.spart == 'O' and self.only_el_str != 'H2O2':
                self.name = 'Вода'
                return 'Вода'
            elif self.fpart == 'H' and self.spart in ANIONS and self.only_el_str == NAME[self.spart][2]:
                print(NAME[self.spart][2])
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
            self.name = 'Ошибка ввода или несуществующее соединение'
            return 'Ошибка ввода'

    def get_name(self):
        self.get_type()
        return self.name.capitalize()

    def get_oxi(self):
        try:
            self.oxis = list()
            if (self.spart is None or self.spart == '') and len(self.fpart_list) == 1:
                self.oxis = [0]
            elif self.only_el_str == 'OF2':
                self.oxis = [1, -1]
            elif (charge(self.fpart) or charge(self.spart)) is None:
                print(charge(self.fpart) is None)
                print(charge(self.spart) is None)
                raise DoesNotExistError
            elif (self.get_particles_number()[0] * charge(self.fpart) +
                  self.get_particles_number()[1] * charge(self.spart)) != 0:
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
                print(summer)
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
                        found_grade1 = set(sym.solveset(summer - charge(self.spart), y)).pop()
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
                    el_lister.append(up(str(abs(self.oxis[a])) + symb))
                    a += 1
            return ''.join(el_lister)
        except DoesNotExistError:
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
        if len(elems) == 2 and elems != ['O', 'H']:
            elems = elems[0]
        self.spart_list = elems
        return ''.join(map(str, elems))


if __name__ == '__main__':
    dioxide = Substance([3, 'O', 'F', 2])
    print(dioxide.get_fpart())
    print(dioxide.get_spart())
    print(dioxide.get_name(), dioxide.get_oxi())
