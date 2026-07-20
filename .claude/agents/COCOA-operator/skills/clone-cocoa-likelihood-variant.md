# Skill: clone a COCOA/cosmolike likelihood class as a variant (without touching the original)

## When to use
You need to test a change in likelihood python code (e.g. P(k) grid bounds, extrapolation
flags) while chains using the original class keep running.

## How registration works in this install
- `cobaya/cobaya/likelihoods/des_y3` is a SYMLINK to `projects/des_y3/likelihood/`
  (same for roman_y1). Any new module dropped in the project likelihood folder is
  instantly importable as `des_y3.<module_name>` — no __init__.py edits needed
  (the __init__.py is empty), no pip reinstall.
- cobaya resolves likelihood name `des_y3.cosmic_shear_kmin` to module
  `cobaya.likelihoods.des_y3.cosmic_shear_kmin`, class `cosmic_shear_kmin`
  (CLASS NAME MUST EQUAL MODULE NAME), defaults file `cosmic_shear_kmin.yaml`
  (same folder, same stem).

## Recipe (validated 2026-07-20, kmin variant)
1. `cp _cosmolike_prototype_base.py _cosmolike_prototype_base_kmin.py` and edit the copy.
2. `cp cosmic_shear.yaml cosmic_shear_kmin.yaml` (defaults can stay identical).
3. New `cosmic_shear_kmin.py`: same 7 lines as `cosmic_shear.py` but import from
   `cobaya.likelihoods.des_y3._cosmolike_prototype_base_kmin` and rename the class
   to `cosmic_shear_kmin`.
4. MCMC/evaluate yamls: sed `des_y3.cosmic_shear:` -> `des_y3.cosmic_shear_kmin:` and
   change the output dir. Nothing else.
5. Sanity: `python -m py_compile` both new files; check they appear under
   `cobaya/cobaya/likelihoods/des_y3/` through the symlink.
Note: the C/C++ side (`cosmolike_des_y3_interface`) is a singleton shared by all classes
in a process — fine for separate runs, do NOT load two variant classes in one process.

## Worst-case CAMB kmin verification (for grid-bound choices)
Use the project CAMB build directly (login node, light):
`sys.path.insert(0, ".../external_modules/code/CAMB")`, build params with the SAME
extra_args as the chain yaml (AccuracyBoost=1.05, k_per_logint=20, nnu=3.046,
num_massive_neutrinos=1, omegach2 from the yaml lambda), `WantTransfer=True`, then
`kmin = get_matter_transfer_data().transfer_data[0,0,0] * h`.
Verified numbers (this prior volume, H0<=91, omegam<=0.9):
- fiducial: kmin = 6.732e-06 1/Mpc (tau0 = 14147 Mpc)
- worst corner H0=91, omegam=0.9: kmin = 1.3922e-05 (tau0 = 6841 Mpc); omegab/mnu ~no effect
- so a request floor of 10^-4.85 = 1.4125e-05 needs NO extrap_kmin anywhere in the
  prior volume (margin 1.46%); 10^-4.90 = 1.259e-05 does NOT clear it (hence extrap_kmin
  in the production fix, see camb-kmin-interpolation-crash.md).
