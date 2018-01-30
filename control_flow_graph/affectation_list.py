
class Skip:
    def __init__(self):
        pass

    def run(self, variable_list):
        return variable_list

class Somme:
    def __init__(self, output, inputs, constant=0):
        #Output is the position in variable list of the result variable
        #Input is a list of positions in variable lists of the vairiables summed
        #Constant is a constant number added to the sum

        #Note: Somme can also be used for initialisation a constant, by choosing a constant and inputs = []

        self.output = output
        self.constant = constant
        self.inputs = inputs

    def run(self, variable_list):
        result = self.constant
        for input in self.inputs:
            result += variable_list[input]
        variable_list[self.output] = result
        return variable_list


class Multiplication:
    def __init__(self, output, inputs, constant=1):
        #Output is the position in variable list of the result variable
        #Input is a list of positions in variable lists of the vairiables multiplied
        #Constant is a constant number to multiply the result

        self.output = output
        self.constant = constant
        self.inputs = inputs

    def run(self, variable_list):
        result = self.constant
        for input in self.inputs:
            result = result * variable_list[input]
        variable_list[self.output] = result
        return variable_list


