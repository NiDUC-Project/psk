import bitarray


class FileIO:
    def __init__(self, file_name):
        """
        Initialize FileIO class
        Parameters
        ----------
        file_name: string File to be manipulated
        """
        self.file_name = file_name

    def read_from_file(self) -> list:
        """
        Read bits from file and return them as a list.
        Returns: list Array of 1 and 0.
        -------
        """
        with open(self.file_name, "rb") as file:
            a = bitarray.bitarray()
            while byte := file.read(1):
                a.frombytes(byte)
            return a.tolist()

    def write_to_file(self, bits_list):
        """
        Write input list of bits to the file.
        Parameters
        ----------
        bits_list: list List of bits to be written to the file.
        """
        with open(self.file_name, 'wb') as file:
            bits = bitarray.bitarray(bits_list)
            bytes_list = bits.tobytes()
            file.write(bytes_list)