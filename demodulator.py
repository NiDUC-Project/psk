import math
import numpy as np
import matplotlib.pylab as plt
from radio_channel import Channel
from scipy.stats import pearsonr

from wireless_signal import WirelessSignal


class Demodulator:
    def __init__(self, period=6, amplitude=1, sample_rate=100):
        """ Set default parameters for modulation

            Parameters
            ----------
            period : number (int, float...)
                Period
            amplitude: number (int, float...)
                Amplitude, signal strength
            sample_rate: int
                Sample rate, number of samples per milisecond
        """
        self.__period = period
        self.__frequency = 1/period
        self.__amplitude = amplitude
        self.__sample_rate = sample_rate

    def __generate_complex_qpsk(self, data_signal):
        """
        Generate complex number array out out input signal.

        Parameters
        ----------
        data_signal: WirelessSignal
            Reference signal.
        Returns
        -------
            complex_array: array of complex numbers.

        """
        sinwave = data_signal.get_sinwave()
        complex_numbers = []
        theta1 = np.pi / 4  # coding 11
        theta2 = 3 * np.pi / 4  # coding 01
        theta3 = 5 * np.pi / 4  # coding 00
        theta4 = 7 * np.pi / 4  # coding 10
        pattern_sin_time = np.arange(0, self.__period, 1 / self.__sample_rate)
        pattern_sinwave1 = self.__amplitude * np.sin(2 * np.pi * self.__frequency * pattern_sin_time + theta1)
        pattern_sinwave2 = self.__amplitude * np.sin(2 * np.pi * self.__frequency * pattern_sin_time + theta2)
        pattern_sinwave3 = self.__amplitude * np.sin(2 * np.pi * self.__frequency * pattern_sin_time + theta3)
        pattern_sinwave4 = self.__amplitude * np.sin(2 * np.pi * self.__frequency * pattern_sin_time + theta4)

        for bit in range(0, len(sinwave), self.__period * self.__sample_rate):
            # take each single period of signal
            start_of_sample = bit
            end_of_sample = bit + self.__period * self.__sample_rate
            sample = sinwave[start_of_sample:end_of_sample]

            # Find the phase shift using pearson correlation.
            coeff1, _ = pearsonr(sample, pattern_sinwave1)
            coeff2, _ = pearsonr(sample, pattern_sinwave2)
            coeff3, _ = pearsonr(sample, pattern_sinwave3)
            coeff4, _ = pearsonr(sample, pattern_sinwave4)

            maxval = max(coeff1, coeff2, coeff3, coeff4)

            if maxval == coeff1:
                phi = np.pi / 4
            elif maxval == coeff2:
                phi = 3 * np.pi / 4
            elif maxval == coeff3:
                phi = 5 * np.pi / 4
            elif maxval == coeff4:
                phi = 7 * np.pi / 4

            # calculate complex number to draw a constalation diagram
            complex_num = np.cos(phi) + 1j * np.sin(phi)

            complex_numbers.append(complex_num)
        return complex_numbers

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

        for bit in range(0, len(sinwave), self.__period * self.__sample_rate):
            # take each single period of signal
            start_of_sample = bit
            end_of_sample = bit + self.__period * self.__sample_rate
            sample = sinwave[start_of_sample:end_of_sample]

            # calculate phase shift between pattern and the next fragment of signal
            # dot - iloczyn skalrany dwóch argumentów
            phi = math.acos(
                np.dot(pattern_sinwave, sample) / (np.linalg.norm(pattern_sinwave) * np.linalg.norm(sample)))
            # print(phi)

            # ALTERNATYWNA WCZEŚNIEJSZA WERSJA
            # if phi < np.pi/2 or phi >= 3*np.pi/2:       # jeśli faza mieści się w zakresie dla 1
            #     result_data_bits.append(1)
            # elif phi >= np.pi/2 or phi < 3*np.pi/2:     # jeśli faza mieści się w zakresie dla 0
            #     result_data_bits.append(0)

            # calculate complex number to draw a constalation diagram
            complex_num = np.cos(phi) + 1j * np.sin(phi)
            # print(complex_num)
            # print("Rel_cos: " + str(np.cos(phi)) + " Ima_sin: " + str(np.sin(phi)))
            complex_numbers.append(complex_num)

        complex_numbers = channel.add_noise_to_complex(complex_numbers)
        result_data_bits = []
        for com in complex_numbers:
            if np.real(com) > 0:
                result_data_bits.append(1)
            elif np.real(com) <= 0:
                result_data_bits.append(0)

        self.draw_constellation_diagram(complex_numbers)
        return result_data_bits

    def make_qpsk_demod(self, data_signal: WirelessSignal, channel: Channel):
        """ Demodulates given signal (WirelessSignal) to list of bits based on qpsk modulation

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
        complex_numbers = self.__generate_complex_qpsk(data_signal)
        complex_numbers = channel.add_noise_to_complex(complex_numbers)
        result_data_bits = []
        for com in complex_numbers:
            if np.real(com) > 0 and np.imag(com) > 0:  # theta1
                result_data_bits.extend([1, 1])
            elif np.real(com) > 0 and np.imag(com) < 0:  # theta4
                result_data_bits.extend([1, 0])
            elif np.real(com) < 0 and np.imag(com) > 0:  # theta2
                result_data_bits.extend([0, 1])
            elif np.real(com) < 0 and np.imag(com) < 0:  # theta3
                result_data_bits.extend([0, 0])

        # if we had an odd number of bits we added one and now it is necessary, we can remove that
        if data_signal.was_odd is True:
            result_data_bits.pop()

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
            plt.title("Diagram konstalacji syganłu")
            plt.grid(True)
            plt.show()
        except IOError as error:
            print("OS error: {0}".format(error))
