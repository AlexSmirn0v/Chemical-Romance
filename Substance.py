from Theory import up, under, isSoluble, elem_parameters, CATIONS, ANIONS, NAME, gentle


class DoesNotExistError(Exception):
    pass


class Substance:
    def __init__(self, el_list):
        self.el_list = el_list
        self.el_str = ''.join(map(str, self.el_list))
        self.fpart = self.get_fpart()
        self.spart = self.get_spart()
        self.part_number = self.get_particles_number()
        self.name = str()

    def __str__(self):
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
        elif self.fpart == 'H' and self.spart == 'O':
            self.name = 'Вода'
            return 'Вода'
        elif self.fpart == 'H' and self.spart in ANIONS:
            self.name = NAME[self.spart][1] + ' кислота'
            return 'Кислота'
        elif self.fpart in CATIONS and self.spart in ANIONS:
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
            else:
                raise DoesNotExistError
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

    def get_name(self):
        self.get_type()
        return self.name.capitalize()

    def get_valence(self):
        pass

    def get_oxi(self):
        pass

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
