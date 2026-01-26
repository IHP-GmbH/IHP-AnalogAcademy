v {xschem version=3.4.6 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N 310 -500 310 -440 {lab=#net1}
N 420 -440 530 -440 {lab=#net1}
N 530 -500 530 -440 {lab=#net1}
N 310 -720 310 -690 {lab=vdd}
N 420 -720 530 -720 {lab=vdd}
N 530 -720 530 -690 {lab=vdd}
N 310 -440 420 -440 {lab=#net1}
N 420 -330 420 -290 {lab=gnd}
N 420 -740 420 -720 {lab=vdd}
N 310 -720 420 -720 {lab=vdd}
N 530 -530 580 -530 {lab=gnd}
N 250 -530 310 -530 {lab=gnd}
N 420 -440 420 -390 {lab=#net1}
N 460 -530 490 -530 {lab=Voplus}
N 310 -590 310 -560 {lab=Voplus}
N 350 -530 380 -530 {lab=Vominus}
N 380 -530 530 -630 {lab=Vominus}
N 310 -630 460 -530 {lab=Voplus}
N 530 -690 600 -690 {lab=vdd}
N 530 -630 600 -630 {lab=Vominus}
N 240 -690 310 -690 {lab=vdd}
N 240 -630 310 -630 {lab=Voplus}
N 310 -630 310 -590 {lab=Voplus}
N 530 -590 530 -560 {lab=Vominus}
N 70 -590 70 -580 {lab=Voplus}
N 70 -520 70 -490 {lab=gnd}
N 770 -590 770 -580 {lab=Vominus}
N 770 -520 770 -490 {lab=gnd}
N 140 -590 310 -590 {lab=Voplus}
N 680 -590 770 -590 {lab=Vominus}
N 530 -630 530 -590 {lab=Vominus}
N 680 -590 680 -560 {lab=Vominus}
N 530 -590 680 -590 {lab=Vominus}
N 140 -590 140 -560 {lab=Voplus}
N 70 -590 140 -590 {lab=Voplus}
N 650 -520 650 -460 {lab=Vcont}
N 680 -460 710 -460 {lab=Vcont}
N 710 -520 710 -460 {lab=Vcont}
N 680 -520 680 -460 {lab=Vcont}
N 650 -460 680 -460 {lab=Vcont}
N 110 -520 110 -460 {lab=Vcont}
N 140 -460 170 -460 {lab=Vcont}
N 170 -520 170 -460 {lab=Vcont}
N 140 -520 140 -460 {lab=Vcont}
N 110 -460 140 -460 {lab=Vcont}
N 140 -460 140 -420 {lab=Vcont}
N 140 -420 680 -420 {lab=Vcont}
N 680 -460 680 -420 {lab=Vcont}
N 680 -420 770 -420 {lab=Vcont}
C {sg13g2_pr/sg13_lv_nmos.sym} 330 -530 0 1 {name=M1
l=0.13u
w=16u
ng=4
m=1
model=sg13_lv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_nmos.sym} 510 -530 0 0 {name=M2
l=0.13u
w=16u
ng=4
m=1
model=sg13_lv_nmos
spiceprefix=X
}
C {res.sym} 600 -660 0 0 {name=R2
value=393
footprint=1206
device=resistor
m=1}
C {isource.sym} 420 -360 0 0 {name=I0 value=1m}
C {lab_pin.sym} 420 -290 2 0 {name=p3 sig_type=std_logic lab=gnd
}
C {lab_pin.sym} 420 -740 2 0 {name=p9 sig_type=std_logic lab=vdd
}
C {iopin.sym} 230 -370 2 0 {name=p24 lab=vdd}
C {iopin.sym} 230 -350 2 0 {name=p25 lab=gnd}
C {ind.sym} 530 -660 0 0 {name=L1
m=1
value=1.56n
footprint=1206
device=inductor}
C {lab_pin.sym} 580 -530 2 0 {name=p1 sig_type=std_logic lab=gnd
}
C {lab_pin.sym} 250 -530 0 0 {name=p5 sig_type=std_logic lab=gnd
}
C {res.sym} 240 -660 0 1 {name=R1
value=393
footprint=1206
device=resistor
m=1}
C {ind.sym} 310 -660 0 1 {name=L2
m=1
value=1.56n
footprint=1206
device=inductor}
C {capa.sym} 70 -550 0 0 {name=C1
m=1
value=300f
footprint=1206
device="ceramic capacitor"}
C {lab_pin.sym} 70 -490 0 0 {name=p2 sig_type=std_logic lab=gnd
}
C {capa.sym} 770 -550 0 1 {name=C2
m=1
value=300f
footprint=1206
device="ceramic capacitor"}
C {lab_pin.sym} 770 -490 0 1 {name=p4 sig_type=std_logic lab=gnd
}
C {lab_pin.sym} 770 -590 2 0 {name=p6 sig_type=std_logic lab=Vominus
}
C {lab_pin.sym} 70 -590 0 0 {name=p7 sig_type=std_logic lab=Voplus
}
C {opin.sym} 230 -330 2 0 {name=p8 lab=Voplus}
C {opin.sym} 230 -310 2 0 {name=p10 lab=Vominus}
C {sg13g2_pr/sg13_lv_nmos.sym} 140 -540 3 1 {name=M3
l=1u
w=16u
ng=4
m=1
model=sg13_lv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_nmos.sym} 680 -540 3 1 {name=M4
l=1u
w=16u
ng=4
m=1
model=sg13_lv_nmos
spiceprefix=X
}
C {lab_pin.sym} 770 -420 2 0 {name=p11 sig_type=std_logic lab=Vcont
}
C {ipin.sym} 230 -290 0 0 {name=p12 lab=Vcont}
