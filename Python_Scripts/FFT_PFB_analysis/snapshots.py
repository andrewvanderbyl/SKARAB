import numpy as np
from IPython import embed

# ---- Reconstruct ----
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

	return recon

# ---- ARM ----
def arm_adc_snapshots(f, man_trig=False, man_valid=False):
	print 'Arming ADC Snapshot'
	f.snapshots.snap_adc_ss.arm(man_trig=man_trig, man_valid=man_valid)

def arm_fft_wb_snapshots(f, man_trig=False, man_valid=False):
	print 'Arming FFT WB Snapshots'
	f.snapshots.ss_fft_ss.arm(man_trig=man_trig, man_valid=man_valid)

def arm_pfb_wb_snapshots(f, man_trig=False, man_valid=False):
	print 'Arming PFB WB Snapshots'
	f.snapshots.ss_pfb0_ss.arm(man_trig=man_trig, man_valid=man_valid)
	f.snapshots.ss_pfb1_ss.arm(man_trig=man_trig, man_valid=man_valid)

def arm_fft_nb_snapshots(f, man_trig=False, man_valid=False):
	print 'Arming FFT NB Snapshots'
	f.snapshots.ss_fft_ss.arm(man_trig=man_trig, man_valid=man_valid)

def arm_pfb_nb_snapshots(f, man_trig=False, man_valid=False):
	print 'Arming PFB NB Snapshots'
	f.snapshots.ss_pfb_ss.arm(man_trig=man_trig, man_valid=man_valid)

def arm_quant_snapshots(f, man_trig=False, man_valid=False):
	print 'Arming Quant Snapshots'
	f.snapshots.ss_quant_ss.arm(man_trig=man_trig, man_valid=man_valid)

def arm_vacc_in_snapshots(f, man_trig=False, man_valid=False):
	print 'Arming VACC In Snapshot'
	f.snapshots.ss_vacc_in_ss.arm(man_trig=man_trig, man_valid=man_valid)

def arm_vacc_snapshots(f, man_trig=False, man_valid=False):
	print 'Arming Vacc Snapshots'
	f.snapshots.ss_vacc0_ss.arm(man_trig=man_trig, man_valid=man_valid)
	f.snapshots.ss_vacc1_ss.arm(man_trig=man_trig, man_valid=man_valid)
	f.snapshots.ss_vacc2_ss.arm(man_trig=man_trig, man_valid=man_valid)
	f.snapshots.ss_vacc3_ss.arm(man_trig=man_trig, man_valid=man_valid)


# ---- READ ----
def read_adc_snapshots(f, arm=False):
	print 'Reading ADC Snapshots'
	recon = []

	adc = f.snapshots.snap_adc_ss.read(arm=arm)
	
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

def read_fft_wb_snapshots(f, arm=False):
	print 'Reading FFT WB Snapshot'
	return _quantss_reconstruct(f.snapshots.ss_fft_ss.read(arm=arm))

def read_pfb_wb_snapshots(f, arm=False):
	print 'Reading PFB Snapshot'
	ss0 = f.snapshots.ss_pfb0_ss.read(arm=arm)
	ss1 = f.snapshots.ss_pfb1_ss.read(arm=arm)

	recon = []
	for i in range(len(ss0['data']['r0'])):
		temp =(	
			ss0['data']['r0'][i],
			ss0['data']['r1'][i],
			ss1['data']['r2'][i],
			ss1['data']['r3'][i],)
		for entry in temp:
			recon.append(entry)

	return recon

def read_fft_nb_snapshots(f, arm=False):
	print 'Reading FFT NB Snapshot'
	snapshot = f.snapshots.ss_fft_ss.read(arm=arm)
	return np.array(snapshot['data']['real'])+np.array(snapshot['data']['imag'])*1j

def read_pfb_nb_snapshots(f, arm=False):
	print 'Reading PFB NB Snapshot'
	snapshot = f.snapshots.ss_pfb_ss.read(arm=arm)
	return np.array(snapshot['data']['real'])+np.array(snapshot['data']['imag'])*1j	

def read_quant_snapshots(f, arm=False):
	print 'Reading Quant Snapshots'
	return _quantss_reconstruct(f.snapshots.ss_quant_ss.read(arm=arm))

def read_vacc_in_snapshots(f, arm=False):
	print 'Reading VACC In Snapshots'
	
	ss0 = f.snapshots.ss_vacc_in_ss.read(arm=arm)
	ss1 = f.snapshots.ss_vacc_in_ss.read(arm=arm)
	ss2 = f.snapshots.ss_vacc_in_ss.read(arm=arm)
	ss3 = f.snapshots.ss_vacc_in_ss.read(arm=arm)

	return _ss_reconstruct([ss0['data']['d0'],ss1['data']['d1'],ss2['data']['d2'],ss3['data']['d3']])	

def read_vacc_snapshots(f, arm=False):
	print 'Reading VACC Snapshots'
	
	ss0 = f.snapshots.ss_vacc0_ss.read(arm=arm)
	ss1 = f.snapshots.ss_vacc1_ss.read(arm=arm)
	ss2 = f.snapshots.ss_vacc2_ss.read(arm=arm)
	ss3 = f.snapshots.ss_vacc3_ss.read(arm=arm)

	ss0_dv = ss0['data']['dv']
	ss1_dv = ss1['data']['dv']
	ss2_dv = ss2['data']['dv']
	ss3_dv = ss3['data']['dv']

	ss0_trig = ss0['data']['trig']
	ss1_trig = ss1['data']['trig']
	ss2_trig = ss2['data']['trig']
	ss3_trig = ss3['data']['trig']

	# Reconstruct FFT form SS
	return _ss_reconstruct([ss0['data']['data'],ss1['data']['data'],ss2['data']['data'],ss3['data']['data']])