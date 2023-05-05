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

% clear
debug = false;


%% Setup parameters
% --- Step 1: Parameters ---:
fft_length = 4096;
amplitude = 1;
fs_freq = 2.8e9;
M = 4;  %number of polyphase fir paths

WindowType='hann'; % 'hamming' or 'hann'
num_taps = 8; % PFB FIR channeliser

% --- Baseband signal parameters
selected_bin = 571;
ch_bw = (fs_freq/M)/fft_length;
bb_if = ch_bw * selected_bin;
bw = 0e6;
num_cycles = 200000;

% -- PFB Profile parameters
ch_bw = (fs_freq/M)/fft_length;
adjacent_channels_to_span = 2;
points_per_bin = 15;

freq_step_size = ch_bw/points_per_bin;
start_freq = ch_bw * (selected_bin - adjacent_channels_to_span);
end_freq = ch_bw * (selected_bin + adjacent_channels_to_span);
total_points = (end_freq - start_freq)/freq_step_size +1;

%% Options: Run PFB (normally) or create a channel profile
% option = 'normal';
option = 'profile';

if strcmp(option, 'normal')

    % --- Step 2: Generate signals ---:
    % --- Generate baseband signal (complex as to emulate pol0 and pol 1)
    [signal_data] = signal_generator(amplitude, fs_freq, bb_if, bw, num_cycles);   

    % --- Phase 2: Decompose signal and filter coefficients into M-paths and process each path
    [polyphase_fir_data] = polyphase_fir(signal_data, M);

    % --- Phase 3: Decompose 1st stage to form 2nd stage PFB for channeliser
    [channelised_data] = polyphase_channeliser(polyphase_fir_data, fft_length, WindowType, num_taps, debug);
    
elseif strcmp(option, 'profile')

    % --- Step 2: Generate a tone linearly increasing in fixed frequency steps ---:
    idx = 1;
    profile = zeros(total_points,fft_length);
    for freq=start_freq:freq_step_size:end_freq
        tic
        sprintf('Progress update: Point %i out of %i', idx ,total_points)
        % Generate the required signal
        [signal_data] = signal_generator(amplitude, fs_freq, freq, 0e6, num_cycles);   
        
        % --- Phase 2: Decompose signal and filter coefficients into M-paths and process each path
        [polyphase_fir_data] = polyphase_fir(signal_data, M);

        % --- Phase 3: Decompose 1st stage to form 2nd stage PFB for channeliser
        [channelised_data] = polyphase_channeliser(polyphase_fir_data, fft_length, WindowType, num_taps, debug);
        
        % --- Log channel (bin) value of interest for current input signal
        profile(idx,:) = channelised_data;
        idx = idx + 1;
        toc
    end
    
    total_channels_to_plot = adjacent_channels_to_span*2 + 1;

    figure(1);
    % Create Title
    title_str = sprintf('Polyphase Channel Profile: %s Window with %i Taps', WindowType, num_taps);
    % Create xlabel
    x_lbl_str = 'Frequency bin (normalized to channel center)';
    % Create ylabel
    y_lbl_str = 'Magnitude Response (dB)';
    x_tick_lbl = (selected_bin-adjacent_channels_to_span):(selected_bin+adjacent_channels_to_span);
    
    plot(10*log(abs(profile(:,((selected_bin-adjacent_channels_to_span):(selected_bin+adjacent_channels_to_span+1))).^2)));
    hold on;
    title(title_str)
    xlabel(x_lbl_str);
    ylabel(y_lbl_str);
    set(gca,'xtick',(1:points_per_bin:total_points))
    set(gca,'xticklabel',x_tick_lbl)
    hold off;

end



% --- Start of functions ---

%% Signal Generator
function [signal_data] = signal_generator(amplitude, fs_freq, bb_if, bw, num_cycles)
    bb_signal_bw_low_cmplx = complex_signal_gen(amplitude, fs_freq, (bb_if - bw), num_cycles);
    bb_signal_if_cmplx = complex_signal_gen(amplitude, fs_freq, bb_if, num_cycles);
    bb_signal_bw_high_cmplx = complex_signal_gen(amplitude, fs_freq, (bb_if + bw), num_cycles);

    common_length = length(bb_signal_bw_high_cmplx);
    signal_data_cmplx = bb_signal_bw_low_cmplx(1:common_length) + bb_signal_if_cmplx(1:common_length) + bb_signal_bw_high_cmplx;
    signal_data = signal_data_cmplx;
end


%% Complex Signal Generator
function [complex_signal] = complex_signal_gen(amplitude, fs, freq, num_cycles)
    num_Samples = fs/freq;
    x1 = 0:(1/num_Samples):1*num_cycles;
    complex_signal = amplitude*exp(1i*2*pi*x1); 
end

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


%% Green PFB: Polyphase FIR
function [polyphase_fir_data] = polyphase_fir(baseband_signal, M)
    % Import coefficients
    load stage1_coeffs.mat

    % --- Step 3: Split into M-paths ---:
    data_row_length = (floor(length(baseband_signal)/M));
    coeff_row_length = (length(stage1_coeffs)/M);

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
            display_channel_data(channelised_data, 0.05);            
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

%% Display channelised Data
function display_channel_data(channelised_data, pause_period)
    %clf
    figure(2)
    semilogy(abs(channelised_data.^2));
    pause(pause_period);
end