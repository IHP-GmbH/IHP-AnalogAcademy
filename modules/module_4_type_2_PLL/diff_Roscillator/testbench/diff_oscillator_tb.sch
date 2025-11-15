v {xschem version=3.4.6 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
B 2 1060 -700 1860 -300 {flags=graph
y1=-0.023
y2=0.7
ypos1=0
ypos2=2
divy=5
subdivy=1
unity=1
x1=2.2231151e-07
x2=2.2291988e-07
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
N 350 -300 350 -270 {lab=vdd}
N 350 -210 350 -180 {lab=GND}
N 600 -290 600 -270 {lab=GND}
N 640 -290 640 -270 {lab=vdd}
N 710 -400 740 -400 {lab=Voplus}
N 710 -360 740 -360 {lab=Vominus}
C {opin.sym} 740 -400 0 0 {name=p3 lab=Voplus}
C {opin.sym} 740 -360 2 1 {name=p4 lab=Vominus}
C {code_shown.sym} 10 -1120 0 0 {name=transient_tb only_toplevel=false
value="
.include diff_oscillator_tb.save
.param temp=27
.ic V(Voplus)=1.2
.control
set noaskquit
set numdgt=12

* Save & simulate
save all
op
write diff_oscillator_tb.raw
set appendwrite
tran 10p 1u 160p
save all

* Explicit vectors
let vo_p    = v(Voplus)
let vo_m    = v(Vominus)
let vo_diff = vo_p - vo_m

* --- Main output (mimic CACE naming, just to compare) ---
set wr_singlescale
wrdata differential_output.txt vo_diff

* --- Extra debug (like we did for CACE) ---
set wr_vecnames
wrdata manual_debug.dat time vo_p vo_m vo_diff
unset wr_vecnames

write diff_oscillator_tb.raw
.endc
"}
C {devices/code_shown.sym} 10 -460 0 0 {name=MODEL only_toplevel=true
format="tcleval( @value )"
value=".lib cornerMOSlv.lib mos_tt
"
}
C {launcher.sym} 1120 -240 0 0 {name=h3
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
C {devices/launcher.sym} 1120 -280 0 0 {name=h1
descr="OP annotate" 
tclcommand="xschem annotate_op"
}
C {launcher.sym} 1120 -190 0 0 {name=h5
descr="load waves" 
tclcommand="xschem raw_read $netlist_dir/diff_oscillator_tb.raw tran"
}
C {vsource.sym} 350 -240 0 0 {name=V1 value=1.2 savecurrent=false}
C {gnd.sym} 350 -180 0 0 {name=l2 lab=GND}
C {lab_pin.sym} 350 -300 0 0 {name=p2 sig_type=std_logic lab=vdd}
C {diff_ring_oscillator.sym} 620 -380 0 0 {name=x1}
C {gnd.sym} 600 -270 0 0 {name=l1 lab=GND}
C {lab_pin.sym} 640 -270 0 1 {name=p1 sig_type=std_logic lab=vdd}
