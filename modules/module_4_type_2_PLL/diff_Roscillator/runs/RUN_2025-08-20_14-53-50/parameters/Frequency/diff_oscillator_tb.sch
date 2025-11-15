v {xschem version=3.4.6 file_version=1.2}
G {}
K {}
V {}
S {}
E {}
N 760 -230 760 -210 {lab=vdd}
N 720 -230 720 -210 {lab=gnd}
N 830 -340 850 -340 {lab=Voplus}
N 830 -300 850 -300 {lab=Vominus}
C {opin.sym} 850 -340 0 0 {name=p3 lab=Voplus}
C {opin.sym} 850 -300 2 1 {name=p4 lab=Vominus}
C {code_shown.sym} 0 -840 0 0 {name=transient_tb only_toplevel=false
value="
.param temp=27
.ic V(Voplus)=1.2
.control
save all 
op
write diff_oscillator_tb.raw
set appendwrite
tran 10p 2n
save all
let vo_diff = v(Voplus) - v(Vominus)
set wr_singlescale
wrdata CACE\{simpath\}/CACE\{filename\}_CACE\{N\}.data vo_diff
write diff_oscillator_tb.raw
.endc
"}
C {iopin.sym} 760 -210 0 0 {name=p1 lab=vdd}
C {devices/code_shown.sym} 10 -510 0 0 {name=MODEL1 only_toplevel=true
format="tcleval( @value )"
value="
.lib CACE\{PDK_ROOT\}/CACE\{PDK\}/libs.tech/ngspice/models/cornerMOSlv.lib mos_CACE\{corner\}

.include CACE\{DUT_path\}

.temp CACE\{temperature\}
"
}
C {diff_ring_oscillator.sym} 740 -320 0 0 {name=x1}
C {iopin.sym} 720 -210 2 0 {name=p2 lab=gnd}
