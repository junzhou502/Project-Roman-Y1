---
name: kicp-cluster-conventions
description: User rules for submitting chain jobs - kicp partition only, don't wait for busy queue, validate via sbatch not trial runs
metadata:
  type: feedback
---

All chain jobs (Roman and DES) must go to the `kicp` partition/account; that is what the
user used for all previous runs. kicp is busy: submitting and confirming PD/R in squeue is
enough — do NOT wait for jobs to start running. Verify new sbatch scripts by careful
comparison against the existing working .sbatch/.yaml files (roman_y1 and des_y3 sbatch/
folders), not by trial runs.
**Why:** user stated this explicitly on 2026-07-17 when the queue was backed up; trial runs
waste queue time and login-node computation is forbidden.
**How to apply:** for any new MCMC/evaluate submission in this project: copy a working
sbatch, sed the names, sanity-check with diff/grep, submit, report job ID + queue state.
Note some existing sbatch dirs have trailing spaces in their names — quote paths, never
create new dirs with trailing spaces. See [[mnu-chain-campaign]].
