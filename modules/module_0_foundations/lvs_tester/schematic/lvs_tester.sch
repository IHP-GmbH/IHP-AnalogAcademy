v {xschem version=3.4.6 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
P 4 1 310 -180 {}
P 4 1 310 -180 {}
N 150 -40 150 -20 {lab=gnd}
N 150 -70 230 -70 {lab=sub}
N 100 -70 110 -70 {lab=G}
N 360 -130 360 -110 {lab=sub}
N 360 -50 360 -30 {lab=gnd}
N 150 -140 150 -100 {lab=D}
C {sg13g2_pr/sg13_lv_nmos.sym} 130 -70 0 0 {name=M3
l=0.45u
w=1.0u
ng=1
m=1
model=sg13_lv_nmos
spiceprefix=X
}
C {lab_pin.sym} 230 -70 0 1 {name=p2 sig_type=std_logic lab=sub}
C {iopin.sym} 100 -70 2 0 {name=p9 lab=G}
C {iopin.sym} 150 -140 0 0 {name=p3 lab=D}
C {lab_pin.sym} 150 -20 0 1 {name=p4 sig_type=std_logic lab=gnd}
C {iopin.sym} 360 -30 0 0 {name=p5 lab=gnd}
C {lab_pin.sym} 360 -130 0 1 {name=p6 sig_type=std_logic lab=sub}
C {sg13g2_pr/ptap1.sym} 360 -80 2 0 {name=R1
model=ptap1
spiceprefix=X
w=0.78e-6
l=0.78e-6
}
