# Chain bookkeeping: mnu-marginalization campaign (July 2026)

This note records exactly how the chains being compared differ, in terms of
(a) neutrino-mass treatment, (b) priors, and (c) the cosmolike prototype
(k-grid) code they ran with. See `stats.txt` for the 68% constraints and
`compare_mnu.py` for the plots.

## Chains

| Chain | Data | mnu treatment | Prototype k-grid | Status |
|---|---|---|---|---|
| roman_lsst_41_mcmc | synthetic Roman-Y1, cov n=41 | fixed 0.06 eV | old: log10k >= -4.99, no extrap_kmin | done (died at R-1=0.158, usable) |
| roman_lsst_50_mcmc | synthetic, cov n=50 | fixed 0.06 eV | old | done |
| roman_lsst_60_mcmc | synthetic, cov n=60 | fixed 0.06 eV | old | done |
| roman_lsst_41_mnu_mcmc | synthetic, cov n=41 | flat [0.056, 0.60] eV | new: log10k >= -4.90 + extrap_kmin=1e-6 | done, R-1<0.05 |
| roman_lsst_60_mnu_mcmc | synthetic, cov n=60 | flat [0.056, 0.60] eV | new | done, R-1<0.05 |
| des_y1_mcmc | DES Y1 real 3x2pt (shear part) | fixed 0.06 eV | old | done |
| des_y3_mcmc | DES Y3 real 3x2pt (shear part) | fixed 0.06 eV | old | done |
| des_y1_mnu_mcmc | DES Y1 real | flat [0.056, 0.93] eV | new | done, R-1<0.05 |
| des_y3_mnu_mcmc | DES Y3 real | flat [0.056, 0.60] eV | new | done, R-1<0.05 |
| des_y1_mnu_kmin_mcmc | DES Y1 real | flat [0.056, 0.93] eV | kmin-test: log10k >= -4.85, NO extrap_kmin | (in progress) |
| des_y3_mnu_kmin_mcmc | DES Y3 real | flat [0.056, 0.60] eV | kmin-test | (in progress) |

## (a) Neutrino-mass treatment

- Fixed chains: `mnu: 0.06` (one massive eigenstate in CAMB, COCOA convention).
- mnu chains: flat prior on Sum m_nu, equivalent to the DES flat prior on
  Omega_nu h^2 (Sum m_nu = 93.14 eV x Omega_nu h^2, 3 degenerate species):
  - DES-Y1 convention: Omega_nu h^2 in [0.0006, 0.01]  -> [0.056, 0.93] eV
    (used by des_y1_mnu_*).
  - DES-Y3 convention: Omega_nu h^2 in [0.0006, 0.00644] -> [0.056, 0.60] eV
    (used by roman_*_mnu and des_y3_mnu_*).
- The synthetic Roman datavector was generated at mnu = 0.06 eV, i.e. at the
  lower edge of the mnu prior. This is one reason mnu-marginalization affects
  the Roman forecast differently from real DES data: for the forecast, the
  posterior can only extend one way (heavier mnu, compensated mostly by
  higher Omega_m), while for real data the whole posterior re-centers
  (S8 shifts down by 0.012-0.016).

## (b) Priors (verified against the papers)

Cosmology (identical in all chains, matches DES Y1 Troxel+18 Table 2 and
DES Y3 2105.13549 Table I): 10^9 As [0.5, 5], ns [0.87, 1.07],
H0 [55, 91], omegab [0.03, 0.07], omegam [0.1, 0.9], tau fixed, w = -1.

Nuisance:
- des_y1_*: source dz Gaussians (-0.001+-0.016, -0.019+-0.013, +0.009+-0.011,
  -0.018+-0.022); m_i = 0.012+-0.023 (all bins); IA = NLA with amplitude and
  redshift-evolution parameters flat [-5, 5] (TATT components fixed to 0).
  All match Troxel et al. 2018 (arXiv:1708.01538) Table 2.
- des_y3_*: source dz Gaussians (0+-0.018, 0+-0.015, 0+-0.011, 0+-0.017);
  m = (-0.006+-0.009, -0.02+-0.008, -0.024+-0.008, -0.037+-0.008);
  IA = TATT with a1, a2 amplitudes and redshift evolutions flat [-5, 5] and
  b_TA flat [0, 2]. All match 2105.13549 Table I (the Y3 cosmic-shear
  fiducial model).
- roman_*: dz Gaussians 0+-0.002, m Gaussians 0+-0.005, NLA 2-param IA.

Important caveat when comparing to PUBLISHED DES chains:
- The published DES Y3 "cosmic shear" fiducial result
  (chain_1x2pt_lcdm_SR_maglim.txt, S8 = 0.759 +0.025/-0.023) includes the
  shear-ratio (SR) likelihood in addition to xi+/-. Our COCOA chains do not
  include SR. SR tightens IA/photo-z and hence S8; part of our extra width
  in the Y3 comparison is expected from this alone.
- Published sampling used PolyChord (Y3) with different burn-in conventions;
  we use cobaya-MCMC with ignore_rows=0.2 in getdist.

## (c) Cosmolike prototype (k-grid) versions

- "old" (all fixed-mnu chains): `log10k_interp_2D = linspace(-4.99, 2.0, ...)`,
  `get_Pk_interpolator(...)` without extrap_kmin. Vulnerable to a crash when
  CAMB's cosmology-dependent grid kmin = (0.1/tau0/AccuracyBoost)*exp(1/k_per_logint)
  rises above 10^-4.99 (young-universe corners of the wide priors).
- "new" (all *_mnu chains): lower bound -4.90 and extrap_kmin=1e-6 added, so
  extreme corners log-log-extrapolate instead of crashing. Fiducial chi2
  changes by <0.1% (des_y3: 777.42 -> 776.87).
- "kmin-test" (des_*_mnu_kmin chains, separate copied prototype
  `_cosmolike_prototype_base_kmin.py` + `cosmic_shear_kmin` likelihood):
  NO extrap_kmin; lower bound -4.85, chosen to clear the worst-case CAMB
  kmin over the whole prior volume. Purpose: isolate whether
  extrap_kmin/k-grid choices influence the DES posteriors at all.
  (Details to be filled in when the runs finish.)
