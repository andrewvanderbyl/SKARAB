%function [Pure_Signal,Random_Signal] = Sig_Gen(Num_Samples,Cycles,fs)
function [Real_Signal,Complex_Signal,Random_Signal,Quant_Signal] = Sig_Gen(freq,cycles,fs,Amplitude, quant_bits)

Config.Total_coeffBits = quant_bits;
Config.coeff_precision =  2^(-1*(Config.Total_coeffBits-1));

% Rounding and Saturate Method
RndMth = 'Nearest';
DoSatur = 'on';

if freq>0
    Num_Samples = fs/freq;

    x1 = 0:(1/Num_Samples):1*cycles;

    Complex_Signal = exp(1i*2*pi*x1); 

    Real_Signal = Amplitude*real(Complex_Signal);
    
    % Random
    Random_Signal = exp(1i*2*pi*randn(1,length(x1))); 
    
    Quant_Signal = num2fixpt(Real_Signal, sfix(Config.Total_coeffBits), Config.coeff_precision, RndMth, DoSatur);

else
    Num_Samples = fs/cycles;
    Complex_Signal = exp(1i*2*pi*zeros(1,Num_Samples));
    Real_Signal = Amplitude*real(Complex_Signal);

    % Random
    Random_Signal = exp(1i*2*pi*randn(1,floor(Num_Samples))); 
    
    Quant_Signal = num2fixpt(Real_Signal, sfix(Config.Total_coeffBits), Config.coeff_precision, RndMth, DoSatur);
end



end 