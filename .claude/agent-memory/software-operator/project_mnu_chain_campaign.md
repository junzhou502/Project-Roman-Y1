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
but was deprioritized and NOT submitted. Production jobs submitted 2026-07-17 to kicp:
52357046 (roman 41), 52357047 (roman 60), 52357048 (des y1), 52357049 (des y3).
Validation evaluates (caslake job 52357010): roman chi2 ~ 3-4e-05 vs fake datavector;
des_y1 chi2=238.65, des_y3 chi2=777.42 vs real data at the reference point.

Status of earlier fixed-mnu template chains (context for comparisons):
- roman_lsst_50_mcmc converged (R-1 = 0.047).
- roman_lsst_41_mcmc did NOT converge (R-1 ~ 0.158); job 52105459 died with a cobaya/CAMB
  error "Not possible to extrapolate to k=1.02e-05 1/Mpc" — a sporadic interpolation edge
  case; the same failure mode can hit any chain in this setup.

**How to apply:** when analyzing/comparing chains, check .checkpoint convergence first; expect
possible k-extrapolation crashes and recommend resuming with the same sbatch (cobaya resumes
from chain files, drop the -f flag when resuming). See [[kicp-cluster-conventions]].
