import numpy as np
import scipy as sp
import camb
import warnings

def binning(vmin, vmax, Nbins: int, domain: str):
    '''
    This function is to calculate the bins under given binning parameters.
    '''
    # Sanity check
    if vmin>=vmax:
        raise ValueError(f'vmin={vmin} should be smaller than vmax={vmax}!')
    domain = domain.lower()
    if domain == 'real' or 'configuration':
                
        logdt = (np.log(vmax) - np.log(vmin))/Nbins
        fac = (2./3.)

        thetas = []
        for i in range(Nbins):
            thetamin = np.exp(np.log(vmin) + (i + 0.)*logdt)
            thetamax = np.exp(np.log(vmin) + (i + 1.)*logdt)
            thetas.append(fac * (thetamax**3 - thetamin**3) / (thetamax**2 - thetamin**2))
        thetas = np.array(thetas)
        return thetas
    elif domain == 'fourier' or 'harmonic':
        logdl = (np.log(vmax) - np.log(vmin))/Nbins
        ell = np.zeros(int(Nbins))
        for i in range(int(Nbins)):
            ell[i] = np.exp(np.log(vmin) + (i + 0.5)*logdl)
        return ell
    else:
        raise ValueError(f'domain={domain} is not acceptable! Consider one of the following: real, configuration, fourier, harmonic.')
    
def comoving_distance(As_1e9= 2.1, 
                      ns    = 0.96605,
                      H0    = 67.32,
                      omegab= 0.0495,
                      omegam= 0.316,
                      mnu   = 0.06,
                      w0pwa = -1.0,
                      w     = -1.0,
                      halofit_version = 'mead2020'
                      ):
    '''
    This function returns redshifts and corresponding comoving ditance given cosmology and CAMB paramteterization.
    Unit of returned comoving distance is Mpc/h.
    '''
    #Sanity check
    Param_latex = ['As_1e9', 'ns', 'H0', 'omegab', 'omegam', 'mnu', 'w0pwa', 'w']
    Param_value = [As_1e9, ns, H0, omegab, omegam, mnu, w0pwa, w]
    Param_range = [[1,3], [0.9, 1], [50,80], [0.03, 0.06], [0.25, 0.35], [0, 0.06], [-2, 0], [-2, 0]]
    for idx, param in enumerate(Param_value):
        if not (Param_range[idx][0]<=param<=Param_range[idx][1]):
            warnings.warn(f'{Param_latex[idx]}={param} is not usual!')
    #Initialize Background Parameter
    As = lambda As_1e9: 1e-9 * As_1e9
    wa = lambda w0pwa, w: w0pwa - w
    omegabh2 = lambda omegab, H0: omegab*(H0/100)**2
    omegach2 = lambda omegam, omegab, mnu, H0: (omegam-omegab)*(H0/100)**2-(mnu*(3.046/3)**0.75)/94.0708
    omegamh2 = lambda omegam, H0: omegam*(H0/100)**2
    pars = camb.set_params(H0=H0, 
                            ombh2=omegabh2(omegab, H0), 
                            omch2=omegach2(omegam, omegab, mnu, H0), 
                            mnu=mnu, 
                            omk=0, 
                            tau=0.0697186,  
                            As=As(As_1e9), 
                            ns=ns, 
                            halofit_version=halofit_version, 
                            lmax=10000,
                            AccuracyBoost=1.0,
                            lens_potential_accuracy=1.0,
                            num_massive_neutrinos=1,
                            nnu=3.046,
                            accurate_massive_neutrino_transfers=False,
                            k_per_logint=15,
                            kmax = 50)
    pars.set_dark_energy(w=w, wa=wa(w0pwa, w), dark_energy_model='ppf')
    results = camb.get_results(pars)
    tmp=1250
    z_interp_1D = np.concatenate((np.linspace(0.0,3.0,max(100,int(0.80*tmp))),
                                    np.linspace(3.001,50.1,max(100,int(0.40*tmp)))),axis=0)
    chi = results.comoving_radial_distance(z_interp_1D) * (H0/100.)
    return z_interp_1D, chi
