% Demo: Implement a Green PFB

% Background:An analgoue baseband signal that has a bandwidth B which is
% oversampled by a factor M due to a fixed ADC rate. M can be any rational
% number. The oversampled signal (generated as a discrete time series in
% this demo) will be rate reduced resulting in spectral replications, one of
% which will alias to baseband. The point is to alias the initial baseband
% signal which was oversampled down to baseband without the use of any
% mixers.

% Process:
% Step 1: Set parameters.
% Step 2: Generate baseband signal.
% Step 3: Resample input signal at rate 1/M and divide into M-paths.
% Step 4: Resample filter coefficients for the M-paths.
% Step 5: Compute the iFFT on the .

clear

%% Phase 1: Generate signals
% --- Step 1: Set parameters ---:
fft_length = 32768;
amplitude = 1;
fs_freq = 2.8e9;
bw = 0e6;

num_cycles = 25000;

% Baseband signal parameters
bb_signal_freq_if = 300.0122e6; % 164.0625e6;
bb_signal_freq_bw_low = bb_signal_freq_if - bw; % subtract half BW (80MHz) from center of band
bb_signal_freq_bw_high = bb_signal_freq_if + bw; % add half BW (80MHz) from center of band

% Import coefficients
load stage1_coeffs.mat

% --- Step 2: Generate signals ---:
% Generate baseband signal (complex as to emulate pol0 and pol 1)
[bb_signal_bw_low_real, bb_signal_bw_low_cmplx, ~, ~] = Sig_Gen(bb_signal_freq_bw_low, num_cycles, fs_freq, amplitude, 10);
[bb_signal_if_real, bb_signal_if_cmplx, ~, ~] = Sig_Gen(bb_signal_freq_if, num_cycles, fs_freq, amplitude, 10);
[bb_signal_bw_high_real, bb_signal_bw_high_cmplx, ~, ~] = Sig_Gen(bb_signal_freq_bw_high, num_cycles, fs_freq, amplitude, 10);

common_length = length(bb_signal_bw_high_cmplx);
baseband_signal_cmplx = bb_signal_bw_low_cmplx(1:common_length) + bb_signal_if_cmplx(1:common_length) + bb_signal_bw_high_cmplx;

% Compute FFT on complex heterodyned signal and on each polarisation.
% fft_pol_cmplx = fft(baseband_signal_cmplx, fft_length);
% fft_pol0 = fft(real(baseband_signal_cmplx), fft_length);
% fft_pol1 = fft(imag(baseband_signal_cmplx), fft_length);

% Plot spectra
% figure(1);
% subplot(3,1,1)
% stem(abs(fft_pol_cmplx.^2))
% subplot(3,1,2)
% stem(abs(fft_pol0.^2))
% subplot(3,1,3)
% stem(abs(fft_pol0.^2))
% stem(abs(fft_pol1.^2))

%% Phase 2: Decompose signal and filter coefficients into M-paths and process each path

% --- Step 3: Split into M-paths ---:
M = 4;

% Coeffs
[M_path_coeffs] = m_path_split(stage1_coeffs, M);

% Signal
[M_path_data] = m_path_split(baseband_signal_cmplx, M);

size_coeff_matrix = size(M_path_coeffs);
size_data_matrix = size(M_path_data);
filter_out = zeros(size_data_matrix(1,1), size_data_matrix(1,2)-1 + size_coeff_matrix(1,2));

% --- Step 4: Process each path ---:
for row = 1:size_coeff_matrix(1,1)
    tmp_real = conv(real(M_path_data(row,1:end)), M_path_coeffs(row,1:end));
    tmp_imag = conv(imag(M_path_data(row,1:end)), M_path_coeffs(row,1:end));
    filter_out(row,:) = tmp_real+1i*tmp_imag;
   
end

% --- Step 5: Add paths together to get rate reduced output ---:
pfb_stage1_output = sum(filter_out);
%stem(abs(fft(pfb_stage1_output,fft_length)));


%% Phase 3: Decompose 1st stage to form 2nd stage PFB for channeliser
% --- Step 6: Split into N-paths ---:
N = 4096;

rounded_split_length = floor(length(pfb_stage1_output)/N);

% Coeffs
[N_path_coeffs] = m_path_split(pfb_stage1_output(1:rounded_split_length), N);

% Signal
[N_path_data] = m_path_split(pfb_stage1_output(1:rounded_split_length), N);


% --- Step 7: Process each path ---:



