%% ADC Eumlator
% -------------
% Input:
% ------
% adc_mode: 'real_mode' or 'ddc_mode' 
% amplitude: any real number
% sig_freq: any real number up to 1.4GHz(real mode) or 1.5GHz(DDC ADC)
% num_cycles: integer nmber in cycles
% output_format: 'serial' or 'split'
% split_length: 16 (optional if output_format = 'serial')

% Output:
% ------
% Pol 0 and Pol1 (either real or I/Q)

% Use: 
% ----
% [pol0, pol1] = adc_emulator('real_mode', 1, 100e6, 100, 'split',16);

% TODO:
% -----
% Add quantisation
% Complete I/Q (ddc version)

% -------------------------------------------------------------

function [pol0, pol1] = adc_emulator(adc_mode, amplitude, sig_freq, num_cycles, output_format, split_length)

    % Enable/Disable debug:
    % ---------------------
    debug = false;

    %%
    if strcmp(adc_mode,'real_mode')
        % Emulate ADC 2.8GSPS (Bypass mode)
        fs_freq = 2.8e9;

        % --- Generate baseband signal (2x real signals - one for pol0 and pol 1)
        % Note: pol0 and pol1 are each real-valued signals each at fs=2.8Gsps 
        [~, pol0, pol1] = signal_generator(amplitude, fs_freq,  sig_freq, num_cycles);   

        if debug
            % Plotting: Real and Imag
            figure(1)
            hold on; plot(pol0); plot(pol1); hold off;

            % Plotting: FFT complex input
            figure(2)
            semilogy(abs(fft(pol0(1:4096))));
        end

        if strcmp(output_format,'split') && split_length > 0
            [pol0] = sample_split(pol0, split_length);
            [pol1] = sample_split(pol1, split_length);
        end
    end

    %%
    if strcmp(adc_mode,'ddc_mode')
        % Emulate ADC 3.0 GSPS (DDC mode)
        fs_freq = 3.0e9;

        % --- Generate baseband signal (2x real signals - one for pol0 and pol 1)
        [signal_cmplx, ~, ~] = signal_generator(amplitude, fs_freq,  sig_freq, num_cycles);   

        if debug
            % Plotting: FFT complex input
            semilogy(abs(fft(signal_cmplx(1:4096))));    
        end


        % Note: pol0 and pol1 are each real-valued signals each at fs=3.0Gsps. Each 
        % real valued sequence will now be I/Q modulated to produce a complex stream
        % for each pol.

        % INCOMPLETE
    end
end
%%
% --- Start of functions ---

%% Signal Generator
function [signal_cmplx, signal_cos, signal_sin] = signal_generator(amplitude, fs_freq, sig_freq, num_cycles)
    signal_cmplx = complex_signal_gen(amplitude, fs_freq, sig_freq, num_cycles);
    signal_cos = real(signal_cmplx);
    signal_sin = imag(signal_cmplx);
end


%% Complex Signal Generator
function [complex_signal] = complex_signal_gen(amplitude, fs, freq, num_cycles)
    num_Samples = fs/freq;
    x1 = 0:(1/num_Samples):1*num_cycles;
    complex_signal = amplitude*exp(1i*2*pi*x1); 
end

%% Split vector
function [split_data] = sample_split(input, split_length)
    % check if the length can accommodate a split of split_length
    if (mod(length(input),split_length)) == 0
        split_data = reshape(input, split_length, length(input)/split_length);
    else
        mod_result = mod(length(input),split_length);
        split_data = reshape(input(:,1:end-mod_result), split_length, length(input(:,1:end-mod_result))/split_length);
        sprintf('split_length needs to be an integer multiple of the initial vector length. Truncating length.')
    end
end