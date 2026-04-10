#!/bin/bash -l
#SBATCH -p smp
#SBATCH --ntasks 1
#SBATCH --cpus-per-task 1
#SBATCH --mem-per-cpu 1G
#SBATCH --constraint OS9
#SBATCH --time=5-12:00:00

set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
RESULTS_DIR=$(cd "${SCRIPT_DIR}/.." && pwd)

cd "${RESULTS_DIR}"
make build-release -j "$(nproc)"
