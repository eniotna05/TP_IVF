
class AlwaysTrue:
    def __init__(self):
        pass

    def test(self, variable_list):
        return True

class Comparaison:
    def __init__(self, var1, var2):
        # var1 is the position of the first variable to compare in variable list
        # var2 is the position of the second variable to compare in variable list
        self.var1 = var1
        self.var2 = var2

    def test(self, variable_list):
        if variable_list[self.var1] < variable_list[self.var2]:
            return True
        else:
            return False


