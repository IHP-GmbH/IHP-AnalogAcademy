v {xschem version=3.4.8RC file_version=1.3}
G {}
K {}
V {}
S {}
F {}
E {}
N 1570 -1060 1570 -1030 {lab=VDD}
N 1570 -970 1570 -940 {lab=GND}
N 1270 -1050 1270 -1030 {lab=GND}
N 1230 -1060 1230 -1030 {lab=VDD}
N 1140 -920 1160 -920 {lab=Voplus}
N 1140 -960 1160 -960 {lab=Vominus}
C {code_shown.sym} 440 -1140 0 0 {name=transient_tb only_toplevel=false
value="
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

set wr_singlescale
wrdata /home/pedersen/projects/IHP-AnalogAcademy/modules/module_4_type_2_PLL/LC_Oscillator/runs/RUN_2025-11-18_14-46-39/parameters/ac_params/run_16/LC_Oscillator_tb_16.data vo_diff
quit

.endc
"}
C {vsource.sym} 1570 -1000 0 0 {name=V1 value=1.2 savecurrent=false}
C {gnd.sym} 1570 -940 0 0 {name=l2 lab=GND}
C {lab_pin.sym} 1570 -1060 0 0 {name=p2 sig_type=std_logic lab=VDD}
C {opin.sym} 1140 -920 2 0 {name=p6 lab=Voplus}
C {gnd.sym} 1270 -1050 2 0 {name=l3 lab=GND}
C {opin.sym} 1140 -960 0 1 {name=p9 lab=Vominus}
C {LC_Oscillator.sym} 1250 -940 2 0 {name=x1}
C {devices/code_shown.sym} 450 -640 0 0 {name=SETUP only_toplevel=true
format="tcleval( @value )"
value="
.lib /home/pedersen/IHP-Open-PDK/ihp-sg13g2/libs.tech/ngspice/models/cornerMOSlv.lib mos_ss

.include /home/pedersen/projects/IHP-AnalogAcademy/modules/module_4_type_2_PLL/LC_Oscillator/xschem/simulations/schematic/LC_Oscillator.spice

.temp 27
"
}
C {iopin.sym} 1230 -1060 2 0 {name=p1 lab=VDD}
