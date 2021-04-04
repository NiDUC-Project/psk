import math
import numpy as np
import matplotlib.pylab as plt
from radio_channel import Channel


class Demodulator:
    def __init__(self, period=6, frequency=1/6, amplitude=1, sample_rate=100):
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

    def make_bpsk_demod(self, data_signal, channel):
        """ Demodulates given signal (WirelessSignal) to list of bits based on bpsk modulation

            Parameters
            ----------
            data_signal: WirelessSignal
                Given signal
            channel : Channel
                Channel responsible for delivering data_signal

            Returns
            -------
                bits : list
                List of bits read from given signal
        """
        sinwave = data_signal.get_sinwave()
        complex_numbers = []
        result_data_bits = []

        # pattern sine wave
        theta = 0
        pattern_sin_time = np.arange(0, self.__period, 1 / self.__sample_rate)
        pattern_sinwave = self.__amplitude * np.sin(2 * np.pi * self.__frequency * pattern_sin_time + theta)

        for bit in range(0, len(sinwave), self.__period*self.__sample_rate):
            # take each single period of signal
            start_of_sample = bit
            end_of_sample = bit + self.__period*self.__sample_rate
            sample = sinwave[start_of_sample:end_of_sample]

            # calculate phase shift between pattern and the next fragment of signal
            # dot - iloczyn skalrany dwóch argumentów
            phi = math.acos(np.dot(pattern_sinwave, sample)/(np.linalg.norm(pattern_sinwave)*np.linalg.norm(sample)))
            # print(phi)

            if phi < np.pi/2 or phi >= 3*np.pi/2:       # jeśli faza mieści się w zakresie dla 1
                result_data_bits.append(1)
            elif phi >= np.pi/2 or phi < 3*np.pi/2:     # jeśli faza mieści się w zakresie dla 0
                result_data_bits.append(0)

            # calculate complex number to draw a constalation diagram
            complex_num = np.cos(phi) + 1j * np.sin(phi)
            # print(complex_num)
            # print("Rel_cos: " + str(np.cos(phi)) + " Ima_sin: " + str(np.sin(phi)))
            complex_numbers.append(complex_num)

        complex_numbers = channel.add_noise_to_complex(complex_numbers)
        self.draw_constellation_diagram(complex_numbers)
        return result_data_bits

    @staticmethod
    def draw_constellation_diagram(complex_numbers):
        """ Draw constellation diagram from given list of complex numbers

           Parameters
           ----------
           complex_numbers: list
                list with complex number
       """
        try:
            # draw constelation diagram
            plt.plot(np.real(complex_numbers), np.imag(complex_numbers), '.')
            plt.axhline(0, color='green')
            plt.axvline(0, color='green')
            plt.grid(True)
            plt.show()
        except IOError as error:
            print("OS error: {0}".format(error))
