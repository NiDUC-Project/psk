def compute_distorted_bits(bit_set_1, bit_set_2) -> int:
    """
    Compare two bit sets and compute number of different bits.
    Parameters
    ----------
    bit_set_1 First bit set to be compared.
    bit_set_2 Second bit set to be compared.

    Returns
    -------
    int Number.
    """
    size = min(len(bit_set_1), len(bit_set_2))
    distorted = 0

    for i in range(0, size):
        if bit_set_1[i] != bit_set_2[i]:
            distorted += 1

    return distorted
