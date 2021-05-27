import enum

import utils
from bitStream.file_binary_io import FileIO
from demodulator import Demodulator
from modulator import Modulator
from radio_channel import Channel
import numpy as np
from matplotlib import pyplot as plt


class Psk(enum.Enum):
    """
    Types of psk.
    """
    Bpsk = 0,
    Qpsk = 1,
    Psk8 = 2,
    Psk16 = 3


class NoiseToBitDistortion:
    """
    Test relationship between noise and bit distortion in chosen psk.
    Draw results as a chart.
    """

    def __init__(self, start_noise: float, end_noise: float, psk_type: Psk, step=0.01):
        """
        Start benchmarking.
        Parameters
        ----------
        start_noise Starting noise.
        end_noise Ending noise (max to be reached).
        psk_type Type of psk to be tested.
        step Noise increase unit.
        """
        self.start_noise = start_noise
        self.end_noise = end_noise
        self.psk_type = psk_type
        self.distorter = None
        self.step = step
        if psk_type == Psk.Bpsk:
            self.distorter = self.bpsk
        elif psk_type == Psk.Qpsk:
            self.distorter = self.qpsk
        elif psk_type == Psk.Psk8:
            self.distorter = self.psk8
        elif psk_type == Psk.Psk16:
            self.distorter = self.psk16
        self.original_bits = FileIO("computerA\\cloud.png").read_from_file()
        self._start()

    @staticmethod
    def bpsk(input_bits, noise):
        """
        Perform simple bpsk modulation-demodulation and return received bits.
        Parameters
        ----------
        input_bits Bits to be trensfered.
        noise Noise strength.

        Returns
        -------
        bits Received bits.
        """
        modulator = Modulator()
        demodulator = Demodulator()
        channel = Channel()
        signal = modulator.make_bpsk_mod(input_bits)

        signal = channel.send_signal(signal, noise)

        result_bits = demodulator.make_bpsk_demod(signal, channel)
        return result_bits

    @staticmethod
    def qpsk(input_bits, noise):
        """
        Perform simple qpsk modulation-demodulation and return received bits.
        Parameters
        ----------
        input_bits Bits to be trensfered.
        noise Noise strength.

        Returns
        -------
        bits Received bits.
        """
        modulator = Modulator()
        demodulator = Demodulator()
        channel = Channel()
        signal = modulator.make_qpsk_mod(input_bits)

        signal = channel.send_signal(signal, noise)

        result_bits = demodulator.make_qpsk_demod(signal, channel)
        return result_bits

    @staticmethod
    def psk8(input_bits, noise):
        """
        Perform simple 8-psk modulation-demodulation and return received bits.
        Parameters
        ----------
        input_bits Bits to be trensfered.
        noise Noise strength.

        Returns
        -------
        bits Received bits.
        """
        modulator = Modulator()
        demodulator = Demodulator()
        channel = Channel()
        signal = modulator.make_8psk_mod(input_bits)

        signal = channel.send_signal(signal, noise)

        result_bits = demodulator.make_8psk_demod(signal, channel)
        return result_bits

    @staticmethod
    def psk16(input_bits, noise):
        """
        Perform simple 16-psk modulation-demodulation and return received bits.
        Parameters
        ----------
        input_bits Bits to be trensfered.
        noise Noise strength.

        Returns
        -------
        bits Received bits.
        """
        modulator = Modulator()
        demodulator = Demodulator()
        channel = Channel()
        signal = modulator.make_16psk_mod(input_bits)

        signal = channel.send_signal(signal, noise)

        result_bits = demodulator.make_16psk_demod(signal, channel)
        return result_bits

    def _start(self):
        """
        Internal function that performs the tests and draws resulting chart.
        """
        distorted_bit_axis = []
        noise_axis = []

        for i in range(int(self.start_noise*100), int(self.end_noise*100), int(self.step*100)):
            print("Testing noise=", i/100, "/", self.end_noise)
            out_bits = self.distorter(self.original_bits, i/100)
            num_distorted_bits = utils.compute_distorted_bits(self.original_bits, out_bits)
            distorted_bit_axis.append(num_distorted_bits)
            noise_axis.append(i/100)
        plt.plot(noise_axis, distorted_bit_axis)
        plt.title("Zależność ilości przekłamanych bitów od szumu")
        plt.xlabel("Szum")
        plt.ylabel("Przekłamane bity")
        plt.grid(True)
        plt.show()
