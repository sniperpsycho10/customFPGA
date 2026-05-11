class Fabric:

    def __init__(self):
        self.luts = {}


    def add_lut(self, lut):

        self.luts[lut.name] = lut


    def show_luts(self):

        for lut_name in self.luts:
            print(lut_name)