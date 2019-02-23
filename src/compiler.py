import sys

from p4module import load_P4module
from assembler import assemble_P4

class commandline:

    def __init__(self):
        self.parser_= {}
        self.tables_ = []
        self.actions_ = []
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
        self.actions_.append({'set_chaining': ['(egressSpec_t prog)', catalogue]})
        self.tables_.append({'shadow':shadow})

        self.applys = """
        apply {
            shadow.apply();

            if(meta.context_control == 1){ \n"""


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

        #TODO packet parser union
        #concatenate applys from the host and the extension
        assembler = assemble_P4()
        assembler.assemble_new_program(self.parser_, self.actions_, self.tables_, self.applys)
