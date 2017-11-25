function [] = PolyphaseDFT_Vacc(input)
% PolyphaseDFT
%
% Function to test the frequency response of a filterbank using various power calculation criteria
%
% Create a DFT Polyphase FIR Quantized Filter Bank.
% The filterbank consists of M channels with N taps in each FIR filter
% Original Author: Ruby Van Rooyen

% Initialize two variables to define the filters and the filter bank.
M = 2^13;  % Number of channels in the filter bank.
N = 4;   % Number of taps in each FIR filter.


% -------------------------------------------------------------------------

%Set the Fixed_point specifications
% PFB Coefficients precision
Config.Total_coeffBits = 18;
Config.coeff_precision =  2^(-17);

% Input data precision
Config.Total_dataBits = 10;
Config.data_precision =  2^(-9);

% Intermediary precision
Config.Total_intmedBits = 25;
Config.intmed_precision =  2^(-24);

% FFT precision
Config.Total_fftBits = 18+13;
Config.fft_precision =  2^(-17);

% Output precision
Config.Total_outBits = 18;
Config.out_precision =  2^(-17);

% Rounding and Saturate Method
RndMth = 'Nearest';
DoSatur = 'on';

% -------------------------------------------------------------------------

% Calculate the coefficients b for the prototype lowpass filter, and zero-pad so that it has length M*N.
%WindowType='hamming'; % Hamming window = Better DFT lowpass
WindowType='blackmanharris'; % Hamming window = Better DFT lowpass


fwidth=1;
alltaps = M*N; % length of finite-impulse response prototype filter = KNt = (# Channels)(# Taps)
windowval = transpose(window(WindowType, alltaps));
b = windowval .* sinc(fwidth*([0:alltaps-1]/(M)-N/2));
b = [b,zeros(1,M*N-length(b))];

% Fixed point
b_fp = num2fixpt(b, sfix(Config.Total_coeffBits), Config.coeff_precision, RndMth, DoSatur);


% Reshape the filter coefficients into a matrix whos rows 
% represent the individual polyphase filters to be distributed among the filter bank.
B = flipud(reshape(b,M,N));

% Fixed point
B_fp = flipud(reshape(b_fp,M,N));

% Construct a bank of M quantized filters and an M-point quantized FFT. Filter a sinusoid that is stepped in frequency from 0 to
% pi radians, store the power of the filtered signal, and plot the results
% for each channel in the filter bank.

w = linspace(0,pi,1);  % Frequency vector from 0 to pi.
P = 1;     % Number of output points from each channel.
t = 1:M*N*P; % Time vector.
HH = zeros(M,length(w));  % Stores output power for each channel.

% -------------------------------------------------------------------------

% Define the number of accumulations
accumulations = 2^10;
HH_vacc =  zeros(M,1);
HH_vacc_fp =  zeros(M,1);

% -------------------------------------------------------------------------

% Generate an input signal
freq = 208984375;
fs = 1712e6;
cycles = alltaps/(floor(fs/freq));
noise_level = 2^(-9);
Amplitude = 0.75;

for i=1:accumulations
    display(i) 
    
    [Real_Signal,Complex_Signal,Random_Signal] = Sig_Gen(freq,cycles,fs,Amplitude);
    awgn = noise_level*randn(size(Real_Signal));
    x = Real_Signal + awgn;

    %x = input(705:length(t)+705);

    % EXECUTE THE FILTER BANK:
    % Reshape the input so that it represents parallel channels of data going into the filter bank.
    X = [x(:);zeros(M*ceil(length(x)/M)-length(x), 1)];
    X = reshape(X,M,length(X)/M);

    % Fixed point
    X_fp = num2fixpt(X, sfix(Config.Total_dataBits), Config.data_precision, RndMth, DoSatur);
    
    % Make the output the same size as the input.
    Y = zeros(size(X));   

    % FIR filter bank.
    for k=1:M
      Y(k,:) = filter(B(k,:),1,X(k,:));
      
      % Fixed point
      Y_fp(k,:) = filter(B_fp(k,:),1,X_fp(k,:));
    end

    % FFT
    Y = fft(Y);
    Ynw=fft(X);
    
    % Fixed point
    %Y_fp_intmed = num2fixpt(Y_fp, sfix(Config.Total_intmedBits), Config.intmed_precision, RndMth, DoSatur);    
    %Y_fp = fft(Y_fp_intmed);
    
    Y_fp = fft(Y_fp);
    Ynw_fp = fft(X_fp);

    % Fixed point
    Y_fp = num2fixpt(Y_fp, sfix(Config.Total_fftBits), Config.fft_precision, RndMth, DoSatur);   
    
    % Store the output power
    HH(:,1) = sqrt(mean((abs(Y).^2).')'); % RMS voltage
    HH_nw(:,1) = sqrt(mean((abs(Ynw).^2).')'); % RMS voltage
    %HH_var(:,1) = var(Y.')';              % Total energy
    %HH_max(:,1) = max(abs(Y).')';         % Max-hold amplitude
    %HH_mean(:,1) = mean(abs(Y).')';       % Average amplitude
    %HH_mean_nw(:,1) = mean(abs(Ynw).');   % Average amplitude

    % Store the output power
    HH_fp(:,1) = sqrt(mean((abs(Y_fp).^2).')'); % RMS voltage
    HH_nw_fp(:,1) = sqrt(mean((abs(Ynw_fp).^2).')'); % RMS voltage
    %HH_var_fp(:,1) = var(Y_fp.')';              % Total energy
    %HH_max_fp(:,1) = max(abs(Y_fp).')';         % Max-hold amplitude
    %HH_mean_fp(:,1) = mean(abs(Y_fp).')';       % Average amplitude
    %HH_mean_nw_fp(:,1) = mean(abs(Ynw_fp).');   % Average amplitude
    
    % Compute log
    %HH_dB = 20*log10(HH(:));
    %HH_dB_nw = 20*log10(HH_nw(:));
    %HH_var_dB = 20*log10(HH_var(:));
    %HH_max_dB = 20*log10(HH_max(:));
    %HH_mean_dB = 20*log10(HH_mean(:));
    %HH_mean_dB_nw = 20*log10(HH_mean_nw(:));

    % Accumulate the spectra
    HH_vacc = HH_vacc + HH;

    HH_vacc_fp = HH_vacc_fp + HH_fp;

end

figure(1)
semilogy(HH_vacc)

figure(2)
semilogy(HH_vacc_fp)

% Save the computed files
save(strcat('/home/jasper/Desktop/','pfb_vacc_',num2str(accumulations),'_freq_',num2str(freq),'.mat'),'HH_vacc','HH_vacc_fp')
