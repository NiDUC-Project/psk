import numpy as np

from demodulator import Demodulator
from wireless_signal import WirelessSignal


class Modulator:
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

        # We need to check if signal has odd number of bits
        odd_number_of_bits = False

        # Deal with odd-sized signal
        if len(signalBits) % 2 != 0:
            signalBits.append(0)
            odd_number_of_bits = True

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

        # save information about odd number of bits
        if odd_number_of_bits:
            signal.was_odd = True

        demodulator = Demodulator()
        return signal

    def make_8psk_mod(self, bits):
        """ Generates WirelessSignal object from given list of bits in 8-phase-shift keying.
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

        # We need to check if signal's number of bits can be defined as 3n
        one_number_of_bits = False
        two_number_of_bits = False

        # Deal with rest equal 2
        if len(signalBits) % 3 == 2:
            signalBits.append(0)
            two_number_of_bits = True
        # Deal with rest equal 1
        if len(signalBits) % 3 == 1:
            signalBits.append(0)
            signalBits.append(0)
            one_number_of_bits = True

        start_time = 0
        end_time = self.__period * len(signalBits) / 3
        timeline = np.arange(start_time, end_time, 1 / self.__sample_rate)

        theta1 = np.pi / 8  # coding 000
        theta2 = 3 * np.pi / 8  # coding 001
        theta3 = 5 * np.pi / 8  # coding 010
        theta4 = 7 * np.pi / 8  # coding 011
        theta5 = 9 * np.pi / 8  # coding 100
        theta6 = 11 * np.pi / 8  # coding 101
        theta7 = 13 * np.pi / 8  # coding 110
        theta8 = 15 * np.pi / 8  # coding 111

        # Generate corresponding sinwaves with length of period
        linspace = np.arange(0, self.__period, 1 / self.__sample_rate)
        sinwave1 = self.__amplitude * np.sin(2 * np.pi * self.__frequency * linspace + theta1)
        sinwave2 = self.__amplitude * np.sin(2 * np.pi * self.__frequency * linspace + theta2)
        sinwave3 = self.__amplitude * np.sin(2 * np.pi * self.__frequency * linspace + theta3)
        sinwave4 = self.__amplitude * np.sin(2 * np.pi * self.__frequency * linspace + theta4)
        sinwave5 = self.__amplitude * np.sin(2 * np.pi * self.__frequency * linspace + theta5)
        sinwave6 = self.__amplitude * np.sin(2 * np.pi * self.__frequency * linspace + theta6)
        sinwave7 = self.__amplitude * np.sin(2 * np.pi * self.__frequency * linspace + theta7)
        sinwave8 = self.__amplitude * np.sin(2 * np.pi * self.__frequency * linspace + theta8)

        sinwave = []

        for i in range(0, len(signalBits) - 1, 3):
            if signalBits[i] == 0 and signalBits[i + 1] == 0 and signalBits[i + 2] == 0:  # theta1 case
                sinwave.extend(sinwave1)
            elif signalBits[i] == 0 and signalBits[i + 1] == 0 and signalBits[i + 2] == 1:  # theta2 case
                sinwave.extend(sinwave2)
            elif signalBits[i] == 0 and signalBits[i + 1] == 1 and signalBits[i + 2] == 0:  # theta3 case
                sinwave.extend(sinwave3)
            elif signalBits[i] == 0 and signalBits[i + 1] == 1 and signalBits[i + 2] == 1:  # theta4 case
                sinwave.extend(sinwave4)
            elif signalBits[i] == 1 and signalBits[i + 1] == 0 and signalBits[i + 2] == 0:  # theta5 case
                sinwave.extend(sinwave5)
            elif signalBits[i] == 1 and signalBits[i + 1] == 0 and signalBits[i + 2] == 1:  # theta6 case
                sinwave.extend(sinwave6)
            elif signalBits[i] == 1 and signalBits[i + 1] == 1 and signalBits[i + 2] == 0:  # theta7 case
                sinwave.extend(sinwave7)
            elif signalBits[i] == 1 and signalBits[i + 1] == 1 and signalBits[i + 2] == 1:  # theta8 case
                sinwave.extend(sinwave8)
        signal = WirelessSignal(timeline, sinwave)

        # save information about rest of bits
        if one_number_of_bits:
            signal.was_one = True
        if two_number_of_bits:
            signal.was_two = True

        demodulator = Demodulator()
        return signal

    def make_16psk_mod(self, bits):
        """ Generates WirelessSignal object from given list of bits in 16-phase-shift keying.
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

        # We need to check if signal's number of bits can be defined as 4n
        one_number_of_bits = False
        two_number_of_bits = False
        three_number_of_bits = False
        # Deal with rest equal 3
        if len(signalBits) % 4 == 3:
            signalBits.append(0)
            three_number_of_bits = True
        # Deal with rest equal 2
        if len(signalBits) % 4 == 2:
            signalBits.append(0)
            signalBits.append(0)
            two_number_of_bits = True
        # Deal with rest equal 1
        if len(signalBits) % 4 == 1:
            signalBits.append(0)
            signalBits.append(0)
            signalBits.append(0)
            one_number_of_bits = True

        start_time = 0
        end_time = self.__period * len(signalBits) / 4
        timeline = np.arange(start_time, end_time, 1 / self.__sample_rate)

        theta1 = np.pi / 16  # coding 0000
        theta2 = 3 * np.pi / 16  # coding 0001
        theta3 = 5 * np.pi / 16  # coding 0010
        theta4 = 7 * np.pi / 16  # coding 0011
        theta5 = 9 * np.pi / 16  # coding 0100
        theta6 = 11 * np.pi / 16  # coding 0101
        theta7 = 13 * np.pi / 16  # coding 0110
        theta8 = 15 * np.pi / 16  # coding 0111
        theta9 = 17 * np.pi / 16  # coding 1000
        theta10 = 19 * np.pi / 16  # coding 1001
        theta11 = 21 * np.pi / 16  # coding 1010
        theta12 = 23 * np.pi / 16  # coding 1011
        theta13 = 25 * np.pi / 16  # coding 1100
        theta14 = 27 * np.pi / 16  # coding 1101
        theta15 = 29 * np.pi / 16  # coding 1110
        theta16 = 31 * np.pi / 16  # coding 1111
        # Generate corresponding sinwaves with length of period
        linspace = np.arange(0, self.__period, 1 / self.__sample_rate)
        sinwave1 = self.__amplitude * np.sin(2 * np.pi * self.__frequency * linspace + theta1)
        sinwave2 = self.__amplitude * np.sin(2 * np.pi * self.__frequency * linspace + theta2)
        sinwave3 = self.__amplitude * np.sin(2 * np.pi * self.__frequency * linspace + theta3)
        sinwave4 = self.__amplitude * np.sin(2 * np.pi * self.__frequency * linspace + theta4)
        sinwave5 = self.__amplitude * np.sin(2 * np.pi * self.__frequency * linspace + theta5)
        sinwave6 = self.__amplitude * np.sin(2 * np.pi * self.__frequency * linspace + theta6)
        sinwave7 = self.__amplitude * np.sin(2 * np.pi * self.__frequency * linspace + theta7)
        sinwave8 = self.__amplitude * np.sin(2 * np.pi * self.__frequency * linspace + theta8)
        sinwave9 = self.__amplitude * np.sin(2 * np.pi * self.__frequency * linspace + theta9)
        sinwave10 = self.__amplitude * np.sin(2 * np.pi * self.__frequency * linspace + theta10)
        sinwave11 = self.__amplitude * np.sin(2 * np.pi * self.__frequency * linspace + theta11)
        sinwave12 = self.__amplitude * np.sin(2 * np.pi * self.__frequency * linspace + theta12)
        sinwave13 = self.__amplitude * np.sin(2 * np.pi * self.__frequency * linspace + theta13)
        sinwave14 = self.__amplitude * np.sin(2 * np.pi * self.__frequency * linspace + theta14)
        sinwave15 = self.__amplitude * np.sin(2 * np.pi * self.__frequency * linspace + theta15)
        sinwave16 = self.__amplitude * np.sin(2 * np.pi * self.__frequency * linspace + theta16)

        sinwave = []

        for i in range(0, len(signalBits) - 1, 4):
            if signalBits[i] == 0 and signalBits[i + 1] == 0 and signalBits[i + 2] == 0 and signalBits[
                i + 3] == 0:  # theta1 case
                sinwave.extend(sinwave1)
            elif signalBits[i] == 0 and signalBits[i + 1] == 0 and signalBits[i + 2] == 0 and signalBits[
                i + 3] == 1:  # theta2 case
                sinwave.extend(sinwave2)
            elif signalBits[i] == 0 and signalBits[i + 1] == 0 and signalBits[i + 2] == 1 and signalBits[
                i + 3] == 0:  # theta3 case
                sinwave.extend(sinwave3)
            elif signalBits[i] == 0 and signalBits[i + 1] == 0 and signalBits[i + 2] == 1 and signalBits[
                i + 3] == 1:  # theta4 case
                sinwave.extend(sinwave4)
            elif signalBits[i] == 0 and signalBits[i + 1] == 1 and signalBits[i + 2] == 0 and signalBits[
                i + 3] == 0:  # theta5 case
                sinwave.extend(sinwave5)
            elif signalBits[i] == 0 and signalBits[i + 1] == 1 and signalBits[i + 2] == 0 and signalBits[
                i + 3] == 1:  # theta6 case
                sinwave.extend(sinwave6)
            elif signalBits[i] == 0 and signalBits[i + 1] == 1 and signalBits[i + 2] == 1 and signalBits[
                i + 3] == 0:  # theta7 case
                sinwave.extend(sinwave7)
            elif signalBits[i] == 0 and signalBits[i + 1] == 1 and signalBits[i + 2] == 1 and signalBits[
                i + 3] == 1:  # theta8 case
                sinwave.extend(sinwave8)
            elif signalBits[i] == 1 and signalBits[i + 1] == 0 and signalBits[i + 2] == 0 and signalBits[
                i + 3] == 0:  # theta9 case
                sinwave.extend(sinwave9)
            elif signalBits[i] == 1 and signalBits[i + 1] == 0 and signalBits[i + 2] == 0 and signalBits[
                i + 3] == 1:  # theta10 case
                sinwave.extend(sinwave10)
            elif signalBits[i] == 1 and signalBits[i + 1] == 0 and signalBits[i + 2] == 1 and signalBits[
                i + 3] == 0:  # theta11 case
                sinwave.extend(sinwave11)
            elif signalBits[i] == 1 and signalBits[i + 1] == 0 and signalBits[i + 2] == 1 and signalBits[
                i + 3] == 1:  # theta12 case
                sinwave.extend(sinwave12)
            elif signalBits[i] == 1 and signalBits[i + 1] == 1 and signalBits[i + 2] == 0 and signalBits[
                i + 3] == 0:  # theta13 case
                sinwave.extend(sinwave13)
            elif signalBits[i] == 1 and signalBits[i + 1] == 1 and signalBits[i + 2] == 0 and signalBits[
                i + 3] == 1:  # theta14 case
                sinwave.extend(sinwave14)
            elif signalBits[i] == 1 and signalBits[i + 1] == 1 and signalBits[i + 2] == 1 and signalBits[
                i + 3] == 0:  # theta15 case
                sinwave.extend(sinwave15)
            elif signalBits[i] == 1 and signalBits[i + 1] == 1 and signalBits[i + 2] == 1 and signalBits[
                i + 3] == 1:  # theta16 case
                sinwave.extend(sinwave16)
        signal = WirelessSignal(timeline, sinwave)

        # save information about rest of bits
        if one_number_of_bits:
            signal.was_one = True
        if two_number_of_bits:
            signal.was_two = True
        if three_number_of_bits:
            signal.was_three = True

        demodulator = Demodulator()
        return signal
