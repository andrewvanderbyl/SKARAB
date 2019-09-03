[osc_data, Dvalid] = Parallel_Serial(dds7, dds6, dds5, dds4, dds3, dds2, dds1, dds0, dvalid2);
[cwg_data, Dvalid] = Parallel_Serial(cwg7, cwg6, cwg5, cwg4, cwg3, cwg2, cwg1, cwg0, dvalid);
fft_cw = fft(cwg_data(502:502+2048));
fft_osc = fft(osc_data(502:502+2048));

% figure(1)
% hold on;
% plot(osc_data)
% plot(cwg_data)

% figure(2)
% plot(abs(fft_osc))
% figure(3)
% plot(abs(fft_cw))

% Before FIR filter
% [mix_data, Dvalid] = Parallel_Serial(ddc1, ddc2, ddc3, ddc4, ddc5, ddc6, ddc7, ddc8, mix_dvalid);
% fft_mix = fft(mix_data(800:800+2048));
% figure(4)
% plot(abs(fft_mix))

% After FIR filter
fft_ddc = fft(ddc_pol0.Data(686:686+512));
figure(5)
plot(abs(fft_ddc))

