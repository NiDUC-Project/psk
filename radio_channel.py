from wireless_signal import WirelessSignal
import numpy as np


class Channel:
    def __init__(self, noise_strength=0.1):
        """ Initialize Channel object and set noise_strength attribute

            Parameters
           ----------
            noise_strength : float
                Strength of noises in channel.
        """
        self.__noise_strength = noise_strength

    def set_noise_strength(self, noise_strength):
        """ Set noise_strength attribute

            Parameters
           ----------
            noise_strength : float
                Strength of noises in channel.
        """
        self.__noise_strength = noise_strength

    def send_signal(self, wireless_signal, noise_strength=None):
        """ Get some WirelessSignal and returns that signal with some noise.

            Parameters
           ----------
            wireless_signal : WirelessSignal
                WirelessSignal object to send over the channel

            noise_strength : float
                Strength of noises.

           Returns
           -------
            wireless_signal : WirelessSignal
               Signal with noise.
        """

        # Set noise strength
        if noise_strength is not None:
            self.__noise_strength = noise_strength

        wireless_signal: WirelessSignal

        # Add some noises
        sinwave = wireless_signal.get_sinwave()
        length = len(sinwave)

        noise = self.__noise_strength * np.random.normal(0, 1, length)
        wireless_signal.set_sinwave(sinwave + noise)        # 15 * np.random.randn(length)

        return wireless_signal

    def add_noise_to_complex(self, complex_numbers):
        """ Demodulates given signal (WirelessSignal) to list of bits based on bpsk modulation

           Parameters
           ----------
           complex_numbers: list
                List of complex numbers representing a sine signal

           Returns
           -------
            complex_numbers : list
               List of complex numbers with added noise with strength of channel noise_strength
        """

        # Generate Gauss noise, AWGN with unity power
        noise = (np.random.randn(len(complex_numbers)) + 1j * np.random.randn(len(complex_numbers))) / np.sqrt(2)
        # Add Gauss noise to complex numbers
        complex_numbers = complex_numbers + noise * np.sqrt(self.__noise_strength)
        return complex_numbers
