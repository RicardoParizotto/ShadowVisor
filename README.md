# ShadowVisor
ShadowVisor is a compositional hypervisor for programmable data planes

It give programming abstractions to merge modular P4 programs sequentially or in parallel in a totally automatized way.

It also provide abstractions for steering of packets through these modules in runtime. 

The following commands can be used to merge programs:

>#python compositional_calc.py

# program_a > program_b

or

# program_a + program_b


An aditional flow table maps input traffic to the modules and can be reconfigured at runtime.



