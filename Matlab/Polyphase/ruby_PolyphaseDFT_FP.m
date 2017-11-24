function [] = PolyphaseDFT()
% PolyphaseDFT
%
% Function to test the frequency response of a filterbank using various power calculation criteria
%
% Create a DFT Polyphase FIR Quantized Filter Bank.
% The filterbank consists of M channels with N taps in each FIR filter
% Original Author: Ruby Van Rooyen

% Initialize two variables to define the filters and the filter bank.
M = 16;  % Number of channels in the filter bank.
N = 8;   % Number of taps in each FIR filter.

Noise_Scale = 2^(-15); %0.0025;

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
% Output precision
Config.Total_outBits = 8;
Config.out_precision =  2^(-7);


% Rounding and Saturate Method
%RndMth = 'Floor';
DoSatur = 'on';



% Calculate the coefficients b for the prototype lowpass filter, and zero-pad so that it has length M*N.
WindowType='hamming'; % Hamming window = Better DFT lowpass
fwidth=1;
alltaps = M*N; % length of finite-impulse response prototype filter = KNt = (# Channels)(# Taps)
windowval = transpose(window(WindowType, alltaps));
b = windowval .* sinc(fwidth*([0:alltaps-1]/(M)-N/2));
b = [b,zeros(1,M*N-length(b))];

% Fixed point
b_fp = num2fixpt(b, sfix(Config.Total_coeffBits), Config.coeff_precision, 'Nearest', DoSatur);


% Reshape the filter coefficients into a matrix whos rows 
% represent the individual polyphase filters to be distributed among the filter bank.
B = flipud(reshape(b,M,N));

% Fixed point
B_fp = flipud(reshape(b_fp,M,N));


% Construct a bank of M quantized filters and an M-point quantized FFT. Filter a sinusoid that is stepped in frequency from 0 to
% pi radians, store the power of the filtered signal, and plot the results
% for each channel in the filter bank.
Nfreq = 1024; % Number of frequencies to sweep.
w = linspace(0,pi,Nfreq);  % Frequency vector from 0 to pi.
P = 100;     % Number of output points from each channel.
t = 1:M*N*P; % Time vector.
HH = zeros(M,length(w));  % Stores output power for each channel.
for j=1:length(w)
  disp([num2str(j),' out of ',num2str(length(w))])
  x = 0.1*sin(w(j)*t);           % Signal to filter
  noise = Noise_Scale*randn(1,length(x));
  %noise_fp = num2fixpt(noise, sfix(10), 2^(-9), 'Floor', 'on');
  
  % Add noise (1 lsb level)
  x = x + noise;
   
  % EXECUTE THE FILTER BANK:
  % Reshape the input so that it represents parallel channels of data going into the filter bank.
  X = [x(:);zeros(M*ceil(length(x)/M)-length(x), 1)];
  X = reshape(X,M,length(X)/M);
  
  X_fp = num2fixpt(X, sfix(Config.Total_dataBits), Config.data_precision, 'Floor', DoSatur);
  
  % Make the output the same size as the input.
  Y = zeros(size(X));   
  
  % Fixed point
  Y_fp = num2fixpt(Y, sfix(Config.Total_coeffBits), Config.coeff_precision, 'Nearest', DoSatur);   
  
  % FIR filter bank.
  for k=1:M
    Y(k,:) = filter(B(k,:),1,X(k,:));

    Y_fp(k,:) = filter(B_fp(k,:),1,X_fp(k,:));
  end

  % FFT
  Y = fft(Y);
  Ynw=fft(X);
  
  Y_fp_intmed = num2fixpt(Y_fp, sfix(Config.Total_intmedBits), Config.intmed_precision, 'Floor', DoSatur);    
  Y_fp = fft(Y_fp_intmed);
  Ynw_fp = fft(X_fp);
  
  
  Y_fp = num2fixpt(Y_fp, sfix(Config.Total_outBits), Config.out_precision, 'Nearest', DoSatur);
  Ynw_fp = num2fixpt(Ynw_fp, sfix(Config.Total_outBits), Config.out_precision, 'Nearest', DoSatur);
  
  
  % Store the output power
  HH(:,j) = sqrt(mean((abs(Y).^2).')'); % RMS voltage
  HH_nw(:,j) = sqrt(mean((abs(Ynw).^2).')'); % RMS voltage
  HH_var(:,j) = var(Y.')';              % Total energy
  HH_max(:,j) = max(abs(Y).')';         % Max-hold amplitude
  HH_mean(:,j) = mean(abs(Y).')';       % Average amplitude
  HH_mean_nw(:,j) = mean(abs(Ynw).');   % Average amplitude
  
  % Store the output power
  HH_fp(:,j) = sqrt(mean((abs(Y_fp).^2).')'); % RMS voltage
  HH_nw_fp(:,j) = sqrt(mean((abs(Ynw_fp).^2).')'); % RMS voltage
  HH_var_fp(:,j) = var(Y_fp.')';              % Total energy
  HH_max_fp(:,j) = max(abs(Y_fp).')';         % Max-hold amplitude
  HH_mean_fp(:,j) = mean(abs(Y_fp).')';       % Average amplitude
  HH_mean_nw_fp(:,j) = mean(abs(Ynw_fp).');   % Average amplitude
  
  
  
end

% Normalize values to get 0dB values as maximum
for k = 1:M
    HH(k,:) = HH(k,:)/max(HH(k,:));
    HH_nw(k,:) = HH_nw(k,:)/max(HH_nw(k,:));
    HH_var(k,:) = HH_var(k,:)/max(HH_var(k,:));
    HH_max(k,:) = HH_max(k,:)/max(HH_max(k,:));
    HH_mean(k,:) = HH_mean(k,:)/max(HH_mean(k,:));
    HH_mean_nw(k,:) = HH_mean_nw(k,:)/max(HH_mean_nw(k,:));
    
    HH_fp(k,:) = HH_fp(k,:)/max(HH_fp(k,:));
    HH_nw_fp(k,:) = HH_nw_fp(k,:)/max(HH_nw_fp(k,:));
    HH_var_fp(k,:) = HH_var_fp(k,:)/max(HH_var_fp(k,:));
    HH_max_fp(k,:) = HH_max_fp(k,:)/max(HH_max_fp(k,:));
    HH_mean_fp(k,:) = HH_mean_fp(k,:)/max(HH_mean_fp(k,:));
    HH_mean_nw_fp(k,:) = HH_mean_nw_fp(k,:)/max(HH_mean_nw_fp(k,:));
    
end
HH_dB = 20*log10(HH(:,2:end-1));
HH_dB_nw = 20*log10(HH_nw(:,2:end-1));
HH_var_dB = 20*log10(HH_var(:,2:end-1));
HH_max_dB = 20*log10(HH_max(:,2:end-1));
HH_mean_dB = 20*log10(HH_mean(:,2:end-1));
HH_mean_dB_nw = 20*log10(HH_mean_nw(:,2:end-1));

HH_dB_fp = 20*log10(HH_fp(:,2:end-1));
HH_dB_nw_fp = 20*log10(HH_nw_fp(:,2:end-1));
HH_var_dB_fp = 20*log10(HH_var_fp(:,2:end-1));
HH_max_dB_fp = 20*log10(HH_max_fp(:,2:end-1));
HH_mean_dB_fp = 20*log10(HH_mean_fp(:,2:end-1));
HH_mean_dB_nw_fp = 20*log10(HH_mean_nw_fp(:,2:end-1));


figure(1)
channel_num = M/4+1;
hold on
plot(w(2:end-1),HH_mean_dB_nw(channel_num,:),'b')
plot(w(2:end-1),HH_mean_dB(channel_num,:),'r')
plot(w(2:end-1),HH_mean_dB_nw_fp(channel_num,:),'c')
plot(w(2:end-1),HH_mean_dB_fp(channel_num,:),'g')
hold off
% legend('sqrt(mean(abs(fft)))','var','max', 'mean')
%legend(sprintf('%i-pt FFT',M),sprintf('%i-tap PFB',N))
legend('FFT',sprintf('%i-tap PFB',N),'FFT FixPt',sprintf('%i-tap PFB FixPt',N))
title('Filter Bank Frequency Response')
xlabel('Frequency (normalized to channel center)')
ylabel('Magnitude Response (dB)')
set(gca,'xtick',(1:M/2)*w(end)/M*2)
set(gca,'xticklabel',(1:M/2)-M/4)

figure(2)
hold on
%plot(w(2:end-1),HH_mean_dB_nw)
plot(w(2:end-1),HH_mean_dB)
plot(w(2:end-1),-3*ones(size(HH(1,2:end-1))))
hold off
title('Filter Bank Frequency Response (Average amplitude or mean(abs(FFT)))')
xlabel('Frequency (normalized to channel center)')
ylabel('Magnitude Response (dB)')
set(gca,'xtick',(1:M/2)*w(end)/M*2)
set(gca,'xticklabel',(1:M/2)-M/4)

% figure(3)
% channel_num = M/4+1;
% hold on
% plot(w(2:end-1),HH_mean_dB_nw_fp(channel_num,:),'b')
% plot(w(2:end-1),HH_mean_dB_fp(channel_num,:),'r')
% hold off
% % legend('sqrt(mean(abs(fft)))','var','max', 'mean')
% %legend(sprintf('%i-pt FFT',M),sprintf('%i-tap PFB',N))
% legend('FFT',sprintf('%i-tap PFB',N))
% title('Filter Bank Frequency Response')
% xlabel('Frequency (normalized to channel center)')
% ylabel('Magnitude Response (dB)')
% set(gca,'xtick',(1:M/2)*w(end)/M*2)
% set(gca,'xticklabel',(1:M/2)-M/4)

figure(4)
hold on
%plot(w(2:end-1),HH_mean_dB_nw)
plot(w(2:end-1),HH_mean_dB_fp)
plot(w(2:end-1),-3*ones(size(HH_fp(1,2:end-1))))
hold off
title('Filter Bank Frequency Response (Average amplitude or mean(abs(FFT)))')
xlabel('Frequency (normalized to channel center)')
ylabel('Magnitude Response (dB)')
set(gca,'xtick',(1:M/2)*w(end)/M*2)
set(gca,'xticklabel',(1:M/2)-M/4)

