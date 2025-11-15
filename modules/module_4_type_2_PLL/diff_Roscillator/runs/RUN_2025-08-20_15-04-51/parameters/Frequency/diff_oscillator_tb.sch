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
C {code_shown.sym} 50 -1230 0 0 {name=transient_tb only_toplevel=false
value="
.param temp=27
* Keep this if your manual run has it — parity matters

.ic V(Voplus)=1.2
.control
* Stability & parity options
set noaskquit
set numdgt=12

* Save vectors and run
save all
op
write diff_oscillator_tb.raw
set appendwrite
tran 10p 2n

* Define explicit vectors (avoid V(...) on calculated vectors)
let vo_p    = v(Voplus)
let vo_m    = v(Vominus)
let vo_diff = vo_p - vo_m

* --- Main file that CACE reads: 2 columns (time, vo_diff) ---
set wr_singlescale
wrdata CACE\{simpath\}/CACE\{filename\}_CACE\{N\}.data vo_diff

* --- Extra debug file (CACE ignores): 4 columns w/ names ---
set wr_vecnames
wrdata CACE\{simpath\}/debug_CACE\{N\}.dat time vo_p vo_m vo_diff
unset wr_vecnames

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
