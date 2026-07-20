---
name: mnu-chain-campaign
description: 2026-07-17 mnu-marginalized MCMC campaign (roman 41/60, des y1/y3), priors used, and status of earlier fixed-mnu chains
metadata:
  type: project
---

On 2026-07-17 the user launched mnu-marginalized cosmic-shear chains: roman_lsst_41_mnu_mcmc,
roman_lsst_60_mnu_mcmc (DES-Y3 prior, mnu flat in [0.056, 0.60] eV) and des_y1_mnu_mcmc
(mnu flat in [0.056, 0.93] eV, DES-Y1 own prior), des_y3_mnu_mcmc ([0.056, 0.60] eV).
**Why:** mirror the published DES Y1/Y3 choice where neutrino density is free; mid-task the
user switched the Roman pair from (41, 50) to (41, 60). A roman_lsst_50_mnu_mcmc.yaml exists
but was deprioritized and NOT submitted. First submission (52357046-49) crashed within hours on the CAMB kmin interpolation bug
(see skill camb-kmin-interpolation-crash.md: cosmology-dependent CAMB kmin vs cosmolike's
fixed 10^-4.99 request; wide H0/omegam priors reach the failing corner). Fixed 2026-07-18
in projects/roman_y1 and projects/des_y3 _cosmolike_prototype_base.py (-4.99 -> -4.90 plus
extrap_kmin=1e-6) and resubmitted FRESH to kicp: 52371509 (roman 41), 52371510 (roman 60),
52371511 (des y1), 52371512 (des y3). Post-fix fiducial chi2: roman 2.849e-05/4.342e-05,
des_y1 238.651, des_y3 776.874 (was 777.419 pre-fix, 0.07% grid-change shift); corner
stress evaluate (H0=90, om=0.85, mnu=0.5) finite. NOTE: fixed-mnu chains ran with -4.99;
mnu chains run with -4.90 — a 0.07%-level chi2 difference, flag if doing precise
fixed-vs-free comparisons.

2026-07-20 kmin-effect test (DES chains look wider than published; testing whether the
extrap_kmin=1e-6 + (-4.90) grid change matters): new variant likelihood
`des_y3.cosmic_shear_kmin` (files cosmic_shear_kmin.py/.yaml,
_cosmolike_prototype_base_kmin.py in projects/des_y3/likelihood/) with NO extrap_kmin
and log10k floor -4.85 (worst-case CAMB kmin 1.3922e-05 at H0=91,om=0.9; floor
1.4125e-05, margin 1.46%). Validation (caslake 52418671): y1 chi2 238.65106
(ref 238.65102), y3 777.05394 (ref 776.87425, 0.023% grid shift), stress finite,
empty .err. Chains on kicp: 52419069 (des_y1_mnu_kmin_mcmc), 52419070
(des_y3_mnu_kmin_mcmc), outputs chains/des_y{1,3}_mnu_kmin_mcmc/. Compare against
des_y{1,3}_mnu_mcmc when converged: if posteriors agree, extrap_kmin is exonerated.
Also verified 2026-07-20: the .dataset shear datavector/cov/mask are exactly the
published DES shear-only setups (227 points each for Y1 and Y3; Y1 mask matches
Troxel+ per-pair theta_min exactly; cov = straight shear-shear sub-block, masked
then inverted; no PM marginalization for probe "xi").

Status of earlier fixed-mnu template chains (context for comparisons):
- roman_lsst_50_mcmc converged (R-1 = 0.047).
- roman_lsst_41_mcmc did NOT converge (R-1 ~ 0.158); job 52105459 died with a cobaya/CAMB
  error "Not possible to extrapolate to k=1.02e-05 1/Mpc" — a sporadic interpolation edge
  case; the same failure mode can hit any chain in this setup.

**How to apply:** when analyzing/comparing chains, check .checkpoint convergence first; expect
possible k-extrapolation crashes and recommend resuming with the same sbatch (cobaya resumes
from chain files, drop the -f flag when resuming). See [[kicp-cluster-conventions]].
