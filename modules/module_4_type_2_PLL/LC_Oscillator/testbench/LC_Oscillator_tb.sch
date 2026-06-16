v {xschem version=3.4.6 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
B 2 1120 -1110 1920 -710 {flags=graph
y1=0.96
y2=1.5
ypos1=0
ypos2=2
divy=5
subdivy=1
unity=1
x1=3.9626115e-09
x2=4.2815126e-09
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
y1=-0.47
y2=0.47
ypos1=0
ypos2=2
divy=5
subdivy=1
unity=1
x1=3.9626115e-09
x2=4.2815126e-09
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
N 540 -200 540 -170 {lab=VCC_oscillator}
N 540 -110 540 -80 {lab=GND}
N 460 -390 670 -390 {lab=Vominus}
N 460 -430 670 -430 {lab=Voplus}
N 660 -200 660 -170 {lab=VCC_Buffer}
N 660 -110 660 -80 {lab=GND}
N 860 -310 920 -310 {lab=VCC_oscillator}
N 860 -290 920 -290 {lab=VCC_Buffer}
N 860 -270 920 -270 {lab=VCC_oscillator}
N 860 -250 920 -250 {lab=bias}
N 860 -230 920 -230 {lab=GND}
N 740 -110 740 -80 {lab=GND}
N 740 -200 740 -170 {lab=bias}
N 550 -530 680 -530 {lab=Vo_buff+}
N 550 -510 680 -510 {lab=Vo_buff-}
N 620 -450 660 -450 {lab=GND}
N 620 -590 660 -590 {lab=GND}
N 860 -410 1000 -410 {lab=Vctrl}
N 810 -110 810 -80 {lab=GND}
N 810 -200 810 -170 {lab=Vctrl}
N 640 -320 670 -320 {lab=V_initial_C}
C {code_shown.sym} 50 -1190 0 0 {name=transient_tb only_toplevel=false
value="
.include LC_Oscillator_tb.save
.param temp=27
.ic V(V_initial_C)=2.5
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
C {devices/code_shown.sym} 610 -1140 0 0 {name=MODEL only_toplevel=true
format="tcleval( @value )"
value="
.lib cornerHBT.lib hbt_typ
.lib cornerRES.lib res_typ
.lib $::MODELS_NGSPICE/cornerCAP.lib cap_typ
.lib cornerMOShv.lib mos_tt
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
C {vsource.sym} 540 -140 0 0 {name=V1 value= 2.5 savecurrent=false}
C {gnd.sym} 540 -80 0 0 {name=l2 lab=GND}
C {lab_pin.sym} 540 -200 0 0 {name=p2 sig_type=std_logic lab=VCC_oscillator}
C {opin.sym} 460 -430 2 0 {name=p6 lab=Voplus}
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
C {opin.sym} 460 -390 0 1 {name=p9 lab=Vominus}
C {LC_Oscillator.sym} 760 -410 0 1 {name=x1}
C {vsource.sym} 740 -140 0 0 {name=V2 value= 2.1 savecurrent=false}
C {vsource.sym} 660 -140 0 0 {name=V3 value= 3.3 savecurrent=false}
C {gnd.sym} 660 -80 0 0 {name=l3 lab=GND}
C {lab_pin.sym} 660 -200 0 0 {name=p1 sig_type=std_logic lab=VCC_Buffer}
C {gnd.sym} 740 -80 0 0 {name=l1 lab=GND}
C {lab_pin.sym} 740 -200 0 0 {name=p3 sig_type=std_logic lab=bias}
C {gnd.sym} 920 -230 0 0 {name=l4 lab=GND}
C {lab_pin.sym} 920 -310 0 1 {name=p4 sig_type=std_logic lab=VCC_oscillator}
C {lab_pin.sym} 920 -270 0 1 {name=p5 sig_type=std_logic lab=VCC_oscillator}
C {lab_pin.sym} 920 -290 0 1 {name=p7 sig_type=std_logic lab=VCC_Buffer}
C {lab_pin.sym} 920 -250 0 1 {name=p8 sig_type=std_logic lab=bias}
C {res.sym} 620 -560 2 0 {name=R1
value=50
footprint=1206
device=resistor
m=1}
C {res.sym} 620 -480 0 0 {name=R2
value=50
footprint=1206
device=resistor
m=1}
C {gnd.sym} 660 -450 3 0 {name=l5 lab=GND}
C {gnd.sym} 660 -590 3 1 {name=l6 lab=GND}
C {vsource.sym} 810 -140 0 0 {name=V4 value= 1.65 savecurrent=false}
C {gnd.sym} 810 -80 0 0 {name=l7 lab=GND
value=1.65}
C {lab_pin.sym} 810 -200 0 0 {name=p10 sig_type=std_logic lab=Vctrl}
C {lab_pin.sym} 1000 -410 0 1 {name=p11 sig_type=std_logic lab=Vctrl}
C {opin.sym} 550 -530 2 0 {name=p12 lab=Vo_buff+}
C {opin.sym} 550 -510 2 0 {name=p13 lab=Vo_buff-}
C {lab_pin.sym} 640 -320 0 0 {name=p14 sig_type=std_logic lab=V_initial_C}
