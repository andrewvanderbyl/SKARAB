function [Serial_Data_a,Serial_Data_b] = Parallel_Serial_Coeff(In0,In1,In2,In3,In4,In5,In6,In7,In8,In9,In10,In11,In12,In13,In14,In15)
% Perform Parallel to serial conversion
k = 0;
Serial_Data_a = zeros(length(In0.signals.values),1);
Serial_Data_b = zeros(length(In0.signals.values),1);


for i=1:length(In0.signals.values)
   Serial_Data_a(k+1,1) = In0.signals.values(i,1);
   Serial_Data_a(k+2,1) = In1.signals.values(i,1);
   Serial_Data_a(k+3,1) = In2.signals.values(i,1);
   Serial_Data_a(k+4,1) = In3.signals.values(i,1);   
   Serial_Data_a(k+5,1) = In4.signals.values(i,1);    
   Serial_Data_a(k+6,1) = In5.signals.values(i,1);
   Serial_Data_a(k+7,1) = In6.signals.values(i,1);   
   Serial_Data_a(k+8,1) = In7.signals.values(i,1);   

   Serial_Data_b(k+1,1) = In8.signals.values(i,1);
   Serial_Data_b(k+2,1) = In9.signals.values(i,1);
   Serial_Data_b(k+3,1) = In10.signals.values(i,1);
   Serial_Data_b(k+4,1) = In11.signals.values(i,1);
   Serial_Data_b(k+5,1) = In12.signals.values(i,1);   
   Serial_Data_b(k+6,1) = In13.signals.values(i,1);    
   Serial_Data_b(k+7,1) = In14.signals.values(i,1);
   Serial_Data_b(k+8,1) = In15.signals.values(i,1);   
   
   k = k + 8;
end

