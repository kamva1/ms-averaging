import Pyxis
import mqt,lsm
import numpy as np
from pyrap.tables import table
import os
import sys
import pylab
from numpy.linalg import svd
import imager,ms
import pyfits

        ####
def sim():
  # defined your parameters here
        ms_set = "MeerKATlores.MS_p0_p0"
        sr_pos = np.arange(0.,100.,10) # arcmin
        options = {}
        options['gridded_sky.source_flux'] = 1. # bringtness
        options['gridded_sky.grid_m0'] = 0
        options['gridded_sky.grid_l0'] = sr_pos

        os.system("wsclean -size 2048  2048  -scale 2.asec -weight natural -niter 100 -name natural_img -datacolumn DATA -make-psf %s"%ms_set)
        #####


def sim_now():
        radius1 = np.arange(0.,100.,10.)
        #radius1 = np.arange(0.,3,0.3)
        Flux_array1 = np.zeros(len(radius1))

        lores1 = "MeerKATlores.MS_p0_p0"

        imager.cellsize = "10.arcsec"
        imager.npix = 512
        imager.niter = 0

        imager.CLEAN_ALGORITHM = "csclean"

        for k  in range(len(radius1)):

            options = {}
            options['gridded_sky.grid_m0'] = radius1[k]
            options['ms_sel.msname'] = lores1;
            mqt.run("turbo-sim.py",job = "_tdl_job_1_simulate_MS",
                    config="tdlconf.profiles1",section="Sim_source_radius",
                    options=options);

            center_min = -45*60+radius1[k];
            center_deg = math.ceil(center_min/60);
            center_min = abs(center_min - center_deg*60);
            imager.make_image(msname=lores1, column = 'CORRECTED_DATA',
                              phasecenter = "j2000,0h0m,%dd%dm"%(center_deg,center_min),
                              restore = False, dirty = True, restore_lsm = False,
                              weight = "natural");

            f1 = np.max(pyfits.open(imager.DIRTY_IMAGE)[0].data[0][0])
            Flux_array1[k] = f1


            np.save("DATA/Flux1", Flux_array1)
            np.save("DATA/radius1", radius1)



if __name__ == '__main__':
    sim_now()
    sim()
