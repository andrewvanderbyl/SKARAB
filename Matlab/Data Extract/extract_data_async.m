ddc_out_re = double(zeros(length(ddc_pol0_re.Data),1));
ddc_out_im = double(zeros(length(ddc_pol0_im.Data),1));
k = 1;
for i=1:length(ddc_pol0_re.Data)
   if ddc_dvalid.Data(i,1)==1
       ddc_out_re(k,1) = ddc_pol0_re.Data(i,1);
       ddc_out_im(k,1) = ddc_pol0_im.Data(i,1);
       k = k + 1;
   end
end

figure(1)
hold on;
plot(ddc_out_re)
plot(ddc_out_im)

ddc_ext_re =  ddc_out_re(100:100+4095);
ddc_ext_im =  ddc_out_im(100:100+4095);
ddc_ext_cmplx =  ddc_ext_re+1i*ddc_ext_im;

fft_ddc = fft(ddc_ext_cmplx);

figure(2)
semilogy(abs(fft_ddc))


% mix_re = double(zeros(length(ddc_re0.Data),1));
% mix_im = double(zeros(length(ddc_im0.Data),1));
% k = 1;
% for i=1:length(ddc_re0.Data)
%    if mix_dvalid.Data(i,1)==1
%        mix_re(k,1) = ddc_re0.Data(i,1);
%        mix_im(k,1) = ddc_im0.Data(i,1);
%        k = k + 1;
%    end
% end
% 
% figure(3)
% plot(mix_re)
% 
% mix_out = double(zeros(length(dec_tp1.Data),1));
% k = 1;
% for i=1:length(dec_tp1.Data)
%    if dec_dv.Data(i,1)==1
%        mix_out(k,1) = dec_tp1.Data(i,1);
%        k = k + 1;
%    end
% end
% figure(2)
% plot(mix_out)
