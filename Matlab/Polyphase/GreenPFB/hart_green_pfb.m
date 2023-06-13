%% Demo: HartRAO Polyphase resampler and PFB

% This is an implementation of a polyphase resampler and PFB for the
% HartRAO spectrometer. The Input would be two polarisations sampled at
% 2.8Gsps (real). This implementation deals only with one polarisation and
% works with an M=4 polyphase resample. The PFB is a direct implementation
% without any additonal optimisations. The input is a sampled vector array
% of length L from the ADC emulator. L can be either 16 or 4 depending on
% the adc mode (real_mode = 16; ddc_mode = 4).

% Process:
% Step 1: Set parameters.
% Step 2: Generate signal.
% Step 3: Resample input signal at rate 1/M and divide into M-paths.
% Step 4: PFB Channeliser.

% clear
debug = true;


%% Setup parameters
% --- Step 1: Parameters ---:
fft_length = 4096;
amplitude = 1;
sig_freq = 175e6; %175e6
adc_mode = 'real_mode';
adc_output_format = 'split';
split_length = 16;
num_cycles = 200000;

% Polyphase Parameters
M = 4;  %number of polyphase fir paths

WindowType='hann'; % 'hamming' or 'hann'
num_taps = 8; % PFB FIR channeliser

%% Run Polyphase resampler and PFB

% --- Step 2: Generate signals
[pol0, pol1] = adc_emulator(adc_mode, amplitude, sig_freq, num_cycles, adc_output_format, split_length);

% --- Step 3: Polyphase resample and filter the input signal using M-paths and process each path
[polyphase_fir_data] = polyphase_resampler_quad(pol0, M, debug);

% --- Step 4: PFB Channeliser
[channelised_data] = polyphase_channeliser(polyphase_fir_data, fft_length, WindowType, num_taps, debug);


%% --- Start of functions ---
%% Generate filter
function [coeffs] = generate_filter(M, WindowType, Num_taps)
    % Calculate the coefficients b for the prototype lowpass filter, and zero-pad so that it has length M*N.
    %WindowType='hamming'; % Hamming window = Better DFT lowpass
    %WindowType='blackmanharris'; % Hamming window = Better DFT lowpass

    fwidth=1;
    alltaps = M*Num_taps; % length of finite-impulse response prototype filter = KNt = (# Channels)(# Taps)
    windowval = transpose(window(WindowType, alltaps));
    b = windowval .* sinc(fwidth*([0:alltaps-1]/(M)-Num_taps/2));
    b = [b,zeros(1,M*Num_taps-length(b))];

    % Reshape the filter coefficients into a matrix whos rows 
    % represent the individual polyphase filters to be distributed among the filter bank.
    coeffs = flipud(reshape(b,M,Num_taps));
end


%% Green PFB: Polyphase Resampler (Quad)
% Operate 4 resamplers in parallel. This is due to the 16 samples provided
% by the ADC per fpga clock tick. One resampler could be used if the fpga
% ran at a rate of 4x175MHz (where fs/16 = 2.8e9/16 = 175MHz which is the
% minimum input rate the fpga needs to handle). If not, then the fpga must
% run multiple (P) resamplers in parallel where the input vector of 16
% samples is split across P resamplers. In this case we want each resampler
% to have M=4 so we need 4 samples per resampler so P = 16/M = 16/4 =4
% which means 4 resamplers rae required to operate in parallel. 
function [polyphase_fir_data] = polyphase_resampler_quad(adc_data, M, debug)
    % Import coefficients for polyphase resampling
    % load stage1_coeffs.mat
    load stage1_coeffs_order100_250MHz_330MHz.mat
    

    [polyphase_resampler_0] = polyphase_fir(adc_data(1:4,:), M, Coeffs); 
    [polyphase_resampler_1] = polyphase_fir(adc_data(5:8,:), M, Coeffs);
    [polyphase_resampler_2] = polyphase_fir(adc_data(9:12,:), M, Coeffs);
    [polyphase_resampler_3] = polyphase_fir(adc_data(13:16,:), M, Coeffs);

    % Reconstruct the sequence from the P number of resamplers. P is equal
    % to 4 in this case.
    polyphase_fir_data = zeros(length(polyphase_resampler_0)*4,1);
    k = 1;
    for i=1:length(polyphase_resampler_0)
        polyphase_fir_data(k,1) = polyphase_resampler_0(i);
        polyphase_fir_data(k+1,1) = polyphase_resampler_1(i);
        polyphase_fir_data(k+2,1) = polyphase_resampler_2(i);
        polyphase_fir_data(k+3,1) = polyphase_resampler_3(i);
        k = k + 4;
    end

    if debug
        fft_length = 4096;
        channelised_data = fft(polyphase_fir_data(500:500+fft_length,1));
        plot_channelised_data(channelised_data,0);
    end
    
end

%% Green PFB: Polyphase FIR
function [polyphase_fir_data] = polyphase_fir(baseband_signal, M, stage1_coeffs)
    % --- Step 3: Split into M-paths ---:
    coeff_row_length = (length(stage1_coeffs)/M);
    data_row_length = length(baseband_signal);
    
    % Coeffs
    M_path_coeffs = reshape(stage1_coeffs, M, length(stage1_coeffs)/M);

    reg=zeros(M,coeff_row_length);

    % --- Step 4: Process each path ---:
    idx = 1;
    for nn=1:M:data_row_length-M
        reg(:,2:coeff_row_length)=reg(:,1:coeff_row_length-1);
        reg(:,1)=flipud(baseband_signal(nn:nn+(M-1)));

        for mm=1:M
          vv(mm,idx)=reg(mm,:)*M_path_coeffs(mm,:)';
        end
        idx = idx + 1;

    end

    % --- Step 5: Add paths together to get rate reduced output ---:
    polyphase_fir_data = sum(vv);
    
end

%% Green PFB: Polyphase Channeliser
function [channelised_data] = polyphase_channeliser(input, N, WindowType, num_taps, debug)
    % Generate window coefficients
    [window_coeffs] = generate_filter(N, WindowType, num_taps);

    % --- Step 6: Split into N-paths ---:
    data_row_length = floor(length(input)/N) * N;
    [~, num_coeff_per_row] = size(window_coeffs);

    % Coeffs
    N_path_coeffs = window_coeffs;

    % --- Step 7: Process each path ---:
    reg=zeros(N,num_coeff_per_row);

    % --- Step 4: Process each path ---:
    for nn=1:N:data_row_length-N
        reg(:,2:num_coeff_per_row)=reg(:,1:num_coeff_per_row-1);
        reg(:,1)=flipud(input(nn:nn+(N-1)));

        h_out = zeros(N,1);
        for mm=1:N
            h_out(mm,1)=reg(mm,:)*N_path_coeffs(mm,:)';
        end
        
        channelised_data = fft(h_out);
        if debug
            % Display sequence if required
            display_input_sequence(h_out, 0.05)

            % Display channelised data if required
            plot_channelised_data(channelised_data, 0.05);            
        end
    end

end

%% Display input sequence
function display_input_sequence(sequence, pause_period)
    clf(figure(1))
    figure(1)
    hold on;
    plot(real(sequence(1:20)));
    plot(imag(sequence(1:20)));
    hold off;
    pause(pause_period);
end

%% Plot Channelised Data
function plot_channelised_data(channelised_data, pause_period)
    figure(2);
    % Create Title
    title_str = sprintf('Channelised Data');
    % Create xlabel
    x_lbl_str = 'Frequency bin';
    % Create ylabel
    y_lbl_str = 'Magnitude Response (dB)';
    plot(10*log10(abs(channelised_data.^2)))
    hold on;
    title(title_str)
    xlabel(x_lbl_str);
    ylabel(y_lbl_str);
    hold off;
    pause(pause_period);
end