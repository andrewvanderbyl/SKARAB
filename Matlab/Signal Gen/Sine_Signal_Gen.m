function [Sine_Out1] = Sine_Signal_Gen(freq,Amplitude,cycles,Fs)

T = 1/Fs;
period = 1/freq;    
points_per_period = period/(1/Fs);

%step = pi/points_per_period;
t = (0:(points_per_period-1)*cycles)*T;

Sine_Out1 = Amplitude*sin(2*pi*freq*t);

%Sine_Out2 = exp(1i*2*pi*freq*t);


end