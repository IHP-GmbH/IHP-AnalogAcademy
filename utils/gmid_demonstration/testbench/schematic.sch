v {xschem version=3.4.6 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N 740 -620 740 -580 {lab=#net1}
N 850 -620 960 -620 {lab=#net1}
N 960 -620 960 -580 {lab=#net1}
N 740 -480 740 -450 {lab=#net2}
N 960 -490 960 -450 {lab=vout}
N 850 -420 920 -420 {lab=#net2}
N 740 -480 850 -480 {lab=#net2}
N 740 -520 740 -480 {lab=#net2}
N 850 -480 850 -420 {lab=#net2}
N 780 -420 850 -420 {lab=#net2}
N 850 -350 960 -350 {lab=vss}
N 850 -650 850 -620 {lab=#net1}
N 740 -620 850 -620 {lab=#net1}
N 850 -750 850 -680 {lab=vdd}
N 590 -750 590 -680 {lab=vdd}
N 590 -750 850 -750 {lab=vdd}
N 630 -680 700 -680 {lab=iout}
N 700 -680 700 -630 {lab=iout}
N 590 -630 700 -630 {lab=iout}
N 590 -650 590 -630 {lab=iout}
N 590 -630 590 -610 {lab=iout}
N 740 -550 960 -550 {lab=vdd}
N 960 -420 960 -350 {lab=vss}
N 740 -420 740 -350 {lab=vss}
N 850 -350 850 -330 {lab=vss}
N 740 -350 850 -350 {lab=vss}
N 960 -490 1050 -490 {lab=vout}
N 960 -520 960 -490 {lab=vout}
N 1000 -550 1040 -550 {lab=V+}
N 660 -550 700 -550 {lab=V-}
N 700 -680 810 -680 {lab=iout}
C {sg13g2_pr/sg13_lv_pmos.sym} 720 -550 0 0 {name=M1
l=5.20u
w=1.25u
ng=1
m=1
model=sg13_lv_pmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_nmos.sym} 760 -420 0 1 {name=M2
l=9.88u
w=0.68u
ng=1
m=1
model=sg13_lv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_pmos.sym} 980 -550 0 1 {name=M3
l=5.20u
w=1.25u
ng=1
m=1
model=sg13_lv_pmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_nmos.sym} 940 -420 0 0 {name=M4
l=9.88u
w=0.68u
ng=1
m=1
model=sg13_lv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_pmos.sym} 830 -680 0 0 {name=M5
l=0.13u
w=2u
ng=1
m=1
model=sg13_lv_pmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_pmos.sym} 610 -680 0 1 {name=M7
l=0.13u
w=2u
ng=1
m=1
model=sg13_lv_pmos
spiceprefix=X
}
C {lab_pin.sym} 850 -550 3 1 {name=p1 sig_type=std_logic lab=vdd}
C {iopin.sym} 850 -750 0 0 {name=p8 lab=vdd}
C {iopin.sym} 590 -610 0 0 {name=p3 lab=iout}
C {iopin.sym} 1050 -490 0 0 {name=p5 lab=vout}
C {iopin.sym} 850 -330 0 0 {name=p4 lab=vss}
C {iopin.sym} 1040 -550 0 0 {name=p2 lab=V+}
C {iopin.sym} 660 -550 0 1 {name=p6 lab=V-}
