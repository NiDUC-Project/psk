from pbm_class import PbmClass
from modulator import Modulator
from demodulator import Demodulator
from radio_channel import Channel
from wireless_signal import WirelessSignal


def test1():
    in_bits = [1, 0, 1, 0, 1, 0, 0]
    modulator = Modulator()
    demodulator = Demodulator()
    channel = Channel()

    signal: WirelessSignal
    # make modulation
    signal = modulator.make_bpsk_mod(in_bits)
    signal.show_signal()
    # send signal over the channel
    signal = channel.send_signal(signal, 0.1)
    signal.show_signal()
    # demodulate the signal
    out_bits = demodulator.make_bpsk_demod(signal, channel)

    print(out_bits)


def test2():
    # tests sending pbm from computerA to computerB with bpsk
    picture_pbm = PbmClass()
    picture_pbm.read_pbm(file_name="computerA\\10_times_small.pbm")
    modulator = Modulator()
    demodulator = Demodulator()
    channel = Channel()

    # send signal to modulator
    bits = picture_pbm.write_wireless_signal_to_bits()
    signal = modulator.make_bpsk_mod(bits)
    signal.show_signal()

    # send signal to channel
    signal = channel.send_signal(signal, 0.4)

    # demodulator receives signal
    result_bits = demodulator.make_bpsk_demod(signal, channel)

    picture_pbm_result = PbmClass()
    picture_pbm_result.read_wireless_signal_from_bits(result_bits)
    # picture_pbm_result.rows = picture_pbm.rows
    # picture_pbm_result.columns = picture_pbm.columns
    # picture_pbm_result.bits = result_bits
    picture_pbm_result.write_pbm("computerB\\recieved.pbm")


def test3():
    # tests magnifying pbm
    picture_pbm = PbmClass()
    picture_pbm.read_pbm("computerA\\small.pbm")
    picture_pbm.multiply_pbm(10, "computerA\\10_times_small.pbm")

def test4():
    # tests sending pbm from computerA to computerB with bpsk
    picture_pbm = PbmClass()
    picture_pbm.read_pbm(file_name="computerA\\10_times_small.pbm")
    modulator = Modulator()
    demodulator = Demodulator()
    channel = Channel()

    # send signal to modulator
    bits = picture_pbm.write_wireless_signal_to_bits()
    signal = modulator.make_qpsk_mod(bits)
    signal.show_signal()

    # send signal to channel
    signal = channel.send_signal(signal, 0.4)

    # demodulator receives signal
    result_bits = demodulator.make_qpsk_demod(signal, channel)

    picture_pbm_result = PbmClass()
    picture_pbm_result.read_wireless_signal_from_bits(result_bits)
    # picture_pbm_result.rows = picture_pbm.rows
    # picture_pbm_result.columns = picture_pbm.columns
    # picture_pbm_result.bits = result_bits
    picture_pbm_result.write_pbm("computerB\\recieved.pbm")

test4()
