v {xschem version=3.4.6 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
B 2 1250 -560 2050 -160 {flags=graph
y1=-0.59
y2=1.3
ypos1=0
ypos2=2
divy=5
subdivy=1
unity=1
x1=0
x2=2e-09
divx=5
subdivx=1
xlabmag=1.0
ylabmag=1.0
dataset=-1
unitx=1
logx=0
logy=0
color="4 7 12"
node="voplus
vominus
vo_diff"}
N 650 -240 700 -240 {lab=#net1}
N 650 -160 700 -160 {lab=#net2}
N 850 -240 900 -240 {lab=#net3}
N 850 -160 900 -160 {lab=#net4}
N 550 -290 550 -270 {lab=vdd}
N 750 -290 950 -290 {lab=vdd}
N 950 -290 950 -270 {lab=vdd}
N 750 -290 750 -270 {lab=vdd}
N 550 -290 750 -290 {lab=vdd}
N 550 -130 550 -110 {lab=GND}
N 550 -110 750 -110 {lab=GND}
N 750 -130 750 -110 {lab=GND}
N 750 -110 950 -110 {lab=GND}
N 950 -130 950 -110 {lab=GND}
N 480 -240 500 -240 {lab=Voplus}
N 480 -330 1070 -330 {lab=Voplus}
N 1050 -240 1070 -240 {lab=Voplus}
N 480 -330 480 -240 {lab=Voplus}
N 1070 -330 1070 -240 {lab=Voplus}
N 1070 -160 1070 -70 {lab=Vominus}
N 1050 -160 1070 -160 {lab=Vominus}
N 480 -160 500 -160 {lab=Vominus}
N 480 -160 480 -70 {lab=Vominus}
N 400 -130 400 -90 {lab=GND}
N 480 -70 1070 -70 {lab=Vominus}
N 400 -230 400 -190 {lab=vdd}
C {differential_core.sym} 650 -200 0 0 {name=x1}
C {differential_core.sym} 850 -200 0 0 {name=x2}
C {differential_core.sym} 1050 -200 0 0 {name=x3}
C {lab_pin.sym} 950 -290 2 0 {name=p1 sig_type=std_logic lab=vdd}
C {vsource.sym} 400 -160 0 0 {name=V1 value=1.2 savecurrent=false}
C {gnd.sym} 950 -110 0 0 {name=l1 lab=GND}
C {gnd.sym} 400 -90 0 0 {name=l2 lab=GND}
C {lab_pin.sym} 400 -230 2 0 {name=p2 sig_type=std_logic lab=vdd}
C {opin.sym} 1070 -330 0 0 {name=p3 lab=Voplus}
C {opin.sym} 1070 -70 2 1 {name=p4 lab=Vominus}
C {code_shown.sym} 0 -450 0 0 {name=transient_tb only_toplevel=false
value="
.include diff_oscillator_tb.save
.param temp=27
.ic V(Voplus)=1.2
.control
save all 
op
write diff_oscillator_tb.raw
set appendwrite
tran 10p 2n
save all
let vo_diff = v(Voplus) - v(Vominus)
write diff_oscillator_tb.raw

.endc
"}
C {devices/code_shown.sym} 0 -110 0 0 {name=MODEL only_toplevel=true
format="tcleval( @value )"
value=".lib cornerMOSlv.lib mos_tt
"}
C {launcher.sym} 1310 -70 0 0 {name=h3
descr=SimulateNGSPICE
tclcommand="
# Setup the default simulation commands if not already set up
# for example by already launched simulations.
set_sim_defaults
puts $sim(spice,1,cmd) 

# Change the Xyce command. In the spice category there are currently
# 5 commands (0, 1, 2, 3, 4). Command 3 is the Xyce batch
# you can get the number by querying $sim(spice,n)
set sim(spice,1,cmd) \{ngspice  \\"$N\\" -a\}

# change the simulator to be used (Xyce)
set sim(spice,default) 0

# Create FET and BIP .save file
mkdir -p $netlist_dir
write_data [save_params] $netlist_dir/[file rootname [file tail [xschem get current_name]]].save

# run netlist and simulation
xschem netlist
simulate
"}
C {devices/launcher.sym} 1310 -110 0 0 {name=h1
descr="OP annotate" 
tclcommand="xschem annotate_op"
}
C {launcher.sym} 1310 -30 0 0 {name=h5
descr="load waves" 
tclcommand="xschem raw_read $netlist_dir/diff_oscillator_tb.raw tran"
}
