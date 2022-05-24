function [out_re, out_im] = extract_data_async(data_in_real, data_in_im, data_sync, data_valid, extract_length)

out_re = double(zeros(length(data_in_real.Data),1));
out_im = double(zeros(length(data_in_im.Data),1));

% Find sync position
sync_pos = find(data_sync.data==1);
k = 1;
for i=sync_pos:length(data_in_real.Data)
   if data_valid.Data(i,1)==1
       out_re(k,1) = data_in_real.Data(i,1);
       out_im(k,1) = data_in_im.Data(i,1);
       k = k + 1;
   end
end

out_re = out_re(extract_length:extract_length+extract_length);
out_im = out_im(extract_length:extract_length+extract_length);

figure(1)
hold on;
plot(out_re)
plot(out_im)
hold off;


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
