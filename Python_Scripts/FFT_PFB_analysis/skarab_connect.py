import time,corr2,casperfpga,sys,struct,pylab
import numpy as np
import argparse
from IPython import embed

host = 'skarab02080A-01'

prog_file = "/home/avanderbyl/fpgs/dds_cwg_32k_fft_nb_2022-08-18_2134.fpg"


def program_fpga(f, args, prog_file):
	if args.program:
		print 'Programming FPGA:', prog_file
		# program_fpga(f, prog_file)
		f.upload_to_ram_and_program(prog_file)
		f.get_system_information(prog_file)
	else:
		print 'Getting system information using', prog_file
		f.get_system_information(prog_file)

def system_reset(f):
	print 'Issue sync'
	f.registers.control.write(sys_rst='pulse')

def manual_sync(f):
	print 'Issue sync'
	f.registers.man_sync.write(sync='pulse')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--skarab", type=str, default=host, help="Specify SKARAB host")
    parser.add_argument("--program", action="store_true", help="Program FPGA")
    parser.add_argument("--sync", action="store_true", help="Issue sync")
    parser.add_argument("--reset", action="store_true", help="Issue reset")
    args = parser.parse_args()
    print 'Using SKARAB:', args.skarab
    
    f = casperfpga.CasperFpga(args.skarab)
    program_fpga(f, args, prog_file)

    if args.sync:
        manual_sync(f)
    
    if args.reset:
        system_reset(f)

if __name__ == '__main__':
	main()
