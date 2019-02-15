% Dan's Overlapped PFB example

% Generate data
freq = 1e6;
cycles = 1000;
fs = 1712e6;
Amplitude = 1;
[Real_Signal] = Sig_Gen_Real_only(freq,cycles,fs,Amplitude);


% Implement a 4k FFT
fft_4k = fft(Real_Signal(1:8192));

% Implement 1024 4-point Inverse-fft using overlapped points

lin_array = 1:(length(fft_4k)/2);

%Setup initial sample positions
shift_array = circshift(lin_array,2);
sample_array = shift_array(1:5);

fft_array = lin_array;
fft_idx = fft_array(1:5);


for i=1:floor(((5/3)*1024))
    
    out(fft_idx,1) = ifft(sample_array);
    test = ifft(sample_array);
    
    shift_array = circshift(shift_array,-3);
    sample_array = shift_array(1:5);
    
    fft_array = circshift(fft_array,-5);
    fft_idx = fft_array(1:5);
end

plot(abs(fft_4k))
