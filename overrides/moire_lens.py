import numpy as np
import diffractsim
from diffractsim import bd, DOE

class MoireLens(DOE):
    def __init__(self, radius = None, theta = 0, correspondent = False, a = 100000000):
        """
        Creates a Moire lens 
        """

        self.radius = radius
        self.theta = theta
        self.correspondent = correspondent
        self.a = a

    def rotate(self, xx, yy):
        x_new = xx * np.cos(self.theta) - yy * np.sin(self.theta)
        y_new = xx * np.sin(self.theta) + yy * np.cos(self.theta)
        return x_new, y_new

    def get_transmittance(self, xx, yy, λ):
        
        t = 1

        if self.radius != None:
            t = bd.where((xx**2 + yy**2) < self.radius**2, t, bd.zeros_like(xx))

        xx, yy = self.rotate(xx, yy)

        r_2 = xx**2 + yy**2
        phi = np.arctan2(yy, xx)

        phase_shift = np.ceil(r_2*self.a)*phi
        if self.correspondent:
            phase_shift = -phase_shift
        
        t = t*bd.exp(1j*phase_shift)

        return t