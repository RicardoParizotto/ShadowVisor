class parser_control_flow:

    tables_= []        #list of tables. I think that a dict would be efficiently
    actions_ = []      #list of actions. Same for dict...
    apply_ = {}        #a dic of every apply found on each control. The control id is the dic index

    #init structures to help the scanning process
    def __init__(self, src_p4):
        self.it_lines = 0
        self.it_symbols = 0
        self.src_code = src_p4
        self.code_len = len(self.src_code)
        self.buffer_ = []
        self.tables = []

    #load param definitions to a different structure
    #this is necessary just for parsing and rewriting
    def parse_params(self):
        params_ = ""

        while True:
            params_ = params_ + self.src_code[self.it_lines]
            if self.src_code[self.it_lines] == ')': 
                break     
            self.it_lines = self.it_lines + 1
        self.it_lines = self.it_lines + 1

        return params_

    #just load a block between '{' and '}'
    #all recursive calls inside the block are loaded with
    def parse_codeBlock(self):
        colchetes = 0
        local_buffer = []

        while self.it_lines < self.code_len:
            if(self.src_code[self.it_lines] == '{'):
                colchetes = colchetes + 1
            elif(self.src_code[self.it_lines] == '}'):
               local_buffer.append(self.src_code[self.it_lines])
               self.it_lines = self.it_lines + 1
               if(colchetes == 1):
                   return local_buffer
               else:
                   colchetes = colchetes - 1
            local_buffer.append(self.src_code[self.it_lines])
            self.it_lines = self.it_lines + 1
        return -1

    #just scan the name (id) of a control flow construct
    #its a naive implementation, since
    def parse_name(self):
        _name = ""
        while self.it_lines < self.code_len:
            it = self.src_code[self.it_lines]
            if(it != '{' and it != '(' and it != ';'):
                _name = _name + it
            else:
                break
            self.it_lines = self.it_lines + 1
        return _name.strip()

    #scan constructs that have identificator such as
    #controls, actions and tables definitions
    def scan_def(self, dic_):
        it_symbols = 0

        while self.it_lines < self.code_len:
            if dic_[it_symbols] == '*':
                return True
            else:
                if(dic_[it_symbols] == self.src_code[self.it_lines]):
                    it_symbols = it_symbols + 1
                else:
                    return False
            self.it_lines = self.it_lines + 1

    def scan_control_block(self, block_name):
        colchetes = 0

        while self.it_lines < self.code_len:
            if(self.src_code[self.it_lines] == '{'):
                colchetes = colchetes + 1
            elif(self.src_code[self.it_lines] == '}'):
               self.it_lines = self.it_lines + 1
               if(colchetes == 1):
                   return #magic
               else:
                   colchetes = colchetes - 1
            elif(self.src_code[self.it_lines] == 't'):
                    #try to read table
                    if(self.scan_def("table*")):
                        name = self.parse_name()
                        block = self.parse_codeBlock()
                        self.tables_.append({name : block})
            elif(self.src_code[self.it_lines] == 'a'):
                if(self.src_code[self.it_lines+1] == 'c'):
                    if(self.scan_def("action*")):
                            name = self.parse_name()
                            params = self.parse_params()
                            block = self.parse_codeBlock()
                            self.actions_.append({name : [params,block]})
                elif(self.scan_def("apply*")):
                    self.apply_[block_name] = self.parse_codeBlock()
            self.it_lines = self.it_lines + 1

    #scan the construct inside a control or parsers
    def scan_control(self):
        while self.it_lines < self.code_len:
            if(self.src_code[self.it_lines] == 'c'):
                if(self.scan_def("control*")):
                    name = self.parse_name()
                    params = self.parse_params()
                    block = self.scan_control_block(name)

            self.it_lines = self.it_lines + 1
