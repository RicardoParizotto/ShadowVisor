
from parser import parser_control_flow


class load_P4module:
    #there is a need to include registers, metadata, and definition of definition of headers and structures
    tables_ = []
    actions_ = []

    def __init__(self, host):
        self.load = parser_control_flow(host)


