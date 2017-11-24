function [Serial_Data] = Parallel_Serial_Struct(ADC0,ADC1,ADC2,ADC3,ADC4,ADC5,ADC6,ADC7)
% Perform Parallel to serial conversion
k = 0;
Serial_Data = zeros(length(ADC0),1);

for i=1:length(ADC0.signals.values)
   Serial_Data(k+1,1) = ADC0.signals.values(i,1);
   Serial_Data(k+2,1) = ADC1.signals.values(i,1);
   Serial_Data(k+3,1) = ADC2.signals.values(i,1);
   Serial_Data(k+4,1) = ADC3.signals.values(i,1);   
   Serial_Data(k+5,1) = ADC4.signals.values(i,1);    
   Serial_Data(k+6,1) = ADC5.signals.values(i,1);
   Serial_Data(k+7,1) = ADC6.signals.values(i,1);   
   Serial_Data(k+8,1) = ADC7.signals.values(i,1);   
   k = k + 8;
end

