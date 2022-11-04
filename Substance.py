from Theory import up, under, isSoluble, elem_parameters, CATIONS, ANIONS


class DoesNotExistError(Exception):
    pass


class Substance:
    def __init__(self, el_list):
        self.el_list = el_list
        self.el_str = ''.join(map(str, self.el_list))
        self.fpart = self.get_fpart()
        self.spart = self.get_spart()
        self.part_number = self.get_particles_number()

    def __str__(self):
        return self.el_str

    def __add__(self, other):
        return str(self) + ' + ' + str(other)

    def get_particles_number(self):
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

        if '(' in self.el_list[self.n:]:
            s_koef = int(self.el_list[self.el_list.index(')', self.n + 1) + 1])
        elif len(self.spart_list) == 1 and type(self.el_list[-1]) == int:
            s_koef = self.el_list[-1]
        else:
            s_koef = 1

        return koef * f_koef, koef * s_koef

    def get_type(self):
        if self.fpart == 'H' and self.spart == 'O':
            return 'Вода'
        elif self.fpart == 'H' and self.spart in ANIONS:
            return 'Кислота'
        elif self.fpart in CATIONS and self.spart in ANIONS:
            return 'Соль'
        elif self.fpart in CATIONS and self.spart == 'OH':
            if isSoluble(self) is True:
                return 'Щёлочь'
            elif isSoluble(self) is False:
                return 'Основание'
            else:
                raise DoesNotExistError
        elif self.spart == 'O':
            grade = int(self.part_number[1] * 2 / self.part_number[0])
            if (self.fpart in ['Zn', 'Be', 'Sn', 'Pb'] or
                  (elem_parameters(self.fpart)['isMetal'] and grade in range(3, 5))):
                return 'Амфотерный оксид'
            elif elem_parameters(self.fpart)['isMetal'] and grade in range(1, 3):
                return 'Основный оксид'
            elif (not elem_parameters(self.fpart)['isMetal'] or
                  (elem_parameters(self.fpart)['isMetal'] and grade in range(5, 8))):
                return 'Кислотный оксид'

    def get_name(self):
        return 'Вода'

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
        if '(' in self.el_list[self.n:]:
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


abra = Substance([3, 'Zn', 'O'])
print(abra.get_fpart())
print(abra.get_spart())
print(abra.get_particles_number())
print(abra.get_type())
