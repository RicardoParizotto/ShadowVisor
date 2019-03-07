
from parser import parser_control_flow


class load_P4module:
    #there is a need to include registers, metadata, and definition of definition of headers and structures
    tables_ = []
    actions_ = []

    def __init__(self, module):
    	self.name = module
        self.load = parser_control_flow(self.read_file(module))

    def read_file(self, file):
        f = open(file+'.p4', 'r')
        return f.read()
