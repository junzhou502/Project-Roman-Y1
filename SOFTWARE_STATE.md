# Project Name

The Project-Aion-cluster project is based on the astronomical foundation model Aion-1 to achieve two ultimate goals:
- Implement Aion-1 to improve redshift estimation of photomoetry by combining multimodal data
- Implement Aion-1 with sophisticated post-training to predict the probability that a galaxy is the member galaxy of a cluster and is the center of a cluster.

## Project Structure

\`\`\`
Project-Aion-cluster/
├── data/          # Raw data from different surveys
├── jupyter/       # Some Jupyter/python files for developments
├── data_macthed/  # dataset for matched objects across surveys
├── results/       # store some results of scripts
\`\`\`

## File Reference

| File/Folder | Description |
|-------------|-------------|
| `jupyter/Tutorial-Aion-1.py` | tutorial that teaches you basic perspectives of Aion-1 |
| `jupyter/Tutorial-MultimodalUniverse.py` |  tutorial that teaches you how to download the dataset and build a matched dataset|

## Common Commands
'conda activate ml-3.11' : activate the env for this project
'caslake' : apply a intel-CPU computation node
'kicp'    : apply a intel-CPU computation node
'amd'     : apply a amd-CPU computation node
'gpu'     : apply a GPU computation node plus some CPUs


# Install dependencies
first activate env 'conda activate ml-3.11'
then use either
'pip install'
or
'conda install'


## Important Notes

- all actions that can change the conda environment are only allowed for the conda environment 'ml-3.11'
- Don't modify any file outside the project folder 'Project-Aion-cluster'
- Never use 'rm -rf *'
- Never do intense computation at login nodes