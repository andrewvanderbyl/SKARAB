import time,corr2,casperfpga,sys,struct,pylab
import numpy as np
import matplotlib.pyplot as plt
import argparse
from IPython import embed


host = 'skarab02080A-01'
#host = 'skarab020406-01'
#host = 'skarab020309-01'

prog_file = "/home/avanderbyl/fpgs/dds_cwg_32k_fft_only_wb_2022-08-09_1247.fpg"
#prog_file = "/home/avanderbyl/fpgs/dds_cwg_32k_pfb_wb_2022-08-02_1953.fpg"

# fft_shift = 65535

#==============================================================================
#   Classes and methods
#==============================================================================
     
def program_fpga(f, prog_file):
        print 'Programming FPGA:', prog_file 
        f.upload_to_ram_and_program(prog_file)
        f.get_system_information(prog_file)   

def set_fft_shift(f, shift):
	print 'Setting FFT Shift:', shift
	f.registers.fft_shift.write(fft_shift=shift)

def set_cw_generator(f,scale=0.7,freq=53.5e6):
	print 'Setting CW Scale:', scale
	print 'Setting CW Freq:', freq
	reg_freq=((freq)*2**27)/1712e6
	f.registers.freq_cwg_input.write(frequency=reg_freq)
	f.registers.cwg_scale.write(scale=scale)

def set_wng_generator(f,scale=2**(-10)):
	print 'Setting WNG Scale:', scale
	f.registers.scale_wng.write(scale=scale)

def set_eq(f,eq=10):
	print 'Setting EQ:', eq
	f.registers.eq.write(eq=eq)

def set_vacc(f, acc_scale=1, acc_len=1):
	f.registers.acc_scale.write(reg=acc_scale)
	f.registers.acc_len.write(reg=acc_len)

def arm_vacc_snapshots(f, man_trig=False, man_valid=False):
	print 'Arming Vacc Snapshots'
	f.snapshots.ss_vacc0_ss.arm(man_trig=man_trig, man_valid=man_valid)
	f.snapshots.ss_vacc1_ss.arm(man_trig=man_trig, man_valid=man_valid)
	f.snapshots.ss_vacc2_ss.arm(man_trig=man_trig, man_valid=man_valid)
	f.snapshots.ss_vacc3_ss.arm(man_trig=man_trig, man_valid=man_valid)

def arm_quant_snapshots(f, man_trig=False, man_valid=False):
	print 'Arming Quant Snapshots'
	f.snapshots.ss_quant_ss.arm(man_trig=man_trig, man_valid=man_valid)

def arm_adc_snapshots(f, man_trig=False, man_valid=False):
	print 'Arming ADC Snapshots'
	f.snapshots.snap_adc_ss.arm(man_trig=man_trig, man_valid=man_valid)

def arm_fft_snapshots(f, man_trig=False, man_valid=False):
	print 'Arming FFT Snapshots'
	f.snapshots.ss_fft_ss.arm(man_trig=man_trig, man_valid=man_valid)

def system_reset(f):
	print 'Issue sync'
	f.registers.control.write(sys_rst='pulse')

def manual_sync(f):
	print 'Issue sync'
	f.registers.man_sync.write(sync='pulse')

def _ss_reconstruct(snapshots):
	recon = []

	for i in range(len(snapshots[0])):
		for ss in snapshots:
			recon.append(ss[i])
	return recon

def _quantss_reconstruct(snapshot):
	recon = []

	for i in range(len(snapshot['data']['r0'])):
		temp = (snapshot['data']['r0'][i]+1j*snapshot['data']['i0'][i],
			snapshot['data']['r1'][i]+1j*snapshot['data']['i1'][i],
			snapshot['data']['r2'][i]+1j*snapshot['data']['i2'][i],
			snapshot['data']['r3'][i]+1j*snapshot['data']['i3'][i])	
		for entry in temp:
			recon.append(entry)

	# embed()
	return recon

def read_vacc_snapshots(f, arm=False):
	print 'Reading Snapshots'
	
	ss0 = f.snapshots.ss_vacc0_ss.read(arm=arm)
	ss1 = f.snapshots.ss_vacc1_ss.read(arm=arm)
	ss2 = f.snapshots.ss_vacc2_ss.read(arm=arm)
	ss3 = f.snapshots.ss_vacc3_ss.read(arm=arm)
	#print 'ss0: ',np.max(ss0['data']['data'])
	#print 'ss1: ',np.max(ss1['data']['data'])
	#print 'ss2: ',np.max(ss2['data']['data'])
	#print 'ss3: ',np.max(ss3['data']['data'])

	#print np.argmax(ss0['data']['data'])
	#print np.argmax(ss1['data']['data'])
	#print np.argmax(ss2['data']['data'])
	#print np.argmax(ss3['data']['data'])
	
	# Reconstruct FFT form SS
	return _ss_reconstruct([ss0['data']['data'],ss1['data']['data'],ss2['data']['data'],ss3['data']['data']])


def read_quant_snapshots(f, arm=False):
	print 'Reading Quant Snapshots'
	return _quantss_reconstruct(f.snapshots.ss_quant_ss.read(arm=arm))

def read_fft_snapshots(f, arm=False):
	print 'Reading FFT Snapshot'
	return _quantss_reconstruct(f.snapshots.ss_fft_ss.read(arm=arm))


def read_adc_snapshots(f, arm=False):
	print 'Reading ADC Snapshots'
	recon = []

	adc = f.snapshots.snap_adc_ss.read(arm=arm)
	
	# embed()
	for i in range(len(adc['data']['p0_d0'])):
		temp =(	adc['data']['p0_d0'][i],
				adc['data']['p0_d1'][i],
				adc['data']['p0_d2'][i],
				adc['data']['p0_d3'][i],
				adc['data']['p0_d4'][i],
				adc['data']['p0_d5'][i],
				adc['data']['p0_d6'][i],
				adc['data']['p0_d7'][i])
		for entry in temp:
			recon.append(entry)

	hist, bins = np.histogram(recon, 31)
	# plt.figure(1)
	# plt.plot(recon)

	# plt.figure(2)
	# plt.plot(hist)

	# plt.show()


def plot_vacc_data(data):
	plt.figure(1)
	plt.plot(data)
	plt.figure(2)
	plt.plot(20*np.log10(np.maximum(data,1e-3)/np.max(data)))
	plt.show()

def plot_spectral_data(data):
	data = np.abs(np.square(data))
	plt.figure(1)
	plt.plot(np.abs(data))
	plt.figure(2)
	plt.plot(20*np.log10(np.maximum(data,1e-3)/np.max(data)))
	plt.show()

def data_analysis(data):
	print 'Max value: ',np.max(data)
	print 'Max value position: ',np.argmax(data)
	plot_vacc_data(data)

def run_fft_tests(f, args):
	# Set parameters
	set_fft_shift(f, shift=args.fft_shift)
	set_eq(f, eq=args.eq)
	set_wng_generator(f, scale=args.wgn)
	set_cw_generator(f, scale=args.cw, freq=args.cw_freq)
	set_vacc(f, acc_len=args.acc)
	arm_adc_snapshots(f)
	arm_fft_snapshots(f)
	arm_quant_snapshots(f)
	arm_vacc_snapshots(f)
	time.sleep(0.5)
	manual_sync(f)
	adc_data = read_adc_snapshots(f)
	fft_data = read_fft_snapshots(f)
	# plot_spectral_data(fft_data)

	quant_data = read_quant_snapshots(f)
	plot_spectral_data(quant_data)

	vacc_data = read_vacc_snapshots(f)
	data_analysis(vacc_data)
	#embed()

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
	args = parser.parse_args()
	print 'Using SKARAB:', args.skarab

	f = casperfpga.CasperFpga(args.skarab)

	if args.program:
		print 'Programming FPGA'
		program_fpga(f, prog_file)		
	else:
		print 'Getting system information using', prog_file		
		f.get_system_information(prog_file)

	run_fft_tests(f, args)

if __name__ == '__main__':
	main()




