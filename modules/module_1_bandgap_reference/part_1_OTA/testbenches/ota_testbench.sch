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

y2=-0.042
y1=-160
color=4
node=ph(vout)
x2=7}
B 2 680 -1295 1480 -895 {flags=graph
y1=-8.7
y2=71
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
sim_type=ac
color=4
node="vout db20()"}
B 2 1535 -1295 2335 -895 {flags=graph
y1=21
y2=67
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
node=cmrr}
B 2 1525 -875 2325 -475 {flags=graph
y1=-21
y2=30
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
node="psrr_linear db20()"}
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
N 1290 -190 1290 -170 {
lab=GND}
N 1290 -335 1290 -320 {
lab=vdd}
N 1135 -295 1155 -295 {
lab=vp}
N 1135 -210 1155 -210 {
lab=vp}
N 1475 -195 1475 -180 {
lab=GND}
N 1455 -255 1565 -255 {
lab=vout1}
N 1215 -170 1215 -135 {
lab=#net2}
N 1215 -75 1215 -60 {
lab=GND}
N 1135 -295 1135 -210 {
lab=vp}
N 335 305 335 325 {
lab=GND}
N 180 285 200 285 {
lab=vm}
N 320 540 580 540 {
lab=vout2}
N 200 540 265 540 {
lab=vm}
N 200 285 200 540 {
lab=vm}
N 200 600 200 610 {
lab=GND}
N 580 240 610 240 {
lab=vout2}
N 580 240 580 540 {
lab=vout2}
N 500 240 580 240 {
lab=vout2}
N 260 325 260 360 {
lab=#net3}
N 260 420 260 435 {
lab=GND}
N 335 65 470 65 {
lab=VDDac}
N 335 65 335 175 {
lab=VDDac}
N 470 130 470 150 {
lab=GND}
N 470 65 470 70 {
lab=VDDac}
N 95 200 200 200 {
lab=#net4}
N 95 260 95 280 {
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
C {isource.sym} 270 -260 0 0 {name=I0 value=80u}
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
.lib $::SG13G2_MODELS/cornerCAP.lib cap_typ
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
let PSRR_linear = v(vout2)/v(VDDac)
let CMRR = db((v(vout)/v(vp))/(v(vout1)/v(vp)))
let phase = 180*cph(vout)/pi
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
C {gnd.sym} 1290 -170 0 0 {name=l8 lab=GND}
C {lab_pin.sym} 1290 -335 0 0 {name=p4 sig_type=std_logic lab=vdd}
C {lab_pin.sym} 1135 -295 0 0 {name=p10 sig_type=std_logic lab=vp}
C {isource.sym} 1215 -105 0 0 {name=I1 value=80u}
C {gnd.sym} 1215 -60 0 0 {name=l9 lab=GND}
C {capa.sym} 1475 -225 0 0 {name=Cload1
m=1
value=500f
footprint=1206
device="ceramic capacitor"}
C {gnd.sym} 1475 -180 0 0 {name=l10 lab=GND}
C {iopin.sym} 1565 -255 0 0 {name=p12 lab=vout1}
C {gnd.sym} 335 325 0 0 {name=l4 lab=GND}
C {lab_pin.sym} 180 285 0 0 {name=p11 sig_type=std_logic lab=vm}
C {isource.sym} 260 390 0 0 {name=I2 value=80u}
C {gnd.sym} 260 435 0 0 {name=l11 lab=GND}
C {iopin.sym} 610 240 0 0 {name=p13 lab=vout2}
C {ind.sym} 295 540 1 0 {name=L13
m=1
value=4G
footprint=1206
device=inductor}
C {capa.sym} 200 570 0 0 {name=C2
m=1
value=4G
footprint=1206
device="ceramic capacitor"}
C {gnd.sym} 200 610 0 0 {name=l14 lab=GND}
C {vsource.sym} 470 100 0 0 {name=V2 value="DC 1.2 AC 1 0"
}
C {gnd.sym} 470 150 0 0 {name=l15 lab=GND}
C {lab_pin.sym} 335 65 0 0 {name=p8 sig_type=std_logic lab=VDDac}
C {vsource.sym} 95 230 0 0 {name=V4 value="DC 0.6"
}
C {gnd.sym} 95 280 0 0 {name=l12 lab=GND}
C {two_stage_OTA.sym} 360 -410 0 0 {name=x1}
C {two_stage_OTA.sym} 350 240 0 0 {name=x2}
C {two_stage_OTA.sym} 1305 -255 0 0 {name=x3}
