class Imprimer:
    def __init__(self, var_position):
        # Print the selected variable in the variable list

        self.var_position = var_position

    def run(self, variable_list):
        print(variable_list[self.var_position])