%Set the Fixed_point specifications


% Fixed Point Coefficients precision
Config.Total_coeffBits = 10;
Config.coeff_precision =  2^(-9);

% Rounding and Saturate Method
RndMth = 'Nearest';
DoSatur = 'on';

fft_bin = 8; 
fft_len = 16384;
freq = 208984.375*fft_bin;
cycles = 100;
fs = 1712e6;
Amplitude = 0.95;
noise_level = 1*2^(-9);

% Generate floating point Real Signal
[Real_Signal] = Sig_Gen_Real_only(freq,cycles,fs,Amplitude);

% Generate some random noise
Random_Signal = noise_level.*rand(1,floor(length(Real_Signal)));

% Add the AWG to the Real Signal
Real_Signal_awg =  Real_Signal + Random_Signal;

% Cast Real Signal to fixed point
Real_signal_fxpt = num2fixpt(Real_Signal_awg, sfix(Config.Total_coeffBits), Config.coeff_precision, RndMth, DoSatur);

% FFT of Quantized Real Signal
fft_fxpt = fft(Real_signal_fxpt(1:fft_len));



figure(1)
hold on
plot(Real_Signal_awg)
plot(Real_signal_fxpt)
hold off

figure(2)
semilogy(abs(fft_fxpt.^2))



