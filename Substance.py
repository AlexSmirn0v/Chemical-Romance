class Substance:
    def __init__(self, el_list):
        self.el_list = el_list
        self.el_str = ''.join(map(str, self.el_list))

    def __str__(self):
        return self.el_str

    def __add__(self, other):
        return str(self) + ' + ' + str(other)

    def get_type(self):
        pass

    def get_name(self):
        return 'Вода'
