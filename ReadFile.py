import numpy as np
import math

class ReadFile:

    def __init__(self, dir) :

        self.opts = np.loadtxt(dir)

        # copy them to maintain the originals

        self.cpts = np.copy(self.opts)

        self.latLongToXY()


    def latLongToXY(self) :

        '''

        Calculates the latitude and longitude to coordinates (unit meter)


        '''

        EarthCon = 40192000

        latitude = np.copy(self.opts[:, 0])

        longitude = np.copy(self.opts[:, 1])



        x = ((longitude + 180) / 360 ) * EarthCon

        y = np.zeros(len(latitude))

        for i in range(len(latitude)):

            sinLatitude = math.sin(latitude[i] * math.pi / 180)

            y[i] = ( 0.5 - math.log((1 + sinLatitude) / (1 - sinLatitude)) / 4 / math.pi ) * EarthCon

        
        self.cpts[:, 0] = x
        self.cpts[:, 1] = y
