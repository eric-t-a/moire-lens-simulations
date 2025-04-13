import diffractsim
diffractsim.set_backend("CPU")

from diffractsim import nm, mm
from overrides.moire_lens import MoireLens
from overrides.monochromatic_simulator import MoireMonochromaticField


def plot_moire_intensity(lens_2_z_pos, thetaDegree):
    F = MoireMonochromaticField(
        wavelength = 980 * nm, extent_x= 0.8 * mm, extent_y=0.8 * mm, Nx=2048, Ny=2048, intensity =0.01
    )

    lens_radius = 5*mm
    thetaRadians = thetaDegree * 3.141592 / 180

    # add a Moire lens at position z = 0 and then another one at position lens_2_z_pos
    F.add(MoireLens(radius = lens_radius))
    F.propagate(lens_2_z_pos)
    F.add(MoireLens(radius = lens_radius, correspondent= True, theta = thetaRadians))


    # plot the intensity in the focal plane
    I = F.get_intensity()
    longitudinal_profile_rgb, longitudinal_profile_E, extent = F.get_longitudinal_profile( start_distance = 0* mm , end_distance = 40* mm , steps = 80) 

    F.plot_longitudinal_profile_intensity(
        longitudinal_profile_E = longitudinal_profile_E, 
        extent = extent, square_root = True, 
        ylim= [float(extent[0]), -float(extent[0])], 
        lens_2_z_pos = lens_2_z_pos, theta = thetaDegree
    )

lens_2_z_pos = 1*mm 
thetaDegree = 90
plot_moire_intensity(lens_2_z_pos, thetaDegree)


