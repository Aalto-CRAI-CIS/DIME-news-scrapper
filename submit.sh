#!/bin/bash
#SBATCH --time=25:00:00
#SBATCH --mem=100M
#SBATCH --output=gen_il_gaza.out

echo "Hello $USER! You are on node $HOSTNAME.  The time is $(date)."

module purge
module load miniconda
source activate conda-venv

bash scrape.sh -s 'Iltalehti' -q "hamas" -f 2023-10-01 -t 2024-02-28 -o 'hamas-il-oct-2023-feb-2024.csv' -l 100

# Remove conda env
conda deactivate

echo "Successfully saved result to ./output"