function [Spec,Sync,Dvalid] = Parallel_Serial_Spectral_4k(Input_0,Input_1,Input_2,Input_3,Sync_in,dvalid_in)
% Perform Parallel to serial conversion
k = 0;

%Check class of input
Input_class = class(Input_0);

if (strcmp(Input_class,'timeseries'))
    Spec = zeros(4*length(Input_0.Data),1);
    Sync = zeros(4*length(Input_0.Data),1);
    Dvalid = zeros(4*length(Input_0.Data),1);
    
    for i=1:length(Input_0.Data)
       Spec(k+1,1) = Input_0.Data(i,1);
       Spec(k+2,1) = Input_1.Data(i,1);
       Spec(k+3,1) = Input_2.Data(i,1);
       Spec(k+4,1) = Input_3.Data(i,1);  
       
       Sync(k+1,1) = Sync_in.Data(i,1);
       
       if dvalid_in.Data(i,1)
           Dvalid((k+1):((k+4)),1) = ones(4,1);    
       else
           Dvalid((k+1):((k+4)),1) = zeros(4,1); 
       end
       k = k + 4;
    end
    
elseif (strcmp(Input_class,'struct'))

    Spec = zeros(length(Input_0.signals.values),1);
    Sync = zeros(4*length(Input_0.Data),1);
    Dvalid = zeros(4*length(Input_0.Data),1);

    for i=1:length(Input_0.signals.values)
       Spec(k+1,1) = Input_0.signals.values(i,1);
       Spec(k+2,1) = Input_1.signals.values(i,1);
       Spec(k+3,1) = Input_2.signals.values(i,1);
       Spec(k+4,1) = Input_3.signals.values(i,1);
       
       Sync(k+1,1) = Sync_in.Data(i,1);
       
       if dvalid_in.Data(i,1)
           Dvalid((k+1):((k+4)),1) = ones(4,1);    
       else
           Dvalid((k+1):((k+4)),1) = zeros(4,1); 
       end
       
       k = k + 4;
    end
    
elseif (strcmp(Input_class,'double'))
    Spec = zeros(4*length(Input_0),1);
    Sync = zeros(4*length(Input_0.Data),1);
    Dvalid = zeros(4*length(Input_0.Data),1);

    for i=1:length(Input_0)
       Spec(k+1,1) = Input_0(i);
       Spec(k+2,1) = Input_1(i);
       Spec(k+3,1) = Input_2(i);
       Spec(k+4,1) = Input_3(i);
       
       Sync(k+1,1) = Sync_in.Data(i,1);
       
       if dvalid_in.Data(i,1)
           Dvalid((k+1):((k+4)),1) = ones(4,1);    
       else
           Dvalid((k+1):((k+4)),1) = zeros(4,1); 
       end
       
       k = k + 4;
    end
end



