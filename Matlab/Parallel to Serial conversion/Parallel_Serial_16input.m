function [Serial_Data, Dvalid] = Parallel_Serial_16input(in0,in1,in2,in3,in4,in5,in6,in7,in8,in9,in10,in11,in12,in13,in14,in15, dvalid_in)
% Perform Parallel to serial conversion
k = 0;

%Check class of input
Input_class = class(in0);

if (strcmp(Input_class,'timeseries'))
    Serial_Data = zeros(16*length(in0.Data),1);
    Dvalid = zeros(16*length(in0.Data),1);

    for i=1:length(in0.Data)
       Serial_Data(k+1,1) = in0.Data(i,1);
       Serial_Data(k+2,1) = in1.Data(i,1);
       Serial_Data(k+3,1) = in2.Data(i,1);
       Serial_Data(k+4,1) = in3.Data(i,1);   
       Serial_Data(k+5,1) = in4.Data(i,1);    
       Serial_Data(k+6,1) = in5.Data(i,1);
       Serial_Data(k+7,1) = in6.Data(i,1);   
       Serial_Data(k+8,1) = in7.Data(i,1);   
       Serial_Data(k+9,1) = in8.Data(i,1);
       Serial_Data(k+10,1) = in9.Data(i,1);
       Serial_Data(k+11,1) = in10.Data(i,1);
       Serial_Data(k+12,1) = in11.Data(i,1);   
       Serial_Data(k+13,1) = in12.Data(i,1);    
       Serial_Data(k+14,1) = in13.Data(i,1);
       Serial_Data(k+15,1) = in14.Data(i,1);   
       Serial_Data(k+16,1) = in15.Data(i,1);   
       
       if dvalid_in.Data(i,1)
           Dvalid((k+1):((k+16)),1) = ones(16,1);    
       else
           Dvalid((k+1):((k+16)),1) = zeros(16,1); 
       end
       k = k + 16;
    end
elseif (strcmp(Input_class,'struct'))

    Serial_Data = zeros(length(Input_0.signals.values),1);
    Dvalid = zeros(8*length(Input_0.signals.values),1);

    for i=1:length(Input_0.signals.values)
       Serial_Data(k+1,1) = Input_0.signals.values(i,1);
       Serial_Data(k+2,1) = Input_1.signals.values(i,1);
       Serial_Data(k+3,1) = Input_2.signals.values(i,1);
       Serial_Data(k+4,1) = Input_3.signals.values(i,1);   
       Serial_Data(k+5,1) = Input_4.signals.values(i,1);    
       Serial_Data(k+6,1) = Input_5.signals.values(i,1);
       Serial_Data(k+7,1) = Input_6.signals.values(i,1);   
       Serial_Data(k+8,1) = Input_7.signals.values(i,1);   
       
       if dvalid_in.Data(i,1)
           Dvalid((k+1):((k+8)),1) = ones(8,1);    
       else
           Dvalid((k+1):((k+8)),1) = zeros(8,1); 
       end
       k = k + 8;
    end
elseif (strcmp(Input_class,'double'))
    Serial_Data = zeros(8*length(Input_0),1);
    Dvalid = zeros(8*length(Input_0),1);

    for i=1:length(Input_0)
       Serial_Data(k+1,1) = Input_0(i);
       Serial_Data(k+2,1) = Input_1(i);
       Serial_Data(k+3,1) = Input_2(i);
       Serial_Data(k+4,1) = Input_3(i);   
       Serial_Data(k+5,1) = Input_4(i);    
       Serial_Data(k+6,1) = Input_5(i);
       Serial_Data(k+7,1) = Input_6(i);   
       Serial_Data(k+8,1) = Input_7(i);  
       
       k = k + 8;
    end
end

