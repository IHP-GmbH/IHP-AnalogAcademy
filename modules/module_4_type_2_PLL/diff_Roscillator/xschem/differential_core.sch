v {xschem version=3.4.6 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N 150 -100 150 -50 {lab=#net1}
N 280 -50 410 -50 {lab=#net1}
N 410 -100 410 -50 {lab=#net1}
N 280 -50 280 -20 {lab=#net1}
N 150 -50 280 -50 {lab=#net1}
N 150 -220 150 -160 {lab=Out-}
N 410 -220 410 -160 {lab=Out+}
N 150 -330 150 -290 {lab=vdd}
N 410 -330 410 -290 {lab=vdd}
N 280 -330 410 -330 {lab=vdd}
N 80 -130 110 -130 {lab=In+}
N 450 -130 480 -130 {lab=In-}
N 150 -330 280 -330 {lab=vdd}
N 280 -370 280 -330 {lab=vdd}
N 150 -130 200 -130 {lab=gnd}
N 360 -130 410 -130 {lab=gnd}
N 0 -220 150 -220 {lab=Out-}
N 150 -230 150 -220 {lab=Out-}
N -0 -220 -0 -200 {lab=Out-}
N -30 -220 0 -220 {lab=Out-}
N -0 -140 -0 -120 {lab=gnd}
N 410 -220 560 -220 {lab=Out+}
N 560 -220 560 -200 {lab=Out+}
N 560 -220 590 -220 {lab=Out+}
N 560 -140 560 -120 {lab=gnd}
N 410 -240 410 -220 {lab=Out+}
N 280 40 280 60 {lab=gnd}
C {sg13g2_pr/sg13_lv_nmos.sym} 430 -130 0 1 {name=M1
l=0.26u
w=2.6u
ng=1
m=1
model=sg13_lv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_nmos.sym} 130 -130 0 0 {name=M2
l=0.26u
w=2.6u
ng=1
m=1
model=sg13_lv_nmos
spiceprefix=X
}
C {res.sym} 150 -260 0 0 {name=R1
value=5k
footprint=1206
device=resistor
m=1}
C {res.sym} 410 -260 0 0 {name=R2
value=5k
footprint=1206
device=resistor
m=1}
C {ipin.sym} 80 -130 0 0 {name=p3 lab=In+}
C {iopin.sym} 280 -370 2 0 {name=p5 lab=vdd}
C {iopin.sym} 280 60 2 0 {name=p1 lab=gnd}
C {lab_pin.sym} 360 -130 0 0 {name=p2 sig_type=std_logic lab=gnd}
C {lab_pin.sym} 200 -130 2 0 {name=p6 sig_type=std_logic lab=gnd}
C {capa.sym} 0 -170 0 0 {name=C1
m=1
value=0.5f
footprint=1206
device="ceramic capacitor"}
C {lab_pin.sym} 0 -120 0 0 {name=p7 sig_type=std_logic lab=gnd}
C {ipin.sym} 480 -130 0 1 {name=p8 lab=In-}
C {capa.sym} 560 -170 0 1 {name=C2
m=1
value=0.5f
footprint=1206
device="ceramic capacitor"}
C {lab_pin.sym} 560 -120 0 1 {name=p9 sig_type=std_logic lab=gnd}
C {opin.sym} 590 -220 0 0 {name=p10 lab=Out+}
C {opin.sym} -30 -220 0 1 {name=p11 lab=Out-}
C {isource.sym} 280 10 0 0 {name=I0 value=200u}
C {sg13g2_pr/annotate_fet_params.sym} 700 -230 0 0 {name=annot1 ref=M1}
C {sg13g2_pr/annotate_fet_params.sym} 810 -230 0 0 {name=annot2 ref=M2}
