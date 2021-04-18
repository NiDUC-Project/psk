import numpy as np

from demodulator import Demodulator
from wireless_signal import WirelessSignal


class Modulator:
    def __init__(self, period=6, frequency=1 / 6.0, amplitude=1, sample_rate=100):
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
        """ Generates WirelessSignal object from given list of bits in binary phase-shift keying.
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
        end_time = self.__period * len(bits)  # period times number of bits
        timeline = np.arange(start_time, end_time, 1 / self.__sample_rate)  # timeline for all bits

        # Phase
        theta1 = 0  # for coding binary 1
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
                sinwave.extend(sinwave1)  # if bit == 1 add period with phase 0
            elif bit == 0:
                sinwave.extend(sinwave2)  # if bit == 0 add period with phase 1

        # print(len(bits))
        out_signal = WirelessSignal(timeline, sinwave)
        return out_signal

    def make_qpsk_mod(self, bits):
        """ Generates WirelessSignal object from given list of bits in quadrature phase-shift keying.
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

        signalBits = bits.copy()

        # Deal with odd-sized signal
        if len(signalBits) % 2 != 0:
            signalBits.append(0)

        start_time = 0
        end_time = self.__period * len(signalBits) / 2
        timeline = np.arange(start_time, end_time, 1 / self.__sample_rate)

        theta1 = np.pi / 4  # coding 11
        theta2 = 3 * np.pi / 4  # coding 01
        theta3 = 5 * np.pi / 4  # coding 00
        theta4 = 7 * np.pi / 4  # coding 10

        # Generate corresponding sinwaves with length of period
        linspace = np.arange(0, self.__period, 1 / self.__sample_rate)
        sinwave1 = self.__amplitude * np.sin(2 * np.pi * self.__frequency * linspace + theta1)
        sinwave2 = self.__amplitude * np.sin(2 * np.pi * self.__frequency * linspace + theta2)
        sinwave3 = self.__amplitude * np.sin(2 * np.pi * self.__frequency * linspace + theta3)
        sinwave4 = self.__amplitude * np.sin(2 * np.pi * self.__frequency * linspace + theta4)

        sinwave = []

        for i in range(0, len(signalBits)-1, 2):
            if signalBits[i] == 1 and signalBits[i + 1] == 1:  # theta1 case
                sinwave.extend(sinwave1)
            elif signalBits[i] == 0 and signalBits[i + 1] == 1:  # theta2 case
                sinwave.extend(sinwave2)
            elif signalBits[i] == 0 and signalBits[i + 1] == 0:  # theta3 case
                sinwave.extend(sinwave3)
            elif signalBits[i] == 1 and signalBits[i + 1] == 0:  # theta4 case
                sinwave.extend(sinwave4)
        signal = WirelessSignal(timeline, sinwave)

        demodulator = Demodulator()
        return signal
