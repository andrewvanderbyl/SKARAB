% Demo: Implement a Green PFB

% Background:An analgoue baseband signal that has a bandwidth B which is
% oversampled by a factor M due to a fixed ADC rate. M can be any integer
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
fft_length = 4096;
amplitude = 1;
fs_freq = 2.8e9;
bw = 10e6;

% Baseband signal parameters
bb_if = 87.5e6; % 164.0625e6;
% bb_signal_freq_bw_low = bb_signal_freq_if - bw; % subtract half BW (80MHz) from center of band
% bb_signal_freq_bw_high = bb_signal_freq_if + bw; % add half BW (80MHz) from center of band

% --- Step 2: Generate signals ---:
% Generate baseband signal (complex as to emulate pol0 and pol 1)
num_cycles = 250000;

bb_signal_bw_low_cmplx = complex_signal_gen(amplitude, fs_freq, (bb_if - bw), num_cycles);
bb_signal_if_cmplx = complex_signal_gen(amplitude, fs_freq, bb_if, num_cycles);
bb_signal_bw_high_cmplx = complex_signal_gen(amplitude, fs_freq, (bb_if + bw), num_cycles);

% [~ , bb_signal_bw_low_cmplx, ~, ~] = Sig_Gen((bb_signal_freq_if - bw), num_cycles, fs_freq, amplitude, 10);
% [~ , bb_signal_if_cmplx, ~, ~] = Sig_Gen(bb_signal_freq_if, num_cycles, fs_freq, amplitude, 10);
% [~ , bb_signal_bw_high_cmplx, ~, ~] = Sig_Gen((bb_signal_freq_if + bw), num_cycles, fs_freq, amplitude, 10);

common_length = length(bb_signal_bw_high_cmplx);
baseband_signal_cmplx = bb_signal_bw_low_cmplx(1:common_length) + bb_signal_if_cmplx(1:common_length) + bb_signal_bw_high_cmplx;
baseband_signal = real(baseband_signal_cmplx);

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
% Import coefficients
load stage1_coeffs.mat

% --- Step 3: Split into M-paths ---:
M = 4;
data_row_length = (floor(length(baseband_signal)/M));
coeff_row_length = (length(stage1_coeffs)/M);

% Coeffs
% [M_path_coeffs] = m_path_split(stage1_coeffs, M);
M_path_coeffs = reshape(stage1_coeffs, M, length(stage1_coeffs)/M);

% Signal
% [M_path_data] = m_path_split(baseband_signal_cmplx, M);
M_path_data = reshape(baseband_signal(1:(M*data_row_length)), M, data_row_length);

size_coeff_matrix = size(M_path_coeffs);
size_data_matrix = size(M_path_data);
%filter_out = zeros(size_data_matrix(1,1), size_data_matrix(1,2)-1 + size_coeff_matrix(1,2));

reg=zeros(M,coeff_row_length);
% n_dat = length(baseband_signal_cmplx);
% rr=zeros(1,n_dat);

idx = 1;
for nn=1:M:data_row_length-M
%     rr=[fliplr(baseband_signal_cmplx(nn:nn+(coeff_row_length-1))) rr(1:n_dat-M)];
  
    reg(:,2:coeff_row_length)=reg(:,1:coeff_row_length-1);
    reg(:,1)=flipud(baseband_signal(nn:nn+(M-1)));

    for mm=1:M
      vv(mm,idx)=reg(mm,:)*M_path_coeffs(mm,:)';
    end
    idx = idx + 1;
    %signal_out(nn,1) = sum(vv);
    
end
% --- Step 4: Process each path ---:
%for row = 1:size_coeff_matrix(1,1)
    
    % tmp_real = conv(real(M_path_data(row,1:end)), M_path_coeffs(row,1:end));
    % tmp_imag = conv(imag(M_path_data(row,1:end)), M_path_coeffs(row,1:end));
    % filter_out(row,:) = tmp_real+1i*tmp_imag;
%end

% --- Step 5: Add paths together to get rate reduced output ---:
pfb_stage1_output = sum(vv);
semilogy(abs(fft(real(pfb_stage1_output),4096)))

%% Phase 3: Decompose 1st stage to form 2nd stage PFB for channeliser
% Import coefficients
load window_coeffs.mat

% --- Step 6: Split into N-paths ---:
N = fft_length;
% hann_window = window('hann', N*32);
data_row_length = floor(length(pfb_stage1_output)/N) * N;
coeff_row_length = (length(window_coeffs)/N);

% Coeffs
[N_path_coeffs] = m_path_split(window_coeffs, N);

% Signal
[N_path_data] = m_path_split(pfb_stage1_output(1:data_row_length), N);

% --- Step 7: Process each path ---:
reg=zeros(N,coeff_row_length);
size_coeff_matrix = size(N_path_coeffs);
size_data_matrix = size(N_path_data);

% --- Step 4: Process each path ---:
for nn=1:N:data_row_length-N
    nn
    reg(:,2:coeff_row_length)=reg(:,1:coeff_row_length-1);
    reg(:,1)=flipud(pfb_stage1_output(nn:nn+(N-1)));

    for mm=1:N
        h_out(mm,1)=reg(mm,:)*N_path_coeffs(mm,:)';
    end
    clf
    figure(1)
    semilogy(abs(fft(h_out')));
    figure(2)
    hold on;
    plot(reg(1,:))
    plot(reg(2,:))
    hold off;
    pause(0.05)
end

%% Signal Generator
function [complex_signal] = complex_signal_gen(amplitude, fs, freq, num_cycles)
    num_Samples = fs/freq;
    x1 = 0:(1/num_Samples):1*num_cycles;
    complex_signal = amplitude*exp(1i*2*pi*x1); 
end
