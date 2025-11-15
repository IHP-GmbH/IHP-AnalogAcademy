v {xschem version=3.4.6 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
B 2 1110 -700 1910 -300 {flags=graph
y1=0.72
y2=1.2
ypos1=0
ypos2=2
divy=5
subdivy=1
unity=1
x1=2.9974739e-10
x2=5.9578291e-10
divx=5
subdivx=1
xlabmag=1.0
ylabmag=1.0
dataset=-1
unitx=1
logx=0
logy=0
color="4 7"
node="vo_m
vo_p"}
B 2 1110 -1120 1910 -720 {flags=graph
y1=0.17956962
y2=0.4801486
ypos1=0
ypos2=2
divy=5
subdivy=1
unity=1
x1=2.9974739e-10
x2=5.9578291e-10
divx=5
subdivx=1
xlabmag=1.0
ylabmag=1.0
dataset=-1
unitx=1
logx=0
logy=0
color="4 7"
node="vinplus
vinminus"
}
B 2 1930 -1120 2730 -720 {flags=graph
y1=-0.41
y2=0.41
ypos1=0
ypos2=2
divy=5
subdivy=1
unity=1
x1=2.9974739e-10
x2=5.9578291e-10
divx=5
subdivx=1
xlabmag=1.0
ylabmag=1.0
dataset=-1
unitx=1
logx=0
logy=0
color=4
node=vo_diff}
N 420 -290 420 -260 {lab=vdd}
N 420 -200 420 -170 {lab=GND}
N 690 -280 690 -260 {lab=GND}
N 690 -430 690 -400 {lab=vdd}
N 810 -360 830 -360 {lab=Vinplus}
N 810 -320 830 -320 {lab=Vinminus}
N 550 -360 570 -360 {lab=Voplus}
N 550 -320 570 -320 {lab=Vominus}
N 210 -300 210 -270 {lab=Vinminus}
N 210 -210 210 -180 {lab=GND}
N 0 -300 0 -270 {lab=Vinplus}
N 0 -210 0 -180 {lab=GND}
C {code_shown.sym} 10 -1150 0 0 {name=transient_tb only_toplevel=false
value="
.include CML_core_tb.save
.param temp=100
.param A = 0.3
.ic V(Voplus)=1.2
.control
set noaskquit
set numdgt=12

* Save & simulate
save all
op
write CML_core_tb.raw
set appendwrite
tran 10p 1n 160p
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

write CML_core_tb.raw
.endc
"}
C {devices/code_shown.sym} 10 -460 0 0 {name=MODEL only_toplevel=true
format="tcleval( @value )"
value=".lib cornerMOSlv.lib mos_ss
"
}
C {devices/launcher.sym} 1190 -250 0 0 {name=h1
descr="OP annotate" 
tclcommand="xschem annotate_op"
}
C {launcher.sym} 1190 -170 0 0 {name=h5
descr="load waves" 
tclcommand="xschem raw_read $netlist_dir/CML_core_tb.raw tran"
}
C {vsource.sym} 420 -230 0 0 {name=V1 value=1.2 savecurrent=false}
C {gnd.sym} 420 -170 0 0 {name=l2 lab=GND}
C {lab_pin.sym} 420 -290 0 0 {name=p2 sig_type=std_logic lab=vdd}
C {opin.sym} 550 -360 2 0 {name=p6 lab=Voplus}
C {gnd.sym} 690 -260 0 0 {name=l3 lab=GND}
C {lab_pin.sym} 690 -430 0 1 {name=p7 sig_type=std_logic lab=vdd}
C {gnd.sym} 210 -180 0 0 {name=l1 lab=GND}
C {lab_pin.sym} 210 -300 0 0 {name=p4 sig_type=std_logic lab=Vinminus}
C {vsource.sym} 0 -240 0 0 {name=V3 value="dc 0 ac 0 SIN(0.6 A 10G 0 0 0)" savecurrent=false}
C {gnd.sym} 0 -180 0 0 {name=l4 lab=GND
value="dc 0 ac 0 SIN(0.6 0.3 12.7k 0 0 0)"}
C {lab_pin.sym} 0 -300 0 0 {name=p8 sig_type=std_logic lab=Vinplus
value="dc 0 ac 0 SIN(0.6 0.3 12.7k 0 0 0)"}
C {launcher.sym} 1190 -210 0 0 {name=h2
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
C {vsource.sym} 210 -240 0 0 {name=V2 value="dc 0 ac 0 SIN(0.6 A 10G 0 0 180)" savecurrent=false}
C {opin.sym} 550 -320 0 1 {name=p9 lab=Vominus}
C {lab_pin.sym} 830 -320 2 0 {name=p1 sig_type=std_logic lab=Vinminus}
C {lab_pin.sym} 830 -360 2 0 {name=p3 sig_type=std_logic lab=Vinplus
value="dc 0 ac 0 SIN(0.6 0.3 12.7k 0 0 0)"}
C {CML_divider.sym} 690 -340 0 0 {name=x1}
