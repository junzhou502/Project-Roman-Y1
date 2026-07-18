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

Status of earlier fixed-mnu template chains (context for comparisons):
- roman_lsst_50_mcmc converged (R-1 = 0.047).
- roman_lsst_41_mcmc did NOT converge (R-1 ~ 0.158); job 52105459 died with a cobaya/CAMB
  error "Not possible to extrapolate to k=1.02e-05 1/Mpc" — a sporadic interpolation edge
  case; the same failure mode can hit any chain in this setup.

**How to apply:** when analyzing/comparing chains, check .checkpoint convergence first; expect
possible k-extrapolation crashes and recommend resuming with the same sbatch (cobaya resumes
from chain files, drop the -f flag when resuming). See [[kicp-cluster-conventions]].
