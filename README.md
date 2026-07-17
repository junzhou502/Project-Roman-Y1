### Project Goal
This project aims to predict the constraining power for Roman Nancy Grace Telescope High Latitude Imaging Survey Year-1 data, providing insights on what cosmological analysis is available for Year-1 data.

### Analyses
There are two parameters needed to be determined: number density and galaxy redshift distribution.

To simplify the question, we start from cosmic shear only.

For number density, there are two exists in literature:
1. LSST DES SRD Y1 (no extra effort)
2. Roman Exposure Time Calculator (need bands, exposure, and other information)

For galaxy redshift distribution, there are two possible way to get:
1. LSST DES SRD Y1 (no extra effort)
2. Roman Exposure Time Calculator (need bands, exposure, and other information)
3. SOMPZ prediction based on some simulations (need someone else run this)

#### Step 1
Using products we already have, first use LSST-Y1 redshift distribution, test number densities of 41, 50 arcmin^-2
Run MCMC or Fisher, compare with DESY1 and DESY3

So we need do the following: (1). retrieve LSST-Y1 redshift distritbution from DESC. (2). Run CosmoCov with a fiducial cosmology, Roman-Y1 survey area, and LSST-Y1 source redshift distribution. (3). Run MCMC or Fisher with simple enough parameterization with Cov. (4) Run DES-Y1 and -Y3, compare with Roman-Y1.
