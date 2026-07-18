#!/bin/bash
#SBATCH --job-name=roman_mnu_validate
#SBATCH --output=roman_mnu_validate_%j.out
#SBATCH --error=roman_mnu_validate_%j.err
#SBATCH --time=02:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=12
#SBATCH --partition=caslake
#SBATCH --account=pi-chihway

echo "Running on host: $(hostname)"
echo "Start time:      $(date '+%Y-%m-%d %H:%M:%S')"

cd /project/chihway/junzhou
source ./miniconda3/etc/profile.d/conda.sh
conda activate cocoa

cd ./Project-Roman-Y1/cocoa/Cocoa
source start_cocoa.sh

export OMP_PROC_BIND=close
export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK

cobaya-run ./projects/roman_y1/roman_lsst_41_mnu_validate.yaml -f
cobaya-run ./projects/roman_y1/roman_lsst_60_mnu_validate.yaml -f
cobaya-run ./projects/des_y3/des_y1_mnu_validate.yaml -f
cobaya-run ./projects/des_y3/des_y3_mnu_validate.yaml -f
