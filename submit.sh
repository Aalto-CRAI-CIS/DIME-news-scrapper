#!/bin/bash
#SBATCH --time=30:00:00
#SBATCH --mem=100M
#SBATCH --output=gen_yle.out

echo "Hello $USER! You are on node $HOSTNAME.  The time is $(date)."

module purge
module load miniconda
source activate conda-venv

bash scrape.sh -s 'YLE News' -q "gaza" -f 2023-10-01 -t 2024-03-05 -o 'gaza-yle-oct-2023-mar-2024.csv' -l 100
bash scrape.sh -s 'YLE News' -q "hamas" -f 2023-10-01 -t 2024-03-05 -o 'hamas-yle-oct-2023-mar-2024.csv' -l 100

# Remove conda env
conda deactivate

echo "Successfully saved result to ./output"
