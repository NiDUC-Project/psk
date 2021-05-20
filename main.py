from bitStream.pbm_class import PbmClass
from modulator import Modulator
from demodulator import Demodulator
from radio_channel import Channel
from wireless_signal import WirelessSignal
from bitStream.FileBinaryIO import FileIO


def test_bpsk(noise_strength):
    in_bits = [1, 0, 1, 0, 1, 0, 0]
    modulator = Modulator()
    demodulator = Demodulator()
    channel = Channel()

    signal: WirelessSignal
    # make modulation
    signal = modulator.make_bpsk_mod(in_bits)
    signal.show_signal()
    # send signal over the channel
    signal = channel.send_signal(signal, noise_strength)
    signal.show_signal()
    # demodulate the signal
    out_bits = demodulator.make_bpsk_demod(signal, channel)

    print(out_bits)


def test_bpsk_picture(noise_strength):
    # tests sending picture from computerA to computerB with bpsk
    modulator = Modulator()
    demodulator = Demodulator()
    channel = Channel()

    # send signal to modulator
    bits = FileIO("computerA\\cloud.png").read_from_file()
    print(bits)
    signal = modulator.make_bpsk_mod(bits)
    signal.show_signal()

    # send signal to channel
    signal = channel.send_signal(signal, noise_strength)

    # demodulator receives signal
    result_bits = demodulator.make_bpsk_demod(signal, channel)

    # picture_pbm_result = PbmClass()
    # picture_pbm_result.read_wireless_signal_from_bits(result_bits)
    # picture_pbm_result.rows = picture_pbm.rows
    # picture_pbm_result.columns = picture_pbm.columns
    # picture_pbm_result.bits = result_bits
    #picture_pbm_result.write_pbm("computerB\\recieved_bpsk.pbm")
    FileIO("computerB\\cloud_bpsk.png").write_to_file(result_bits)


def test_pbm_mul():
    # tests magnifying pbm
    picture_pbm = PbmClass()
    picture_pbm.read_pbm("computerA\\small.pbm")
    picture_pbm.multiply_pbm(10, "computerA\\10_times_small.pbm")


def test_qpsk_picture(noise_strength):
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
    signal = channel.send_signal(signal, noise_strength)

    # demodulator receives signal
    result_bits = demodulator.make_qpsk_demod(signal, channel)

    picture_pbm_result = PbmClass()
    picture_pbm_result.read_wireless_signal_from_bits(result_bits)
    # picture_pbm_result.rows = picture_pbm.rows
    # picture_pbm_result.columns = picture_pbm.columns
    # picture_pbm_result.bits = result_bits
    picture_pbm_result.write_pbm("computerB\\recieved_qpsk.pbm")


def test_qpsk(noise_strength):
    lista = [1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1]
    modulator = Modulator()
    demodulator = Demodulator()
    channel = Channel()

    signal = modulator.make_qpsk_mod(lista)
    signal.show_signal()
    signal = channel.send_signal(signal, noise_strength)
    signal.show_signal()
    bits = demodulator.make_qpsk_demod(signal, channel)
    print(bits)


def test_8psk(noise_strength):
    lista = [0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1]
    modulator = Modulator()
    demodulator = Demodulator()
    channel = Channel()

    signal = modulator.make_8psk_mod(lista)
    signal.show_signal()
    signal = channel.send_signal(signal, noise_strength)
    signal.show_signal()
    bits = demodulator.make_8psk_demod(signal, channel)
    print("Komputer A: ", lista)
    print("Komputer B: ", bits)


def test_16psk(noise_strength):
    lista = [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0,
             1, 0, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1]
    modulator = Modulator()
    demodulator = Demodulator()
    channel = Channel()

    signal = modulator.make_16psk_mod(lista)
    signal.show_signal()
    signal = channel.send_signal(signal, noise_strength)
    signal.show_signal()
    bits = demodulator.make_16psk_demod(signal, channel)
    print("Komputer A: ", lista)
    print("Komputer B: ", bits)


def test_16psk_picture(noise_strength):
    # tests sending pbm from computerA to computerB with bpsk
    picture_pbm = PbmClass()
    picture_pbm.read_pbm(file_name="computerA\\10_times_small.pbm")
    modulator = Modulator()
    demodulator = Demodulator()
    channel = Channel()

    # send signal to modulator
    bits = picture_pbm.write_wireless_signal_to_bits()
    signal = modulator.make_16psk_mod(bits)
    signal.show_signal()

    # send signal to channel
    signal = channel.send_signal(signal, noise_strength)

    # demodulator receives signal
    result_bits = demodulator.make_16psk_demod(signal, channel)

    picture_pbm_result = PbmClass()
    picture_pbm_result.read_wireless_signal_from_bits(result_bits)
    # picture_pbm_result.rows = picture_pbm.rows
    # picture_pbm_result.columns = picture_pbm.columns
    # picture_pbm_result.bits = result_bits
    picture_pbm_result.write_pbm("computerB\\recieved_16psk.pbm")


def test_8psk_picture(noise_strength):
    # tests sending pbm from computerA to computerB with bpsk
    picture_pbm = PbmClass()
    picture_pbm.read_pbm(file_name="computerA\\10_times_small.pbm")
    modulator = Modulator()
    demodulator = Demodulator()
    channel = Channel()

    # send signal to modulator
    bits = picture_pbm.write_wireless_signal_to_bits()
    signal = modulator.make_8psk_mod(bits)
    signal.show_signal()

    # send signal to channel
    signal = channel.send_signal(signal, noise_strength)

    # demodulator receives signal
    result_bits = demodulator.make_8psk_demod(signal, channel)

    picture_pbm_result = PbmClass()
    picture_pbm_result.read_wireless_signal_from_bits(result_bits)
    # picture_pbm_result.rows = picture_pbm.rows
    # picture_pbm_result.columns = picture_pbm.columns
    # picture_pbm_result.bits = result_bits
    picture_pbm_result.write_pbm("computerB\\recieved_8psk.pbm")


# Try sending PNG image through channel using qpsk
def qpsk_send_png(noise_strength):
    bit_list = FileIO('./computerA/cloud.png').read_from_file()
    modulator = Modulator()
    demodulator = Demodulator()
    channel = Channel()
    signal = modulator.make_qpsk_mod(bit_list)
    signal.show_signal()

    # With noise=0.1 the image is completely shattered, with noise=0.01 the image is fine
    signal = channel.send_signal(signal, noise_strength)

    result_bits = demodulator.make_qpsk_demod(signal, channel)

    FileIO('./computerB/cloud.png').write_to_file(result_bits)


# qpsk_send_png(0.06)  # Try sending png file through the channel
noise_strength = 0.13
# test_bpsk(noise_strength)
# test_bpsk_picture(noise_strength)
# test_qpsk(noise_strength)
# test_qpsk_picture(noise_strength)
# test_8psk(noise_strength)
# test_8psk_picture(noise_strength)
# test_16psk(noise_strength)
# test_16psk_picture(noise_strength)
