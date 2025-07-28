v {xschem version=3.4.6 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
B 2 685 -880 1485 -480 {flags=graph


ypos1=0
ypos2=2
divy=5
subdivy=4
unity=1
x1=0

divx=5
subdivx=8
xlabmag=1.0
ylabmag=1.0


dataset=-1
unitx=1
logx=1
logy=0
autoload=0







sim_type=ac

y2=0.029
y1=-160
color=4
node=ph(vout)
x2=7}
B 2 680 -1295 1480 -895 {flags=graph
y1=-23
y2=32
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
dataset=-1
unitx=1
logx=1
logy=0
x2=7
color=4
node="vout / db20()"
}
N 775 -265 775 -235 {
lab=vp}
N 1010 -265 1010 -235 {
lab=vdd}
N 1010 -175 1010 -155 {
lab=GND}
N 885 -155 1010 -155 {
lab=GND}
N 345 -345 345 -325 {
lab=GND}
N 345 -490 345 -475 {
lab=vdd}
N 190 -450 210 -450 {
lab=vp}
N 190 -365 210 -365 {
lab=vm}
N 530 -350 530 -335 {
lab=GND}
N 330 -110 590 -110 {
lab=vout}
N 210 -110 275 -110 {
lab=vm}
N 210 -365 210 -110 {
lab=vm}
N 210 -50 210 -40 {
lab=GND}
N 885 -155 885 -135 {
lab=GND}
N 775 -155 885 -155 {
lab=GND}
N 775 -175 775 -155 {
lab=GND}
N 590 -410 620 -410 {
lab=vout}
N 590 -410 590 -110 {
lab=vout}
N 510 -410 590 -410 {
lab=vout}
N 270 -325 270 -290 {
lab=#net1}
N 270 -230 270 -215 {
lab=GND}
C {vsource.sym} 775 -205 0 0 {name=V1 value="DC 0.6 AC 1 0"
}
C {vsource.sym} 1010 -205 0 0 {name=VDD value="DC 1.2"}
C {gnd.sym} 885 -135 0 0 {name=l1 lab=GND}
C {gnd.sym} 345 -325 0 0 {name=l2 lab=GND}
C {lab_pin.sym} 345 -490 0 0 {name=p1 sig_type=std_logic lab=vdd}
C {lab_pin.sym} 1010 -265 0 0 {name=p2 sig_type=std_logic lab=vdd}
C {lab_pin.sym} 775 -265 0 0 {name=p3 sig_type=std_logic lab=vp}
C {lab_pin.sym} 190 -450 0 0 {name=p5 sig_type=std_logic lab=vp}
C {lab_pin.sym} 190 -365 0 0 {name=p6 sig_type=std_logic lab=vm}
C {isource.sym} 270 -260 0 0 {name=I0 value=2u}
C {gnd.sym} 270 -215 0 0 {name=l3 lab=GND}
C {capa.sym} 530 -380 0 0 {name=Cload
m=1
value=500f
footprint=1206
device="ceramic capacitor"}
C {gnd.sym} 530 -335 0 0 {name=l5 lab=GND}
C {iopin.sym} 620 -410 0 0 {name=p7 lab=vout}
C {devices/code_shown.sym} -415 -290 0 0 {name=MODEL only_toplevel=false
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
C {two_stage_OTA.sym} 360 -410 0 0 {name=x1}
