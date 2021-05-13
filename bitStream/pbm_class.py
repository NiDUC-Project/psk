import re


class PbmClass:
    def __init__(self, columns=0, rows=0, bits=None):
        """ Initialize PbmClass object and set default attributes

            Parameters
            ----------
            columns: int
                Number of columns
            rows: int
                Number of rows
            bits: list
                List of bits
        """
        if bits is None:
            bits = []
        self.columns = columns
        self.rows = rows
        self.bits = bits

    def write_pbm(self, file_name):
        """ Writes PbmClass objesct to .pbm file

            Parameters
            ----------
            file_name: string
                Name of the outfile
        """
        try:
            file = open(file_name, 'w')

            # Write the header
            string_to_save = 'P1\n'
            # Write columns and rows numbers
            string_to_save += str(self.columns) + ' ' + str(self.rows) + '\n'

            # Write every bit in appropriate order
            index = 0
            for i in range(self.rows):
                for j in range(self.columns):
                    string_to_save += str(self.bits[index])
                    if j < self.columns - 1:
                        string_to_save += ' '
                    index += 1
                if i < self.rows - 1:
                    string_to_save += '\n'

            # Write to file
            file.write(string_to_save)
            file.close()
        except Exception as error:
            print("Exception: {0}".format(error))
            print("Check file name (write pbm)")

    def read_pbm(self, file_name):
        """ Read data from .pbm file to PbmClass object

            Parameters
            ----------
            file_name: string
                Name of infile
        """
        try:
            # Read file content
            file = open(file_name, 'r')
            content = re.split(' |\n|\t ', file.read())

            # Read column number
            self.columns = int(content[1])
            print(self.columns)

            # Read row number
            self.rows = int(content[2])
            print(self.rows)

            # Read bits
            self.bits = content[3:]
            for i in range(0, len(self.bits)):
                if self.bits[i] != '':
                    self.bits[i] = int(self.bits[i])

            # Print bits out
            index = 0
            for i in range(self.rows):
                for j in range(self.columns):
                    print(str(self.bits[index]), end=' ')
                    index += 1
                print()

            file.close()
        except Exception as error:
            print("Exception: {0}".format(error))
            print("Check file name (read pbm)")

    def write_wireless_signal_to_bits(self):
        """ Write PbmClass object to list of bits.
            First byte (8 bits) dedicated for storing binary column number (we should convert it to decimal)
            Second byte (8 bits) dedicated for storing binary row number (we should convert it to decimal)
            Rest of bits dedicated for storing actual bits for bitmap

           Return
           ----------
           bits: list
                List of bits to make PbmClass object from it
        """
        # Convert columns and rows numbers to lists of bits with padding to 8 bits (maximum numbers 256)
        column_bits = list(map(int, f'{self.columns:08b}'))
        row_bits = list(map(int, f'{self.rows:08b}'))

        # Show info about columns and rows
        print("========\nColumns: " + str(column_bits) + "\nRows: " + str(row_bits) + "\n")

        # Add lists of bits together
        bits = column_bits + row_bits + self.bits
        return bits

    def read_wireless_signal_from_bits(self, bits):
        """ Read data from list of bits to the PbmClass object.
            First byte (8 bits) dedicated for storing binary column number (we should convert it to decimal)
            Second byte (8 bits) dedicated for storing binary row number (we should convert it to decimal)
            Rest of bits dedicated for storing actual bits for bitmap

           Parameters
           ----------
           bits: list
                List of bits to make PbmClass object from it
        """
        # Get columns and rows binary numbers
        column_bits = bits[0:8]     # one byte is a number of rows
        row_bits = bits[8:16]       # one byte is a number of columns

        # Change bits to integer
        columns = int("".join(str(x) for x in column_bits), 2)
        rows = int("".join(str(x) for x in row_bits), 2)

        # Show info about columns and rows
        print("========\nColumns: " + str(columns) + "\nRows: " + str(rows) + "\n")

        # Save pbm parameters
        self.columns = columns
        self.rows = rows
        self.bits = bits[16:]

    def multiply_pbm(self, times, out_file):
        """ Enlarge actual bitmap.
            Rows

            Parameters
            ----------
            times: int
                Number representing how many times number of columns and rows should be multiplied
            out_file: string
                Name of the .pbm file that PbmClass object should be saved in
        """
        try:
            # Create new, temporary map
            new_map = []
            # Duplicate bit in every row times "times"
            for x in self.bits:
                for i in range(0, times):
                    new_map.append(x)

            # Assign new_map to self.bits
            self.bits = new_map
            # Save new columns number
            self.columns = self.columns * times

            # Create new, temporary map
            new_map = []
            # Duplicate every row times "times"
            for i in range(self.rows):
                a = self.bits[i * self.columns: i * self.columns + self.columns]
                for j in range(times):
                    new_map.extend(a)

            # Save new columns number
            self.rows = self.rows * times

            # Assign new_map to self.bits
            self.bits = new_map
            # Save new and bigger pbm to .pbm file
            self.write_pbm(out_file)
        except Exception as error:
            print("Exception: {0}".format(error))
            print("Something went wrong during multiplying pbm")
