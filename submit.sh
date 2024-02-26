#!/bin/bash
#SBATCH --time=00:05:00
#SBATCH --mem=100M
#SBATCH --output=gen.out

echo "Hello $USER! You are on node $HOSTNAME.  The time is $(date)."

module purge
module load miniconda
conda env create --file conda-venv.yml
source activate conda-venv

bash scrape.sh -s 'Iltalehti'  -q corona -f 2020-09-01 -t 2020-09-30 -o 'test.csv' -l 5

# Remove conda env
conda env remove --name conda-venv