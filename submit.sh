#!/bin/bash
#SBATCH --time=15:00:00
#SBATCH --mem=100M
#SBATCH --output=gen_is.out

echo "Hello $USER! You are on node $HOSTNAME.  The time is $(date)."

module purge
module load miniconda
source activate conda-venv

bash scrape.sh -s 'Ilta-Sanomat' -q korona -f 2020-11-01 -t 2021-02-01 -o 'korona-is-nov-2020-jan-2021.csv' -l 100

# Remove conda env
conda deactivate

echo "Successfully saved result to ./output"