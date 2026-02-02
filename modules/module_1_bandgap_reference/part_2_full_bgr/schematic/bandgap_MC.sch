v {xschem version=3.4.6 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N -720 -850 -720 -795 {
lab=#net1}
N -575 -980 -485 -980 {
lab=vdd}
N -645 -930 -615 -930 {
lab=#net1}
N -720 -850 -645 -850 {
lab=#net1}
N -720 -900 -720 -850 {
lab=#net1}
N -645 -930 -645 -850 {
lab=#net1}
N -680 -930 -645 -930 {
lab=#net1}
N -720 -765 -720 -710 {
lab=GND}
N -575 -850 -575 -795 {
lab=#net2}
N -720 -710 -575 -710 {
lab=GND}
N -575 -735 -575 -710 {
lab=GND}
N -680 -765 -485 -765 {
lab=v-}
N -485 -980 -485 -850 {
lab=vdd}
N -575 -850 -525 -850 {
lab=#net2}
N -575 -900 -575 -850 {
lab=#net2}
N -485 -765 -485 -650 {
lab=v-}
N -485 -820 -485 -765 {
lab=v-}
N -110 -695 -80 -695 {
lab=Vo1}
N -275 -795 -275 -760 {
lab=vdd}
N -350 -610 -350 -595 {
lab=#net3}
N -350 -535 -275 -535 {
lab=GND}
N -275 -535 -275 -520 {
lab=GND}
N -275 -630 -275 -535 {
lab=GND}
N -435 -735 -410 -735 {
lab=v+}
N -485 -650 -410 -650 {
lab=v-}
N -780 -930 -720 -930 {
lab=vdd}
N -575 -930 -530 -930 {
lab=vdd}
N -575 -980 -575 -960 {
lab=vdd}
N -720 -980 -575 -980 {
lab=vdd}
N -720 -980 -720 -960 {
lab=vdd}
N 890 -405 890 -360 {
lab=vdd}
N 890 -300 890 -270 {
lab=GND}
N 370 -560 390 -560 {
lab=#net4}
N 370 -620 370 -560 {
lab=#net4}
N 370 -620 430 -620 {
lab=#net4}
N 130 -560 130 -460 {
lab=GND}
N 280 -460 430 -460 {
lab=GND}
N 130 -740 230 -740 {
lab=v-}
N 280 -965 280 -940 {
lab=vdd}
N 130 -940 280 -940 {
lab=vdd}
N 130 -840 130 -740 {
lab=v-}
N 430 -750 430 -740 {
lab=v+}
N 430 -740 430 -710 {
lab=v+}
N 430 -560 430 -460 {
lab=GND}
N 430 -620 430 -590 {
lab=#net4}
N 430 -650 430 -620 {
lab=#net4}
N 280 -460 280 -430 {
lab=GND}
N 130 -460 280 -460 {
lab=GND}
N 170 -870 390 -870 {
lab=Vo1}
N 595 -900 595 -870 {
lab=Vo1}
N 430 -750 595 -750 {
lab=v+}
N 980 -770 1030 -770 {
lab=VBG}
N 635 -840 635 -770 {
lab=VBG}
N 315 -740 430 -740 {
lab=v+}
N 430 -840 430 -750 {
lab=v+}
N 595 -750 595 -710 {
lab=v+}
N 430 -460 595 -460 {
lab=GND}
N 595 -650 595 -460 {
lab=GND}
N 430 -940 635 -940 {
lab=vdd}
N 980 -655 980 -460 {
lab=GND}
N 800 -460 980 -460 {
lab=GND}
N 980 -770 980 -715 {
lab=VBG}
N 800 -770 980 -770 {
lab=VBG}
N 635 -940 635 -900 {
lab=vdd}
N 635 -870 725 -870 {
lab=vdd}
N 430 -940 430 -900 {
lab=vdd}
N 280 -940 430 -940 {
lab=vdd}
N 430 -870 495 -870 {
lab=vdd}
N 130 -940 130 -900 {
lab=vdd}
N 70 -870 130 -870 {
lab=vdd}
N 130 -740 130 -590 {
lab=v-}
N 170 -560 315 -560 {
lab=v+}
N 315 -740 315 -560 {
lab=v+}
N 800 -770 800 -715 {
lab=VBG}
N 635 -770 800 -770 {
lab=VBG}
N 800 -655 800 -460 {
lab=GND}
N 595 -460 800 -460 {
lab=GND}
N -630 -795 -575 -795 {
lab=#net2}
N -630 -735 -575 -735 {
lab=GND}
C {devices/code_shown.sym} -980 -463.828125 0 0 {name=NGSPICE only_toplevel=false 
value="
.param mm_ok=1
.param mc_ok=1

.control
  let run = 1
  let mc_runs = 100
  set curplot = new
  set scratch = $curplot
  dowhile run <= mc_runs
    reset
    dc temp 100 -50 -5
    set run = $&run
    set dc = $curplot
    setplot $scratch
    let off\{$run\} = \{$dc\}.v(VBG)
    let mytemp\{$run\} = \\"\{$dc\}.temp-sweep\\"
    setplot $dc
    let run = run + 1
  end
  set nolegend
  plot \{$scratch\}.allv vs \{$scratch\}.mytemp1
  write bandgap_testbench_mc_mis.raw \{$scratch\}.allv \{$scratch\}.mytemp1
.endc

"}
C {devices/code_shown.sym} -980 -595 0 0 {name=MODEL only_toplevel=true
format="tcleval( @value )"
value="
.lib $::SG13G2_MODELS/cornerCAP.lib cap_typ
.lib $::SG13G2_MODELS/cornerRES.lib res_typ
.lib cornerMOSlv.lib mos_tt_stat"}
C {sg13g2_pr/sg13_lv_nmos.sym} -700 -765 2 0 {name=M8
l=10u
w=150n
ng=1
m=1
model=sg13_lv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_pmos.sym} -700 -930 0 1 {name=M6
l=1u
w=1u
ng=1
m=1
model=sg13_lv_pmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_pmos.sym} -595 -930 0 0 {name=M7
l=1u
w=1u
ng=1
m=1
model=sg13_lv_pmos
spiceprefix=X
}
C {gnd.sym} -720 -710 0 0 {name=l1 lab=GND}
C {sg13g2_pr/sg13_lv_pmos.sym} -505 -850 0 0 {name=M9
l=4u
w=200n
ng=1
m=1
model=sg13_lv_pmos
spiceprefix=X
}
C {lab_pin.sym} -485 -980 0 1 {name=p5 sig_type=std_logic lab=vdd}
C {lab_pin.sym} -275 -795 0 1 {name=p1 sig_type=std_logic lab=vdd}
C {gnd.sym} -275 -520 0 1 {name=l4 lab=GND}
C {isource.sym} -350 -565 0 1 {name=I1 value=80u}
C {iopin.sym} -435 -735 0 1 {name=p16 lab=v+}
C {iopin.sym} -435 -650 3 1 {name=p7 lab=v-}
C {iopin.sym} -80 -695 0 0 {name=p10 lab=Vo1}
C {lab_pin.sym} -530 -930 0 1 {name=p4 sig_type=std_logic lab=vdd}
C {lab_pin.sym} -780 -930 0 0 {name=p17 sig_type=std_logic lab=vdd}
C {vsource.sym} 890 -330 0 0 {name=V1 value="DC 1.2" savecurrent=false}
C {lab_pin.sym} 890 -405 0 1 {name=p6 sig_type=std_logic lab=vdd}
C {gnd.sym} 890 -270 0 0 {name=l18 lab=GND}
C {sg13g2_pr/sg13_lv_nmos.sym} 150 -560 2 0 {name=M1
l=5u
w=7.14u
ng=4
m=1
model=sg13_lv_nmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_nmos.sym} 410 -560 2 1 {name=M2
l=5u
w=21u
ng=8
m=1
model=sg13_lv_nmos
spiceprefix=X
}
C {gnd.sym} 280 -430 0 0 {name=l3 lab=GND}
C {sg13g2_pr/sg13_lv_pmos.sym} 150 -870 0 1 {name=M3
l=5u
w=15u
ng=8
m=1
model=sg13_lv_pmos
spiceprefix=X
}
C {sg13g2_pr/sg13_lv_pmos.sym} 410 -870 0 0 {name=M4
l=5u
w=15u
ng=8
m=1
model=sg13_lv_pmos
spiceprefix=X
}
C {lab_pin.sym} 280 -965 0 1 {name=p2 sig_type=std_logic lab=vdd}
C {lab_pin.sym} 230 -740 3 0 {name=p3 sig_type=std_logic lab=v-}
C {lab_pin.sym} 315 -740 0 0 {name=p8 sig_type=std_logic lab=v+}
C {lab_pin.sym} 285 -870 1 1 {name=p9 sig_type=std_logic lab=Vo1}
C {sg13g2_pr/sg13_lv_pmos.sym} 615 -870 0 0 {name=M5
l=5u
w=16u
ng=8
m=1
model=sg13_lv_pmos
spiceprefix=X
}
C {opin.sym} 1030 -770 0 0 {name=p11 lab=VBG}
C {lab_pin.sym} 595 -900 2 1 {name=p12 sig_type=std_logic lab=Vo1}
C {lab_pin.sym} 70 -870 0 0 {name=p13 sig_type=std_logic lab=vdd}
C {lab_pin.sym} 495 -870 0 1 {name=p14 sig_type=std_logic lab=vdd}
C {lab_pin.sym} 725 -870 0 1 {name=p15 sig_type=std_logic lab=vdd}
C {sg13g2_pr/cap_cmim.sym} 980 -685 0 0 {name=C3
model=cap_cmim
w=72.965e-6
l=72.965e-6
m=1
spiceprefix=X}
C {sg13g2_pr/rppd.sym} 430 -680 0 0 {name=R3
w=0.5e-6
l=194.345e-6
model=rppd
spiceprefix=X
b=0
m=1
}
C {sg13g2_pr/rppd.sym} 595 -680 0 0 {name=R1
w=0.5e-6
l=194.345e-6
model=rppd
spiceprefix=X
b=0
m=1.2
}
C {sg13g2_pr/rppd.sym} 800 -685 0 0 {name=R2
w=0.5e-6
l=192.395e-6
model=rppd
spiceprefix=X
b=0
m=1
}
C {sg13g2_pr/cap_cmim.sym} -630 -765 0 0 {name=C1
model=cap_cmim
w=18.195e-6
l=18.195e-6
m=1
spiceprefix=X}
C {two_stage_OTA.sym} -260 -695 0 0 {name=x1}
C {devices/gnd.sym} 760 -370 2 0 {name=l6 lab=GND}
C {sg13g2_pr/ptap1.sym} 760 -340 0 0 {name=R4
model=ptap1
spiceprefix=X
w=100.78e-6
l=100.78e-6
}
C {sg13g2_pr/sub.sym} 760 -310 0 0 {name=l7 lab=sub!}
