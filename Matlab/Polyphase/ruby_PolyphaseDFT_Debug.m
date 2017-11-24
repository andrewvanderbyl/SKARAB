function [] = PolyphaseDFT()
% PolyphaseDFT
%
% Function to test the frequency response of a filterbank using various power calculation criteria
%
% Create a DFT Polyphase FIR Quantized Filter Bank.
% The filterbank consists of M channels with N taps in each FIR filter
% Original Author: Ruby Van Rooyen

% Initialize two variables to define the filters and the filter bank.
M = 64;  % Number of channels in the filter bank.
N = 4;   % Number of taps in each FIR filter.

% Calculate the coefficients b for the prototype lowpass filter, and zero-pad so that it has length M*N.
WindowType='hamming'; % Hamming window = Better DFT lowpass
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
Nfreq = 1024; % Number of frequencies to sweep.
w = linspace(0,pi,Nfreq);  % Frequency vector from 0 to pi.
P = 100;     % Number of output points from each channel.
t = 1:M*N*P; % Time vector.
HH = zeros(M,length(w));  % Stores output power for each channel.

for j=1:length(w)

  disp([num2str(j),' out of ',num2str(length(w))])
  % Real signal
  x = sin(w(j)*t);           % Signal to filter
  % Complex Signal
  %x = exp(1i*w(j)*t);
  
  
  % EXECUTE THE FILTER BANK:
  % Reshape the input so that it represents parallel channels of data going into the filter bank.
  X = [x(:);zeros(M*ceil(length(x)/M)-length(x), 1)];
  X = reshape(X,M,length(X)/M);
  
  
%   % Make the output the same size as the input.
   Y = zeros(size(X));   
  
  % FIR filter bank.
  for k=1:M
    Y(k,:) = filter(B(k,:),1,X(k,:));
  end

 
  % Non Filtered input 
  %-------------------
  %Y = X;
  
  Temp = Y;

  % FFT
  %----
  Y = fft(Y);
  Ynw=fft(X);

  Debug = 0;
 
  if Debug == 1 && j == 650 %65 %65 %257 %65

      n = linspace(0, M-1, M);
      u = 0:M-1;
      complex_exp = exp(-2*pi*1i*(u')*n/M)';

      for s=1:length(Y)
          
        figure(3)
        subplot(4,1,1)
        hold on;
        stem(real(Y(:,s)));
        stem(imag(Y(:,s)),'r');
        hold off;   

        % Create xlabel
        xlabel('Freqency (Bin number)');

        % Create ylabel
        ylabel('Magnitude');

        % Create title
        title('FFT (Truncated input)');
        
        
        %Y(1,s)
        
        subplot(4,1,2)
        hold on;
        plot(Temp(:,s),'g')
        % Create xlabel
        xlabel('Sample number');

        % Create ylabel
        ylabel('Magnitude');

        % Create title
        title('Input Signal (Truncated)');
        
        
        subplot(4,1,3)
        hold on;
        plot(real(complex_exp(:,1)))
        plot(real(complex_exp(:,2)),'r')
        plot(real(complex_exp(:,3)),'g')
        hold off;
        
        % Create xlabel
        xlabel('Sample number');

        % Create ylabel
        ylabel('Magnitude');

        % Create title
        title('Complex Exp: Real');
        
        subplot(4,1,4)
        hold on;
        plot(imag(complex_exp(:,1)))
        plot(imag(complex_exp(:,2)),'r')
        plot(imag(complex_exp(:,3)),'g')
        hold off;
        
        % Create xlabel
        xlabel('Sample Number');

        % Create ylabel
        ylabel('Magnitude');

        % Create title
        title('Complex Exp: Imaginary');

        %pause(0.1);
        %clf
        s
        
    end
    a = 1;
  end
  %-------------------
  
  % Store the output power
  HH(:,j) = sqrt(mean((abs(Y).^2).')'); % RMS voltage
  HH_nw(:,j) = sqrt(mean((abs(Ynw).^2).')'); % RMS voltage
  HH_var(:,j) = var(Y.')';              % Total energy
  HH_max(:,j) = max(abs(Y).')';         % Max-hold amplitude
  HH_mean(:,j) = mean(abs(Y).')';       % Average amplitude
  HH_mean_nw(:,j) = mean(abs(Ynw).');   % Average amplitude
end

% Normalize values to get 0dB values as maximum
for k = 1:M
    HH(k,:) = HH(k,:)/max(HH(k,:));
    HH_nw(k,:) = HH_nw(k,:)/max(HH_nw(k,:));
    HH_var(k,:) = HH_var(k,:)/max(HH_var(k,:));
    HH_max(k,:) = HH_max(k,:)/max(HH_max(k,:));
    HH_mean(k,:) = HH_mean(k,:)/max(HH_mean(k,:));
    HH_mean_nw(k,:) = HH_mean_nw(k,:)/max(HH_mean_nw(k,:));
end
HH_dB = 20*log10(HH(:,2:end-1));
HH_dB_nw = 20*log10(HH_nw(:,2:end-1));
HH_var_dB = 20*log10(HH_var(:,2:end-1));
HH_max_dB = 20*log10(HH_max(:,2:end-1));
HH_mean_dB = 20*log10(HH_mean(:,2:end-1));
HH_mean_dB_nw = 20*log10(HH_mean_nw(:,2:end-1));

% figure(1)
% channel_num = M/4+1;
% hold on
% plot(w(2:end-1),HH_mean_dB_nw(channel_num,:),'b')
% plot(w(2:end-1),HH_mean_dB(channel_num,:),'r')
% hold off
% % legend('sqrt(mean(abs(fft)))','var','max', 'mean')
% %legend(sprintf('%i-pt FFT',M),sprintf('%i-tap PFB',N))
% legend('FFT',sprintf('%i-tap PFB',N))
% title('Filter Bank Frequency Response')
% xlabel('Frequency (normalized to channel center)')
% ylabel('Magnitude Response (dB)')
% set(gca,'xtick',(1:M/2)*w(end)/M*2)
% set(gca,'xticklabel',(1:M/2)-M/4)

figure(2)
hold on
%plot(w(2:end-1),HH_mean_dB_nw)
%plot(w(2:end-1),HH_mean_dB)
plot(w(2:end-1),HH_dB(1:9,:))
%plot(w(2:end-1),-3*ones(size(HH(1,2:end-1))))
hold off
title('Filter Bank Frequency Response (Average amplitude or sqrt(mean((abs(FFT)^2))))')
%title('Filter Bank Frequency Response (Average amplitude or mean(abs(FFT)))')
xlabel('Frequency (normalized to channel center)')
ylabel('Magnitude Response (dB)')
set(gca,'xtick',(1:M/2)*w(end)/M*2)
set(gca,'xticklabel',(1:M/2)-M/4)

