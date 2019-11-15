[Real_Signal] = Sig_Gen_Real_only(100e6,100,1712e6,1);

sig_shift = circshift(Real_Signal,-1);

hold on; plot(Real_Signal); plot(sig_shift);

fft_sig = fft(Real_Signal(1:1024))';

fft_sig_shift = fft(sig_shift(1:1024))';

a = 1;
