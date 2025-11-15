v {xschem version=3.4.6 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N 560 -430 610 -430 {lab=#net1}
N 560 -350 610 -350 {lab=#net2}
N 760 -430 810 -430 {lab=#net3}
N 760 -350 810 -350 {lab=#net4}
N 460 -480 460 -460 {lab=vdd}
N 660 -480 860 -480 {lab=vdd}
N 860 -480 860 -460 {lab=vdd}
N 660 -480 660 -460 {lab=vdd}
N 460 -480 660 -480 {lab=vdd}
N 460 -320 460 -300 {lab=gnd}
N 460 -300 660 -300 {lab=gnd}
N 660 -320 660 -300 {lab=gnd}
N 660 -300 860 -300 {lab=gnd}
N 860 -320 860 -300 {lab=gnd}
N 390 -430 410 -430 {lab=#net5}
N 390 -520 980 -520 {lab=#net5}
N 960 -430 980 -430 {lab=#net5}
N 390 -520 390 -430 {lab=#net5}
N 980 -520 980 -430 {lab=#net5}
N 980 -350 980 -260 {lab=Voplus}
N 960 -350 980 -350 {lab=Voplus}
N 390 -350 410 -350 {lab=Voplus}
N 390 -350 390 -260 {lab=Voplus}
N 390 -260 980 -260 {lab=Voplus}
C {differential_core.sym} 560 -390 0 0 {name=x1}
C {differential_core.sym} 760 -390 0 0 {name=x2}
C {differential_core.sym} 960 -390 0 0 {name=x3}
C {opin.sym} 980 -260 0 0 {name=p3 lab=Voplus}
C {opin.sym} 980 -510 2 1 {name=p4 lab=Vominus}
C {iopin.sym} 860 -480 0 0 {name=p1 lab=vdd}
C {iopin.sym} 860 -300 0 0 {name=p2 lab=gnd}
