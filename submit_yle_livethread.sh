#!/bin/bash
# SBATCH --time=00:10:00
# SBATCH --mem=100M
# SBATCH --output=gen_yle_livethread.out

echo "Hello $USER! You are on node $HOSTNAME.  The time is $(date)."

module purge
module load miniconda
source activate conda-venv

python3 -m utils.fetch_yle_livethreads

# Remove conda env
conda deactivate

echo "Successfully saved result to ./output"
