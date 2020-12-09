function [pfb_out, weights, windowed] = katfgpu_pfb(data, channels)

% Parameters
taps = 16;

% Generate Weights
weights = generate_weights(channels, taps);

% Compute FIR
[fir_out, windowed] = fir(data, channels, weights);

% Compute FFT
fft_data = fft(data(1:channels*2));
pfb_out = fft(fir_out);

% Square FFT Results
fft_data_sqr = fft_data.^2;
pfb_sqr = pfb_out.^2;


% Plot FFT's
figure(1)
semilogy(abs(fft_data_sqr))

figure(2)
semilogy(abs(pfb_sqr))


end

function [weights] = generate_weights(channels, taps)
    step = 2*channels;
    window_size = step * taps;
    idx = linspace(1,window_size,window_size);
    hann = sin(pi*idx/(window_size - 1)).^2;
    sinc_gen = sinc(idx/step - taps /2);
    weights = hann.*sinc_gen;
end

function [fir_out, windowed] = fir(data, channels, weights)
    step = 2*channels;
    taps = length(weights)/step;
    window_size = 2 * channels * taps;
    
    out = zeros(length(data)/step - taps +1, step);
    for i=0:step:length(out)-1
        windowed = data((i*step+1):(i*step) + window_size).*weights;
        out = sum(reshape(windowed,step,taps)'); 
    end
    fir_out = out;
end
