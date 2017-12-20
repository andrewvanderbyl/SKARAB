%Set the Fixed_point specifications
% PFB Coefficients precision
Config.Total_coeffBits = 18;
Config.coeff_precision =  2^(-17);

% Rounding and Saturate Method
RndMth = 'Nearest';
DoSatur = 'on';

acc_len = 2^0;

noise_level = 1*2^(-17);

error_awg = 0;

Random_Signal_sum = 0;

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
    
    Random_Signal_sum = Random_Signal +Random_Signal_sum;
    
end

rs = Real_Signal';

mean_diff_test1 = mean( (Real_Signal(1:2048)-X_fp(1:2048)) )
mean_diff_test2 = mean( (Real_Signal(2048:2048+2047)-X_fp(2048:2048+2047)) )


mean_diff1 = mean( (Real_Signal(1:2048)-X_fp(1:2048)) )
mean_diff2 = mean( (Real_Signal(2049:2049+2047)-X_fp(2049:2049+2047)) )
mean_diff3 = mean( (Real_Signal(4097:4097+2047)-X_fp(4097:4097+2047)) )
mean_diff4 = mean( (Real_Signal(6145:6145+2047)-X_fp(6145:6145+2047)) )

rms_diff1 = sqrt(mean( (Real_Signal(1:2048)-X_fp(1:2048)).^2 ))
rms_diff2 = sqrt(mean( (Real_Signal(2049:2049+2047)-X_fp(2049:2049+2047)).^2 ))
rms_diff3 = sqrt(mean( (Real_Signal(4097:4097+2047)-X_fp(4097:4097+2047)).^2 ))
rms_diff4 = sqrt(mean( (Real_Signal(6145:6145+2047)-X_fp(6145:6145+2047)).^2 ))


figure(1)
hold on
plot(Real_Signal-X_fp)
plot(Real_Signal*1e-05)
hold off

figure(2)
hold on
plot(Real_Signal-X_fp_awg)
plot(Sig_awg*1e-05)
hold off

figure(3)
hold on
plot(Real_Signal)
plot(Sig_awg)
hold off


figure(4)
plot(Random_Signal)
%hist(error_awg)

