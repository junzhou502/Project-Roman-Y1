#!/bin/bash
#SBATCH --job-name=des_y1_mnu_kmin_mcmc
#SBATCH --output=des_y1_mnu_kmin_mcmc_%j.out          
#SBATCH --error=des_y1_mnu_kmin_mcmc_%j.err            
#SBATCH --time=48:00:00
#SBATCH --nodes=1                   
#SBATCH --ntasks=4                           # 4 MPI ranks (chains)
#SBATCH --ntasks-per-node=4
#SBATCH --cpus-per-task=12                   # 8 OMP threads per rank
#SBATCH --partition=kicp                  # Midway3 partition
#SBATCH --account=kicp                 # your group account
#SBATCH --exclusive

echo "Running on host: $(hostname)"
echo "Start time:      $(date '+%Y-%m-%d %H:%M:%S')"
echo "Working dir:     $(pwd)"
echo Slurm job NAME is $SLURM_JOB_NAME
echo Slurm job ID is $SLURM_JOB_ID
echo Number of task is $SLURM_NTASKS
echo Number of cpus per task is $SLURM_CPUS_PER_TASK

cd /project/chihway/junzhou
source ./miniconda3/etc/profile.d/conda.sh
conda activate cocoa
#module load openmpi/4.1.0

echo "Conda environment: $CONDA_DEFAULT_ENV"
echo "MPI version: $(mpirun --version | head -1)"

cd ./Project-Roman-Y1/cocoa/Cocoa
source start_cocoa.sh

export OMP_PROC_BIND=close
if [ -n "$SLURM_CPUS_PER_TASK" ]; then
  export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
else
  export OMP_NUM_THREADS=1
fi

mpirun -n 4 \
  --mca pml ob1 \
  --mca mtl ^ofi,^psm2 \
  --mca btl vader,tcp,self \
  --bind-to core:no-overload \
  --map-by numa:pe=${OMP_NUM_THREADS} \
  cobaya-run ./projects/des_y3/des_y1_mnu_kmin_mcmc.yaml -f
