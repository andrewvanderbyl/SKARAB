import time,corr2,casperfpga,sys,struct,pylab
from IPython import embed

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

def set_mixer_freq(f,mix_freq):
	print 'Setting DDS mixer frequency:', mix_freq
	reg_freq=((mix_freq)*2**22)/1712e6
	f.registers.freq_cwg_osc.write(frequency=reg_freq)

def set_vacc(f, acc_scale=1, acc_len=1):
	f.registers.acc_scale.write(reg=acc_scale)
	f.registers.acc_len.write(reg=acc_len)

def reset_counters(f):
	f.registers.control.write(cnt_rst='pulse')