v {xschem version=3.4.6 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N 330 -280 370 -280 {lab=Vin}
N 330 -280 330 -190 {lab=Vin}
N 330 -190 370 -190 {lab=Vin}
N 410 -230 490 -230 {lab=Vout}
N 410 -230 410 -220 {lab=Vout}
N 410 -250 410 -230 {lab=Vout}
N 410 -160 410 -130 {lab=Gnd}
N 410 -340 410 -310 {lab=Vdd}
N 410 -280 520 -280 {lab=#net1}
N 410 -340 520 -340 {lab=Vdd}
N 410 -190 520 -190 {lab=#net2}
N 410 -130 520 -130 {lab=Gnd}
C {sg13g2_pr/sg13_lv_nmos.sym} 390 -190 2 1 {name=M1
l=0.45u
w=1.0u
ng=1
m=1
model=sg13_lv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_pmos.sym} 390 -280 0 0 {name=M2
l=0.45u
w=2.0u
ng=1
m=1
model=sg13_lv_pmos
spiceprefix=X
}
C {iopin.sym} 490 -230 2 1 {name=p2 lab=Vout}
C {iopin.sym} 410 -340 2 0 {name=p5 lab=Vdd}
C {iopin.sym} 330 -240 2 0 {name=p6 lab=Vin}
C {iopin.sym} 410 -130 2 0 {name=p1 lab=Gnd}
C {sg13g2_pr/ntap1.sym} 520 -310 0 0 {name=R1
model=ntap1
spiceprefix=X
w=0.78e-6
l=0.78e-6
}
C {sg13g2_pr/ptap1.sym} 520 -160 2 1 {name=R2
model=ptap1
spiceprefix=X
w=0.78e-6
l=0.78e-6
}
