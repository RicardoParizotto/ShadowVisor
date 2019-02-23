{}


control MyIngress(inout headers hdr,
                  inout metadata meta,
                  inout standard_metadata_t standard_metadata) {
            action set_chaining(egressSpec_t prog){
         meta.context_control = 1;
         meta.extension_id1 = prog;
        } action drop() {
        mark_to_drop();
    }

action simple_forward(egressSpec_t port){
        standard_metadata.egress_spec = port;
    }

action drop() {
        mark_to_drop();
    }

action simple_forward(egressSpec_t port){
        standard_metadata.egress_spec = port;
    }

action drop() {
        mark_to_drop();
    }

action set_ecmp_select(bit<16> ecmp_base, bit<32> ecmp_count) {
        /* TODO: hash on 5-tuple and save the hash result in meta.ecmp_select 
           so that the ecmp_nhop table can use it to make a forwarding decision accordingly */
    }

action set_nhop(bit<48> nhop_dmac, bit<32> nhop_ipv4, bit<9> port) {
        hdr.ethernet.dstAddr = nhop_dmac;
        hdr.ipv4.dstAddr = nhop_ipv4;
        standard_metadata.egress_spec = port;
        hdr.ipv4.ttl = hdr.ipv4.ttl - 1;
    }

action rewrite_mac(bit<48> smac) {
        hdr.ethernet.srcAddr = smac;
    }

action drop() {
        mark_to_drop();
    }

table shadow{
           key = {
              hdr.ethernet.dstAddr: lpm;
           }
           actions = {
               set_chaining;
               NoAction;
           }
           size = 1024;
           default_action = NoAction();
        }

table eth_exact{
        key = {
            hdr.ethernet.srcAddr:exact;
        }
        actions={
             simple_forward();
             NoAction;
             drop;
        }
        size = 1024;
        default_action = NoAction();
    }

table eth_exact{
        key = {
            hdr.ethernet.srcAddr:exact;
        }
        actions={
             simple_forward();
             NoAction;
             drop;
        }
        size = 1024;
        default_action = NoAction();
    }

table ecmp_group{
        key = {
            hdr.ipv4.dstAddr: lpm;
        }
        actions = {
            drop;
            set_ecmp_select;
        }
        size = 1024;
    }

table ecmp_nhop{
        key = {
            meta.ecmp_select: exact;
        }
        actions = {
            drop;
            set_nhop;
        }
        size = 2;
    }

table send_frame{
        key = {
            standard_metadata.egress_port: exact;
        }
        actions = {
            rewrite_mac;
            drop;
        }
        size = 256;
    }

}
        apply {
            shadow.apply();

            if(meta.context_control == 1){ 
if(meta.extension_host_id==1) { 

                     {
        if (hdr.ipv4.isValid() && hdr.ipv4.ttl > 0) {
            ecmp_group.apply();
            ecmp_nhop.apply();
        }
    }
                }if(meta.extension_host_id==666){
                     {
        if (hdr.ipv4.isValid() && hdr.ipv4.ttl > 0) {
            ecmp_group.apply();
            ecmp_nhop.apply();
        }
    }
                }
            
            }
        }
        