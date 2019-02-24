import sys

from p4module import load_P4module
from assembler import assemble_P4

class commandline:
    def __init__(self):
        self.tables_ = []
        self.actions_ = []
        self.parser_ = {}        #dic of states of the parser. Each state maps to a list of attributes
        self.params_ = []
        self.selects_ = {}
        self.extract_ = {}

        self.init_catalogue()

    def init_catalogue(self):
        catalogue = """{
         meta.context_control = 1;
         meta.extension_id1 = prog;
        } """

        shadow = """{
           key = {
              hdr.ethernet.dstAddr: lpm;
           }
           actions = {
               set_chaining;
               NoAction;
           }
           size = 1024;
           default_action = NoAction();
        }"""

        #more param to the set_chatining
        #i read this comment now and i dont understand it anymore
        #i will keep it here for artistic purposes
        self.actions_.append({'set_chaining': ['(egressSpec_t prog)', catalogue]})
        self.tables_.append({'shadow':shadow})

        self.applys = """
        apply {
            shadow.apply();
            if(meta.context_control == 1){ \n"""

    def build_parser_extension(self):
        #remember that packet extracts are optinal
        #remember also that selects may follow from transitions
        parser_def = """
        parser MyParser(packet_in packet,
                        out headers hdr,
                        inout metadata meta,
                        inout standard_metadata_t standard_metadata) {
         {\n\n"""

        for item in self.parser_:
            parser_def = parser_def + """ state """ + item + """ { \n"""

            if(item in self.extract_):
                parser_def = parser_def + 'packet.extract' + str(self.extract_[item] + ';\n')
            if(item in self.selects_):
                parser_def = parser_def + 'transition select' + str(self.selects_[item] + '{\n')
            for transition in self.parser_[item]:
                if(transition == '*'):
                    parser_def = parser_def + 'transition ' + str(self.parser_[item]['*']) + """; \n"""
                else:
                    parser_def = parser_def + str(transition) + ':' + str(self.parser_[item][transition]) + """; \n"""
            if(item in self.selects_):
                parser_def = parser_def + """}\n"""  #close the state brackets
            parser_def = parser_def + """}\n"""  #close the state brackets
        parser_def = parser_def + "}\n"  #close the parser brackets

        return parser_def


    def calc_sequential_(self, host, extension):
        return  """if(meta.extension_""" + "host_id" + """==1) { \n
                    """ + ''.join(map(str, host.load.apply_['MyIngress'])) + """
                }if(meta.extension_""" + "host_id" + """==666){
                    """ + ''.join(map(str, extension.load.apply_['MyIngress'])) + """
                }
            """
    #TODO
    def calc_parallel_(self, host, extension):
        return  """if(meta.extension_""" + "host_id" + """==1) { \n
                    """ + ''.join(map(str, host.apply_['MyIngress'])) + """
                }if(meta.extension_""" + "host_id" + """==666){
                    """ + ''.join(map(str, extension.apply_['MyIngress'])) + """
                }
            """

    def read_file(self, file):
        f = open(file, 'r')
        return f.read()

    def parser_union(self, module):
        for item in module.parser.parser_:
            if not item in self.parser_:
                self.parser_[item] = module.parser.parser_[item]
                print(str(self.parser_[item]) + '\n')
            else:
                for transition in module.parser.parser_[item]:
                    if not transition in self.parser_[item]:
                        self.parser_[item].add(transition)
                        print(str(transition) + '\n')

        for item in module.parser.selects_:
            print('teste\n')
            if not item in self.selects_:
                self.selects_[item] = module.parser.selects_[item]

        for item in module.parser.extract_:
            print('teste2\n')
            if not item in self.extract_:
                self.extract_[item] = module.parser.extract_[item]
        print('union of packet parser')

    #just calculates de union of table definitions
    def table_union(self, module):
        self.tables_ = self.tables_ + module.tables_

    def action_union(self, module):
        self.actions_ = self.actions_ + module.actions_

    #this only make unions of the constructors of both the host and the extension
    def carry_composition(self, module):
        if not isinstance(module, load_P4module):
            #union of parsers???  todo
            module = load_P4module(self.read_file(module))
            self.parser_union(module)
            self.table_union(module.load)
            self.action_union(module.load)
        return module

    def write_composition_(self, skeleton):
        #if sequential composition the extension id is always 1. Different ids can be used to
        #point to more modules
        self.applys = self.applys + skeleton +"""
            }
        }
        """

        #concatenate applys from the host and the extension
        assembler = assemble_P4()
        assembler.assemble_new_program(self.build_parser_extension(), self.actions_, self.tables_, self.applys)
