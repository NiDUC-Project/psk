import numpy as np
from wireless_signal import WirelessSignal


class Modulator:
    def __init__(self, period=6, frequency=1/6.0, amplitude=1, sample_rate=100):
        """ Set default parameters for modulation

            Parameters
            ----------
            period : number (int, float...)
                Period
            frequency: float
                Frequency, inverse of period
            amplitude: number (int, float...)
                Amplitude, signal strength
            sample_rate: int
                Sample rate, number of samples per milisecond
        """
        self.__period = period
        self.__frequency = frequency
        self.__amplitude = amplitude
        self.__sample_rate = sample_rate

    def make_bpsk_mod(self, bits):
        """ Generates WirelessSignal object from given list of bits.
            WirelessSignal objects contains linspace and sinwave.

           Parameters
           ----------
           bits : list
               List of bits to generate sinwave from it

           Returns
           -------
           signal : WirelessSignal
               Signal generated from bits
        """

        # x-axis, time
        start_time = 0
        end_time = self.__period * len(bits)                                       # period times number of bits
        timeline = np.arange(start_time, end_time, 1 / self.__sample_rate)         # timeline for all bits

        # Phase
        theta1 = 0      # for coding binary 1
        theta2 = np.pi  # for coding binary 0

        # sin
        # two single period sinwaves with opposites phases
        sample_sin_time = np.arange(0, self.__period, 1 / self.__sample_rate)
        sinwave1 = self.__amplitude * np.sin(2 * np.pi * self.__frequency * sample_sin_time + theta1)
        sinwave2 = self.__amplitude * np.sin(2 * np.pi * self.__frequency * sample_sin_time + theta2)

        # sinwave for final signal
        sinwave = []

        for bit in bits:
            # add a single period of sinwave for different value of bits
            if bit == 1:
                sinwave.extend(sinwave1)    # if bit == 1 add period with phase 0
            elif bit == 0:
                sinwave.extend(sinwave2)    # if bit == 0 add period with phase 1

        print(len(bits))
        out_signal = WirelessSignal(timeline, sinwave)
        return out_signal
