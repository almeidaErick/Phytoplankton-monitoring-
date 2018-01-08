import seabreeze.spectrometers as sb
import matplotlib.pyplot as plt
from time import sleep
from random import shuffle
from xbee import XBee
import warnings


class STS:
    """STS class for spectrometer definition"""
    def __init__(self):
        self.intensities_max = []
        self.intensities_min = []
        self.intensities_read = []

        warnings.filterwarnings('ignore')

        devices = sb.list_devices()
        self.spec = sb.Spectrometer(devices[0])
        self.spec.integration_time_micros(12000)
        self.wavelengths = self.spec.wavelengths()
        self.percentage_wave = self.wavelengths
        

    """Read maximum values from the STS spectrometer (example: reflection againts a white surface),
    an store those values into a list for later use in calibration"""
    def calibrate_max(self):
        self.intensities_max = self.spec.intensities()

    """Read minimum values from the STS spectrometer (example: reflection againts a black surface),
    an store those values into a list for later use in calibration"""
    def calibrate_min(self):
        self.intensities_min = self.spec.intensities()

    """Read samples and calibrate readings in order to measure reflectance spectrum and grap those results
    NOTE:
    * This calibration works when comparing the resulting graph and the graph shown by OceanView app.
    * Check oceanView app to see how they do calibration for reflection.
    """
    def read_samples(self):
        plt.xlabel('Wavelengths')
        plt.ylabel('Intensities')
        plt.ylim((0, 100))

        #read samples
        self.intensities_read = self.spec.intensities()

        #calibrate reading according to max and min values, if needed to change just only change the line from below
        self.percentage_wave = 100*(self.intensities_read - self.intensities_min)/(self.intensities_max - self.intensities_min)

        plt.plot(self.wavelengths, self.percentage_wave)
        plt.scatter(self.wavelengths, self.percentage_wave)
        plt.show()

        return self.percentage_wave

    """Read samples and calibrate readings in order to measure fluorescence spectrum and graph those results
    NOTE:
    * This calibration does not work properly, I made it according with the oceanView app, same way as
    reflectance calibration. PLEASE CHECK WHAT OTHER VALUES NEED TO BE CONSIDERED IN ORDER TO GET A PROPER
    CALIBRATION FOR FLUORESCENCE.
    * Check oceanView app to see how they do calibration for fluorescence
    """

    def read_samples_fluo(self):
        plt.xlabel('Wavelengths')
        plt.ylabel('Intensities')

        #read samples
        self.intensities_read = self.spec.intensities()

        #calibrate reading according to max values, if needed to change just only change the line from below
        self.percentage_wave = self.intensities_read - self.intensities_max
        
        plt.plot(self.wavelengths, self.percentage_wave)
        plt.scatter(self.wavelengths, self.percentage_wave)
        plt.show()
