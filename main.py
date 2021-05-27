import utils
import csv

from bitStream.pbm_class import PbmClass
from modulator import Modulator
from demodulator import Demodulator
from noise_to_bit_distortion import NoiseToBitDistortion, Psk
from radio_channel import Channel
from wireless_signal import WirelessSignal
from bitStream.file_binary_io import FileIO


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

    FileIO("computerB\\cloud_bpsk.png").write_to_file(result_bits)


def test_qpsk_picture(noise_strength):
    # tests sending png from computerA to computerB with qpsk
    modulator = Modulator()
    demodulator = Demodulator()
    channel = Channel()

    # send signal to modulator
    bits = FileIO("computerA\\cloud.png").read_from_file()
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
    FileIO("computerB\\recieved_qpsk_cloud.png").write_to_file(result_bits)


def test_8psk_picture(noise_strength):
    # tests sending png from computerA to computerB with 8psk
    modulator = Modulator()
    demodulator = Demodulator()
    channel = Channel()

    # send signal to modulator
    bits = FileIO("computerA\\cloud.png").read_from_file()
    signal = modulator.make_8psk_mod(bits)
    signal.show_signal()

    # send signal to channel
    signal = channel.send_signal(signal, noise_strength)

    # demodulator receives signal
    result_bits = demodulator.make_8psk_demod(signal, channel)

    picture_pbm_result = PbmClass()
    picture_pbm_result.read_wireless_signal_from_bits(result_bits)
    FileIO("computerB\\recieved_8psk_cloud.png").write_to_file(result_bits)


def test_16psk_picture(noise_strength):
    # tests sending png from computerA to computerB with 16psk
    modulator = Modulator()
    demodulator = Demodulator()
    channel = Channel()

    # send signal to modulator
    bits = FileIO("computerA\\cloud.png").read_from_file()
    signal = modulator.make_16psk_mod(bits)
    signal.show_signal()

    # send signal to channel
    signal = channel.send_signal(signal, noise_strength)

    # demodulator receives signal
    result_bits = demodulator.make_16psk_demod(signal, channel)

    picture_pbm_result = PbmClass()
    picture_pbm_result.read_wireless_signal_from_bits(result_bits)
    FileIO("computerB\\recieved_16psk_cloud.png").write_to_file(result_bits)


def wrong_bits_test():
    noise_strength = [0.001, 0.009, 0.01, 0.03, 0.05, 0.1, 0.2, 0.5]
    bpsk = {}
    qpsk = {}
    psk8 = {}
    psk16 = {}

    # tests sending png from computerA to computerB with 16psk
    modulator = Modulator()
    demodulator = Demodulator()
    channel = Channel()

    # send signal to modulator
    bits = FileIO("computerA\\cloud.png").read_from_file()

    for noise in noise_strength:
        # bpsk
        signal1 = modulator.make_bpsk_mod(bits)
        # send signal to channel
        signal1 = channel.send_signal(signal1, noise)
        result_bits1 = demodulator.make_bpsk_demod(signal1, channel)

        # qpsk
        signal2 = modulator.make_qpsk_mod(bits)
        # send signal to channel
        signal2 = channel.send_signal(signal2, noise)
        result_bits2 = demodulator.make_qpsk_demod(signal2, channel)

        # 8psk
        signal3 = modulator.make_8psk_mod(bits)
        # send signal to channel
        signal3 = channel.send_signal(signal3, noise)
        result_bits3 = demodulator.make_8psk_demod(signal3, channel)

        # 16psk
        signal4 = modulator.make_16psk_mod(bits)
        # send signal to channel
        signal4 = channel.send_signal(signal4, noise)
        result_bits4 = demodulator.make_16psk_demod(signal4, channel)

        # wrong bits counters
        wrong_bpsk = 0
        wrong_qpsk = 0
        wrong_8psk = 0
        wrong_16psk = 0

        for i in range(len(result_bits1)):
            # check how many wrong bits
            if bits[i] != result_bits1[i]:
                wrong_bpsk += 1
            if bits[i] != result_bits2[i]:
                wrong_qpsk += 1
            if bits[i] != result_bits3[i]:
                wrong_8psk += 1
            if bits[i] != result_bits4[i]:
                wrong_16psk += 1

        bpsk[noise] = wrong_bpsk
        qpsk[noise] = wrong_qpsk
        psk8[noise] = wrong_8psk
        psk16[noise] = wrong_16psk

    out_file = open('wrong_bits.csv', 'w', newline='')
    headers = ['noise', 'bpsk', 'qpsk', 'psk8', 'psk16', 'oryginal_size']
    writer = csv.DictWriter(out_file, delimiter=';', lineterminator='\n', fieldnames=headers)

    writer.writeheader()

    for i in range(0, 8):
        writer.writerow({'noise': noise_strength[i],
                         'bpsk': str(list(bpsk.values())[i]).replace('.', ','),
                         'qpsk': str(list(qpsk.values())[i]).replace('.', ','),
                         'psk8': str(list(psk8.values())[i]).replace('.', ','),
                         'psk16': str(list(psk16.values())[i]).replace('.', ','),
                         'oryginal_size': len(bits)})

    out_file.close()


# Try sending PNG image through channel using qpsk
def qpsk_send_png(noise_strength):
    bit_list = FileIO("computerA\\cloud.png").read_from_file()
    modulator = Modulator()
    demodulator = Demodulator()
    channel = Channel()
    signal = modulator.make_qpsk_mod(bit_list)
    signal.show_signal()

    # With noise=0.1 the image is completely shattered, with noise=0.01 the image is fine
    signal = channel.send_signal(signal, noise_strength)

    result_bits = demodulator.make_qpsk_demod(signal, channel)

    FileIO("computerB\\cloud.png").write_to_file(result_bits)


def qpsk_img_compute_distorsion(noise_strength):
    bit_list = FileIO("computerA\\cloud.png").read_from_file()
    modulator = Modulator()
    demodulator = Demodulator()
    channel = Channel()
    signal = modulator.make_qpsk_mod(bit_list)

    # With noise=0.1 the image is completely shattered, with noise=0.01 the image is fine
    signal = channel.send_signal(signal, noise_strength)

    result_bits = demodulator.make_qpsk_demod(signal, channel)
    print("Number of distorted bits: ", utils.compute_distorted_bits(bit_list, result_bits))


noise_strength = 0.1
# test_bpsk(noise_strength)
# test_bpsk_picture(noise_strength)
# test_qpsk(noise_strength)
# test_qpsk_picture(noise_strength)
# test_8psk(noise_strength)
# test_8psk_picture(noise_strength)
# test_16psk(noise_strength)
# test_16psk_picture(noise_strength)
# wrong_bits_test()
# qpsk_img_compute_distorsion(noise_strength)

NoiseToBitDistortion(0.01, 0.5, Psk.Qpsk, 0.02)
