function[simin1] = gen_hmc_reord_sim_data(randomness,length)
uppr=length/randomness
for n=0:uppr
simin1(n*randomness+1:(n+1)*randomness,2)=((randperm(randomness,randomness)-1)+randomness*n);
simin1(n*randomness+1:(n+1)*randomness,1)=[n*randomness:(n+1)*randomness-1];
end
end

%try this: gen_hmc_reord_sim_data(16,65536)