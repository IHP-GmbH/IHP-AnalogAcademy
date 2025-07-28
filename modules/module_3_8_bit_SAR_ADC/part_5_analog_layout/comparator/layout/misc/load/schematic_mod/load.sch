v {xschem version=3.4.6 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N 720 -270 720 -230 {
lab=Drain2}
N 810 -270 900 -270 {
lab=Drain2}
N 900 -270 900 -230 {
lab=Drain2}
N 810 -470 810 -270 {
lab=Drain2}
N 720 -270 810 -270 {
lab=Drain2}
N 900 -170 900 -130 {
lab=gnd}
N 720 -170 720 -130 {
lab=gnd}
N 400 -270 400 -230 {
lab=Drain1}
N 490 -270 580 -270 {
lab=Drain1}
N 580 -270 580 -230 {
lab=Drain1}
N 400 -270 490 -270 {
lab=Drain1}
N 580 -170 580 -130 {
lab=gnd}
N 400 -170 400 -130 {
lab=gnd}
N 490 -470 490 -270 {
lab=Drain1}
N 580 -130 720 -130 {
lab=gnd}
N 900 -130 1060 -130 {
lab=gnd}
N 490 -470 680 -200 {
lab=Drain1}
N 620 -200 810 -470 {
lab=Drain2}
N 330 -200 360 -200 {
lab=clk}
N 810 -200 900 -200 {
lab=well}
N 720 -130 900 -130 {
lab=gnd}
N 490 -200 580 -200 {
lab=well}
N 400 -130 580 -130 {
lab=gnd}
N 940 -200 960 -200 {
lab=clk}
N 490 -200 490 -110 {lab=well}
N 650 -110 810 -110 {lab=well}
N 810 -200 810 -110 {lab=well}
N 720 -200 810 -200 {
lab=well}
N 650 -30 650 -10 {lab=gnd}
N 650 -110 650 -90 {lab=well}
N 490 -110 650 -110 {lab=well}
N 390 -200 490 -200 {lab=well}
N 1190 -400 1190 -370 {lab=gnd}
N 1190 -400 1230 -400 {lab=gnd}
N 1230 -400 1230 -280 {lab=gnd}
N 1190 -280 1230 -280 {lab=gnd}
N 1190 -310 1190 -280 {lab=gnd}
N 1140 -340 1190 -340 {lab=well}
C {iopin.sym} 1060 -130 0 0 {name=p2 lab=gnd}
C {ipin.sym} 330 -200 0 0 {name=p6 lab=clk}
C {sg13g2_pr/sg13_lv_nmos.sym} 600 -200 0 1 {name=M6
l=0.200u
w=4.0u
ng=1
m=1
model=sg13_lv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_nmos.sym} 380 -200 0 0 {name=M10
l=0.200u
w=4.0u
ng=1
m=1
model=sg13_lv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_nmos.sym} 920 -200 0 1 {name=M7
l=0.200u
w=4.0u
ng=1
m=1
model=sg13_lv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_nmos.sym} 700 -200 0 0 {name=M8
l=0.200u
w=4.0u
ng=1
m=1
model=sg13_lv_nmos
spiceprefix=X
}
C {lab_pin.sym} 960 -200 2 0 {name=p11 sig_type=std_logic lab=clk}
C {iopin.sym} 490 -470 2 0 {name=p1 lab=Drain1}
C {iopin.sym} 810 -470 0 0 {name=p7 lab=Drain2}
C {sg13g2_pr/ptap1.sym} 650 -60 2 0 {name=R2
model=ptap1
spiceprefix=X
w=0.78e-6
l=0.78e-6
}
C {lab_pin.sym} 650 -10 2 0 {name=p3 sig_type=std_logic lab=gnd}
C {lab_pin.sym} 810 -110 2 0 {name=p4 sig_type=std_logic lab=well}
C {sg13g2_pr/sg13_lv_nmos.sym} 1210 -340 0 1 {name=M2
l=0.200u
w=4.0u
ng=1
m=4
model=sg13_lv_nmos
spiceprefix=X
}
C {lab_pin.sym} 1140 -340 0 0 {name=p8 sig_type=std_logic lab=well
m=4}
C {lab_pin.sym} 1190 -400 0 0 {name=p10 sig_type=std_logic lab=gnd
m=4}
