%Set the Fixed_point specifications
% PFB Coefficients precision
Config.Total_coeffBits = 18;
Config.coeff_precision =  2^(-17);

% Rounding and Saturate Method
RndMth = 'Nearest';
DoSatur = 'on';

acc_len = 2^5;

noise_level = 1*2^(-17);

error_awg = 0;

error_status = false;

for i=1:acc_len
   
    freq = 208984.375*1;
    cycles = 1;
    fs = 1712e6;
    Amplitude = 0.5;

    [Real_Signal] = Sig_Gen_Real_only(freq,cycles,fs,Amplitude);

    X_fp = num2fixpt(Real_Signal, sfix(Config.Total_coeffBits), Config.coeff_precision, RndMth, DoSatur);
    
   
    % Random
    Random_Signal = noise_level.*rand(1,floor(length(Real_Signal)));
    
    Sig_awg = Random_Signal + Real_Signal;
    
    X_fp_awg = num2fixpt(Sig_awg, sfix(Config.Total_coeffBits), Config.coeff_precision, RndMth, DoSatur);
    
    error_awg = error_awg + (Sig_awg-X_fp_awg);
    
end

figure(1)
hold on
plot(Real_Signal-X_fp)
plot(Real_Signal*1e-05)
hold off

figure(2)
hold on
plot(Sig_awg-X_fp_awg)
plot(Sig_awg*1e-05)
hold off

figure(3)
plot(error_awg)

%hist(error_awg)

