function [M_path_data] = m_path_split(input, M)

    entries_per_row = floor(length(input)/M);
    M_path_data = zeros(M, entries_per_row);
    
    % Split the input data series into M-paths.
    for r = 1:M
        row_data = input(r:M:end);
        M_path_data(r,:) = row_data(1:entries_per_row);
    end

end