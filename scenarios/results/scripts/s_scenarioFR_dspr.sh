#!/bin/bash -l
#SBATCH -p smp
#SBATCH --ntasks 1
#SBATCH --cpus-per-task 1
#SBATCH --mem-per-cpu 1G
#SBATCH --array=0-999
#SBATCH --constraint OS9
#SBATCH --time=5-12:00:00

source "$(cd "$(dirname "$0")" && pwd)/s_common_config.sh"
trap 'set_dijkstra_imports disable' EXIT
set_dijkstra_imports enable

echo "Using CPU settings: ${NUM_CPUS} cores and ${MEM_PER_CPU} per CPU."
echo "SIM_BINARY: ${SIM_BINARY_DSPR_RELEASE}"
echo "INI_FILE: ${INI_FILE_FR_EF}"
echo "CONFIG: ${DSPR_CONFIG}"
echo "INCL: ${INCL_DSPR}"

opp_runall -j1 "${SIM_BINARY_DSPR_RELEASE}" "${INI_FILE_FR_EF}" -c "${DSPR_CONFIG}" ${INCL_DSPR} -r "${SLURM_ARRAY_TASK_ID}"
