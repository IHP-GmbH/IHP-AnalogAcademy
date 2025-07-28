v {xschem version=3.4.6 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N 450 -435 450 -395 {
lab=#net1}
N 450 -435 560 -435 {
lab=#net1}
N 560 -365 620 -365 {
lab=#net1}
N 560 -435 560 -365 {
lab=#net1}
N 490 -365 560 -365 {
lab=#net1}
N 450 -495 450 -435 {
lab=#net1}
N 450 -525 660 -525 {
lab=vdd}
N 450 -575 450 -555 {
lab=#net2}
N 660 -575 660 -555 {
lab=#net2}
N 560 -575 660 -575 {
lab=#net2}
N 380 -525 410 -525 {
lab=v+}
N 700 -525 730 -525 {
lab=v-}
N 390 -625 520 -625 {
lab=iout}
N 170 -575 170 -555 {
lab=iout}
N 170 -575 220 -575 {
lab=iout}
N 220 -625 240 -625 {
lab=iout}
N 170 -595 170 -575 {
lab=iout}
N 220 -625 220 -575 {
lab=iout}
N 210 -625 220 -625 {
lab=iout}
N 660 -400 660 -395 {
lab=vout}
N 560 -595 560 -575 {
lab=#net2}
N 450 -575 560 -575 {
lab=#net2}
N 660 -495 660 -400 {
lab=vout}
N 660 -400 800 -400 {
lab=vout}
N 450 -305 660 -305 {
lab=vss}
N 170 -675 170 -625 {
lab=vdd}
N 560 -675 560 -625 {
lab=vdd}
N 170 -675 560 -675 {
lab=vdd}
N 450 -365 450 -305 {
lab=vss}
N 660 -365 660 -305 {
lab=vss}
C {sg13g2_pr/sg13_lv_nmos.sym} 640 -365 0 0 {name=M4
l=6.24u
w=3.09u
ng=1
m=1
model=sg13_lv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_nmos.sym} 470 -365 0 1 {name=M3
l=6.24u
w=3.09u
ng=1
m=1
model=sg13_lv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_pmos.sym} 430 -525 0 0 {name=M1
l=5.46u
w=2.75u
ng=1
m=1
model=sg13_lv_pmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_pmos.sym} 540 -625 0 0 {name=M5
l=9.98u
w=66u
ng=10
m=1
model=sg13_lv_pmos
spiceprefix=X
}
C {iopin.sym} 730 -525 0 0 {name=p10 lab=v-}
C {iopin.sym} 380 -525 0 1 {name=p11 lab=v+}
C {iopin.sym} 560 -305 1 1 {name=p5 lab=vss}
C {iopin.sym} 560 -675 1 1 {name=p1 lab=vdd}
C {iopin.sym} 170 -555 0 1 {name=p3 lab=iout}
C {iopin.sym} 800 -400 0 0 {name=p8 lab=vout}
C {lab_pin.sym} 240 -625 0 1 {name=p7 sig_type=std_logic lab=iout}
C {lab_pin.sym} 390 -625 0 0 {name=p4 sig_type=std_logic lab=iout}
C {lab_pin.sym} 555 -525 3 0 {name=p2 sig_type=std_logic lab=vdd}
C {sg13g2_pr/sg13_lv_pmos.sym} 190 -625 0 1 {name=M6
l=9.98u
w=66u
ng=10
m=1
model=sg13_lv_pmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_pmos.sym} 680 -525 0 1 {name=M2
l=5.46u
w=2.75u
ng=1
m=1
model=sg13_lv_pmos
spiceprefix=X
}
