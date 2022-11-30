function [Serial_Data, Dvalid] = Parallel_Serial_4input_dv(Input_0,Input_1,Input_2,Input_3, dvalid_in)
% Perform Parallel to serial conversion
k = 0;
num_inputs = 4;

%Check class of input
Input_class = class(Input_0);

if (strcmp(Input_class,'timeseries'))
    Serial_Data = zeros(num_inputs*length(Input_0.Data),1);
    Sync = zeros(num_inputs*length(Input_0.Data),1);
    Dvalid = zeros(num_inputs*length(Input_0.Data),1);

    for i=1:length(Input_0.Data)
       Serial_Data(k+1,1) = Input_0.Data(i,1);
       Serial_Data(k+2,1) = Input_1.Data(i,1);
       Serial_Data(k+3,1) = Input_2.Data(i,1);
       Serial_Data(k+4,1) = Input_3.Data(i,1);   
       
       Sync(k+1,1) = Sync_in.Data(i,1);
       
       if dvalid_in.Data(i,1)
           Dvalid((k+1):((k+num_inputs)),1) = ones(num_inputs,1);    
       else
           Dvalid((k+1):((k+num_inputs)),1) = zeros(num_inputs,1); 
       end
       k = k + num_inputs;
    end
elseif (strcmp(Input_class,'struct'))

    Serial_Data = zeros(length(Input_0.signals.values),1);
    Dvalid = zeros(num_inputs*length(Input_0.signals.values),1);

    for i=1:length(Input_0.signals.values)
       Serial_Data(k+1,1) = Input_0.signals.values(i,1);
       Serial_Data(k+2,1) = Input_1.signals.values(i,1);
       Serial_Data(k+3,1) = Input_2.signals.values(i,1);
       Serial_Data(k+4,1) = Input_3.signals.values(i,1);   
       
       if dvalid_in.Data(i,1)
           Dvalid((k+1):((k+num_inputs)),1) = ones(num_inputs,1);    
       else
           Dvalid((k+1):((k+num_inputs)),1) = zeros(num_inputs,1); 
       end
       k = k + num_inputs;
    end
elseif (strcmp(Input_class,'double'))
    Serial_Data = zeros(num_inputs*length(Input_0),1);
    Dvalid = zeros(num_inputs*length(Input_0),1);

    for i=1:length(Input_0)
       
       if dvalid_in(i,1)
           Serial_Data(k+1,1) = Input_0(i);
           Serial_Data(k+2,1) = Input_1(i);
           Serial_Data(k+3,1) = Input_2(i);
           Serial_Data(k+4,1) = Input_3(i);   

           Dvalid((k+1):((k+num_inputs)),1) = ones(num_inputs,1);    
           k = k + num_inputs;
       else
           Dvalid((k+1):((k+num_inputs)),1) = zeros(num_inputs,1); 
       end
       
    end
end

