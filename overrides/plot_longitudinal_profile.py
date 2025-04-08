import matplotlib.pyplot as plt
import numpy as np
from diffractsim.util.constants import *


def plot_moire_longitudinal_profile_intensity(self,  longitudinal_profile_E, extent,  square_root = False, grid = False, xlim=None, ylim=None, units = mm,  z_units = mm, dark_background = False, lens_2_z_pos = 1*mm, theta = 0):
    """visualize the diffraction pattern longitudinal profile intensity with matplotlib"""

    from diffractsim.util.backend_functions import backend as bd
    from diffractsim.util.backend_functions import backend_name

    if dark_background == True:
        plt.style.use("dark_background")
    else:
        plt.style.use("default")

    I = bd.real(longitudinal_profile_E*np.conjugate(longitudinal_profile_E))
    I = I.transpose(1,0)

    if square_root == False:
        if backend_name == 'cupy':
            I = I.get()
        else:
            I = I

    else:
        if backend_name == 'cupy':
            I = np.sqrt(I.get())
        else:
            I = np.sqrt(I)

    fig = plt.figure(figsize=(16/9 *6,6)) 
    ax = fig.add_subplot(1,1,1)  


    if xlim != None:
        ax.set_xlim(np.array(xlim)/cm)

    if ylim != None:
        ax.set_ylim(np.array(ylim)/units)

    if units == mm:
        ax.set_ylabel("[mm]")
    elif units == um:
        ax.set_ylabel("[um]")
    elif units == cm:
        ax.set_ylabel("[cm]")
    elif units == nm:
        ax.set_ylabel("[nm]")
    elif units == m:
        ax.set_ylabel("[m]")



    if z_units == mm:
        ax.set_xlabel('Screen Distance [mm]')
    elif z_units == um:
        ax.set_xlabel('Screen Distance [um]')
    elif z_units == cm:
        ax.set_xlabel('Screen Distance [cm]')
    elif z_units == nm:
        ax.set_xlabel('Screen Distance [nm]')
    elif z_units == m:
        ax.set_xlabel('Screen Distance [m]')



    ax.set_title("Longitudinal Profile")
    if grid == True:
        ax.grid(alpha =0.2)

    dz = (extent[3] - extent[2])/ I.shape[1]
    im = ax.imshow(I, cmap= 'inferno',  extent = [(extent[2]- dz/2)/z_units ,  (extent[3]+ dz/2)/z_units, float(extent[0]- self.dx/2) / units, float(extent[1]+ self.dx/2) / units],  interpolation='spline36', aspect = 'auto')
    
    cb = fig.colorbar(im, orientation = 'vertical')

    if square_root == False:
        cb.set_label(r'Intensity $\left[W / m^2 \right]$', fontsize=13, labelpad =  14 )
    else:
        cb.set_label(r'Square Root Intensity $\left[ \sqrt{W / m^2 } \right]$', fontsize=13, labelpad =  14 )

    lens_radius = - float(extent[0]) / units

    #lens 1 arrow
    plt.arrow(0, 0, 0, lens_radius, width=lens_radius/10, length_includes_head=True, head_width=lens_radius/3, head_length=lens_radius/7, fc='red', ec='red')
    plt.arrow(0, 0, 0, -lens_radius, width=lens_radius/10, length_includes_head=True, head_width=lens_radius/3, head_length=lens_radius/7, fc='red', ec='red')

    #lens 2 arrow
    plt.arrow(lens_2_z_pos / units, 0, 0, lens_radius, width=lens_radius/10, length_includes_head=True, head_width=lens_radius/3, head_length=lens_radius/7, fc='red', ec='red')
    plt.arrow(lens_2_z_pos / units, 0, 0, -lens_radius, width=lens_radius/10, length_includes_head=True, head_width=lens_radius/3, head_length=lens_radius/7, fc='red', ec='red')

    # distance between lenses
    plt.arrow(lens_2_z_pos / (2 * units), -lens_radius+0.03, lens_2_z_pos / (2 * units), 0, width=lens_radius/100, length_includes_head=True, head_width=lens_radius/30, head_length=lens_radius*10/7, fc='white', ec='white')
    plt.arrow(lens_2_z_pos / (2 * units), -lens_radius+0.03, -lens_2_z_pos / (2 * units), 0, width=lens_radius/100, length_includes_head=True, head_width=lens_radius/30, head_length=lens_radius*10/7, fc='white', ec='white')
    plt.text(0, -lens_radius +0.06, 'd = '+str(round(lens_2_z_pos / units, 1))+"mm", fontsize=12, color='white')

    # rotatio degree
    plt.text(float(extent[3]) / units - 5, -lens_radius +0.06, 'θ = '+str(int(theta))+"°", fontsize=12, color='white')

    plt.show()
    
