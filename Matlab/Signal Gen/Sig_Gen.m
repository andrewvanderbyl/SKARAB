%function [Pure_Signal,Random_Signal] = Sig_Gen(Num_Samples,Cycles,fs)
function [Real_Signal,Complex_Signal,Random_Signal] = Sig_Gen(freq,cycles,fs,Amplitude)

if freq>0
    Num_Samples = fs/freq;

    x1 = 0:(1/Num_Samples):1*cycles;

    Complex_Signal = exp(1i*2*pi*x1); 

    Real_Signal = Amplitude*real(Complex_Signal);

else
    Num_Samples = fs/cycles;
    Complex_Signal = exp(1i*2*pi*zeros(1,Num_Samples));
    Real_Signal = Amplitude*real(Complex_Signal);
end

% Random
Random_Signal = exp(1i*2*pi*randn(1,floor(Num_Samples))); 


end 