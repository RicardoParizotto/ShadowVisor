import sys

class assemble_P4:
    '''
    open and write the merged structures to a new file
    it is importante to note that the verification must come earlier
    '''
    def assemble_new_program(self, headers, parser, actions, tables, control_flow):
        with open('composition.p4', 'w') as f:

            '''
            TODO
            make the includes and defs a dynamical thing
            that is: parse through the modules and '''    
            defs = """
            #include <core.p4>
            #include <v1model.p4>"""


            for item in headers:
                f.write('%s' % 'header ' + str(item) + ''.join(map(str, headers[item])) + '\n\n')

            f.write("%s" % parser)

            control = """\n\n\ncontrol MyIngress(inout headers hdr,
                  inout metadata meta,
                  inout standard_metadata_t standard_metadata) {
            """

            f.write("%s" % control)

            for item in actions:
                for action in item: #action name
                    f.write("%s" % "action " + action)
                    for j in item[action]:
                        if isinstance(j, list):
                            f.write("%s\n\n" % ''.join(map(str, j)))
                        else:
                            f.write("%s" % j)

            for item in tables:
                for table in item:   #table name
                    f.write("%s" % "table " + table)
                    for j in item[table]:
                        f.write("%s" % j)
                    f.write("\n\n")
            f.write("%s" % "}")

            #calculate a simple sequential composition. This need to be connected to the composition calc
            #dont know how

            f.write("%s" % control_flow)


            end = """
            /*************************************************************************
            ****************  E G R E S S   P R O C E S S I N G   *******************
            *************************************************************************/

            control MyEgress(inout headers hdr,
                             inout metadata meta,
                             inout standard_metadata_t standard_metadata) {
                apply {  }
            }

            /*************************************************************************
            *************   C H E C K S U M    C O M P U T A T I O N   **************
            *************************************************************************/
            control MyComputeChecksum(inout headers hdr, inout metadata meta) {
                apply {   }
            }


            /*************************************************************************
            ***********************  D E P A R S E R  *******************************
            *************************************************************************/

            control MyDeparser(packet_out packet, in headers hdr) {
                apply {
                    packet.emit(hdr.ethernet);
                }
            }

            /*************************************************************************
            ***********************  S W I T C H  *******************************
            *************************************************************************/

            V1Switch(
            MyParser(),
            MyVerifyChecksum(),
            MyIngress(),
            MyEgress(),
            MyComputeChecksum(),
            MyDeparser()
            ) main;"""

            f.write("%s" % end)

