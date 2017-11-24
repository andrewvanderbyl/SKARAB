function [Y] = PolyphaseDFT(signal)
% PolyphaseDFT
%
% Function to test the frequency response of a filterbank using various power calculation criteria
%
% Create a DFT Polyphase FIR Quantized Filter Bank.
% The filterbank consists of M channels with N taps in each FIR filter
% Original Author: Ruby Van Rooyen
% Modified: Andrew van der Byl

% Initialize two variables to define the filters and the filter bank.
M = 2^13;  % Number of channels in the filter bank.
N = 4;   % Number of taps in each FIR filter.

% Calculate the coefficients b for the prototype lowpass filter, and zero-pad so that it has length M*N.
%WindowType='hamming'; % Hamming window = Better DFT lowpass
WindowType='blackmanharris'; % Hamming window = Better DFT lowpass

fwidth=1;
alltaps = M*N; % length of finite-impulse response prototype filter = KNt = (# Channels)(# Taps)
windowval = transpose(window(WindowType, alltaps));
b = windowval .* sinc(fwidth*([0:alltaps-1]/(M)-N/2));
b = [b,zeros(1,M*N-length(b))];

% Reshape the filter coefficients into a matrix whos rows 
% represent the individual polyphase filters to be distributed among the filter bank.
B = flipud(reshape(b,M,N));

% Construct a bank of M quantized filters and an M-point quantized FFT. Filter a sinusoid that is stepped in frequency from 0 to
% pi radians, store the power of the filtered signal, and plot the results
% for each channel in the filter bank.
%Nfreq = 1024; % Number of frequencies to sweep.
%w = linspace(0,pi,Nfreq);  % Frequency vector from 0 to pi.
%P = 100;     % Number of output points from each channel.
%t = 1:M*N*P; % Time vector.
%HH = zeros(M,length(w));  % Stores output power for each channel.

x = signal;
  
% EXECUTE THE FILTER BANK:
% Reshape the input so that it represents parallel channels of data going into the filter bank.
X = [x(:);zeros(M*ceil(length(x)/M)-length(x), 1)];
X = reshape(X,M,length(X)/M);
% Make the output the same size as the input.
Y = zeros(size(X));   
% FIR filter bank.
for k=1:M
  Y(k,:) = filter(B(k,:),1,X(k,:));
end

% FFT
Y = fft(Y);
Ynw=fft(X);
% Store the output power
%Y = sqrt(mean((Y(:,(N+1):end).^2).'));
Y = sqrt(mean((Y(:,(1):end).^2).'));


