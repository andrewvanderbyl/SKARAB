function [resampled] = resample_series(input, R)

    % extract every R sample where R is the resample factor.
    resampled = input(1:R:end);

end