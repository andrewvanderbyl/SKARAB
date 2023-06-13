%% ADC Eumlator
% -------------
% Input:
% ------
% ADC to be used: Option - 'real_mode' or 'ddc_mode' 
% Amplitude: any real number
% Frequency: any real number up to 1.4GHz(real mode) or 1.5GHz(DDC ADC)
% Number of cycles: integer nmber in cycles

% Output:
% ------
% Pol 0 and Pol1 (either real or I/Q)

% Use: 
% ----
% [pol0, pol1] = adc_emulator('real_mode', 1, 100e6, 100);

% -------------------------------------------------------------

function [pol0, pol1] = adc_emulator(adc_mode, amplitude, sig_freq, num_cycles)

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