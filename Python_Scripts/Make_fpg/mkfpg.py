#! /usr/bin/env python

# Use example: 

# import the python file: import mkfpg

# call method and pass (binary file location, name for fpg, compile directory, output directory):

# mkfpg.mkfpg('/home/jasper/FEng/top.bin','feng.fpg','/home/jasper/FEng/', '~/')


import os
import logging
from optparse import OptionParser
import hashlib  # Added to calculate md5hash of .bin bitstream and add it to the .fpg header
import struct

MAX_IMAGE_CHUNK_SIZE = 1988

def mkfpg(filename_bin, filename_fpg, compile_dir, output_dir):
    """
    This function makes the fpg file header and the final fpg file, which 
    consists of the fpg file header (core_info.tab, design_info.tab and 
    git_info.tab) and the compressed binary file. The fpg file is used
    to configure the ROACH, ROACH2, MKDIG and SKARAB boards.

    :param filename_bin: This is the path and binary file (top.bin) that 
        contains the FPGA programming data.
    :type filename_bin: str
    :param filename_fpg: This is the output time stamped fpg file name
    :type filename_fpg: str
    """
    # files to read from (core_info.tab, design_info.tab and git_info.tab)
    basefile_core = '%s/core_info.tab' % compile_dir
    basefile_design = '%s/design_info.tab' % compile_dir
    basefile_git = '%s/git_info.tab' % compile_dir

    # file, which represents the fpg file header only
    extended_info = '%s/extended_info.kcpfpg' % compile_dir

    # read base files and write to fpg header file in correct format
    with open(extended_info, 'w') as fh4:
        fh4.write('#!/bin/kcpfpg\n')
        fh4.write('?uploadbin\n')
        with open(basefile_core, 'r') as fh1:
            for row in fh1:
                col1, col2, col3, col4 = row.split()
                fh4.write('?register\t'+col1+'\t0x'+col3+'\t0x'+col4+'\n')
        with open(basefile_design, 'r') as fh2:
            line = fh2.readline()
            while line:
                fh4.write('?meta\t' + line)
                line = fh2.readline()
        with open(basefile_git, 'r') as fh3:
            line = fh3.readline()
            while line:
                fh4.write(line)
                line = fh3.readline()
    # add the MD5 Checksums here
    with open(extended_info, 'r') as fh:
        md5_header = hashlib.md5(fh.read()).hexdigest()
    with open(filename_bin, 'rb') as fh:
        bitstream = fh.read()
        # 1) Calculate MD5 Checksum on binary data
        md5_bitstream = hashlib.md5(bitstream).hexdigest()

        # 2) Calculate 'FlashWriteChecksum' to be compared to
        #    SpartanChecksum when upload_to_ram()
        #   - Need to give it the chunk size being used in upload_to_ram
        #   - This alters how the SPARTAN calculates the checksum
        flash_write_checksum = calculate_checksum_using_bitstream(
            bitstream, packet_size=MAX_IMAGE_CHUNK_SIZE)

    # add the md5sums, checksum and ?quit to the extended info file
    with open(extended_info, 'a') as fh:
        # Line to write must follow general format, as per Paul
        line = '77777\t77777\tmd5_header\t' + md5_header + '\n'
        fh.write("?meta\t" + line)
        line = '77777\t77777\tmd5_bitstream\t' + md5_bitstream + '\n'
        fh.write("?meta\t" + line)
        line = '77777\t77777\tflash_write_checksum\t' + \
               str(flash_write_checksum) + '_' + str(MAX_IMAGE_CHUNK_SIZE) + '\n'
        fh.write("?meta\t" + line)
        fh.write('?quit\n')

    # copy binary file from binary file location and rename to system.bin
    mkfpg_cmd1 = 'cp %s %s/system.bin' % (filename_bin, compile_dir)
    os.system(mkfpg_cmd1)
    # compress binary file in new location
    mkfpg_cmd2 = 'gzip -c %s/system.bin > %s/system.bin.gz' % (
        compile_dir, compile_dir)
    os.system(mkfpg_cmd2)
    # append the compressed binary file to the extended_info.kcpfpg file
    mkfpg_cmd3 = 'cat %s/system.bin.gz >> %s/extended_info.kcpfpg' % (
        compile_dir, compile_dir)
    os.system(mkfpg_cmd3)
    # copy extended_info.kcpfpg and rename to time stamped file and
    # place in output directory with the bof file
    mkfpg_cmd4 = 'cp %s/extended_info.kcpfpg %s/%s' % (
        compile_dir, output_dir, filename_fpg)
    os.system(mkfpg_cmd4)

def calculate_checksum_using_bitstream(bitstream, packet_size=8192):
    """
    Summing up all the words in the input bitstream, and returning a
    'Checksum' - Assuming that the bitstream HAS NOT been padded yet
    :param bitstream: The actual bitstream of the file in question
    :param packet_size: max size of image packets that we pad to
    :return: checksum
    """

    size = len(bitstream)

    flash_write_checksum = 0x00

    for i in range(0, size, 2):
        # This is just getting a substring, need to convert to hex
        two_bytes = bitstream[i:i + 2]
        one_word = struct.unpack('!H', two_bytes)[0]
        flash_write_checksum += one_word

    if (size % packet_size) != 0:
        # padding required
        num_padding_bytes = packet_size - (size % packet_size)
        for i in range(num_padding_bytes / 2):
            flash_write_checksum += 0xffff

    # Last thing to do, make sure it is a 16-bit word
    flash_write_checksum &= 0xffff

    return flash_write_checksum
