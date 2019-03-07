import sys

from assembler import assemble_P4
from p4module import load_P4module

class commandline:
    def __init__(self):
        self.tables_ = []
        self.actions_ = []
        self.parser_ = {}        #dic of states of the parser. Each state maps to a list of attributes
        self.params_ = []
        self.selects_ = {}
        self.extract_ = {}
        self.headers_ = {}
        self.emit_ = []
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

    '''
    carry the operators from the modules already parsed and composed
    it also open a module if it
    '''
    def carry_composition(self, module):
        if not isinstance(module, load_P4module):
            module = load_P4module(module)
            self.parser_union(module)
            self.table_union(module.load)
            self.action_union(module.load)
            self.header_union(module)
            self.deparser_union(module)
        return module

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
        print(host.name + extension.name)
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

    def deparser_union(self, module):
        #TODO reorder transitions
        for item in module.load.emit_:
            print(item)
            if not item in self.emit_:
                self.emit_.append(item)


    #TODO reorder transitions
    def parser_union(self, module):
        for item in module.load.parser_:
            if not item in self.parser_:
                self.parser_[item] = module.load.parser_[item]
            else:
                for transition in module.load.parser_[item]:
                    if not transition in self.parser_[item]:
                        self.parser_[item].add(transition)

        for item in module.load.selects_:
            if not item in self.selects_:
                self.selects_[item] = module.load.selects_[item]

        for item in module.load.extract_:
            if not item in self.extract_:
                self.extract_[item] = module.load.extract_[item]

    #just calculates de union of table definitions
    def table_union(self, module):
        self.tables_ = self.tables_ + module.tables_

    def action_union(self, module):
        self.actions_ = self.actions_ + module.actions_

    def header_union(self, module):
        for item in module.load.headers_:
            if not item in self.headers_:
                self.headers_[item] = module.load.headers_[item]

    def write_composition_(self, skeleton):
        #if sequential composition the extension id is always 1. Different ids can be used to
        #point to more modules
        self.applys = self.applys + str(skeleton) +"""
            }
        }
        """

        #concatenate applys from the host and the extension
        assembler = assemble_P4()
        assembler.assemble_new_program(self.headers_, self.build_parser_extension(), self.actions_, self.tables_, self.applys, self.emit_)
