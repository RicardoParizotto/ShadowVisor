
from parser import parser_control_flow


class load_P4module:
    #there is a need to include registers, metadata, and definition of definition of headers and structures
    name = ''
    tables_ = []
    actions_ = []

    def __init__(self, module):
        self.load = parser_control_flow(self.read_file(module))

    def read_file(self, file):
        f = open(file, 'r')
        return f.read()
