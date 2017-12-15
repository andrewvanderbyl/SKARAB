% Clear the workspace
clear

% Load coefficients captured in Matlab (cosin_init.m)(before fixed_point
% conversion)
cd /home/jasper/Desktop/
load d_bf0.mat
load d_bf10.mat
load d_bf11.mat
load d_bf20.mat
load d_bf21.mat
load d_bf22.mat
load d_bf23.mat

% Load coefficients captured in simulink (fixed-point)
%load coeffs_direct_fft_new.mat
%load coeffs_direct_fft_BRAM_Share.mat
%load coeffs_direct_fft_all.mat
load coeffs_direct_fft_no_select.mat



% Transpose the matrix for each direct_fft (float) coefficient
d_bf0_real = d_bf0_real';
d_bf0_imag =  d_bf0_imag';

d_bf10_imag = d_bf10_imag';
d_bf10_real = d_bf10_real';

d_bf11_imag = d_bf11_imag';
d_bf11_real = d_bf11_real';

d_bf20_real = d_bf20_real';
d_bf20_imag = d_bf20_imag';

d_bf21_imag = d_bf21_imag';
d_bf21_real = d_bf21_real';

d_bf22_imag = d_bf22_imag';
d_bf22_real = d_bf22_real';

d_bf23_imag = d_bf23_imag';
d_bf23_real = d_bf23_real';

% Compare Coefficients

% Direct FFT: BF0
diff_bf00_real = butterfly0_0r.Data(2029:2029+1020,1) - d_bf0_real(4:end,1);
diff_bf00_imag = butterfly0_0i.Data(2029:2029+1020,1) - d_bf0_imag(4:end,1);

tc00 = butterfly0_0r.Data(2029:2029+1020,1);
ts00 = d_bf0_real(4:end,1);

% Direct FFT: BF10
diff_bf10_real = butterfly1_0r.Data(2073:2073+length(d_bf10_real(7:end,1))-1,1) - d_bf10_real(7:end,1);
diff_bf10_imag = butterfly1_0i.Data(2073:2073+length(d_bf10_imag(7:end,1))-1,1) - d_bf10_imag(7:end,1);

tc10 = butterfly1_0r.Data(2073:2073+length(d_bf10_real(7:end,1))-1,1);
ts10 = d_bf10_real(7:end,1);

% Direct FFT: BF11
diff_bf11_real = butterfly1_1r.Data(2067:2067+length(d_bf11_real(:,1))-1,1) - d_bf11_real(:,1);
diff_bf11_imag = butterfly1_1i.Data(2067:2067+length(d_bf11_imag(:,1))-1,1) - d_bf11_imag(:,1);

tc11 = butterfly1_1i.Data(2067:2067+length(d_bf11_real(:,1))-1,1);
ts11 = d_bf11_real(:,1);

% Direct FFT: BF20
diff_bf20_real = butterfly2_0r.Data(2120:2120+length(d_bf20_real(14:end,1))-1,1) - d_bf20_real(14:end,1);
diff_bf20_imag = butterfly2_0r.Data(2120:2120+length(d_bf20_imag(14:end,1))-1,1) - d_bf20_imag(14:end,1);

tc20 = butterfly2_0r.Data(2120:2120+length(d_bf20_real(14:end,1))-1,1);
ts20 = d_bf20_real(14:end,1);


% Direct FFT: BF21
diff_bf21_real = butterfly2_1r.Data(2108:2108+length(d_bf21_real(2:end,1))-1,1) - d_bf21_real(2:end,1);
diff_bf21_imag = butterfly2_1i.Data(2108:2108+length(d_bf21_imag(2:end,1))-1,1) - d_bf21_imag(2:end,1);

tc21 = butterfly2_1r.Data(2108:2108+length(d_bf21_real(2:end,1))-1,1);
ts21 = d_bf21_real(2:end,1);

% Direct FFT: BF22
diff_bf22_real = butterfly2_2r.Data(2107:2107+length(d_bf22_real(1:end,1))-1,1) - d_bf22_real(1:end,1);
diff_bf22_imag = butterfly2_2i.Data(2107:2107+length(d_bf22_imag(1:end,1))-1,1) - d_bf22_imag(1:end,1);

tc22 = butterfly2_2r.Data(2107:2107+length(d_bf22_real(1:end,1))-1,1);
ts22 = d_bf22_real(1:end,1);


% Direct FFT: BF23
diff_bf23_real = butterfly2_3r.Data(2107:2107+length(d_bf23_real(:,1))-1,1) - d_bf23_real(:,1);
diff_bf23_imag = butterfly2_3i.Data(2107:2107+length(d_bf23_imag(:,1))-1,1) - d_bf23_imag(:,1);

tc23 = butterfly2_3r.Data(2107:2107+length(d_bf23_real(:,1))-1,1);
ts23 = d_bf23_real(:,1);



figure(1)
subplot(3,3,1)
hold on
plot(butterfly0_0r.Data)
plot(butterfly0_0i.Data)
hold off
subplot(3,3,2)
hold on
plot(butterfly1_0r.Data)
plot(butterfly1_0i.Data)
hold off
subplot(3,3,3)
hold on
plot(butterfly1_1r.Data)
plot(butterfly1_1i.Data)
hold off
subplot(3,3,4)
hold on
plot(butterfly2_0r.Data)
plot(butterfly2_0i.Data)
hold off
subplot(3,3,5)
hold on
plot(butterfly2_1r.Data)
plot(butterfly2_1i.Data)
hold off
subplot(3,3,6)
hold on
plot(butterfly2_2r.Data)
plot(butterfly2_2i.Data)
hold off
subplot(3,3,7)
hold on
plot(butterfly2_3r.Data)
plot(butterfly2_3i.Data)
hold off

figure(2)
subplot(3,3,1)
hold on
plot(tc00)
plot(ts00)
hold off
subplot(3,3,2)
hold on
plot(tc10)
plot(ts10)
hold off
subplot(3,3,3)
hold on
plot(tc11)
plot(ts11)
hold off
subplot(3,3,4)
hold on
plot(tc20)
plot(ts20)
hold off
subplot(3,3,5)
hold on
plot(tc21)
plot(ts21)
hold off
subplot(3,3,6)
hold on
plot(tc22)
plot(ts22)
hold off
subplot(3,3,7)
hold on
plot(tc23)
plot(ts23)
hold off

figure(3)
subplot(3,3,1)
hold on
plot(diff_bf00_real)
hold off
subplot(3,3,2)
hold on
plot(diff_bf10_real)
hold off
subplot(3,3,3)
hold on
plot(diff_bf11_real)
hold off
subplot(3,3,4)
hold on
plot(diff_bf20_real)
hold off
subplot(3,3,5)
hold on
plot(diff_bf21_real)
hold off
subplot(3,3,6)
hold on
plot(diff_bf22_real)
hold off
subplot(3,3,7)
hold on
plot(diff_bf23_real)
hold off

figure(4)
subplot(3,3,1)
hold on
plot(diff_bf00_imag)
hold off
subplot(3,3,2)
hold on
plot(diff_bf10_imag)
hold off
subplot(3,3,3)
hold on
plot(diff_bf11_imag)
hold off
subplot(3,3,4)
hold on
plot(diff_bf20_imag)
hold off
subplot(3,3,5)
hold on
plot(diff_bf21_imag)
hold off
subplot(3,3,6)
hold on
plot(diff_bf22_imag)
hold off
subplot(3,3,7)
hold on
plot(diff_bf23_imag)
hold off
