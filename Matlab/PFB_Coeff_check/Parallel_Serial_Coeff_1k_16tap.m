function [coeffs] = Parallel_Serial_Coeff_1k_16tap()

% Command line use case:
% First run simulation (pfb_coeff_sim.slx) with bus_expand blocks tapped to the 'coeffs' out of the 
% pfb_fir_coeff_gen block (before the munge). The bus_exand should be set
% as (num outputs = 2; output width = 64*18; output bin point = 0). This will
% split the bus as 64 18b outputs (which is native to the rom output). To
% the 'msb_out2' of the bus expand add another bus expand set 
% as (num outputs = 64; output width = 18; output bin point = 17, fix=1 with 'Output to workspace checked and 
% Variable prefix name set as coeffs). Run the sim and save all the
% 'coeffs_x' in one .mat file (e.g. coeffs_1k_16tap.mat).

%Once saved, run on the command line (or click 'Run'):

% coeffs = Parallel_Serial_Coeff_1k_16tap;

%NOTE: It may be necessary to manually determine the starting point for
%each phase when rebuilding.

%filename = 'coeffs_1k_16tap_bin1';
filename = 'coeffs_1k_16tap_bin091';


load(filename)

%function [Serial_Data_a] = Parallel_Serial_Coeff_1k_16tap(coeffs_1,coeffs_2,coeffs_3,coeffs_4,coeffs_5,coeffs_6,coeffs_7,coeffs_8,coeffs_9,coeffs_10,coeffs_11,coeffs_12,coeffs_13,coeffs_14,coeffs_15,coeffs_16,coeffs_17,coeffs_18,coeffs_19,coeffs_20, coeffs_21,coeffs_22,coeffs_23,coeffs_24,coeffs_25,coeffs_26,coeffs_27,coeffs_28,coeffs_29,coeffs_30,coeffs_31,coeffs_32,coeffs_33,coeffs_34,coeffs_35,coeffs_36,coeffs_37,coeffs_38,coeffs_39,coeffs_40,coeffs_41,coeffs_42,coeffs_43,coeffs_44,coeffs_45,coeffs_46,coeffs_47,coeffs_48,coeffs_49,coeffs_50,coeffs_51,coeffs_52,coeffs_53,coeffs_54,coeffs_55,coeffs_56,coeffs_57,coeffs_58,coeffs_59,coeffs_60,coeffs_61,coeffs_62,coeffs_63,coeffs_64,coeffs_65,coeffs_66,coeffs_67,coeffs_68,coeffs_69,coeffs_70,coeffs_71,coeffs_72,coeffs_73,coeffs_74,coeffs_75,coeffs_76,coeffs_77,coeffs_78,coeffs_79,coeffs_80,coeffs_91,coeffs_92,coeffs_93,coeffs_94,coeffs_95,coeffs_96,coeffs_97,coeffs_98,coeffs_99,coeffs_100,coeffs_101,coeffs_102,coeffs_103,coeffs_104,coeffs_105,coeffs_106,coeffs_107,coeffs_108,coeffs_109,coeffs_110,coeffs_111,coeffs_112,coeffs_113,coeffs_114,coeffs_115,coeffs_116,coeffs_117,coeffs_118,coeffs_119,coeffs_120,coeffs_121,coeffs_122,coeffs_123,coeffs_124,coeffs_125,coeffs_126,coeffs_127,coeffs_128)

%function [Serial_Data_a] = Parallel_Serial_Coeff_1k_16tap(coeffs_1,coeffs_2,coeffs_3,coeffs_4,coeffs_5,coeffs_6,coeffs_7,coeffs_8,coeffs_9,coeffs_10,...
%    coeffs_11,coeffs_12,coeffs_13,coeffs_14,coeffs_15,coeffs_16,coeffs_17,coeffs_18,coeffs_19,coeffs_20, ...
%    coeffs_21,coeffs_22,coeffs_23,coeffs_24,coeffs_25,coeffs_26,coeffs_27,coeffs_28,coeffs_29,coeffs_30, ...
%    coeffs_31,coeffs_32,coeffs_33,coeffs_34,coeffs_35,coeffs_36,coeffs_37,coeffs_38,coeffs_39,coeffs_40, ...    
%    coeffs_41,coeffs_42,coeffs_43,coeffs_44,coeffs_45,coeffs_46,coeffs_47,coeffs_48,coeffs_49,coeffs_50, ...
%    coeffs_51,coeffs_52,coeffs_53,coeffs_54,coeffs_55,coeffs_56,coeffs_57,coeffs_58,coeffs_59,coeffs_60, ...
%    coeffs_61,coeffs_62,coeffs_63,coeffs_64,coeffs_65,coeffs_66,coeffs_67,coeffs_68,coeffs_69,coeffs_70, ...
%    coeffs_71,coeffs_72,coeffs_73,coeffs_74,coeffs_75,coeffs_76,coeffs_77,coeffs_78,coeffs_79,coeffs_80, ...
%    coeffs_91,coeffs_92,coeffs_93,coeffs_94,coeffs_95,coeffs_96,coeffs_97,coeffs_98,coeffs_99,coeffs_100, ...
%   coeffs_101,coeffs_102,coeffs_103,coeffs_104,coeffs_105,coeffs_106,coeffs_107,coeffs_108,coeffs_109,coeffs_110, ...
%   coeffs_111,coeffs_112,coeffs_113,coeffs_114,coeffs_115,coeffs_116,coeffs_117,coeffs_118,coeffs_119,coeffs_120, ...    
%   coeffs_121,coeffs_122,coeffs_123,coeffs_124,coeffs_125,coeffs_126,coeffs_127,coeffs_128)




% Perform Parallel to serial conversion
k = 0;
phase1 = zeros(length(coeffs_1.signals.values),1);
phase2 = zeros(length(coeffs_1.signals.values),1);
phase3 = zeros(length(coeffs_1.signals.values),1);
phase4 = zeros(length(coeffs_1.signals.values),1);
phase5 = zeros(length(coeffs_1.signals.values),1);
phase6 = zeros(length(coeffs_1.signals.values),1);
phase7 = zeros(length(coeffs_1.signals.values),1);
phase8 = zeros(length(coeffs_1.signals.values),1);

for i=1:length(coeffs_1.signals.values)
   phase1(k+1,1) = coeffs_8.signals.values(i,1);
   phase1(k+2,1) = coeffs_7.signals.values(i,1);
   phase1(k+3,1) = coeffs_6.signals.values(i,1);
   phase1(k+4,1) = coeffs_5.signals.values(i,1);   
   phase1(k+5,1) = coeffs_4.signals.values(i,1);    
   phase1(k+6,1) = coeffs_3.signals.values(i,1);
   phase1(k+7,1) = coeffs_2.signals.values(i,1);   
   phase1(k+8,1) = coeffs_1.signals.values(i,1);   

   phase2(k+1,1) = coeffs_16.signals.values(i,1);
   phase2(k+2,1) = coeffs_15.signals.values(i,1);
   phase2(k+3,1) = coeffs_14.signals.values(i,1);
   phase2(k+4,1) = coeffs_13.signals.values(i,1);   
   phase2(k+5,1) = coeffs_12.signals.values(i,1);    
   phase2(k+6,1) = coeffs_11.signals.values(i,1);
   phase2(k+7,1) = coeffs_10.signals.values(i,1);   
   phase2(k+8,1) = coeffs_9.signals.values(i,1);   
   
   phase3(k+1,1) = coeffs_24.signals.values(i,1);
   phase3(k+2,1) = coeffs_23.signals.values(i,1);
   phase3(k+3,1) = coeffs_22.signals.values(i,1);
   phase3(k+4,1) = coeffs_21.signals.values(i,1);   
   phase3(k+5,1) = coeffs_20.signals.values(i,1);    
   phase3(k+6,1) = coeffs_19.signals.values(i,1);
   phase3(k+7,1) = coeffs_18.signals.values(i,1);   
   phase3(k+8,1) = coeffs_17.signals.values(i,1);   
   
   phase4(k+1,1) = coeffs_32.signals.values(i,1);
   phase4(k+2,1) = coeffs_31.signals.values(i,1);
   phase4(k+3,1) = coeffs_30.signals.values(i,1);
   phase4(k+4,1) = coeffs_29.signals.values(i,1);   
   phase4(k+5,1) = coeffs_28.signals.values(i,1);    
   phase4(k+6,1) = coeffs_27.signals.values(i,1);
   phase4(k+7,1) = coeffs_26.signals.values(i,1);   
   phase4(k+8,1) = coeffs_25.signals.values(i,1);   
   
   phase5(k+1,1) = coeffs_40.signals.values(i,1);
   phase5(k+2,1) = coeffs_39.signals.values(i,1);
   phase5(k+3,1) = coeffs_38.signals.values(i,1);
   phase5(k+4,1) = coeffs_37.signals.values(i,1);   
   phase5(k+5,1) = coeffs_36.signals.values(i,1);    
   phase5(k+6,1) = coeffs_35.signals.values(i,1);
   phase5(k+7,1) = coeffs_34.signals.values(i,1);   
   phase5(k+8,1) = coeffs_33.signals.values(i,1); 
   
   phase6(k+1,1) = coeffs_48.signals.values(i,1);
   phase6(k+2,1) = coeffs_47.signals.values(i,1);
   phase6(k+3,1) = coeffs_46.signals.values(i,1);
   phase6(k+4,1) = coeffs_45.signals.values(i,1);   
   phase6(k+5,1) = coeffs_44.signals.values(i,1);    
   phase6(k+6,1) = coeffs_43.signals.values(i,1);
   phase6(k+7,1) = coeffs_42.signals.values(i,1);   
   phase6(k+8,1) = coeffs_41.signals.values(i,1);  
   
   phase7(k+1,1) = coeffs_56.signals.values(i,1);
   phase7(k+2,1) = coeffs_55.signals.values(i,1);
   phase7(k+3,1) = coeffs_54.signals.values(i,1);
   phase7(k+4,1) = coeffs_53.signals.values(i,1);   
   phase7(k+5,1) = coeffs_52.signals.values(i,1);    
   phase7(k+6,1) = coeffs_51.signals.values(i,1);
   phase7(k+7,1) = coeffs_50.signals.values(i,1);   
   phase7(k+8,1) = coeffs_49.signals.values(i,1);  
   
   phase8(k+1,1) = coeffs_64.signals.values(i,1);
   phase8(k+2,1) = coeffs_63.signals.values(i,1);
   phase8(k+3,1) = coeffs_62.signals.values(i,1);
   phase8(k+4,1) = coeffs_61.signals.values(i,1);   
   phase8(k+5,1) = coeffs_60.signals.values(i,1);    
   phase8(k+6,1) = coeffs_59.signals.values(i,1);
   phase8(k+7,1) = coeffs_58.signals.values(i,1);   
   phase8(k+8,1) = coeffs_57.signals.values(i,1);  
   
   k = k + 8;
end   

phase_length = 2048;
p8_sp = 16433; %12458 %12338 
p8_ep = p8_sp + phase_length;

p7_sp = 16433; %12337 %12338
p7_ep = p7_sp + phase_length;

p6_sp = 16433;
p6_ep = p6_sp + phase_length;

p5_sp = 16433;
p5_ep = p5_sp + phase_length;

p4_sp = 16433;
p4_ep = p4_sp + phase_length;

p3_sp = 16433;
p3_ep = p3_sp + phase_length;

p2_sp = 16433;
p2_ep = p2_sp + phase_length;

p1_sp = 16433;
p1_ep = p1_sp + phase_length;

coeffs = 0;

% Recombine
coeffs(1:phase_length,1) = phase8(p8_sp:p8_ep-1,1);
coeffs((phase_length+1:phase_length*2),1) = phase7(p7_sp:p7_ep-1,1);
coeffs((phase_length*2+1:phase_length*3),1) = phase6(p6_sp:p6_ep-1,1);
coeffs((phase_length*3+1:phase_length*4),1) = phase5(p5_sp:p5_ep-1,1);   
coeffs((phase_length*4+1:phase_length*5),1) = phase4(p4_sp:p4_ep-1,1);    
coeffs((phase_length*5+1:phase_length*6),1) = phase3(p3_sp:p3_ep-1,1);
coeffs((phase_length*6+1:phase_length*7),1) = phase2(p2_sp:p2_ep-1,1);   
coeffs((phase_length*7+1:phase_length*8),1) = phase1(p1_sp:p1_ep-1,1);  

plot(coeffs)

a = 1;
%    Serial_Data_a(k+9,1) = coeffs_120.signals.values(i,1);
%    Serial_Data_a(k+10,1) = coeffs_119.signals.values(i,1);
%    Serial_Data_a(k+11,1) = coeffs_118.signals.values(i,1);
%    Serial_Data_a(k+12,1) = coeffs_117.signals.values(i,1);   
%    Serial_Data_a(k+13,1) = coeffs_116.signals.values(i,1);    
%    Serial_Data_a(k+14,1) = coeffs_115.signals.values(i,1);
%    Serial_Data_a(k+15,1) = coeffs_114.signals.values(i,1);   
%    Serial_Data_a(k+16,1) = coeffs_113.signals.values(i,1);   
% 
%    Serial_Data_a(k+17,1) = coeffs_112.signals.values(i,1);
%    Serial_Data_a(k+18,1) = coeffs_111.signals.values(i,1);
%    Serial_Data_a(k+19,1) = coeffs_110.signals.values(i,1);
%    Serial_Data_a(k+20,1) = coeffs_109.signals.values(i,1);   
%    Serial_Data_a(k+20,1) = coeffs_108.signals.values(i,1);    
%    Serial_Data_a(k+22,1) = coeffs_107.signals.values(i,1);
%    Serial_Data_a(k+23,1) = coeffs_106.signals.values(i,1);   
%    Serial_Data_a(k+24,1) = coeffs_105.signals.values(i,1);   
% 
%    Serial_Data_a(k+25,1) = coeffs_104.signals.values(i,1);
%    Serial_Data_a(k+26,1) = coeffs_103.signals.values(i,1);
%    Serial_Data_a(k+27,1) = coeffs_102.signals.values(i,1);
%    Serial_Data_a(k+28,1) = coeffs_101.signals.values(i,1);   
%    Serial_Data_a(k+29,1) = coeffs_100.signals.values(i,1);    
%    Serial_Data_a(k+30,1) = coeffs_99.signals.values(i,1);
%    Serial_Data_a(k+31,1) = coeffs_98.signals.values(i,1);   
%    Serial_Data_a(k+32,1) = coeffs_97.signals.values(i,1);   
%    
%    Serial_Data_a(k+33,1) = coeffs_96.signals.values(i,1);
%    Serial_Data_a(k+34,1) = coeffs_95.signals.values(i,1);
%    Serial_Data_a(k+35,1) = coeffs_94.signals.values(i,1);
%    Serial_Data_a(k+36,1) = coeffs_93.signals.values(i,1);   
%    Serial_Data_a(k+37,1) = coeffs_92.signals.values(i,1);    
%    Serial_Data_a(k+38,1) = coeffs_91.signals.values(i,1);
%    Serial_Data_a(k+39,1) = coeffs_90.signals.values(i,1);   
%    Serial_Data_a(k+40,1) = coeffs_89.signals.values(i,1);  
% 
%    Serial_Data_a(k+41,1) = coeffs_88.signals.values(i,1);
%    Serial_Data_a(k+42,1) = coeffs_87.signals.values(i,1);
%    Serial_Data_a(k+43,1) = coeffs_86.signals.values(i,1);
%    Serial_Data_a(k+44,1) = coeffs_85.signals.values(i,1);   
%    Serial_Data_a(k+45,1) = coeffs_84.signals.values(i,1);    
%    Serial_Data_a(k+46,1) = coeffs_83.signals.values(i,1);
%    Serial_Data_a(k+47,1) = coeffs_82.signals.values(i,1);   
%    Serial_Data_a(k+48,1) = coeffs_81.signals.values(i,1);  
%    
%    Serial_Data_a(k+49,1) = coeffs_80.signals.values(i,1);
%    Serial_Data_a(k+50,1) = coeffs_79.signals.values(i,1);
%    Serial_Data_a(k+51,1) = coeffs_78.signals.values(i,1);
%    Serial_Data_a(k+52,1) = coeffs_77.signals.values(i,1);   
%    Serial_Data_a(k+53,1) = coeffs_76.signals.values(i,1);    
%    Serial_Data_a(k+54,1) = coeffs_75.signals.values(i,1);
%    Serial_Data_a(k+55,1) = coeffs_74.signals.values(i,1);   
%    Serial_Data_a(k+56,1) = coeffs_73.signals.values(i,1);  
% 
%    Serial_Data_a(k+57,1) = coeffs_72.signals.values(i,1);
%    Serial_Data_a(k+58,1) = coeffs_71.signals.values(i,1);
%    Serial_Data_a(k+59,1) = coeffs_70.signals.values(i,1);
%    Serial_Data_a(k+60,1) = coeffs_69.signals.values(i,1);   
%    Serial_Data_a(k+61,1) = coeffs_68.signals.values(i,1);    
%    Serial_Data_a(k+62,1) = coeffs_67.signals.values(i,1);
%    Serial_Data_a(k+63,1) = coeffs_66.signals.values(i,1);   
%    Serial_Data_a(k+64,1) = coeffs_65.signals.values(i,1);  
%    
%    
%    
%    Serial_Data_a(k+65,1) = coeffs_64.signals.values(i,1);
%    Serial_Data_a(k+66,1) = coeffs_63.signals.values(i,1);
%    Serial_Data_a(k+67,1) = coeffs_62.signals.values(i,1);
%    Serial_Data_a(k+68,1) = coeffs_61.signals.values(i,1);   
%    Serial_Data_a(k+69,1) = coeffs_60.signals.values(i,1);    
%    Serial_Data_a(k+70,1) = coeffs_59.signals.values(i,1);
%    Serial_Data_a(k+71,1) = coeffs_58.signals.values(i,1);   
%    Serial_Data_a(k+72,1) = coeffs_57.signals.values(i,1);   
%    
%    Serial_Data_a(k+73,1) = coeffs_56.signals.values(i,1);
%    Serial_Data_a(k+74,1) = coeffs_55.signals.values(i,1);
%    Serial_Data_a(k+75,1) = coeffs_54.signals.values(i,1);
%    Serial_Data_a(k+76,1) = coeffs_53.signals.values(i,1);   
%    Serial_Data_a(k+77,1) = coeffs_52.signals.values(i,1);    
%    Serial_Data_a(k+78,1) = coeffs_51.signals.values(i,1);
%    Serial_Data_a(k+79,1) = coeffs_50.signals.values(i,1);   
%    Serial_Data_a(k+80,1) = coeffs_49.signals.values(i,1);   
% 
%    Serial_Data_a(k+81,1) = coeffs_48.signals.values(i,1);
%    Serial_Data_a(k+82,1) = coeffs_47.signals.values(i,1);
%    Serial_Data_a(k+83,1) = coeffs_46.signals.values(i,1);
%    Serial_Data_a(k+84,1) = coeffs_45.signals.values(i,1);   
%    Serial_Data_a(k+85,1) = coeffs_44.signals.values(i,1);    
%    Serial_Data_a(k+86,1) = coeffs_43.signals.values(i,1);
%    Serial_Data_a(k+87,1) = coeffs_42.signals.values(i,1);   
%    Serial_Data_a(k+88,1) = coeffs_42.signals.values(i,1);   
% 
%    Serial_Data_a(k+89,1) = coeffs_40.signals.values(i,1);
%    Serial_Data_a(k+90,1) = coeffs_39.signals.values(i,1);
%    Serial_Data_a(k+91,1) = coeffs_38.signals.values(i,1);
%    Serial_Data_a(k+92,1) = coeffs_37.signals.values(i,1);   
%    Serial_Data_a(k+93,1) = coeffs_36.signals.values(i,1);    
%    Serial_Data_a(k+94,1) = coeffs_35.signals.values(i,1);
%    Serial_Data_a(k+95,1) = coeffs_34.signals.values(i,1);   
%    Serial_Data_a(k+96,1) = coeffs_33.signals.values(i,1);   
%    
%    Serial_Data_a(k+97,1) = coeffs_32.signals.values(i,1);
%    Serial_Data_a(k+98,1) = coeffs_31.signals.values(i,1);
%    Serial_Data_a(k+99,1) = coeffs_30.signals.values(i,1);
%    Serial_Data_a(k+100,1) = coeffs_29.signals.values(i,1);   
%    Serial_Data_a(k+101,1) = coeffs_28.signals.values(i,1);    
%    Serial_Data_a(k+102,1) = coeffs_27.signals.values(i,1);
%    Serial_Data_a(k+103,1) = coeffs_26.signals.values(i,1);   
%    Serial_Data_a(k+104,1) = coeffs_25.signals.values(i,1);  
% 
%    Serial_Data_a(k+105,1) = coeffs_24.signals.values(i,1);
%    Serial_Data_a(k+106,1) = coeffs_23.signals.values(i,1);
%    Serial_Data_a(k+107,1) = coeffs_22.signals.values(i,1);
%    Serial_Data_a(k+108,1) = coeffs_21.signals.values(i,1);   
%    Serial_Data_a(k+109,1) = coeffs_20.signals.values(i,1);    
%    Serial_Data_a(k+110,1) = coeffs_19.signals.values(i,1);
%    Serial_Data_a(k+111,1) = coeffs_18.signals.values(i,1);   
%    Serial_Data_a(k+112,1) = coeffs_17.signals.values(i,1);  
%    
%    Serial_Data_a(k+113,1) = coeffs_16.signals.values(i,1);
%    Serial_Data_a(k+114,1) = coeffs_15.signals.values(i,1);
%    Serial_Data_a(k+115,1) = coeffs_14.signals.values(i,1);
%    Serial_Data_a(k+116,1) = coeffs_13.signals.values(i,1);   
%    Serial_Data_a(k+117,1) = coeffs_12.signals.values(i,1);    
%    Serial_Data_a(k+118,1) = coeffs_11.signals.values(i,1);
%    Serial_Data_a(k+119,1) = coeffs_10.signals.values(i,1);   
%    Serial_Data_a(k+120,1) = coeffs_9.signals.values(i,1);  
% 
%    Serial_Data_a(k+121,1) = coeffs_8.signals.values(i,1);
%    Serial_Data_a(k+122,1) = coeffs_7.signals.values(i,1);
%    Serial_Data_a(k+123,1) = coeffs_6.signals.values(i,1);
%    Serial_Data_a(k+124,1) = coeffs_5.signals.values(i,1);   
%    Serial_Data_a(k+125,1) = coeffs_4.signals.values(i,1);    
%    Serial_Data_a(k+126,1) = coeffs_3.signals.values(i,1);
%    Serial_Data_a(k+127,1) = coeffs_2.signals.values(i,1);   
%    Serial_Data_a(k+128,1) = coeffs_1.signals.values(i,1);  
%    
%    
%    
%    k = k + 128;
% end



