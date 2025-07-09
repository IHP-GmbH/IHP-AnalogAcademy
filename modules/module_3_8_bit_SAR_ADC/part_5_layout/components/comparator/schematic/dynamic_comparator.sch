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
N 550 -830 610 -830 {
lab=vbias}
N 650 -930 1060 -930 {
lab=vdd}
N 650 -800 650 -770 {
lab=#net2}
N 1060 -470 1060 -450 {
lab=out-}
N 980 -530 1020 -530 {
lab=#net3}
N 980 -470 980 -420 {
lab=#net3}
N 980 -420 1020 -420 {
lab=#net3}
N 1060 -930 1060 -530 {
lab=vdd}
N 810 -540 810 -470 {
lab=#net3}
N 810 -470 980 -470 {
lab=#net3}
N 980 -530 980 -470 {
lab=#net3}
N 720 -270 720 -230 {
lab=#net3}
N 810 -270 900 -270 {
lab=#net3}
N 900 -270 900 -230 {
lab=#net3}
N 810 -470 810 -270 {
lab=#net3}
N 720 -270 810 -270 {
lab=#net3}
N 810 -130 900 -130 {
lab=gnd}
N 900 -170 900 -130 {
lab=gnd}
N 720 -170 720 -130 {
lab=gnd}
N 810 -200 900 -200 {
lab=gnd}
N 400 -270 400 -230 {
lab=#net4}
N 490 -270 580 -270 {
lab=#net4}
N 580 -270 580 -230 {
lab=#net4}
N 400 -270 490 -270 {
lab=#net4}
N 490 -130 580 -130 {
lab=gnd}
N 580 -170 580 -130 {
lab=gnd}
N 400 -170 400 -130 {
lab=gnd}
N 490 -200 580 -200 {
lab=gnd}
N 650 -650 810 -650 {
lab=#net1}
N 650 -710 650 -650 {
lab=#net1}
N 490 -650 650 -650 {
lab=#net1}
N 650 -930 650 -830 {
lab=vdd}
N 650 -740 700 -740 {
lab=vdd}
N 490 -570 810 -570 {
lab=vdd}
N 320 -470 490 -470 {
lab=#net4}
N 490 -470 490 -270 {
lab=#net4}
N 490 -540 490 -470 {
lab=#net4}
N 240 -470 240 -450 {
lab=out+}
N 280 -530 320 -530 {
lab=#net4}
N 320 -470 320 -420 {
lab=#net4}
N 280 -420 320 -420 {
lab=#net4}
N 320 -530 320 -470 {
lab=#net4}
N 240 -930 240 -530 {
lab=vdd}
N 240 -930 650 -930 {
lab=vdd}
N 240 -130 400 -130 {
lab=gnd}
N 580 -130 720 -130 {
lab=gnd}
N 900 -130 1060 -130 {
lab=gnd}
N 490 -470 680 -200 {
lab=#net4}
N 620 -200 810 -470 {
lab=#net3}
N 140 -470 240 -470 {
lab=out+}
N 240 -500 240 -470 {
lab=out+}
N 1060 -470 1160 -470 {
lab=out-}
N 1060 -500 1060 -470 {
lab=out-}
N 330 -200 360 -200 {
lab=clk}
N 440 -570 450 -570 {
lab=v+}
N 850 -570 860 -570 {
lab=v-}
N 360 -740 610 -740 {
lab=clk}
N 360 -740 360 -200 {
lab=clk}
N 1060 -420 1060 -130 {
lab=gnd}
N 810 -200 810 -130 {
lab=gnd}
N 720 -200 810 -200 {
lab=gnd}
N 720 -130 810 -130 {
lab=gnd}
N 490 -200 490 -130 {
lab=gnd}
N 400 -200 490 -200 {
lab=gnd}
N 400 -130 490 -130 {
lab=gnd}
N 240 -420 240 -130 {
lab=gnd}
N 940 -200 960 -200 {
lab=clk}
C {iopin.sym} 1060 -930 0 0 {name=p1 lab=vdd}
C {iopin.sym} 1060 -130 0 0 {name=p2 lab=gnd}
C {ipin.sym} 440 -570 0 0 {name=p3 lab=v+}
C {ipin.sym} 860 -570 0 1 {name=p4 lab=v-}
C {ipin.sym} 550 -830 0 0 {name=p5 lab=vbias}
C {ipin.sym} 330 -200 0 0 {name=p6 lab=clk}
C {opin.sym} 1160 -470 0 0 {name=p7 lab=out-}
C {opin.sym} 140 -470 0 1 {name=p8 lab=out+}
C {lab_pin.sym} 650 -570 3 0 {name=p9 sig_type=std_logic lab=vdd}
C {lab_pin.sym} 700 -740 2 0 {name=p10 sig_type=std_logic lab=vdd}
C {sg13g2_pr/sg13_lv_pmos.sym} 630 -740 0 0 {name=M13
l=0.3u
w=18u
ng=3
m=1
model=sg13_lv_pmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_pmos.sym} 630 -830 0 0 {name=M3
l=0.3u
w=18u
ng=3
m=1
model=sg13_lv_pmos
spiceprefix=X
}
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
C {sg13g2_pr/sg13_lv_pmos.sym} 1040 -530 0 0 {name=M4
l=0.200u
w=8u
ng=1
m=1
model=sg13_lv_pmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_pmos.sym} 260 -530 0 1 {name=M5
l=0.200u
w=8u
ng=1
m=1
model=sg13_lv_pmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_nmos.sym} 260 -420 2 0 {name=M11
l=0.200u
w=4.0u
ng=1
m=1
model=sg13_lv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_nmos.sym} 1040 -420 2 1 {name=M12
l=0.200u
w=4.0u
ng=1
m=1
model=sg13_lv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_nmos.sym} 600 -200 2 0 {name=M6
l=0.200u
w=4.0u
ng=1
m=1
model=sg13_lv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_nmos.sym} 380 -200 2 1 {name=M10
l=0.200u
w=4.0u
ng=1
m=1
model=sg13_lv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_nmos.sym} 920 -200 2 0 {name=M7
l=0.200u
w=4.0u
ng=1
m=1
model=sg13_lv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_nmos.sym} 700 -200 2 1 {name=M8
l=0.200u
w=4.0u
ng=1
m=1
model=sg13_lv_nmos
spiceprefix=X
}
C {lab_pin.sym} 960 -200 2 0 {name=p11 sig_type=std_logic lab=clk}
