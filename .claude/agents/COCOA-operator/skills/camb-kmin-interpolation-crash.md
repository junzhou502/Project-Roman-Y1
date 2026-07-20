# Skill: diagnose/fix the CAMB "Not possible to extrapolate to k=1.02e-05" crash

## Symptom
cobaya MCMC dies mid-chain with
`LoggedError: Not possible to extrapolate to k=1.0233e-05 1/Mpc (minimum k possible is 1.1e-05 ...)`
raised from `boltzmannbase.check_ranges` via `_cosmolike_prototype_base.py set_cosmo_related`.
The "minimum k possible" value varies between crashes — that is the fingerprint.

## Root cause (verified 2026-07-18 by reading CAMB fortran)
- Cosmolike requests P(k) on a FIXED grid down to 10^-4.99 = 1.0233e-05 1/Mpc
  (`self.log10k_interp_2D = np.linspace(-4.99, 2.0, ...)`).
- CAMB's transfer-function k grid (when `k_per_logint > 0`, the "fixed spacing" branch in
  `fortran/cmbmain.f90` InitTransfer) starts at
  `kmin = (0.1 / tau0 / (AccuracyBoost*TimeStepBoost)) * exp(1/k_per_logint)`,
  where tau0 = conformal age in Mpc — i.e. kmin is COSMOLOGY-DEPENDENT.
- At fiducial (tau0 ~ 14000 Mpc) kmin ~ 6.7e-06: fine. In young-universe corners
  (high H0 x high omegam, tau0 ~ 7000-9000 Mpc) kmin rises to ~1.1-1.4e-05 > 1.0233e-05: crash.
- Why older installs (cocoa_approx/cocoa_caslake) "never" crashed: identical CAMB/cobaya/
  prototype code, but their chains used NARROW priors (H0 in [61,73], omegam in [0.24,0.40])
  that cannot reach the corner. Wide priors (H0 to 91, omegam to 0.9) + burn-in dispersion
  make the crash likely; adding params (e.g. free mnu) lengthens burn-in and raises the odds.
  It is NOT an mnu-specific or CAMB-version issue.

## Fix (applied in Project-Roman-Y1 cocoa, projects/roman_y1 and projects/des_y3
## likelihood/_cosmolike_prototype_base.py; cobaya/likelihoods/* are symlinks to these)
1. Raise the request floor: `log10k_interp_2D` lower bound -4.99 -> -4.90
   (10^-4.90 = 1.259e-05).
2. Harden every `provider.get_Pk_interpolator(...)` call with `extrap_kmin=1e-6`
   (both nonlinear=False and nonlinear=True calls). cobaya then log-log-extrapolates
   below CAMB's grid instead of raising; P ~ k^ns there so this is accurate, and it
   covers the residual corner where CAMB kmin (~1.36e-05 at H0=91, omegam=0.9) still
   exceeds 10^-4.90.

## No-extrapolation alternative (verified 2026-07-20)
A variant with NO extrap_kmin and floor -4.85 (10^-4.85 = 1.4125e-05 > worst-case
CAMB kmin 1.3922e-05 at H0=91, omegam=0.9) also passes fiducial + corner validation;
see clone-cocoa-likelihood-variant.md for the measurement recipe and clone wiring.

## Validation pattern
Rerun fiducial evaluates (chi2 impact of the grid change was negligible: roman ~1e-9
absolute; des_y3 777.42 -> 776.87, 0.07%) AND a corner stress evaluate
(H0=90, omegam=0.85, mnu=0.5) that forces the extrapolation path — must return finite
chi2 with empty .err. After a likelihood-code fix, restart crashed chains FRESH (-f):
early-burn-in samples from the old code are not worth resuming into a changed likelihood.
