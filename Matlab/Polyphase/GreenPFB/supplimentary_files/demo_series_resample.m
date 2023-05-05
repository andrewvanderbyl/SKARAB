% Demo: Time series resampling

% Background:An analgoue baseband signal that has a bandwidth B which is
% oversampled by a factor M due to a fixed ADC rate. M can be any rational
% number. The oversampled signal (generated as a discrete time series in
% this demo) will be rate reduced resuling in spectral replications, one of
% which will alias to baseband. The point is to alias the initial baseband
% signal which was oversampled down to baseband without the use of any
% mixers.

% Process:
% Step 1: Generate upconverted baseband signal
% Step 2: Resample input signal at rate R.

% Step 0:
clear
fft_length = 32768;

% Step 1:

% Mixer: Upconverter parameters
cw_freq = 2.8e9;
bw = 0e6;
bin_width = cw_freq/(fft_length/2);
fs_rotator = cw_freq*2;
rotator_cycles = 20000;

% Baseband signal parameters
amplitude = 1;
baseband_signal_freq_if = 164.0625e6;
baseband_signal_freq_bw_low = baseband_signal_freq_if - bw; % subtract half BW (80MHz) from center of band
baseband_signal_freq_bw_high = baseband_signal_freq_if + bw; % add half BW (80MHz) from center of band

% Generate baseband signal (complex as to emulate pol0 and pol 1)
upsample_ratio = cw_freq/(baseband_signal_freq_bw_high*2);
baseband_cycles = rotator_cycles/upsample_ratio;
fs_baseband = baseband_signal_freq_bw_high*2*upsample_ratio*2; %first x2 as we need Nyquist rate; 2nd x2 as we Nyquist rate for upconversion rotator

[baseband_signal_freq_bw_low_real,baseband_signal_freq_bw_low_cmplx,~,~] = Sig_Gen(baseband_signal_freq_bw_low, baseband_cycles, fs_baseband, amplitude, 10);
[baseband_signal_freq_if_real,baseband_signal_freq_if_cmplx,~,~] = Sig_Gen(baseband_signal_freq_if, baseband_cycles, fs_baseband, amplitude, 10);
[baseband_signal_freq_bw_high_real,baseband_signal_freq_bw_high_cmplx,~,~] = Sig_Gen(baseband_signal_freq_bw_high, baseband_cycles, fs_baseband, amplitude, 10);

common_length = length(baseband_signal_freq_bw_high_cmplx);
baseband_signal_cmplx = baseband_signal_freq_bw_low_cmplx(1:common_length) + baseband_signal_freq_if_cmplx(1:common_length) + baseband_signal_freq_bw_high_cmplx;

% Generate complex rotator
[rotator_real,rotator_cmplx,~,~] = Sig_Gen(cw_freq,rotator_cycles, fs_rotator, amplitude, 10);

% Upconvert complex signal
upsampled_signal = baseband_signal_cmplx(1:fft_length).*rotator_cmplx(1:fft_length);

% create equivalent upsampled IF signal. This should be the baseband IF
% with the baseband IF centered around fs (in frequency domain).
% full_signal = upsampled_signal + baseband_signal_cmplx(1:fft_length);
full_signal = upsampled_signal;

pol0 = real(full_signal);
pol1 = imag(full_signal);

% Compute FFT on complex heterodyned signal and on each polarisation.
fft_pol_cmplx = fft(full_signal);
fft_pol0 = fft(pol0);
fft_pol1 = fft(pol1);

% Plot spectra
% figure(1);
% stem(abs(fft(full_signal).^2));

%figure(2);
%subplot(3,1,1)
%stem(abs(fft_pol_cmplx.^2))
%subplot(3,1,2)
%stem(abs(fft_pol0.^2))
%subplot(3,1,3)
%stem(abs(fft_pol0.^2))
%stem(abs(fft_pol1.^2))

resample_factor = 18;
[resampled_series] = resample_series(full_signal, resample_factor);

figure(3);
subplot(2,1,1)
stem(abs(fft(full_signal)));
subplot(2,1,2)
stem(abs(fft(resampled_series,fft_length)));

a = 1;
