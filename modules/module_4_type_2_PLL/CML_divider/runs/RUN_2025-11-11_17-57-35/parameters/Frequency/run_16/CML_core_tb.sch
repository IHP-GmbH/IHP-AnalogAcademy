v {xschem version=3.4.6 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N 740 -940 740 -920 {lab=GND}
N 740 -1090 740 -1060 {lab=VDD}
N 600 -1020 620 -1020 {lab=Vinplus}
N 600 -980 620 -980 {lab=Vinminus}
N 860 -1020 880 -1020 {lab=Voplus}
N 860 -980 880 -980 {lab=Vominus}
N 1150 -850 1150 -820 {lab=VDD}
N 1150 -760 1150 -730 {lab=GND}
N 930 -850 930 -820 {lab=Vinminus}
N 930 -760 930 -730 {lab=GND}
N 720 -850 720 -820 {lab=Vinplus}
N 720 -760 720 -730 {lab=GND}
C {code_shown.sym} 10 -1220 0 0 {name=transient_tb only_toplevel=false
value="
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

* Explicit vectors
let vo_p    = v(Voplus)
let vo_m    = v(Vominus)
let vo_diff = vo_p - vo_m

set wr_singlescale
wrdata /home/pedersen/projects/IHP-AnalogAcademy/modules/module_4_type_2_PLL/CML_divider/runs/RUN_2025-11-11_17-57-35/parameters/Frequency/run_16/CML_core_tb_16.data vo_diff
quit

.endc
"}
C {opin.sym} 880 -1020 2 1 {name=p6 lab=Voplus}
C {opin.sym} 880 -980 0 0 {name=p9 lab=Vominus}
C {devices/code_shown.sym} 10 -620 0 0 {name=SETUP only_toplevel=true
format="tcleval( @value )"
value="
.lib /home/pedersen/IHP-Open-PDK/ihp-sg13g2/libs.tech/ngspice/models/cornerMOSlv.lib mos_ff

.include /home/pedersen/projects/IHP-AnalogAcademy/modules/module_4_type_2_PLL/CML_divider/xschem/simulations/schematic/CML_divider.spice

.temp 80
"
}
C {iopin.sym} 740 -1090 0 1 {name=p2 lab=VDD}
C {ipin.sym} 600 -1020 2 1 {name=p4 lab=Vinplus}
C {ipin.sym} 600 -980 2 1 {name=p1 lab=Vinminus}
C {CML_divider.sym} 740 -1000 0 1 {name=x1}
C {vsource.sym} 1150 -790 0 0 {name=V1 value=1.2 savecurrent=false}
C {gnd.sym} 1150 -730 0 0 {name=l2 lab=GND}
C {lab_pin.sym} 1150 -850 0 0 {name=p5 sig_type=std_logic lab=VDD}
C {gnd.sym} 930 -730 0 0 {name=l1 lab=GND}
C {lab_pin.sym} 930 -850 0 0 {name=p8 sig_type=std_logic lab=Vinminus}
C {vsource.sym} 720 -790 0 0 {name=V3 value="SIN(0.6 0.3 10G 0 0 0)" savecurrent=false}
C {gnd.sym} 720 -730 0 0 {name=l4 lab=GND
value="dc 0 ac 0 SIN(0.6 0.3 12.7k 0 0 0)"}
C {lab_pin.sym} 720 -850 0 0 {name=p10 sig_type=std_logic lab=Vinplus
value="dc 0 ac 0 SIN(0.6 0.3 12.7k 0 0 0)"}
C {vsource.sym} 930 -790 0 0 {name=V2 value="SIN(0.6 0.3 10G 0 0 180)" savecurrent=false}
C {gnd.sym} 740 -920 0 0 {name=l3 lab=GND}
