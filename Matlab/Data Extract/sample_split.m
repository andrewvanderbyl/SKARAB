% Purpose: Accept in a n-sample vector sequence and split according to
% desired length. 
% Input: n-smaple vector
% Output: Matrix where each row is a contiguous set of values of length M.
% Each col represents a new sample set separated by M-samples.

function [split_data] = sample_split(input, split_length)
    % check if the length can accommodate a split of split_length
    if (mod(length(input),split_length)) == 0
        split_data = reshape(input, split_length, length(input)/split_length);
    else
        mod_result = mod(length(input),split_length);
        split_data = reshape(input(:,1:end-mod_result), split_length, length(input(:,1:end-mod_result))/split_length);
        sprintf('split_length needs to be an integer multiple of the initial vector length. Truncating length.')
    end

end