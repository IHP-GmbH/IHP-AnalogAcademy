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
N 1060 -470 1060 -450 {
lab=out-}
N 980 -530 1020 -530 {
lab=#net2}
N 980 -470 980 -420 {
lab=#net2}
N 980 -420 1020 -420 {
lab=#net2}
N 810 -540 810 -470 {
lab=#net2}
N 810 -470 980 -470 {
lab=#net2}
N 980 -530 980 -470 {
lab=#net2}
N 720 -270 720 -230 {
lab=#net2}
N 810 -270 900 -270 {
lab=#net2}
N 900 -270 900 -230 {
lab=#net2}
N 810 -470 810 -270 {
lab=#net2}
N 720 -270 810 -270 {
lab=#net2}
N 900 -170 900 -130 {
lab=gnd}
N 720 -170 720 -130 {
lab=gnd}
N 400 -270 400 -230 {
lab=#net3}
N 490 -270 580 -270 {
lab=#net3}
N 580 -270 580 -230 {
lab=#net3}
N 400 -270 490 -270 {
lab=#net3}
N 580 -170 580 -130 {
lab=gnd}
N 400 -170 400 -130 {
lab=gnd}
N 650 -650 810 -650 {
lab=#net1}
N 650 -710 650 -650 {
lab=#net1}
N 490 -650 650 -650 {
lab=#net1}
N 320 -470 490 -470 {
lab=#net3}
N 490 -470 490 -270 {
lab=#net3}
N 490 -540 490 -470 {
lab=#net3}
N 240 -470 240 -450 {
lab=out+}
N 280 -530 320 -530 {
lab=#net3}
N 320 -470 320 -420 {
lab=#net3}
N 280 -420 320 -420 {
lab=#net3}
N 320 -530 320 -470 {
lab=#net3}
N 650 -930 1060 -930 {
lab=vdd}
N 240 -130 400 -130 {
lab=gnd}
N 580 -130 720 -130 {
lab=gnd}
N 900 -130 1060 -130 {
lab=gnd}
N 490 -470 680 -200 {
lab=#net3}
N 620 -200 810 -470 {
lab=#net2}
N 140 -470 240 -470 {
lab=out+}
N 240 -500 240 -470 {
lab=out+}
N 1060 -470 1160 -470 {
lab=out-}
N 1060 -500 1060 -470 {
lab=out-}
N 340 -200 360 -200 {
lab=clk}
N 440 -570 450 -570 {
lab=v+}
N 850 -570 860 -570 {
lab=v-}
N 720 -130 900 -130 {
lab=gnd}
N 400 -130 580 -130 {
lab=gnd}
N 940 -200 960 -200 {
lab=clk}
N 1500 -340 1500 -320 {lab=well}
N 1500 -260 1500 -240 {lab=vdd}
N 490 -570 810 -570 {
lab=well}
N 1240 -360 1240 -330 {lab=gnd}
N 1240 -360 1280 -360 {lab=gnd}
N 1280 -360 1280 -240 {lab=gnd}
N 1240 -240 1280 -240 {lab=gnd}
N 1240 -270 1240 -240 {lab=gnd}
N 1190 -300 1240 -300 {lab=sub}
N 1370 -270 1370 -250 {lab=gnd}
N 400 -200 580 -200 {
lab=sub}
N 720 -200 900 -200 {
lab=sub}
N 240 -390 240 -130 {lab=gnd}
N 1370 -340 1370 -330 {lab=sub}
N 1060 -420 1110 -420 {lab=sub}
N 190 -420 240 -420 {lab=sub}
N 1060 -390 1060 -130 {lab=gnd}
N 1060 -930 1060 -560 {lab=vdd}
N 240 -930 240 -560 {lab=vdd}
N 1060 -530 1110 -530 {lab=well}
N 190 -530 240 -530 {lab=well}
N 650 -810 650 -770 {lab=#net4}
N 650 -930 650 -870 {lab=vdd}
N 240 -930 650 -930 {
lab=vdd}
N 340 -740 340 -200 {lab=clk}
N 330 -200 340 -200 {
lab=clk}
N 340 -740 610 -740 {lab=clk}
N 580 -840 610 -840 {lab=vbias}
N 650 -740 710 -740 {lab=well}
N 650 -840 710 -840 {lab=well}
N 710 -840 710 -740 {lab=well}
C {iopin.sym} 1060 -930 0 0 {name=p1 lab=vdd}
C {iopin.sym} 1060 -130 0 0 {name=p2 lab=gnd}
C {ipin.sym} 440 -570 0 0 {name=p3 lab=v+}
C {ipin.sym} 860 -570 0 1 {name=p4 lab=v-}
C {ipin.sym} 330 -200 0 0 {name=p6 lab=clk}
C {opin.sym} 1160 -470 0 0 {name=p7 lab=out-}
C {opin.sym} 140 -470 0 1 {name=p8 lab=out+}
C {sg13g2_pr/sg13_lv_pmos.sym} 470 -570 0 0 {name=M2
l=200n
w=8u
ng=2
m=4
model=sg13_lv_pmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_pmos.sym} 830 -570 0 1 {name=M1
l=200n
w=8u
ng=2
m=4
model=sg13_lv_pmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_pmos.sym} 1040 -530 0 0 {name=M4
l=0.200u
w=8u
ng=2
m=1
model=sg13_lv_pmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_pmos.sym} 260 -530 0 1 {name=M5
l=0.200u
w=8u
ng=2
m=1
model=sg13_lv_pmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_nmos.sym} 260 -420 2 0 {name=M11
l=0.200u
w=4.0u
ng=2
m=1
model=sg13_lv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_nmos.sym} 1040 -420 2 1 {name=M12
l=0.200u
w=4.0u
ng=2
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
C {sg13g2_pr/ntap1.sym} 1500 -290 2 0 {name=R1
model=ntap1
spiceprefix=X
w=100e-6
l=100e-6

}
C {lab_pin.sym} 1500 -240 2 0 {name=p9 sig_type=std_logic lab=vdd}
C {sg13g2_pr/sg13_lv_nmos.sym} 1260 -300 0 1 {name=M3
l=0.200u
w=4.0u
ng=1
m=4
model=sg13_lv_nmos
spiceprefix=X
}
C {lab_pin.sym} 1190 -300 0 0 {name=p10 sig_type=std_logic lab=sub
m=4}
C {lab_pin.sym} 1240 -360 0 0 {name=p12 sig_type=std_logic lab=gnd
m=4}
C {sg13g2_pr/ptap1.sym} 1370 -300 2 0 {name=R2
model=ptap1
spiceprefix=X
w=100e-6
l=100e-6
}
C {lab_pin.sym} 1370 -250 0 0 {name=p13 sig_type=std_logic lab=gnd
m=4}
C {lab_pin.sym} 820 -200 3 0 {name=p14 sig_type=std_logic lab=sub}
C {lab_pin.sym} 490 -200 3 0 {name=p15 sig_type=std_logic lab=sub}
C {lab_pin.sym} 1370 -340 0 1 {name=p16 sig_type=std_logic lab=sub}
C {lab_pin.sym} 1500 -340 0 1 {name=p17 sig_type=std_logic lab=well}
C {lab_pin.sym} 660 -570 1 1 {name=p18 sig_type=std_logic lab=well}
C {lab_pin.sym} 1110 -530 0 1 {name=p19 sig_type=std_logic lab=well}
C {lab_pin.sym} 190 -530 2 1 {name=p20 sig_type=std_logic lab=well}
C {lab_pin.sym} 1110 -420 0 1 {name=p21 sig_type=std_logic lab=sub}
C {lab_pin.sym} 190 -420 2 1 {name=p22 sig_type=std_logic lab=sub}
C {sg13g2_pr/sg13_lv_pmos.sym} 630 -740 0 0 {name=M13
l=0.3u
w=18u
ng=4
m=1
model=sg13_lv_pmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_pmos.sym} 630 -840 0 0 {name=M9
l=0.3u
w=18u
ng=4
m=1
model=sg13_lv_pmos
spiceprefix=X
}
C {ipin.sym} 580 -840 0 0 {name=p5 lab=vbias}
C {lab_pin.sym} 710 -790 0 1 {name=p23 sig_type=std_logic lab=well}
C {sg13g2_pr/annotate_fet_params.sym} 240 -400 0 0 {name=annot1 ref=M1}
