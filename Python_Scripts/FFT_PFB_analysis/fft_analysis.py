# Use: Casper FFT  
# python fft_analysis.py --cw 0.9 --cw_freq 100e6 --acc 1 --eq 10 --fft_shift 65535 --program
# python fft_analysis.py --cw 0.9 --cw_freq 100e6 --acc 1 --eq 10 --fft_shift 65535

# Use: Xilinx FFT
# python fft_analysis.py --cw 0.99 --cw_freq 100e6 --wgn 0.07 --acc 1024 --eq 100 --mix_freq 100e6 --fft_shift 21845 --program
# python fft_analysis.py --cw 0.99 --cw_freq 100e6 --wgn 0.07 --acc 1024 --eq 100 --mix_freq 100e6 --fft_shift 21845 

import time,corr2,casperfpga,sys,struct,pylab
import numpy as np
import argparse
from IPython import embed
import fft_plotting
import set_registers
import snapshots

host = 'skarab02080A-01'

# WB: CASPER FFT
prog_file = "/home/avanderbyl/fpgs/dds_cwg_32k_fft_wb_2022-08-22_1645.fpg"
# prog_file = "/home/avanderbyl/fpgs/dds_cwg_32k_pfb_wb_2022-08-09_2044.fpg"

# NB: Xilinx FFT
# prog_file = "/home/avanderbyl/fpgs/dds_cwg_32k_fft_nb_2022-08-19_1634.fpg"
# prog_file = "/home/avanderbyl/fpgs/dds_cwg_32k_pfb_nb_2022-08-22_1052.fpg"

#==============================================================================
#   Classes and methods
#==============================================================================
     
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

def data_analysis(data):
	print 'Max value: ',np.max(data)
	print 'Max value position: ',np.argmax(data)
	fft_plotting.plot_vacc_data(data)

def run_fft_tests(f, args):
	# Is this the FFT or PFB version?
	if prog_file.find('pfb') >= 0:
		print 'PFB in design'
		pfb = True
	else:
		print 'Only FFT in design'
		pfb = False

	# Is this the CASPER FFT or Xilinx FFT version?
	if prog_file.find('wb') >= 0:
		print 'Wideband design under test'
		wideband = True

	else: # NB (Xilinx FFT)
		print 'Narrowband design under test'
		wideband = False
		set_registers.set_mixer_freq(f, mix_freq=args.mix_freq)

	# Set parameters
	set_registers.set_fft_shift(f, shift=args.fft_shift)
	set_registers.set_eq(f, eq=args.eq)
	set_registers.set_wng_generator(f, scale=args.wgn)
	set_registers.set_cw_generator(f, scale=args.cw, freq=args.cw_freq)
	set_registers.set_vacc(f, acc_len=args.acc)

	# Arm snapshots
	snapshots.arm_adc_snapshots(f)

	if pfb:
		if wideband:
			snapshots.arm_pfb_wb_snapshots(f)
		else:			
			snapshots.arm_pfb_nb_snapshots(f)
	else:
		if wideband:
			snapshots.arm_fft_wb_snapshots(f)
		else:
			snapshots.arm_fft_nb_snapshots(f)

	snapshots.arm_quant_snapshots(f)
	snapshots.arm_vacc_in_snapshots(f)
	snapshots.arm_vacc_snapshots(f)

	# Sleep
	time.sleep(0.5)

	# Issue manual sync
	manual_sync(f)

	# List to hold results
	data = []

	# Read Snapshot data
	# adc_data = snapshots.read_adc_snapshots(f)
	# data.append((snapshots.read_adc_snapshots(f), 'adc'))

	# Read FFT/PFB Snapshots and plot
	if pfb:
		if wideband:
			name = 'CASPER FFT with PFB'
			data.append((snapshots.read_pfb_wb_snapshots(f), name))
		else:
			name = 'Xil FFT with PFB'
			data.append((snapshots.read_pfb_nb_snapshots(f), name))
	else:
		if wideband:
			name = 'CASPER FFT without PFB'
			data.append((snapshots.read_fft_wb_snapshots(f), name))
		else:
			name = 'Xil FFT w/o PFB'
			data.append((snapshots.read_fft_nb_snapshots(f), name))

	data.append((snapshots.read_quant_snapshots(f), name + ' ' + '(Quant)'))
	# data.append((snapshots.read_vacc_in_snapshots(f), name + ' ' + '(VACC In)'))

	data.append((snapshots.read_vacc_snapshots(f), name + ' ' + '(Acc:'+str(args.acc)+')'))
	
	if args.plot:
		fft_plotting.plot_results_separate(data, args)

	if args.embed:
		embed()

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("--skarab", type=str, default=host, help="Specify SKARAB host")
	parser.add_argument("--program", action="store_true", help="Program FPGA")
	parser.add_argument("--acc", type=int, default=64, help="Number of accumulations")
	parser.add_argument("--cw", type=float, default=0.75, help="CW scale")
	parser.add_argument("--cw_freq", type=float, default=53.5e6, help="CW frequency")
	parser.add_argument("--wgn", type=float, default=2**(-10), help="WGN scale")
	parser.add_argument("--eq", type=int, default=1, help="EQ scale")
	parser.add_argument("--fft_shift", type=int, default=65535, help="FFT shift")
	parser.add_argument("--mix_freq", type=float, default=100e6, help="DDS Mixer frequency")
	parser.add_argument("--embed", action="store_true", default=False, help="Enable Ipython embed")
	parser.add_argument("--plot", action="store_true", default=True, help="Enable plotting")
	args = parser.parse_args()
	print 'Using SKARAB:', args.skarab

	f = casperfpga.CasperFpga(args.skarab)
	program_fpga(f, args, prog_file)
	run_fft_tests(f, args)

if __name__ == '__main__':
	main()




