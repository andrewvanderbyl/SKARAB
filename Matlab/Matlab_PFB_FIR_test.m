function [Serial_Data, Sync, Dvalid] = Matlab_PFB_FIR_test(fft_length, Sync_in,dvalid_in,Input_8,Input_7,Input_6,Input_5,Input_4,Input_3,Input_2,Input_1)

    % Recombine data (Time domain)
    sprintf('Recombine data (Time domain)')
    [Serial_Data,Sync,Dvalid] = Parallel_Serial_sync(Sync_in,dvalid_in,Input_8,Input_7,Input_6,Input_5,Input_4,Input_3,Input_2,Input_1);

    % Extract the valid region
    sprintf('Extracting valid region from time domain data')
    find_result_dv = find(Dvalid > 0);
    Valid_tone = Serial_Data(find_result_dv(1,1):end).*Dvalid(find_result_dv(1,1):end);
    % ---------------------------------------------------------------------
    

    % Divide up the PFB result so it can be averaged
    spectrum_length = fft_length;
    
    no_iter = floor(length(Valid_tone)/spectrum_length);
        
    start_point = 1;
    end_point = spectrum_length;

    pfb = zeros(spectrum_length,1);
    pfb_current = zeros(spectrum_length,1);

    for i=1:no_iter
        sprintf('PFB Iteration %f of %f', i, no_iter)
        pfb_current(:,i) = fft(Valid_tone(start_point:end_point));
        start_point = end_point + 1;
        end_point = end_point + spectrum_length;
    end
    
    pfb = pfb_current(:,(1):end).^2;
    pfb = sqrt(mean(pfb'));
        
    figure(1)
    plot(20*log10(abs(pfb(:,2:end-1))));


end