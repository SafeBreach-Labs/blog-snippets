#!/usr/bin/env python
import sys, struct, random
from string import ascii_letters, digits
from base64 import b64encode, b64decode


def generate_packed_string(magic_str, data):
    encoded_data = b64encode(data)
    return "%s%s%s" % (
        magic_str,
        b64encode(struct.pack("<H", len(encoded_data))),
        encoded_data
        )

def generate_packed_string_longest(magic_str, data, pad_to=0):
    packed_string = generate_packed_string(magic_str, data)
    if len(packed_string) < pad_to:
        packed_string += ''.join(random.choice(ascii_letters + digits) for _ in
         range(pad_to - len(packed_string)))
    return packed_string

def extract_packed_string(magic_str, bin_data):
    magic_offset = bin_data.find(magic_str)
    length_offset = magic_offset + len(magic_str)
    data_length = struct.unpack("<H",
        b64decode(bin_data[length_offset:length_offset+4]))[0]
    return b64decode(bin_data[length_offset+4:length_offset+4+data_length])

def get_file_data(file_path):
    bin_data = None
    with open(file_path, "rb") as f:
        bin_data = f.read()
    return bin_data

def main(argv):
    magic_str = argv[0]
    if len(argv) == 3:
        data_to_exfiltrate = argv[1]
        pad_to = int(argv[2])
        print ("Packed String: %s" % generate_packed_string_longest(magic_str, data_to_exfiltrate, pad_to=pad_to))
        print ("Longest? %s" % (pad_to != 0))
    elif len(argv) == 2:
        bin_data = get_file_data(argv[1])
        print ("Extracted data: %s" % extract_packed_string(magic_str, bin_data))


if __name__ == '__main__':
    argv = sys.argv[1:]
    if len(argv) < 2 or len(argv) > 3:
        print ("Usage: script.py MAGIC_STR [DATA_TO_EXFIL PAD_TO]|[FILE_TO_EXTRACT_DATA_FROM]\n \
            PAD_TO should be 0 if string does not need to be the longest")
    main(argv)
