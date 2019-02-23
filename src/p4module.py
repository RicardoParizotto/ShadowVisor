
from parser import parser_control_flow
from packet_parser import packet_parser

class load_P4module:
    #there is a need to include registers, metadata, and definition of definition of headers and structures
    tables_ = []
    actions_ = []

    def __init__(self, host):
        self.load = parser_control_flow(host)
        self.load.scan_control()
        self.parser = packet_parser(host)
        self.parser.scan_control()
