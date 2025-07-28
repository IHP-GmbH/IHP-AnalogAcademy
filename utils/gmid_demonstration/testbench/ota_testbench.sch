v {xschem version=3.4.6 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
B 2 650 -935 1450 -535 {flags=graph
y1=25
y2=110
ypos1=0
ypos2=2
divy=5
subdivy=1
unity=1
x1=0

divx=5
subdivx=8
xlabmag=1.0
ylabmag=1.0
node=av
color=4
dataset=-1
unitx=1
logx=1
logy=0
x2=7
hcursor1_y=123.573}
N 775 -265 775 -235 {
lab=vp}
N 1010 -265 1010 -235 {
lab=vdd}
N 1010 -175 1010 -155 {
lab=GND}
N 885 -155 1010 -155 {
lab=GND}
N 190 -450 210 -450 {
lab=vp}
N 555 -340 555 -325 {
lab=GND}
N 330 -110 615 -110 {
lab=vout}
N 210 -110 275 -110 {
lab=vm}
N 210 -50 210 -40 {
lab=GND}
N 885 -155 885 -135 {
lab=GND}
N 775 -155 885 -155 {
lab=GND}
N 775 -175 775 -155 {
lab=GND}
N 615 -400 620 -400 {
lab=vout}
N 615 -400 615 -110 {
lab=vout}
N 510 -400 615 -400 {
lab=vout}
N 270 -230 270 -215 {
lab=GND}
N 330 -330 330 -295 {lab=GND}
N 270 -310 270 -290 {lab=#net1}
N 185 -350 210 -350 {lab=vm}
N 210 -350 210 -110 {lab=vm}
N 330 -500 330 -470 {lab=vdd}
C {vsource.sym} 775 -205 0 0 {name=V1 value="DC 0.6 AC 1 0"
}
C {vsource.sym} 1010 -205 0 0 {name=VDD value="DC 1.2"}
C {gnd.sym} 885 -135 0 0 {name=l1 lab=GND}
C {gnd.sym} 330 -295 0 0 {name=l2 lab=GND}
C {lab_pin.sym} 330 -500 0 0 {name=p1 sig_type=std_logic lab=vdd}
C {lab_pin.sym} 1010 -265 0 0 {name=p2 sig_type=std_logic lab=vdd}
C {lab_pin.sym} 775 -265 0 0 {name=p3 sig_type=std_logic lab=vp}
C {lab_pin.sym} 190 -450 0 0 {name=p5 sig_type=std_logic lab=vp}
C {lab_pin.sym} 185 -350 0 0 {name=p6 sig_type=std_logic lab=vm}
C {isource.sym} 270 -260 0 0 {name=I0 value=150n}
C {gnd.sym} 270 -215 0 0 {name=l3 lab=GND}
C {capa.sym} 555 -370 0 0 {name=Cload
m=1
value=1e-12
footprint=1206
device="ceramic capacitor"}
C {gnd.sym} 555 -325 0 0 {name=l5 lab=GND}
C {iopin.sym} 620 -400 0 0 {name=p7 lab=vout}
C {devices/code_shown.sym} -415 -320 0 0 {name=MODEL only_toplevel=false
format="tcleval( @value )"
value="
.lib cornerMOSlv.lib mos_tt
"}
C {devices/code_shown.sym} -435 -650 0 0 {name=NGSPICE only_toplevel=false 
value="
.control
op
save all
write tb_OTA_op.raw
.endc

.control
op
ac dec 100 1 10e6 
save all
let Av = db(v(vout))
write output_file.raw 
.endc
"}
C {ind.sym} 305 -110 1 0 {name=L6
m=1
value=4G
footprint=1206
device=inductor}
C {capa.sym} 210 -80 0 0 {name=C1
m=1
value=4G
footprint=1206
device="ceramic capacitor"}
C {gnd.sym} 210 -40 0 0 {name=l7 lab=GND}
C {launcher.sym} 420 -635 0 0 {name=h5
descr="load waves" 
tclcommand="xschem raw_read $netlist_dir/output_file.raw ac"
}
C {schematic.sym} 360 -400 0 0 {name=x1}
