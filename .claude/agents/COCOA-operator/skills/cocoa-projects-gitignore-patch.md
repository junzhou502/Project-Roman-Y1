# Skill: keep roman_y1/des_y3 out of COCOA's auto-regenerated projects/.gitignore

## Problem
COCOA's `installation_scripts/start_all_projects.sh` (sourced by every
`start_cocoa.sh`, including inside sbatch jobs) deletes and regenerates
`projects/.gitignore`, appending EVERY project folder name; `stop_all_projects.sh`
deletes the file. The outer Project-Roman-Y1 repo tracks `projects/roman_y1`,
`projects/des_y3`, and a one-line cleared `projects/.gitignore` — the regenerated
list silently hides new files under those projects from `git add`.

## Patch applied (our install only, 2026-07-18)
- `start_all_projects.sh` (append inside the project loop, ~line 81): wrapped the
  `echo "${TMP2:?}" >> .gitignore` in
  `if [ "${TMP2:?}" != "roman_y1" ] && [ "${TMP2:?}" != "des_y3" ]; then ... fi`
  so those two names are never written; other projects keep original behavior.
- `stop_all_projects.sh` (~line 92): replaced `rm -f projects/.gitignore` with
  `echo '# Cleared: project folders are tracked by the Project-Roman-Y1 repo (do not restore the ignore list)' > projects/.gitignore`
  so after stop the file matches the tracked one-liner exactly (clean git status).
  The `rm -f` of external_modules/{data,code}/.gitignore stays (those are untracked).

## Verification method
`bash -c 'conda activate cocoa && cd Cocoa && source start_cocoa.sh; cat projects/.gitignore; source stop_cocoa.sh; cat projects/.gitignore'`
— after start: only roman_fourier/lsst_y1/roman_real listed; after stop: the single
comment line; `git status` clean for .gitignore and new project files visible.
Sourcing start/stop_cocoa is lightweight env setup (safe on login node); it also
recreates the cobaya/likelihoods symlinks, so it does not disturb running chains.

## Caveat
If a new project must be tracked by the outer repo later, add its name to the same
if-condition in start_all_projects.sh.
