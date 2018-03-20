#!/usr/bin/env python
import sys
import pefile
import logging


RDATA_SEC_NAME = ".rdata\x00\x00"
LOGGING_FORMAT = "[*] %(levelname)s - %(message)s"
OUT_FILE_SUFFIX = "_embeddedstring"

# Initialize logging
logging.basicConfig(format=LOGGING_FORMAT, level=logging.DEBUG)


def get_file_data(file):
	data = ""
	with open(file, "rb") as f:
		data = f.read()
	logging.info("Got %s bytes from file %s" % (len(data), file))
	return data

def output_to_file(original_file, data):
	out_file_name = original_file + OUT_FILE_SUFFIX
	with open(out_file_name, "wb") as of:
		of.write(data)
	logging.info("%s bytes written to file %s" % (len(data), out_file_name))

def embed_string_to_rdata_sec(str_data, file):
	pe = pefile.PE(file)

	rdata_sec = [sec for sec in pe.sections if sec.Name == RDATA_SEC_NAME][0]
	logging.debug("RDATA section in PE found")
	file_data = get_file_data(file)

	# calculate how much free (null) space is in the rdata section
	window_length = len(file_data[rdata_sec.VirtualAddress+rdata_sec.Misc:
		rdata_sec.VirtualAddress+rdata_sec.SizeOfRawData])
	logging.debug("%s free (null) bytes available at end of section" % window_length)
	if window_length < len(str_data):
		logging.error("Insufficient space for string in rdata section")
		exit()

	# embed desired data string into the rdata section, keeping the section size the same
	new_data = file_data[:rdata_sec.VirtualAddress+rdata_sec.Misc] + \
		str_data + chr(0)*(window_length - len(str_data)) + \
		file_data[rdata_sec.VirtualAddress+rdata_sec.SizeOfRawData:]

	logging.debug("Original file length: %s, New file length: %s" % (len(file_data), len(new_data)))
	output_to_file(file, new_data)

if __name__ == '__main__':
	embed_string_to_rdata_sec(*sys.argv[1:])