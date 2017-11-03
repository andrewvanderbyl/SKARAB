function [Serial_Data, Sync, Dvalid] = Matlab_PFB_test(fft_length, no_taps, Sync_in,dvalid_in,Input_8,Input_7,Input_6,Input_5,Input_4,Input_3,Input_2,Input_1,pfb_sync,pfb_dv,pfb3,pfb2,pfb1,pfb0,pfbAcc3,pfbAcc2,pfbAcc1,pfbAcc0,offset)
    
    % Note: Change to load workspace into script rather than pass values

    % ------------------------------------%
    % Simulink PFB - Accumulated Spectrum %
    % ------------------------------------%

    % Extract the accumulated spectrum
    length_pfb_acc = length(pfbAcc0);
    no_iter = length_pfb_acc/(fft_length/8);
    End_extract = (length_pfb_acc - offset.Data(end));
    Start_extract =  End_extract - fft_length/8 + 1;

    
    pfbAcc0_local = pfbAcc0(Start_extract:End_extract);
    pfbAcc1_local = pfbAcc1(Start_extract:End_extract);
    pfbAcc2_local = pfbAcc2(Start_extract:End_extract);
    pfbAcc3_local = pfbAcc3(Start_extract:End_extract);
    
    % Recombine data (PFB Simulink)
    sprintf('Recombine data (PFB Simulink)')
    [Acc_Spec,Acc_Spec_Sync,Acc_Spec_Dvalid] = Parallel_Serial_Spectral_4k(pfbAcc3_local,pfbAcc2_local,pfbAcc1_local,pfbAcc0_local,pfb_sync,pfb_dv);
    
    Acc_Spec = Acc_Spec/no_iter;
    
    figure(1)
    plot(20*log10(abs(Acc_Spec)));
    
    
    % ---------------------------------------------------------------------
    
    % Recombine data (PFB Simulink)
    sprintf('Recombine data (PFB Simulink)')
    [Spec,Spec_Sync,Spec_Dvalid] = Parallel_Serial_Spectral_4k(pfb3,pfb2,pfb1,pfb0,pfb_sync,pfb_dv);
    
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
        pfb_current(:,i) = Valid_spec(start_point:end_point);
        start_point = end_point + 1;
        end_point = end_point + spectrum_length;
           
    end
    
    pfb = pfb_current(:,(1):end).^2;
    pfb = sqrt(mean(pfb'));
        
    figure(2)
    plot(20*log10(abs(pfb(:,2:end-1))));
    
    % ---------------------------------------------------------------------
    
    % -----------%
    % Matlab PFB %
    % -----------%

    % Recombine data (Time domain)
    sprintf('Recombine data (Time domain)')
    [Serial_Data,Sync,Dvalid] = Parallel_Serial_sync(Sync_in,dvalid_in,Input_8,Input_7,Input_6,Input_5,Input_4,Input_3,Input_2,Input_1);

    
    % Extract the valid region
    sprintf('Extracting valid region from time domain data')
    find_result_dv = find(dvalid_in.Data > 0);
    find_result_sync = find(Sync > 0);
    Valid_tone = Serial_Data(find_result_sync(1,1):end).*Dvalid(find_result_sync(1,1):end);
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

    end
    
    figure(3)
    plot(20*log10(abs(Ypfb(:,2:end-1))));
    
end