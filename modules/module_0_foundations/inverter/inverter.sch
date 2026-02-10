v {xschem version=3.4.6 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N 410 -190 410 -130 {lab=Gnd}
N 410 -340 410 -280 {lab=Vdd}
N 330 -280 370 -280 {lab=Vin}
N 330 -280 330 -190 {lab=Vin}
N 330 -190 370 -190 {lab=Vin}
N 410 -230 490 -230 {lab=Vout}
N 410 -230 410 -220 {lab=Vout}
N 410 -250 410 -230 {lab=Vout}
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
C {iopin.sym} 410 -130 2 1 {name=p1 lab=Gnd}
