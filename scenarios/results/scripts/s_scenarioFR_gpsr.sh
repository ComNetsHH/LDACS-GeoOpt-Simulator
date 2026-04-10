#!/bin/bash -l
#SBATCH -p smp
#SBATCH --ntasks 1
#SBATCH --cpus-per-task 1
#SBATCH --mem-per-cpu 1G
#SBATCH --constraint OS9
#SBATCH --array=0-999
#SBATCH --time=5-12:00:00

source "$(cd "$(dirname "$0")" && pwd)/s_common_config.sh"

echo "Using CPU settings: ${NUM_CPUS} cores and ${MEM_PER_CPU} per CPU."
echo "SIM_BINARY: ${SIM_BINARY_GPSR_RELEASE}"
echo "INI_FILE: ${INI_FILE_FR_EF}"
echo "CONFIG: ${GPSR_CONFIG}"
echo "INCL: ${INCL_GPSR}"

opp_runall -j1 "${SIM_BINARY_GPSR_RELEASE}" "${INI_FILE_FR_EF}" -c "${GPSR_CONFIG}" ${INCL_GPSR} -r "${SLURM_ARRAY_TASK_ID}"
