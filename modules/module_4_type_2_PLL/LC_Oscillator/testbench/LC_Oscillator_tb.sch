v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
B 2 1120 -1110 1920 -710 {flags=graph
y1=1.1
y2=1.3
ypos1=0
ypos2=2
divy=5
subdivy=1
unity=1
x1=1.628e-10
x2=1e-09
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
B 2 1930 -1120 2730 -720 {flags=graph
y1=-0.41
y2=0.41
ypos1=0
ypos2=2
divy=5
subdivy=1
unity=1
x1=1.628e-10
x2=1e-09
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
N 1040 -530 1040 -500 {lab=vdd}
N 1040 -440 1040 -410 {lab=GND}
N 740 -520 740 -500 {lab=GND}
N 700 -530 700 -500 {lab=vdd}
N 610 -390 630 -390 {lab=Voplus}
N 610 -430 630 -430 {lab=Vominus}
C {code_shown.sym} 440 -1140 0 0 {name=transient_tb only_toplevel=false
value="
.include LC_Oscillator_tb.save
.param temp=27
.ic V(Voplus)=1.2
.control
set noaskquit
set numdgt=12

* Save & simulate
save all
op
write LC_Oscillator_tb.raw
set appendwrite
tran 10p 10n 160p
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

write LC_Oscillator_tb.raw
.endc
"}
C {devices/code_shown.sym} 810 -1130 0 0 {name=MODEL only_toplevel=true
format="tcleval( @value )"
value=".lib cornerMOSlv.lib mos_tt
"
}
C {devices/launcher.sym} 1190 -250 0 0 {name=h1
descr="OP annotate" 
tclcommand="xschem annotate_op"
}
C {launcher.sym} 1190 -170 0 0 {name=h5
descr="load waves" 
tclcommand="xschem raw_read $netlist_dir/LC_Oscillator_tb.raw tran"
}
C {vsource.sym} 1040 -470 0 0 {name=V1 value=1.2 savecurrent=false}
C {gnd.sym} 1040 -410 0 0 {name=l2 lab=GND}
C {lab_pin.sym} 1040 -530 0 0 {name=p2 sig_type=std_logic lab=vdd}
C {opin.sym} 610 -390 2 0 {name=p6 lab=Voplus}
C {gnd.sym} 740 -520 2 0 {name=l3 lab=GND}
C {lab_pin.sym} 700 -530 2 1 {name=p7 sig_type=std_logic lab=vdd}
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
C {opin.sym} 610 -430 0 1 {name=p9 lab=Vominus}
C {LC_Oscillator.sym} 720 -410 2 0 {name=x1}
