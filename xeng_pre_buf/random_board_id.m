function random_board_id

random_number = rand(1,1);

if ((random_number)< 0.25)
    init_board_id = 0;
elseif ((random_number >= 0.25) && (random_number < 0.5))
    init_board_id = 1;
elseif ((random_number >= 0.5) && (random_number < 0.75))
    init_board_id = 2;
else
    init_board_id = 3;
end

random_number = rand(1,1);

% Compute next board id
if init_board_id == 0
    if ((random_number)< 1/3)
        init_board_id = 1;
    elseif ((random_number >= 1/3) && (random_number < 2/3))
        init_board_id = 2;
    else
        init_board_id = 3;
    end    
end

if init_board_id == 1
    if ((random_number)< 1/3)
        init_board_id = 0;
    elseif ((random_number >= 1/3) && (random_number < 2/3))
        init_board_id = 2;
    else
        init_board_id = 3;
    end    
end

if init_board_id == 2
    if ((random_number)< 1/3)
        init_board_id = 0;
    elseif ((random_number >= 1/3) && (random_number < 2/3))
        init_board_id = 1;
    else
        init_board_id = 3;
    end    
end

if init_board_id == 3
    if ((random_number)< 1/3)
        init_board_id = 0;
    elseif ((random_number >= 1/3) && (random_number < 2/3))
        init_board_id = 1;
    else
        init_board_id = 2;
    end    
end

end