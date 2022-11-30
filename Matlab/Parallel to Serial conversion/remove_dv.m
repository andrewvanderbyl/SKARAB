function [output] = remove_dv(Input, dvalid)
% Remove gaps in data where dvalid is zero.
k = 1;
    for i=1:length(Input)
        if dvalid(i)
            output(k,1) = Input(i);        
            k = k+1;
        end
    end
end
