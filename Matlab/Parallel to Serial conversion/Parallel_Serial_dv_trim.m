function [Serial_Data] = Parallel_Serial_dv_trim(Input_0,Input_1,Input_2,Input_3,Input_4,Input_5,Input_6,Input_7, dvalid_in)
% Perform Parallel to serial conversion
k = 0;


%Check class of input
Input_class = class(Input_0);

if (strcmp(Input_class,'timeseries'))
    Serial_Data = zeros(8*length(Input_0.Data),1);

    for i=1:length(Input_0.Data)
       if dvalid_in.Data(i,1)
           Serial_Data(k+1,1) = Input_0.Data(i,1);
           Serial_Data(k+2,1) = Input_1.Data(i,1);
           Serial_Data(k+3,1) = Input_2.Data(i,1);
           Serial_Data(k+4,1) = Input_3.Data(i,1);   
           Serial_Data(k+5,1) = Input_4.Data(i,1);    
           Serial_Data(k+6,1) = Input_5.Data(i,1);
           Serial_Data(k+7,1) = Input_6.Data(i,1);   
           Serial_Data(k+8,1) = Input_7.Data(i,1); 
           k=k+8;
       end
    end
elseif (strcmp(Input_class,'struct'))

    Serial_Data = zeros(length(Input_0.signals.values),1);

    for i=1:length(Input_0.signals.values)
       
       if dvalid_in.Data(i,1)
           Serial_Data(k+1,1) = Input_0.signals.values(i,1);
           Serial_Data(k+2,1) = Input_1.signals.values(i,1);
           Serial_Data(k+3,1) = Input_2.signals.values(i,1);
           Serial_Data(k+4,1) = Input_3.signals.values(i,1);   
           Serial_Data(k+5,1) = Input_4.signals.values(i,1);    
           Serial_Data(k+6,1) = Input_5.signals.values(i,1);
           Serial_Data(k+7,1) = Input_6.signals.values(i,1);   
           Serial_Data(k+8,1) = Input_7.signals.values(i,1);   
           k=k+8;
       end
    end
    
elseif (strcmp(Input_class,'double'))
    Serial_Data = zeros(8*length(Input_0),1);
    for i=1:length(Input_0)
       if dvalid_in.Data(i,1)       
       %if dvalid_in(i,1)
           Serial_Data(k+1,1) = Input_0(i);
           Serial_Data(k+2,1) = Input_1(i);
           Serial_Data(k+3,1) = Input_2(i);
           Serial_Data(k+4,1) = Input_3(i);   
           Serial_Data(k+5,1) = Input_4(i);    
           Serial_Data(k+6,1) = Input_5(i);
           Serial_Data(k+7,1) = Input_6(i);   
           Serial_Data(k+8,1) = Input_7(i); 
           k=k+8;
       end
    end
end

