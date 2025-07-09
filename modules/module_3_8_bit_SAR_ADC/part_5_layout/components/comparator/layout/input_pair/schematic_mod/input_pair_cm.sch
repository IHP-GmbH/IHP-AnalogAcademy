v {xschem version=3.4.6 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N 490 -650 490 -600 {
lab=#net1}
N 810 -650 810 -600 {
lab=#net1}
N 810 -540 810 -470 {
lab=Drain2}
N 650 -650 810 -650 {
lab=#net1}
N 650 -710 650 -650 {
lab=#net1}
N 490 -650 650 -650 {
lab=#net1}
N 650 -570 810 -570 {
lab=#net2}
N 490 -540 490 -470 {
lab=Drain1}
N 440 -570 450 -570 {
lab=v+}
N 850 -570 860 -570 {
lab=v-}
N 650 -570 650 -550 {lab=#net2}
N 490 -570 650 -570 {
lab=#net2}
N 650 -490 650 -470 {lab=#net3}
C {ipin.sym} 440 -570 0 0 {name=p3 lab=v+}
C {ipin.sym} 860 -570 0 1 {name=p4 lab=v-}
C {sg13g2_pr/sg13_lv_pmos.sym} 470 -570 0 0 {name=M2
l=200n
w=32u
ng=4
m=1
model=sg13_lv_pmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_pmos.sym} 830 -570 0 1 {name=M1
l=200n
w=32u
ng=4
m=1
model=sg13_lv_pmos
spiceprefix=X
}
C {sg13g2_pr/ntap1.sym} 650 -520 0 0 {name=R1
model=ntap1
spiceprefix=X
w=0.78e-6
l=0.78e-6
}
C {iopin.sym} 810 -470 0 0 {name=p7 lab=Drain2}
C {iopin.sym} 490 -470 0 0 {name=p1 lab=Drain1}
C {iopin.sym} 650 -470 0 0 {name=p2 lab=vdd}
C {iopin.sym} 650 -710 0 0 {name=p5 lab=top}
