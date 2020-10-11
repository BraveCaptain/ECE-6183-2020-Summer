
clear
[x, Fs] = audioread('lab1_5.wav');

%% Plot waveform

figure(1)
clf
plot(x)
xlabel('Time (sample)')
title('Signal')

%% Time axis in seconds

N = length(x);
t = (1:N)/Fs;

figure(1)
clf
plot(t, x)
xlabel('Time (sec)')
title('Signal')

%% Zoom in to 50 msec

xlim(0.4 + [0 0.050])

%% Distribution of samples

xs = sort(x);

figure(1)
clf
plot(xs)
title('Sorted signal values')

%% What is the quantization increment ?

% smallest positive value (SPV)

SPV = min(x(x > 0))

%% Verify the quantization step size

% The smallest positive value is 1/2^7
1/SPV
2^7


%% Frequency spectrum
% Use Fast Fourier Transform (FFT)

% Use power of 2 for FFT efficiency
N = length(x)
Nfft = 2^ceil(2+log2(N))  % smallest power of 2 greater than signal length

%% Compute Fourier transform 

X = fft(x, Nfft);   
k = 0:Nfft-1;      % FFT index

figure(1)
clf
plot(k, abs(X))
xlabel('FFT index')
title('Spectrum')

%% Center dc

X2 = fftshift(X);
k2 = -Nfft/2 : Nfft/2-1;

figure(1)
clf
plot(k2, abs(X2))
xlabel('FFT index')
title('Spectrum')

%% Normalized frequency
% Normalized frequency is in units of [cycles per sample]

fn = ( -Nfft/2 : Nfft/2-1 ) / Nfft;

figure(1)
clf
plot(fn, abs(X2))
xlabel('Frequency (cycles/sample)')
title('Spectrum')

%% Frequency in Hz

f = fn * Fs;

figure(1)
clf
plot(f, abs(X2))
xlabel('Frequency (cycles/second, i.e. Hz)')
title('Spectrum')


