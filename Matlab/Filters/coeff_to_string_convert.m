function [C] = coeff_to_string_convert(Coeffs) 
%Take Coeff variable in worspace and make a string inserting commas between
%values.
c = [sprintf('%.20f',Coeffs(1,1)),','];
    
for i=2:length(Coeffs)
    c = [c, sprintf('%.20f',Coeffs(1,i))];
    
    if i < length(Coeffs)
        c = [c, ','];
    end
end

C = ['[',c,']'];

% Print to command window. Copy this output to the Coeff variable place in
% filter block
C

