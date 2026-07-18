# Skill: switch a COCOA yaml from fixed to marginalized (sampled) mnu

## When to use
A cosmic-shear/2x2pt MCMC yaml fixes `mnu: {value: 0.06}` and you need to
marginalize over the sum of neutrino masses (e.g. DES Y1/Y3-style analysis).

## Recipe (3 edits, nothing else changes)
1. Replace the fixed mnu with a sampled block. Flat prior on Omega_nu h^2
   maps linearly to flat prior on Sum m_nu: `Sum m_nu = 93.14 eV x Omega_nu h^2`.
   - DES-Y3 prior: Omega_nu h^2 in [0.0006, 0.00644]  ->  mnu in [0.056, 0.60] eV
   - DES-Y1 prior: Omega_nu h^2 in [0.0006, 0.01]     ->  mnu in [0.056, 0.93] eV
   ```yaml
   mnu:
     prior:
       min: 0.056
       max: 0.60
     ref:
       dist: norm
       loc: 0.1
       scale: 0.05
     proposal: 0.05
     latex: \sum m_\nu
   ```
2. Add `mnu` to the SLOW block of `sampler.mcmc.blocking` (the speed-1 block
   with As_1e9, ns, H0, omegab, omegam). mnu changes the CAMB power spectrum,
   so it is a slow cosmology parameter.
3. Change `output:` to a new chain directory (never overwrite existing chains).

## What NOT to change
- Keep the `omegach2` derived lambda unchanged; it already handles the
  mnu -> omegach2 conversion: `(omegam-omegab)*(H0/100)**2-(mnu*(3.046/3)**0.75)/94.0708`.
- Keep CAMB `num_massive_neutrinos: 1, nnu: 3.046` as in the template (COCOA
  standard, one massive eigenstate carrying Sum m_nu; consistent with how the
  fake datavectors were generated at mnu=0.06). Reference example:
  `/project/chihway/junzhou/cocoa_caslake/Cocoa/projects/roman_real/roman_lcdm_neutrino_mcmc.yaml`.
- If the mcmc block uses a proposal `covmat` file that lacks mnu (e.g.
  des_y3 EXAMPLE_MCMC1.covmat), that is fine: cobaya fills missing params
  from their `proposal` widths and learns the rest.

## Validation before submitting
Create an evaluate twin: keep everything above `sampler:`, replace sampler by
`evaluate` with `override:` at the exact fiducial point used to generate the
fake datavector (for roman_y1: As_1e9 2.1, ns 0.96605, H0 67.32, omegab 0.04,
omegam 0.3, mnu 0.06, all DZ/M = 0, A1_1 = 0.5, A1_2 = 0 — taken from
`chains/roman_lsst_41_evaluate/input.yaml`). chi2 should be ~0 for fake
datavectors; finite and O(ndata) for real DES data. Run the evaluate through a
small sbatch job (1 task, 12 cpus) — never on the login node. If kicp is backed up,
run validation on `--partition=caslake --account=pi-chihway` (user-approved; the cocoa
conda env + build works on caslake nodes; 4 evaluates took ~2 min there). Reference
values observed 2026-07-17 at the fiducial point with mnu=0.06:
roman 41 chi2=2.85e-05, roman 60 chi2=4.34e-05, des_y1 chi2=238.65, des_y3 chi2=777.42.

## Cluster conventions (this project)
- All chain jobs: partition kicp, account kicp, 1 node, 4 MPI ranks x 12 OMP
  threads, `--exclusive`, 48 h; copy an existing working sbatch and sed the names.
- kicp is busy: submitting + `squeue` showing PD/R is sufficient confirmation;
  do not wait for jobs to start.
- Some existing sbatch dir names have trailing spaces (e.g. `roman_lsst_50_mcmc `);
  always quote paths and never create new dirs with trailing spaces.
