function [Real_Signal] = Sig_Gen_Real_only(freq,cycles,fs,Amplitude)

Num_Samples = fs/freq;

x1 = 0:(1/Num_Samples):1*cycles;

Real_Signal =  Amplitude*real(exp(1i*2*pi*x1)); 

end 