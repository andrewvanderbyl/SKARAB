function [Serial_Data, Sync, Dvalid] = Matlab_PFB_test(fft_length, no_taps, Sync_in,dvalid_in,Input_0,Input_1,Input_2,Input_3,Input_4,Input_5,Input_6,Input_7,pfb_sync,pfb_dv,pfb0,pfb1,pfb2,pfb3)

    % Recombine data (Time domain)
    sprintf('Recombine data (Time domain)')
    [Serial_Data,Sync,Dvalid] = Parallel_Serial_sync(Sync_in,dvalid_in,Input_7,Input_6,Input_5,Input_4,Input_3,Input_2,Input_1,Input_0);

    % Recombine data (PFB Simulink)
    sprintf('Recombine data (PFB Simulink)')
    [Spec,Spec_Sync,Spec_Dvalid] = Parallel_Serial_Spectral_4k(pfb0,pfb1,pfb2,pfb3,pfb_sync,pfb_dv);
    % ---------------------------------------------------------------------

    % Extract the valid region
    sprintf('Extracting valid region from time domain data')
    find_result_dv = find(dvalid_in.Data > 0);
    Valid_tone = Serial_Data(find_result_dv(1,1):end).*Dvalid(find_result_dv(1,1):end);
    % ---------------------------------------------------------------------

    % Simulink PFB %
    % -------------%
    
    % Extract the valid region
    sprintf('Extracting valid region from Simulink PFB data')
    find_result_dv = find(Spec_Dvalid > 0);
    find_result_sync = find(Spec_Sync > 0);
    Valid_spec = Spec(find_result_sync(1,1):end).*Spec_Dvalid(find_result_sync(1,1):end);
    
    % Divide up the PFB result so it can be averaged
    spectrum_length = fft_length/2;
    
    no_iter = floor(length(Valid_spec)/spectrum_length);
        
    start_point = 1;
    end_point = spectrum_length;

    pfb = zeros(spectrum_length,1);
    pfb_current = zeros(spectrum_length,1);

    for i=1:no_iter
        sprintf('PFB Iteration %f of %f', i, no_iter)
        [pfb_current] = Valid_spec(start_point:end_point);
        start_point = end_point + 1;
        end_point = end_point + spectrum_length;
        pfb = pfb + pfb_current;

        figure(1)
        semilogy(abs(pfb));
        pause(0.1)
    end
    
    % ---------------------------------------------------------------------
    
    % Step through the input data and run through the pfb 
    extract_length = fft_length*no_taps;

    no_iter = floor(length(Valid_tone)/extract_length);

    start_point = 1;
    end_point = extract_length;

    Ypfb = zeros(1,fft_length);
    Ypfb_current = zeros(1,fft_length);

    for i=1:no_iter
        sprintf('Iteration %f of %f', i, no_iter)
        [Ypfb_current] = PolyphaseDFT(Valid_tone(start_point:end_point));
        start_point = end_point + 1;
        end_point = end_point + extract_length;
        Ypfb = Ypfb + Ypfb_current;

        figure(2)
        semilogy(abs(Ypfb));
        pause(0.1)
    end


end