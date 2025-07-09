v {xschem version=3.4.6 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
B 2 710 -550 1510 -150 {flags=graph
y1=-0.0023
y2=1.3
ypos1=0
ypos2=2
divy=5
subdivy=1
unity=1
x1=0
x2=2e-06
divx=5
subdivx=1
xlabmag=1.0
ylabmag=1.0
node=vout
color=4
dataset=-1
unitx=1
logx=0
logy=0
}
N 150 -170 150 -140 {lab=Vin}
N 70 -170 70 -140 {lab=Vdd}
N 70 -80 70 -60 {lab=GND}
N 110 -60 150 -60 {lab=GND}
N 150 -80 150 -60 {lab=GND}
N 110 -60 110 -50 {lab=GND}
N 70 -60 110 -60 {lab=GND}
N 320 -410 320 -380 {lab=Vdd}
N 320 -210 320 -190 {lab=GND}
N 220 -300 240 -300 {lab=Vin}
N 520 -300 540 -300 {lab=Vout}
C {vsource.sym} 150 -110 0 0 {name=V1 value="PULSE(0 1.2 0.5u 10n 10n 1u 2u 1)" savecurrent=false}
C {vsource.sym} 70 -110 0 0 {name=V2 value=1.2 savecurrent=false}
C {gnd.sym} 110 -50 0 0 {name=l2 lab=GND}
C {lab_pin.sym} 150 -170 0 0 {name=p1 sig_type=std_logic lab=Vin}
C {lab_pin.sym} 70 -170 0 0 {name=p3 sig_type=std_logic lab=Vdd}
C {code_shown.sym} 40 -540 0 0 {name=NGSPICE
only_toplevel=true
value="
.control
save all
tran 50n 2u 
write test_inverter.raw
.endc
" }
C {devices/code_shown.sym} 280 -540 0 0 {name=MODEL only_toplevel=true
format="tcleval( @value )"
value="
.lib cornerMOSlv.lib mos_tt
.lib cornerRES.lib res_typ

"}
C {launcher.sym} 770 -120 0 0 {name=h5
descr="load waves" 
tclcommand="xschem raw_read $netlist_dir/test_inverter.raw tran"
}
C {inverter.sym} 390 -300 0 0 {
name=x1
schematic=inverter_pex
spice_sym_def="
.subckt inverter_pex Vdd Vin Vout Gnd
X0 Vout Vin Vdd Vdd sg13_lv_pmos ad=0.68p pd=4.68u as=0.68p ps=4.68u w=2u l=0.45u
X1 Vout Vin Gnd Gnd sg13_lv_nmos ad=0.34p pd=2.68u as=0.34p ps=2.68u w=1u l=0.45u
C0 Vdd Vin 0.14482f
C1 Vout Vdd 0.13155f
C2 Vout Vin 0.10077f
R0 Vin Vin.n0 7.52248
C3 Vout Gnd 0.39245f
C4 Vin Gnd 0.64666f
C5 Vdd Gnd 0.15308f
.ends
"
}
C {lab_pin.sym} 220 -300 0 0 {name=p2 sig_type=std_logic lab=Vin}
C {gnd.sym} 320 -190 0 0 {name=l1 lab=GND}
C {lab_pin.sym} 320 -410 0 0 {name=p4 sig_type=std_logic lab=Vdd}
C {lab_pin.sym} 540 -300 0 1 {name=p5 sig_type=std_logic lab=Vout}
