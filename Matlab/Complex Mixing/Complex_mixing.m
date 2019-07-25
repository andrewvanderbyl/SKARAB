% Complex Mixing
% --------------

% Set variables: Osc Freq
freq = 153.5e6;
cycles = 1000;
fs = 1712e6;
Amplitude = 1;

[Real_Signal,Complex_Signal,Random_Signal] = Sig_Gen(freq,cycles,fs,Amplitude);
cmplx_osc = Complex_Signal;
real_osc = Real_Signal;

%--------------------------------------------------------------------------
% Set variables: Input Freq
freq = 153.5e6;
%freq = 207e6;
cycles = 1000;
fs = 1712e6;
Amplitude = 1;

[Real_Signal,Complex_Signal,Random_Signal] = Sig_Gen(freq,cycles,fs,Amplitude);
cmplx_input = Complex_Signal;
real_input = Real_Signal;
%--------------------------------------------------------------------------

% Mix
cmplx_mix = cmplx_osc(1:1024).*cmplx_input(1:1024);
real_cmplx_mix = cmplx_osc(1:1024).*real_input(1:1024);
real_mix = real_osc(1:1024).*real_input(1:1024);


fft_cmpx_mix = fft(cmplx_mix);
fft_real_cmplx_mix = fft(real_cmplx_mix);
fft_real_mix = fft(real_mix);



% figure(1)
% subplot(3,1,1)
% plot(abs(fft_cmpx_mix.^2))
% subplot(3,1,2)
% plot(abs(fft_real_cmplx_mix.^2))
% subplot(3,1,3)
% plot(abs(fft_real_mix.^2))

% Simulink Results
[cwg, Dvalid] = Parallel_Serial(cwg0.Data, cwg1.Data, cwg2.Data, cwg3.Data, cwg4.Data, cwg5.Data, cwg6.Data, cwg7.Data, dvalid);
[dds_cos, Dvalid] = Parallel_Serial(dds_cos0.Data, dds_cos1.Data, dds_cos2.Data, dds_cos3.Data, dds_cos4.Data, dds_cos5.Data, dds_cos6.Data, dds_cos7.Data, dvalid);
[dds_sin, Dvalid] = Parallel_Serial(dds_sin0.Data, dds_sin1.Data, dds_sin2.Data, dds_sin3.Data, dds_sin4.Data, dds_sin5.Data, dds_sin6.Data, dds_sin7.Data, dvalid);

dds_cmplx = dds_cos+1i*dds_sin;

%Mix
real_cmplx_mix_sim = dds_cmplx(500:500+1023).*cwg(500:500+1023);
fft_mix_sim =  fft(real_cmplx_mix_sim);

% figure(3)
% semilogy(abs(fft_mix_sim.^2))

% Simulink Mix
[ddc_re, Dvalid] = Parallel_Serial(ddc_re0.Data, ddc_re1.Data, ddc_re2.Data, ddc_re3.Data, ddc_re4.Data, ddc_re5.Data, ddc_re6.Data, ddc_re7.Data, mix_dvalid);
[ddc_im, Dvalid] = Parallel_Serial(ddc_im0.Data, ddc_im1.Data, ddc_im2.Data, ddc_im3.Data, ddc_im4.Data, ddc_im5.Data, ddc_im6.Data, ddc_im7.Data, mix_dvalid);

ddc_cmplx = ddc_re+1i*ddc_im;
fft_ddc_sim =  fft(ddc_cmplx(755:755+1023));

% figure(4)
% semilogy(abs(fft_ddc_sim.^2))

% Iterate through as the dvalid toggles
k=1;
for i=1:length(ddc_dvalid.data)
    if ddc_dvalid.data(i,1) == 1
        ddc_out_cmplx(k,1) =  ddc_pol0_re.data(i,1)+1i*ddc_pol0_im.data(i,1);
        k = k+1;
    end
end

fft_ddc_out_sim =  fft(ddc_out_cmplx(100:100+1023,1));

% figure(5)
% semilogy(abs(fft_ddc_out_sim.^2))



% Iterate through as the dvalid toggles
k=1;
for i=1:length(fir_dv.data)
    if fir_dv.data(i,1) == 1
        fir_cmplx(k,1) =  fir_re.data(i,1)+1i*fir_im.data(i,1);
        k = k+1;
    end
end

figure(6)
plot(real(fir_cmplx))

fft_fir_cmplx_sim =  fft(fir_cmplx(2305:2305+1023,1));

figure(7)
semilogy(abs(fft_fir_cmplx_sim.^2))

fft_sim = fft_re.data+1i*fft_im.data;
figure(8)
semilogy(abs(fft_sim.^2))


